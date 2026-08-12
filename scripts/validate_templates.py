#!/usr/bin/env python3
"""Validate the reviewed Markdown-template catalog sources.

Usage (from the knowledge repository root):
  python3 scripts/validate_templates.py

The template directory is deliberately validated separately from the ordinary
OKF concept catalog. Templates have their own frontmatter contract because
their assistant guidance is consumed as trusted, immutable application input.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from okf_lint import split_frontmatter


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = ROOT / "templates"
SUPPORTED_TYPES = {"Markdown Template"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LOCALE_RE = re.compile(r"^[a-z]{2}(?:-[A-Z]{2})?$")


@dataclass(frozen=True)
class TemplateRecord:
    path: Path
    metadata: dict[str, Any]
    body: str


class TemplateValidationError(ValueError):
    """Raised when one or more template source documents are invalid."""


def _required_string(metadata: dict[str, Any], key: str, path: Path) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TemplateValidationError(f"{path}: {key} must be a non-empty string")
    return value.strip()


def load_template(path: Path) -> TemplateRecord:
    source = path.read_text(encoding="utf-8")
    raw, body = split_frontmatter(source)
    if raw is None or body is None:
        raise TemplateValidationError(
            f"{path}: missing or unterminated YAML frontmatter"
        )

    try:
        metadata = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        raise TemplateValidationError(f"{path}: invalid YAML frontmatter: {error}") from error

    if not isinstance(metadata, dict):
        raise TemplateValidationError(f"{path}: frontmatter must be a YAML mapping")

    template_type = _required_string(metadata, "type", path)
    if template_type not in SUPPORTED_TYPES:
        supported = ", ".join(sorted(SUPPORTED_TYPES))
        raise TemplateValidationError(
            f"{path}: unsupported template type {template_type!r}; expected {supported}"
        )

    template_id = _required_string(metadata, "id", path)
    if not ID_RE.fullmatch(template_id):
        raise TemplateValidationError(
            f"{path}: id {template_id!r} must match {ID_RE.pattern}"
        )

    version = _required_string(metadata, "version", path)
    if not SEMVER_RE.fullmatch(version):
        raise TemplateValidationError(
            f"{path}: version {version!r} must be semantic versioning like 1.0.0"
        )

    locale = _required_string(metadata, "locale", path)
    if not LOCALE_RE.fullmatch(locale):
        raise TemplateValidationError(
            f"{path}: locale {locale!r} must be a BCP-47 language or language-region tag"
        )

    title = _required_string(metadata, "title", path)
    description = _required_string(metadata, "description", path)
    template_kind = _required_string(metadata, "template_kind", path)
    if template_kind != "markdown":
        raise TemplateValidationError(
            f"{path}: supported Markdown Templates must have template_kind: markdown"
        )

    assistant = metadata.get("assistant")
    if not isinstance(assistant, dict):
        raise TemplateValidationError(f"{path}: assistant must be a YAML mapping")
    guidance = assistant.get("guidance")
    if not isinstance(guidance, str) or not guidance.strip():
        raise TemplateValidationError(
            f"{path}: assistant.guidance must be a non-empty string"
        )

    if not body.strip():
        raise TemplateValidationError(f"{path}: Markdown body must not be empty")

    expected_name = f"{template_id}.{locale}.md"
    if path.name != expected_name:
        raise TemplateValidationError(
            f"{path}: filename must be {expected_name!r} for its id and locale"
        )

    return TemplateRecord(path=path, metadata=metadata, body=body)


def load_templates(root: Path = TEMPLATES_ROOT) -> list[TemplateRecord]:
    if not root.is_dir():
        raise TemplateValidationError(f"Template source directory not found: {root}")

    paths = sorted(root.rglob("*.md"))
    if not paths:
        raise TemplateValidationError(f"No Markdown templates found in {root}")

    records: list[TemplateRecord] = []
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    for path in paths:
        try:
            record = load_template(path)
        except TemplateValidationError as error:
            errors.append(str(error))
            continue
        template_id = str(record.metadata["id"])
        previous = seen_ids.get(template_id)
        if previous:
            errors.append(
                f"{path}: duplicate template id {template_id!r}; already defined by {previous}"
            )
        else:
            seen_ids[template_id] = path
        records.append(record)

    if errors:
        raise TemplateValidationError("\n".join(errors))
    return records


def main() -> int:
    try:
        records = load_templates()
    except TemplateValidationError as error:
        print(f"Template validation failed:\n{error}", file=sys.stderr)
        return 1

    print(f"Validated {len(records)} Markdown template(s) in {TEMPLATES_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
