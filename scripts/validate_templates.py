#!/usr/bin/env python3
"""Validate the reviewed workspace-template catalog sources.

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
# Type names are normalised case-insensitively; "Form template" and
# "Form Template" are the same catalog kind (see the Universal Workspace
# Form Templates plan). Kinds are validated case-sensitively below.
SUPPORTED_TYPES = {"markdown template": "markdown", "form template": "form"}
SUPPORTED_FIELD_TYPES = {"text", "textarea", "number", "date", "select", "roster"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# Form field ids follow snake_case (e.g. due_date, word_target) so they can be
# referenced naturally in the markdown body and downstream submission records.
FIELD_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
LOCALE_RE = re.compile(r"^[a-z]{2}(?:-[A-Z]{2})?$")
PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-z0-9][a-z0-9_-]*)\s*\}\}")


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


def _validate_form_fields(metadata: dict[str, Any], path: Path) -> dict[str, str]:
    """Validate the fields mapping of a Form template; return field id -> type."""
    fields = metadata.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise TemplateValidationError(
            f"{path}: Form templates require a non-empty 'fields' mapping"
        )

    field_types: dict[str, str] = {}
    for field_id, definition in fields.items():
        if not FIELD_ID_RE.fullmatch(field_id):
            raise TemplateValidationError(
                f"{path}: field id {field_id!r} must match {FIELD_ID_RE.pattern}"
            )
        if not isinstance(definition, dict):
            raise TemplateValidationError(
                f"{path}: field {field_id!r} must be a YAML mapping"
            )

        label = definition.get("label")
        if not isinstance(label, str) or not label.strip():
            raise TemplateValidationError(
                f"{path}: field {field_id!r} requires a non-empty 'label' string"
            )

        field_type = definition.get("type")
        if field_type not in SUPPORTED_FIELD_TYPES:
            supported = ", ".join(sorted(SUPPORTED_FIELD_TYPES))
            raise TemplateValidationError(
                f"{path}: field {field_id!r} type {field_type!r} is not supported; "
                f"expected one of: {supported}"
            )

        if "required" in definition and not isinstance(definition["required"], bool):
            raise TemplateValidationError(
                f"{path}: field {field_id!r} 'required' must be a boolean"
            )

        for key in ("max_length", "display_chars", "display_lines", "min", "max"):
            if key in definition and (
                not isinstance(definition[key], int) or isinstance(definition[key], bool)
            ):
                raise TemplateValidationError(
                    f"{path}: field {field_id!r} {key!r} must be an integer"
                )

        if field_type == "select":
            options = definition.get("options")
            if (
                not isinstance(options, list)
                or not options
                or not all(isinstance(o, str) and o.strip() for o in options)
            ):
                raise TemplateValidationError(
                    f"{path}: select field {field_id!r} requires a non-empty "
                    "'options' list of strings"
                )

        if field_type == "number":
            lower = definition.get("min")
            upper = definition.get("max")
            if lower is not None and upper is not None and lower > upper:
                raise TemplateValidationError(
                    f"{path}: number field {field_id!r} has min {lower} > max {upper}"
                )

        field_types[field_id] = field_type
    return field_types


def _validate_placeholders(body: str, field_types: dict[str, str], path: Path) -> None:
    """Cross-check body placeholders against the declared fields."""
    remaining = PLACEHOLDER_RE.sub("", body)
    if "{{" in remaining or "}}" in remaining:
        marker = "{{" if "{{" in remaining else "}}"
        index = remaining.find(marker)
        context = remaining[max(0, index - 40): index + 40].replace("\n", " ")
        raise TemplateValidationError(
            f"{path}: malformed placeholder syntax in body near ...{context}..."
        )

    used = set(PLACEHOLDER_RE.findall(body))
    undeclared = sorted(used - set(field_types))
    if undeclared:
        raise TemplateValidationError(
            f"{path}: body uses undeclared placeholder(s): {', '.join(undeclared)}"
        )
    unused = sorted(set(field_types) - used)
    if unused:
        raise TemplateValidationError(
            f"{path}: declared field(s) never used in body: {', '.join(unused)}"
        )


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
    expected_kind = SUPPORTED_TYPES.get(template_type.lower())
    if expected_kind is None:
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
    if template_kind != expected_kind:
        raise TemplateValidationError(
            f"{path}: template type {template_type!r} requires "
            f"template_kind: {expected_kind}, got {template_kind!r}"
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

    if expected_kind == "form":
        field_types = _validate_form_fields(metadata, path)
        _validate_placeholders(body, field_types, path)

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

    print(f"Validated {len(records)} template(s) in {TEMPLATES_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
