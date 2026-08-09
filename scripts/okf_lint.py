#!/usr/bin/env python3
"""OKF lint (stdlib-only). Run from repo root: python3 scripts/okf_lint.py"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LANG_RE = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MD_LINK_TARGET = re.compile(r"\.md(?:#.*)?$", re.IGNORECASE)

# Spec reserved + scaffold meta docs (not OKF concepts; no frontmatter).
RESERVED_NAMES = {
    "index.md",
    "log.md",
    "readme.md",
    "license",
    "license-code",
    "contributing.md",
    "agents.md",
    "agent.md",
}
SKIP_DIR_NAMES = {".github", "templates", ".git"}

ROOT = Path(".").resolve()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def is_reserved(path: Path) -> bool:
    return path.name.lower() in RESERVED_NAMES


def under_skip_dir(path: Path) -> bool:
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return any(p in SKIP_DIR_NAMES for p in parts[:-1])


def split_frontmatter(text: str) -> tuple[str | None, str | None]:
    """Return (yaml_block, body). Both None = missing/unterminated."""
    if text.startswith("\ufeff"):
        text = text[1:]
    if not (text.startswith("---") and len(text) > 3 and text[3] in "\r\n"):
        return None, None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    return None, None


def _parse_scalar(raw: str):
    s = raw.strip()
    if not s:
        return ""
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part) for part in _split_flow(inner)]
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        if not inner:
            return {}
        obj = {}
        for part in _split_flow(inner):
            if ":" not in part:
                continue
            k, v = part.split(":", 1)
            obj[k.strip()] = _parse_scalar(v)
        return obj
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _split_flow(inner: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    in_str = None
    for ch in inner:
        if in_str:
            buf.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in "\"'":
            in_str = ch
            buf.append(ch)
            continue
        if ch in "[{":
            depth += 1
            buf.append(ch)
            continue
        if ch in "]}":
            depth = max(0, depth - 1)
            buf.append(ch)
            continue
        if ch == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    if buf or parts:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def _absorb_indented_line(nested: dict | list, stripped: str) -> dict | list | None:
    """Absorb one indented frontmatter line into nested structure. None = hard fail."""
    if stripped.startswith("-"):
        item_body = stripped[1:].strip()
        if not isinstance(nested, list):
            # promote / start a list under a mapping parent handled by caller
            nested = []
        if not item_body:
            nested.append({})
            return nested
        if ":" in item_body:
            k, v = item_body.split(":", 1)
            entry: dict = {k.strip(): _parse_scalar(v) if v.strip() else ""}
            nested.append(entry)
        else:
            nested.append(_parse_scalar(item_body))
        return nested
    if ":" not in stripped:
        return None
    k, v = stripped.split(":", 1)
    key = k.strip()
    val = _parse_scalar(v) if v.strip() else ""
    if isinstance(nested, list):
        if not nested:
            nested.append({key: val})
        elif isinstance(nested[-1], dict):
            nested[-1][key] = val
        else:
            nested.append({key: val})
        return nested
    nested[key] = val
    return nested


def parse_simple_yaml(block: str) -> dict | None:
    """Minimal YAML: key: value, flow lists/maps, indented maps/lists."""
    result: dict = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        if line.startswith(" ") or line.startswith("\t"):
            # orphan indent — invalid at top level without a pending key
            return None
        if ":" not in line:
            return None
        key, rest = line.split(":", 1)
        key = key.strip()
        if not key:
            return None
        if rest.strip() == "":
            j = i + 1
            nested: dict | list = {}
            saw_list = False
            while j < len(lines):
                nxt = lines[j]
                if not nxt.strip() or nxt.strip().startswith("#"):
                    j += 1
                    continue
                if not (nxt.startswith(" ") or nxt.startswith("\t")):
                    break
                stripped = nxt.strip()
                if stripped.startswith("-"):
                    if not saw_list:
                        nested = []
                        saw_list = True
                absorbed = _absorb_indented_line(nested, stripped)
                if absorbed is None:
                    return None
                nested = absorbed
                j += 1
            result[key] = nested
            i = j
            continue
        result[key] = _parse_scalar(rest)
        i += 1
    return result


def filename_slug_and_lang(path: Path) -> tuple[str, str | None]:
    stem = path.name[:-3] if path.name.lower().endswith(".md") else path.name
    if "." not in stem:
        return stem, None
    slug, lang = stem.rsplit(".", 1)
    return slug, lang


def normalize_link_target(target: str, from_file: Path) -> Path | None:
    t = target.strip()
    if not t or t.startswith("#"):
        return None
    if "://" in t or t.startswith("mailto:"):
        return None
    if t.startswith("resource:"):
        return None
    if "#" in t:
        t = t.split("#", 1)[0]
    if not t:
        return None
    if not MD_LINK_TARGET.search(t):
        return None
    if t.startswith("/"):
        return (ROOT / t.lstrip("/")).resolve()
    return (from_file.parent / t).resolve()


def collect_md_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            if not name.lower().endswith(".md"):
                continue
            p = Path(dirpath) / name
            if under_skip_dir(p):
                continue
            files.append(p)
    return sorted(files, key=lambda p: rel(p))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    files = collect_md_files()
    checked = 0

    by_id: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    parsed: dict[Path, tuple[dict | None, str | None, str | None]] = {}

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        raw, body = split_frontmatter(text)
        if raw is None:
            parsed[path] = (None, None, "missing or unterminated YAML frontmatter")
            continue
        meta = parse_simple_yaml(raw)
        if meta is None:
            parsed[path] = (None, body, "frontmatter is not parseable simple YAML")
            continue
        parsed[path] = (meta, body, None)
        cid = meta.get("id")
        if isinstance(cid, str) and cid:
            by_id[cid].append((path, meta))

    for path in files:
        r = rel(path)
        checked += 1
        reserved = is_reserved(path)
        meta, body, fm_err = parsed.get(path, (None, None, "unreadable"))

        if path.resolve() == (ROOT / "index.md").resolve():
            if fm_err or meta is None:
                errors.append(
                    f"ERROR: {r}: root index.md missing or invalid frontmatter (need okf_version)"
                )
            elif "okf_version" not in meta:
                errors.append(f"ERROR: {r}: missing okf_version")
            elif str(meta.get("okf_version")) != "0.2":
                errors.append(
                    f"ERROR: {r}: okf_version must be \"0.2\" (got {meta.get('okf_version')!r})"
                )

        if not reserved:
            if fm_err or meta is None:
                errors.append(f"ERROR: {r}: {fm_err or 'missing frontmatter'}")
            else:
                typ = meta.get("type")
                if typ is None or (isinstance(typ, str) and not str(typ).strip()):
                    errors.append(f"ERROR: {r}: missing or empty type")

                slug, lang_suffix = filename_slug_and_lang(path)
                cid = meta.get("id")
                if cid is None or (isinstance(cid, str) and not str(cid).strip()):
                    errors.append(f"ERROR: {r}: missing or empty id")
                elif str(cid) != slug:
                    errors.append(
                        f"ERROR: {r}: id {cid!r} does not equal filename slug {slug!r}"
                    )

                lang = meta.get("lang")
                if lang is None or (isinstance(lang, str) and not str(lang).strip()):
                    errors.append(f"ERROR: {r}: missing or empty lang")
                else:
                    lang_s = str(lang)
                    if not LANG_RE.match(lang_s):
                        errors.append(
                            f"ERROR: {r}: lang {lang_s!r} is not a plausible BCP-47 tag"
                        )
                    if lang_suffix is None:
                        errors.append(
                            f"ERROR: {r}: filename language suffix missing (expected .{lang_s}.md)"
                        )
                    elif lang_suffix != lang_s:
                        errors.append(
                            f"ERROR: {r}: filename language suffix {lang_suffix!r} "
                            f"does not match lang {lang_s!r}"
                        )

                desc = meta.get("description")
                if desc is None or (isinstance(desc, str) and not str(desc).strip()):
                    errors.append(f"ERROR: {r}: missing or empty description")

                if meta.get("origin") == "translation":
                    gen = meta.get("generated")
                    by = gen.get("by") if isinstance(gen, dict) else None
                    if not by or (isinstance(by, str) and not str(by).strip()):
                        warnings.append(
                            f"WARNING: {r}: origin: translation without generated.by"
                        )

                if "translations" in meta:
                    cid_s = str(meta.get("id") or "")
                    derived = sorted(
                        {
                            str(m.get("lang"))
                            for _p, m in by_id.get(cid_s, [])
                            if m.get("lang")
                        }
                    )
                    listed = meta.get("translations")
                    if isinstance(listed, list):
                        listed_norm = sorted(str(x) for x in listed)
                    elif isinstance(listed, str):
                        listed_norm = [listed]
                    else:
                        listed_norm = []
                    if listed_norm != derived:
                        warnings.append(
                            f"WARNING: {r}: translations {listed_norm} "
                            f"inconsistent with derived languages {derived}"
                        )

                try:
                    rel_parts = path.resolve().relative_to(ROOT).parts
                except ValueError:
                    rel_parts = ()
                if "findings" in rel_parts and body is not None:
                    if "## Evidence" not in body:
                        warnings.append(f"WARNING: {r}: findings file missing ## Evidence")
                    if "## Limitations" not in body:
                        warnings.append(
                            f"WARNING: {r}: findings file missing ## Limitations"
                        )

        # Link warnings: all non-reserved concept bodies, plus every index.md
        # (reserved indexes still get missing-target warnings).
        do_links = (not reserved) or path.name.lower() == "index.md"
        if do_links:
            scan = (
                body
                if body is not None
                else path.read_text(encoding="utf-8", errors="replace")
            )
            for m in LINK_RE.finditer(scan):
                target = m.group(1)
                resolved = normalize_link_target(target, path)
                if resolved is None:
                    continue
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    continue
                if not resolved.is_file():
                    try:
                        trel = str(resolved.relative_to(ROOT)).replace("\\", "/")
                    except ValueError:
                        trel = target
                    if path.name.lower() == "index.md":
                        warnings.append(
                            f"WARNING: {r}: index entry target missing: {trel}"
                        )
                    else:
                        warnings.append(f"WARNING: {r}: broken link to {trel}")

    for e in errors:
        print(e)
    for w in warnings:
        print(w)

    n_err = len(errors)
    n_warn = len(warnings)
    if n_err:
        print(f"FAILED: {checked} files checked, {n_err} errors")
        return 1
    print(f"OK: {checked} files checked, {n_err} errors, {n_warn} warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
