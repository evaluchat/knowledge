#!/usr/bin/env python3
"""Build a static GitHub Pages site from the OKF research catalog.

Usage (from repo root):
  python3 scripts/build_site.py

Uses the `markdown` package when importable; otherwise a minimal fallback
renderer (fenced code + headings). Output → site/ (local artifact; Pages
workflow publishes site/ to the gh-pages branch).

Rendering model:
- index.html — the repo's human-maintained index.md rendered as the landing
  page (frontmatter stripped, relative .md links rewritten to generated
  pages), plus a compact "Recently updated" strip.
- <dir>/index.html — one section page per top-level content directory
  (theory/, methods/, ...): the directory's own index.md (if any), a compact
  list of its concept groups, an empty-state block for empty sections, and
  that section's "Recently updated" strip.
- /{id}.html — one page per concept group (canonical language), plus
  /{id}.{lang}.html for non-en representations.
- Evidence contributions are grouped per bundle (methods/<id>/evidence/<contribution>/): the bundle's index.md becomes the
  page; role files (question/results/...) are not separate concepts.
- catalog.json — derived from frontmatter for agent consumers.
"""

from __future__ import annotations

import html
import json
import os
import posixpath
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from okf_lint import (  # noqa: E402
    RESERVED_NAMES,
    parse_simple_yaml,
    split_frontmatter,
)

# BEGIN KNOWLEDGE TEMPLATE IMPORT
from validate_templates import load_templates  # noqa: E402
# END KNOWLEDGE TEMPLATE IMPORT

try:
    import markdown as md_lib

    def render_markdown(text: str) -> str:
        return md_lib.markdown(
            text,
            extensions=["fenced_code", "tables", "toc"],
        )

except ImportError:

    def render_markdown(text: str) -> str:
        return _minimal_markdown(text)


ROOT = Path(".").resolve()
OUT = ROOT / "site"
GITHUB_BLOB = "https://github.com/evaluchat/knowledge/blob/main/"
REPO_URL = GITHUB_BLOB[: GITHUB_BLOB.index("/blob/")]
SITE_LABEL = "Knowledge catalog"
SITE_DOMAIN = "knowledge.evaluchat.org"
SKIP_DIR_NAMES = {".github", "templates", ".git", "scripts", "site"}

# Site-root-relative registries, filled by build() before rendering:
#   CONCEPT_PAGES: repo file path → page path (e.g. "theory/camdle.en.md" → "camdle.html")
#   SECTION_PAGES: top-level dir → section page path (e.g. "theory" → "theory/index.html")
CONCEPT_PAGES: dict[str, str] = {}
SECTION_PAGES: dict[str, str] = {}

ISO_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?)"
)
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")


def under_skip_dir(path: Path) -> bool:
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return any(p in SKIP_DIR_NAMES for p in parts[:-1])


def is_reserved(path: Path) -> bool:
    return path.name.lower() in RESERVED_NAMES


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _minimal_markdown(text: str) -> str:
    """Tiny fallback: fenced code + ATX headings + paragraphs."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_lang = ""
    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_para()
            if not in_code:
                in_code = True
                code_lang = line[3:].strip()
                cls = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                out.append(f"<pre><code{cls}>")
            else:
                in_code = False
                out.append("</code></pre>")
            i += 1
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            level = len(m.group(1))
            out.append(f"<h{level}>{html.escape(m.group(2))}</h{level}>")
            i += 1
            continue
        if not line.strip():
            flush_para()
            i += 1
            continue
        para.append(line.strip())
        i += 1
    flush_para()
    return "\n".join(out)


def parse_ts(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return parse_ts(value.get("at"))
    s = str(value).strip()
    m = ISO_RE.search(s)
    if not m:
        return None
    raw = m.group(1).replace(" ", "T")
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    if len(raw) == 10:
        raw += "T00:00:00+00:00"
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def meta_updated(meta: dict) -> datetime | None:
    candidates = [
        parse_ts(meta.get("timestamp")),
        parse_ts(meta.get("created")),
        parse_ts(meta.get("generated")),
        parse_ts(meta.get("verified")),
    ]
    times = [t for t in candidates if t]
    return max(times) if times else None


def resolve_target(base_dir: Path, target: str, out_dir: str) -> str:
    """Map a markdown link target to a rendered page (or GitHub fallback URL).

    base_dir: source file's directory (repo-relative resolution base).
    out_dir:  site-root-relative directory of the OUTPUT page ("." for root
              pages, e.g. "theory" for theory/index.html).
    """
    if target.startswith(("http://", "https://", "mailto:")):
        return target
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    if not target:
        return anchor or "#"
    base_rel = rel(base_dir)  # "." for the repo root
    raw = target.lstrip("/")  # leading slash = repo-root relative
    if raw.endswith("/"):
        raw = raw[:-1]
    resolved = (
        posixpath.normpath(raw)
        if base_rel == "."
        else posixpath.normpath(posixpath.join(base_rel, raw))
    )
    if not resolved or resolved == ".":
        dest = "index.html"
    elif resolved in CONCEPT_PAGES:
        dest = CONCEPT_PAGES[resolved]
    elif resolved in SECTION_PAGES:
        dest = SECTION_PAGES[resolved]
    elif resolved.endswith(".md"):
        d, f = posixpath.split(resolved)
        if f == "index.md" and d in SECTION_PAGES:
            dest = SECTION_PAGES[d]
        else:
            return GITHUB_BLOB + resolved + anchor
    else:
        return REPO_URL + "/tree/main/" + resolved + anchor
    link = posixpath.relpath(dest, out_dir) if out_dir else dest
    return link + anchor


def rewrite_links(md: str, base_dir: Path, out_dir: str = "") -> str:
    def sub(m: re.Match) -> str:
        text, target = m.group(1), m.group(2)
        return f"[{text}]({resolve_target(base_dir, target, out_dir)})"

    return LINK_RE.sub(sub, md)


def collect_concepts() -> tuple[dict[str, list[tuple[Path, dict, str]]], dict[Path, list[tuple[Path, dict, str]]]]:
    """id → reps, and evidence bundle root → reps (bundle index.md + role files)."""
    by_id: dict[str, list[tuple[Path, dict, str]]] = defaultdict(list)
    bundles: dict[Path, list[tuple[Path, dict, str]]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            if not name.lower().endswith(".md"):
                continue
            path = Path(dirpath) / name
            if under_skip_dir(path) or is_reserved(path):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            raw, body = split_frontmatter(text)
            if raw is None:
                continue
            meta = parse_simple_yaml(raw)
            if meta is None:
                continue
            if "evidence" in path.parts:
                # Collection index.md (methods/<id>/evidence/index.md) is not a concept; role
                # files belong to the bundle dir that carries an index.md.
                parent = path.parent
                if parent.name != "evidence" and (parent / "index.md").is_file():
                    bundles[parent].append((path, meta, body or ""))
                continue
            cid = meta.get("id")
            if not isinstance(cid, str) or not cid.strip():
                continue
            by_id[cid.strip()].append((path, meta, body or ""))
    return by_id, bundles


def pick_canonical(reps: list[tuple[Path, dict, str]]) -> tuple[Path, dict, str]:
    for path, meta, body in reps:
        if str(meta.get("lang", "")).lower() == "en":
            return path, meta, body
    return reps[0]


def fmt_meta_value(v) -> str:
    if v is None:
        return ""
    if isinstance(v, dict):
        return ", ".join(f"{k}={v[k]}" for k in v)
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def page_shell(
    title: str, body_html: str, *, nav: str = "", breadcrumbs: bool = True, base: str = "",
    hero: bool = False,
) -> str:
    esc_title = html.escape(title)
    home = f"{base}index.html"
    favicon = f"{base}favicon.ico"
    logo = f"{base}assets/evaluchat.png"
    if not breadcrumbs:
        crumbs = ""
    elif nav:
        crumbs = f'<p class="breadcrumb">{nav}</p>'
    else:
        crumbs = (
            '<p class="breadcrumb">'
            f'<a href="{home}">{SITE_LABEL}</a>'
            '<span class="sep">/</span>'
            f"<span>{esc_title}</span>"
            "</p>"
        )
    if hero:
        pre_main = (
            '<section class="page-hero-slim">'
            f'<div class="page-hero-slim-inner">{crumbs}<h1>{esc_title}</h1></div>'
            "</section>"
        )
        inner_crumbs = ""
    else:
        pre_main = ""
        inner_crumbs = crumbs
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc_title}</title>
<link rel="icon" href="{favicon}" sizes="any"/>
<link rel="stylesheet" href="{base}assets/style.css"/>
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <div class="logo">
      <a href="{home}" aria-label="{SITE_LABEL}">
        <img class="logo-mark" src="{logo}" width="32" height="32" alt=""/>
        evaluchat
      </a>
    </div>
    <nav class="main-nav" aria-label="Primary navigation">
      <a href="{home}">{SITE_LABEL}</a>
      <a href="{REPO_URL}">GitHub</a>
      <a href="{GITHUB_BLOB}README.md">README</a>
      <a href="https://evaluchat.org/" class="nav-cta">Open evaluchat ↗</a>
    </nav>
  </div>
</header>
{pre_main}
<main class="page-wrap">
{inner_crumbs}
  <article class="content">
{body_html}
  </article>
</main>
<footer class="site-footer">
  <p>
    <a href="https://evaluchat.org">evaluchat.com</a>
    &middot; {SITE_LABEL}
    &middot; <a href="{REPO_URL}">GitHub</a>
    &middot; <a href="mailto:hello@evaluchat.com">hello@evaluchat.com</a>
  </p>
  <p class="copyright">© 2026 Evaluchat · Open Knowledge Format</p>
</footer>
</body>
</html>
"""


def copy_theme_assets() -> None:
    """Ship brand assets (logo mark, favicon) into the built site."""
    theme_dir = Path(__file__).parent / "theme"
    assets_out = OUT / "assets"
    assets_out.mkdir(parents=True, exist_ok=True)
    for name in ("evaluchat.png", "style.css"):
        src = theme_dir / name
        if src.is_file():
            (assets_out / name).write_bytes(src.read_bytes())
    favicon = theme_dir / "favicon.ico"
    if favicon.is_file():
        (OUT / "favicon.ico").write_bytes(favicon.read_bytes())


# BEGIN KNOWLEDGE TEMPLATE RENDERER
def build_templates() -> None:
    """Render reviewed Markdown templates without adding them to the concept catalog."""
    records = load_templates(ROOT / "templates")
    templates_out = OUT / "templates"
    templates_out.mkdir(parents=True, exist_ok=True)

    rows: list[str] = []
    for record in records:
        metadata = record.metadata
        template_id = str(metadata["id"])
        title = str(metadata["title"])
        description = str(metadata["description"])
        source_name = record.path.name
        source_out = templates_out / source_name
        source_out.parent.mkdir(parents=True, exist_ok=True)
        source_out.write_text(record.path.read_text(encoding="utf-8"), encoding="utf-8")

        preview = render_markdown(
            rewrite_links(record.body.strip(), record.path.parent, out_dir="templates")
        )
        detail_body = (
            f"<h1>{html.escape(title)}</h1>\n"
            f'<p class="lede">{html.escape(description)}</p>\n'
            '<p class="muted"><a href="index.html">All templates</a> · '
            f'<a href="{html.escape(source_name)}">Raw Markdown source</a></p>\n'
            '<h2>Preview</h2>\n'
            f'<article class="body">{preview}</article>\n'
        )
        detail_path = templates_out / f"{template_id}.html"
        detail_path.write_text(
            page_shell(title, detail_body, base="../"), encoding="utf-8"
        )
        rows.append(
            "<tr>"
            f'<td><a href="{html.escape(detail_path.name)}">{html.escape(title)}</a>'
            f'<br/><span class="muted"><code>{html.escape(template_id)}</code></span></td>'
            f'<td>{html.escape(description)}</td>'
            f'<td><a href="{html.escape(source_name)}">Raw Markdown</a></td>'
            "</tr>"
        )

    index_body = (
        "<h1>Templates</h1>\n"
        "<p class=\"lede\">Reviewed Markdown starters for the Evaluchat workspace.</p>\n"
        '<table class="catalog"><thead><tr><th>Template</th><th>Description</th>'
        f'<th>Source</th></tr></thead><tbody>{"".join(rows)}</tbody></table>\n'
    )
    index_path = templates_out / "index.html"
    index_path.write_text(
        page_shell("Templates", index_body, base="../", hero=True), encoding="utf-8"
    )

    getting_started = next(
        (record for record in records if record.metadata.get("id") == "evaluchat-getting-started"),
        None,
    )
    if getting_started is None:
        raise RuntimeError("Template build assertion failed: Getting Started is missing")
    expected_files = (
        index_path,
        templates_out / "evaluchat-getting-started.html",
        templates_out / getting_started.path.name,
    )
    missing = [str(path) for path in expected_files if not path.is_file()]
    if missing:
        raise RuntimeError(f"Template build assertion failed; missing: {', '.join(missing)}")
    if "Welcome to Evaluchat" not in expected_files[1].read_text(encoding="utf-8"):
        raise RuntimeError("Template build assertion failed: preview body is missing")
    if expected_files[2].read_text(encoding="utf-8") != getting_started.path.read_text(
        encoding="utf-8"
    ):
        raise RuntimeError("Template build assertion failed: raw source changed")
# END KNOWLEDGE TEMPLATE RENDERER


def build() -> int:
    by_id, bundles = collect_concepts()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    (OUT / "CNAME").write_text(SITE_DOMAIN + "\n", encoding="utf-8")
    copy_theme_assets()

    global CONCEPT_PAGES, SECTION_PAGES

    catalog: list[dict] = []
    groups: list[dict] = []

    def register(cid: str, reps, is_bundle: bool, extra_files=()) -> dict:
        langs = sorted(
            {str(m.get("lang")) for _p, m, _b in reps if m.get("lang")}
        )
        canon_path, canon_meta, canon_body = pick_canonical(reps)
        status = str(canon_meta.get("status") or ("draft" if is_bundle else ""))
        typ = str(canon_meta.get("type") or ("Evidence" if is_bundle else ""))
        desc = str(canon_meta.get("description") or "")
        if not desc and is_bundle:
            m = re.search(r"\n\n(.+?)(?:\n\n|\Z)", "\n" + canon_body, re.S)
            desc = m.group(1).strip()[:200] if m else ""
        title = str(canon_meta.get("title") or cid)
        tier = ""
        if typ == "Finding":
            tier = status if status in ("provisional", "tentative", "supported") else ""
            if not tier and canon_meta.get("confidence"):
                conf = str(canon_meta.get("confidence")).lower()
                tier = {"low": "provisional", "medium": "tentative", "high": "supported"}.get(
                    conf, ""
                )
        updates = [meta_updated(m) for _p, m, _b in list(reps) + list(extra_files)]
        updates = [u for u in updates if u]
        updated = max(updates).isoformat() if updates else ""
        g = {
            "cid": cid,
            "type": typ,
            "status": status,
            "tier": tier,
            "desc": desc,
            "title": title,
            "langs": langs,
            "updated": updated,
            "canon_path": canon_path,
            "canon_meta": canon_meta,
            "canon_body": canon_body,
            "reps": reps,
            "page": f"{cid}.html",
        }
        groups.append(g)
        catalog.append(
            {
                "id": cid,
                "type": typ,
                "languages": langs,
                "status": status,
                "description": desc,
                "updated": updated,
                "canonical_resource": GITHUB_BLOB + rel(canon_path),
            }
        )
        return g

    for cid in sorted(by_id.keys()):
        register(cid, by_id[cid], False)
    for root in sorted(bundles.keys()):
        breps = bundles[root]
        idx = [r for r in breps if r[0].name == "index.md"]
        register(root.name, idx or breps, True, extra_files=breps)

    # Registries for link rewriting.
    for g in groups:
        for path, meta, _b in g["reps"]:
            lang = str(meta.get("lang") or "")
            CONCEPT_PAGES[rel(path)] = (
                g["page"] if lang.lower() == "en" else f"{g['cid']}.{lang}.html"
            )
        CONCEPT_PAGES[rel(g["canon_path"])] = g["page"]  # canonical wins

    section_dirs: set[str] = set()
    for g in groups:
        parts = rel(g["canon_path"]).split("/")
        if len(parts) > 1:
            section_dirs.add(parts[0])
    for d in os.listdir(ROOT):
        p = ROOT / d
        if p.is_dir() and d not in SKIP_DIR_NAMES and not d.startswith(".") and (p / "index.md").is_file():
            section_dirs.add(d)
    SECTION_PAGES = {d: f"{d}/index.html" for d in sorted(section_dirs)}

    def lang_badges_html(g: dict, prefix: str = "") -> str:
        out = []
        for lang in g["langs"]:
            href = g["page"] if lang.lower() == "en" else f"{g['cid']}.{lang}.html"
            out.append(f'<a href="{prefix}{html.escape(href)}">{html.escape(lang)}</a>')
        return " ".join(out)

    def table_html(headers: list[str], rows_html: str) -> str:
        return (
            '<table class="catalog"><thead><tr>'
            + "".join(f"<th>{h}</th>" for h in headers)
            + "</tr></thead><tbody>"
            + rows_html
            + "</tbody></table>"
        )

    def row_section(g: dict, prefix: str) -> str:
        return (
            "<tr>"
            f'<td><a href="{prefix}{html.escape(g["page"])}">{html.escape(g["title"])}</a><br/>'
            f'<span class="muted"><code>{html.escape(g["cid"])}</code></span></td>'
            f'<td>{html.escape(g["type"])}</td>'
            f'<td>{html.escape(g["status"])}</td>'
            f'<td class="lang-badges">{lang_badges_html(g, prefix)}</td>'
            "</tr>"
        )

    def row_recent(g: dict, prefix: str) -> str:
        return (
            "<tr>"
            f'<td><a href="{prefix}{html.escape(g["page"])}">{html.escape(g["title"])}</a><br/>'
            f'<span class="muted"><code>{html.escape(g["cid"])}</code></span></td>'
            f'<td>{html.escape(g["type"])}</td>'
            f'<td>{html.escape(g["status"])}</td>'
            f'<td class="muted">{html.escape(g["updated"][:10])}</td>'
            "</tr>"
        )

    def recent_strip(gs: list[dict], limit: int, prefix: str) -> str:
        recent = sorted(gs, key=lambda g: g["updated"], reverse=True)
        recent = [g for g in recent if g["updated"]][:limit]
        if not recent:
            return ""
        return (
            "<h2>Recently updated</h2>"
            + table_html(
                ["Title / id", "Type", "Status", "Updated"],
                "".join(row_recent(g, prefix) for g in recent),
            )
        )

    def section_label(d: str) -> str:
        p = ROOT / d / "index.md"
        if p.is_file():
            _raw, body = split_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            m = re.match(r"^#\s+(.+)$", body or "", re.M)
            if m:
                return m.group(1).strip()
        return d[:1].upper() + d[1:]

    # --- Concept pages (canonical + language variants) ---
    for g in groups:
        cid, title = g["cid"], g["title"]
        canon_path, canon_meta, canon_body = g["canon_path"], g["canon_meta"], g["canon_body"]
        langs, status, typ, tier = g["langs"], g["status"], g["type"], g["tier"]
        facts = [
            ("type", typ),
            ("id", cid),
            ("status", status),
            ("lang", str(canon_meta.get("lang") or "")),
            ("origin", str(canon_meta.get("origin") or "")),
            ("generated", fmt_meta_value(canon_meta.get("generated"))),
            ("verified", fmt_meta_value(canon_meta.get("verified"))),
            ("sources", fmt_meta_value(canon_meta.get("sources"))),
        ]
        if typ == "Finding":
            facts.insert(3, ("claim", str(canon_meta.get("claim") or "")))
            facts.insert(4, ("confidence", str(canon_meta.get("confidence") or "")))
            if tier:
                facts.insert(2, ("tier", tier))
        facts_html = "<table class=\"facts\">" + "".join(
            f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
            for k, v in facts
            if v
        ) + "</table>"

        other_langs = [lang for lang in langs if lang != str(canon_meta.get("lang") or "en")]
        other_html = ""
        if other_langs:
            links = " · ".join(
                f'<a href="{html.escape(cid)}.{html.escape(lang)}.html">{html.escape(lang)}</a>'
                for lang in other_langs
            )
            other_html = f'<p class="muted">Other languages: {links}</p>'

        body_html = (
            f"<h1>{html.escape(title)}</h1>\n"
            f"{facts_html}\n"
            f"{other_html}\n"
            f'<article class="body">{render_markdown(rewrite_links(canon_body, canon_path.parent))}</article>\n'
        )
        (OUT / g["page"]).write_text(page_shell(title, body_html), encoding="utf-8")

        # Non-en representations
        for path, meta, body in g["reps"]:
            lang = str(meta.get("lang") or "")
            if not lang or lang == "en":
                continue
            if path == canon_path:
                continue
            t = str(meta.get("title") or title)
            facts_l = [
                ("type", str(meta.get("type") or "")),
                ("id", cid),
                ("status", str(meta.get("status") or "")),
                ("lang", lang),
                ("origin", str(meta.get("origin") or "")),
                ("generated", fmt_meta_value(meta.get("generated"))),
                ("verified", fmt_meta_value(meta.get("verified"))),
            ]
            facts_l_html = "<table class=\"facts\">" + "".join(
                f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
                for k, v in facts_l
                if v
            ) + "</table>"
            nav = f'<p class="muted"><a href="{html.escape(cid)}.html">Canonical (en)</a></p>'
            page = page_shell(
                f"{t} ({lang})",
                f"<h1>{html.escape(t)}</h1>\n{facts_l_html}\n"
                f'<article class="body">{render_markdown(rewrite_links(body, path.parent))}</article>\n',
                nav=nav,
            )
            (OUT / f"{cid}.{lang}.html").write_text(page, encoding="utf-8")

    # --- Section pages: <dir>/index.html (docs-style slim hero band) ---
    for d in sorted(section_dirs):
        sgroups = [g for g in groups if rel(g["canon_path"]).startswith(d + "/")]
        label = section_label(d)
        parts: list[str] = []
        idx_path = ROOT / d / "index.md"
        if idx_path.is_file():
            _raw, body = split_frontmatter(idx_path.read_text(encoding="utf-8", errors="replace"))
            # The hero band carries the h1; strip the directory index's own H1.
            body = re.sub(r"^#\s+.+\n?", "", body or "", count=1)
            parts.append(
                f'<article class="body">{render_markdown(rewrite_links(body, idx_path.parent, out_dir=d))}</article>'
            )
        if not sgroups:
            parts.append(
                '<div class="empty-state">No entries in this section yet — the first contribution lands here.</div>'
            )
        else:
            parts.append(
                table_html(
                    ["Title / id", "Type", "Status", "Languages"],
                    "".join(row_section(g, "../") for g in sgroups),
                )
            )
        parts.append(recent_strip(sgroups, 5, "../"))
        (OUT / d).mkdir(parents=True, exist_ok=True)
        (OUT / d / "index.html").write_text(
            page_shell(label, "\n".join(parts), base="../", hero=True), encoding="utf-8"
        )

    # --- Landing page: index.md + recently updated strip ---
    index_md = ROOT / "index.md"
    landing_body = ""
    if index_md.is_file():
        _raw, body = split_frontmatter(index_md.read_text(encoding="utf-8", errors="replace"))
        landing_body = render_markdown(rewrite_links(body or "", ROOT))
    landing_body += recent_strip(groups, 8, "")
    landing_body += (
        f'\n<p class="muted">{len(groups)} concept groups · generated by build_site.py</p>'
    )
    (OUT / "index.html").write_text(
        page_shell(f"evaluchat {SITE_LABEL.lower()}", landing_body, breadcrumbs=False),
        encoding="utf-8",
    )
    (OUT / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # BEGIN KNOWLEDGE TEMPLATE BUILD
    build_templates()
    # END KNOWLEDGE TEMPLATE BUILD
    print(
        f"Built {len(groups)} concept groups ({len(bundles)} evidence bundles) + "
        f"{len(section_dirs)} section pages → site/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
