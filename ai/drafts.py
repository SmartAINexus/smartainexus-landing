from __future__ import annotations

from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Mapping, Sequence

from ai.character_limits import FieldLimit, LimitResult, require_within_limit


@dataclass(frozen=True)
class ValidatedDraft:
    fields: Mapping[str, str]
    limits: Mapping[str, LimitResult]
    requires_human_review: bool = True


def validate_draft_output(
    fields: Mapping[str, str] | Sequence[tuple[str, str]], rules: Sequence[FieldLimit]
) -> ValidatedDraft:
    """Validate a complete structured draft without truncating or rewriting it."""

    rule_by_field = {rule.field_id: rule for rule in rules}
    if len(rule_by_field) != len(rules):
        raise ValueError("draft field limit identifiers must be unique")

    items = list(fields.items()) if isinstance(fields, Mapping) else list(fields)
    supplied_names = [field_id for field_id, _text in items]
    if len(set(supplied_names)) != len(supplied_names):
        raise ValueError("draft output contains duplicate field identifiers")
    supplied_fields = dict(items)

    expected = set(rule_by_field)
    supplied = set(supplied_fields)
    missing = sorted(expected - supplied)
    unexpected = sorted(supplied - expected)
    if missing or unexpected:
        raise ValueError(
            f"draft fields do not match limits; missing={missing}, unexpected={unexpected}"
        )

    validated_fields: dict[str, str] = {}
    results: dict[str, LimitResult] = {}
    for field_id, rule in rule_by_field.items():
        text = supplied_fields[field_id]
        if not isinstance(text, str):
            raise TypeError(f"{field_id} draft value must be text")
        results[field_id] = require_within_limit(text, rule)
        validated_fields[field_id] = text

    return ValidatedDraft(
        fields=MappingProxyType(validated_fields),
        limits=MappingProxyType(results),
    )


def validate_draft_json(raw_json: str, rules: Sequence[FieldLimit]) -> ValidatedDraft:
    """Parse a flat JSON object while retaining duplicate keys for fail-closed validation."""

    try:
        pairs = json.loads(raw_json, object_pairs_hook=lambda items: items)
    except json.JSONDecodeError as error:
        raise ValueError("draft output must be valid JSON") from error
    if not isinstance(pairs, list) or not all(
        isinstance(item, tuple) and len(item) == 2 for item in pairs
    ):
        raise ValueError("draft output must be a JSON object")
    return validate_draft_output(pairs, rules)
