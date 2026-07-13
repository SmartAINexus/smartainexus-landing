import pytest

from ai.character_limits import CountMode, FieldLimit
from ai.drafts import validate_draft_json, validate_draft_output


def test_exact_2000_character_field_is_accepted_for_review() -> None:
    text = "a" * 2_000
    draft = validate_draft_output(
        {"objectives": text}, [FieldLimit("objectives", 2_000)]
    )

    assert draft.fields["objectives"] == text
    assert draft.limits["objectives"].remaining == 0
    assert draft.requires_human_review is True


def test_over_limit_output_is_rejected_without_truncation() -> None:
    text = "a" * 2_001
    with pytest.raises(ValueError, match="exceeds the character limit by 1"):
        validate_draft_output(
            {"objectives": text}, [FieldLimit("objectives", 2_000)]
        )
    assert len(text) == 2_001


def test_utf16_platform_mode_counts_supplementary_characters_as_two_units() -> None:
    text = "A😀"
    codepoints = validate_draft_output(
        {"summary": text}, [FieldLimit("summary", 2)]
    )
    assert codepoints.limits["summary"].count == 2

    with pytest.raises(ValueError, match="exceeds the character limit by 1"):
        validate_draft_output(
            {"summary": text},
            [FieldLimit("summary", 2, mode=CountMode.UTF16_CODE_UNITS)],
        )


def test_every_configured_field_must_be_present_and_no_extra_field_is_allowed() -> None:
    rules = [FieldLimit("objectives", 2_000), FieldLimit("impact", 1_000)]
    with pytest.raises(ValueError, match=r"missing=\['impact'\]"):
        validate_draft_output({"objectives": "Synthetic"}, rules)
    with pytest.raises(ValueError, match=r"unexpected=\['notes'\]"):
        validate_draft_output(
            {"objectives": "Synthetic", "impact": "Synthetic", "notes": "Hidden"},
            rules,
        )


def test_duplicate_limit_identifiers_are_rejected() -> None:
    with pytest.raises(ValueError, match="identifiers must be unique"):
        validate_draft_output(
            {"objectives": "Synthetic"},
            [FieldLimit("objectives", 10), FieldLimit("objectives", 20)],
        )


def test_duplicate_supplied_fields_are_rejected_before_mapping_collapse() -> None:
    with pytest.raises(ValueError, match="duplicate field identifiers"):
        validate_draft_output(
            [("objectives", "First"), ("objectives", "Second")],
            [FieldLimit("objectives", 20)],
        )


def test_strict_json_parser_retains_and_rejects_duplicate_keys() -> None:
    with pytest.raises(ValueError, match="duplicate field identifiers"):
        validate_draft_json(
            '{"objectives":"First","objectives":"Second"}',
            [FieldLimit("objectives", 20)],
        )
