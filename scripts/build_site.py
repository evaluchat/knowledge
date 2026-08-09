#!/usr/bin/env python3
"""Build a static GitHub Pages site from the OKF research catalog.

Usage (from repo root):
  python3 scripts/build_site.py

Uses the `markdown` package when importable; otherwise a minimal fallback
renderer (fenced code + headings). Output → site/ (local artifact; Pages
workflow publishes site/ to the gh-pages branch).
"""

from __future__ import annotations

import html
import json
import os
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
SKIP_DIR_NAMES = {".github", "templates", ".git", "scripts", "site"}

ISO_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?)"
)


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


def collect_concepts() -> dict[str, list[tuple[Path, dict, str]]]:
    """id → list of (path, meta, body)."""
    by_id: dict[str, list[tuple[Path, dict, str]]] = defaultdict(list)
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
            cid = meta.get("id")
            if not isinstance(cid, str) or not cid.strip():
                continue
            by_id[cid.strip()].append((path, meta, body or ""))
    return by_id


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


def page_shell(title: str, body_html: str, *, nav: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
  :root {{ --fg:#1a1a1a; --muted:#555; --link:#0b57d0; --bg:#fafafa; --border:#ddd; }}
  body {{ font-family: Georgia, "Times New Roman", serif; line-height:1.55; color:var(--fg);
         max-width: 52rem; margin: 0 auto; padding: 1.5rem; background: var(--bg); }}
  a {{ color: var(--link); }}
  header {{ border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; padding-bottom: .75rem; }}
  header .brand {{ font-size: 1.25rem; font-weight: bold; }}
  .muted {{ color: var(--muted); font-size: .95rem; }}
  table.facts {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .95rem; }}
  table.facts th, table.facts td {{ border: 1px solid var(--border); padding: .35rem .6rem; text-align: left; vertical-align: top; }}
  table.facts th {{ width: 8rem; background: #f0f0f0; }}
  .lang-badges a {{ margin-right: .4rem; }}
  .catalog {{ width: 100%; border-collapse: collapse; }}
  .catalog th, .catalog td {{ border-bottom: 1px solid var(--border); padding: .45rem .3rem; text-align: left; vertical-align: top; }}
  .catalog th {{ font-size: .85rem; color: var(--muted); }}
  pre {{ background: #f3f3f3; padding: .75rem; overflow-x: auto; }}
  code {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .9em; }}
</style>
</head>
<body>
<header>
  <div class="brand"><a href="index.html">evaluchat research</a></div>
  <p class="muted">Open Knowledge Format catalog ·
    <a href="https://github.com/evaluchat/research">GitHub</a> ·
    <a href="https://github.com/evaluchat/research/blob/main/README.md">README</a>
  </p>
  {nav}
</header>
<main>
{body_html}
</main>
</body>
</html>
"""


def build() -> int:
    by_id = collect_concepts()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    catalog: list[dict] = []
    index_rows: list[str] = []

    for cid in sorted(by_id.keys()):
        reps = by_id[cid]
        langs = sorted(
            {
                str(m.get("lang"))
                for _p, m, _b in reps
                if m.get("lang")
            }
        )
        canon_path, canon_meta, canon_body = pick_canonical(reps)
        status = str(canon_meta.get("status") or "")
        typ = str(canon_meta.get("type") or "")
        desc = str(canon_meta.get("description") or "")
        title = str(canon_meta.get("title") or cid)
        tier = ""
        if typ == "Finding":
            tier = status if status in ("provisional", "tentative", "supported") else ""
            if not tier and canon_meta.get("confidence"):
                conf = str(canon_meta.get("confidence")).lower()
                tier = {"low": "provisional", "medium": "tentative", "high": "supported"}.get(
                    conf, ""
                )

        updates = [meta_updated(m) for _p, m, _b in reps]
        updates = [u for u in updates if u]
        updated = max(updates).isoformat() if updates else ""

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

        lang_badges = " ".join(
            f'<a href="{html.escape(cid if lang == "en" else f"{cid}.{lang}")}.html">{html.escape(lang)}</a>'
            for lang in langs
        )
        tier_cell = html.escape(tier) if tier else "—"
        index_rows.append(
            "<tr>"
            f'<td><a href="{html.escape(cid)}.html">{html.escape(title)}</a><br/>'
            f'<span class="muted"><code>{html.escape(cid)}</code></span></td>'
            f"<td>{html.escape(typ)}</td>"
            f"<td>{html.escape(desc)}</td>"
            f"<td>{html.escape(status)}</td>"
            f"<td>{tier_cell}</td>"
            f'<td class="lang-badges">{lang_badges}</td>'
            "</tr>"
        )

        # Per-group canonical page (en body)
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

        other_langs = [
            lang for lang in langs if lang != str(canon_meta.get("lang") or "en")
        ]
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
            f'<article class="body">{render_markdown(canon_body)}</article>\n'
        )
        (OUT / f"{cid}.html").write_text(
            page_shell(title, body_html), encoding="utf-8"
        )

        # Non-en representations
        for path, meta, body in reps:
            lang = str(meta.get("lang") or "")
            if not lang or lang == "en":
                continue
            # skip if this is the canonical already written as {id}.html
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
                f'<article class="body">{render_markdown(body)}</article>\n',
                nav=nav,
            )
            (OUT / f"{cid}.{lang}.html").write_text(page, encoding="utf-8")

    # Index
    readme_blurb = ""
    readme = ROOT / "README.md"
    if readme.is_file():
        raw = readme.read_text(encoding="utf-8", errors="replace")
        # strip a leading H1 if present; keep first ~paragraphs as intro
        lines = raw.splitlines()
        if lines and lines[0].startswith("# "):
            lines = lines[1:]
        intro = "\n".join(lines).strip()
        # keep it short
        paras = intro.split("\n\n")
        readme_blurb = render_markdown("\n\n".join(paras[:3]))

    index_body = f"""
<h1>Research catalog</h1>
<div class="intro muted">{readme_blurb}</div>
<p class="muted">{len(catalog)} concept groups · generated by build_site.py</p>
<table class="catalog">
<thead>
<tr><th>Title / id</th><th>Type</th><th>Description</th><th>Status</th><th>Tier</th><th>Languages</th></tr>
</thead>
<tbody>
{"".join(index_rows)}
</tbody>
</table>
"""
    (OUT / "index.html").write_text(
        page_shell("evaluchat research catalog", index_body), encoding="utf-8"
    )
    (OUT / "catalog.json").write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Built {len(catalog)} concept groups → site/")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
