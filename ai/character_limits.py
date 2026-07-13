from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import unicodedata


class CountMode(StrEnum):
    UNICODE_CODEPOINTS = "unicode_codepoints"
    NORMALIZED_CODEPOINTS = "normalized_codepoints"
    UTF16_CODE_UNITS = "utf16_code_units"


@dataclass(frozen=True)
class FieldLimit:
    field_id: str
    maximum: int
    mode: CountMode = CountMode.UNICODE_CODEPOINTS
    count_spaces: bool = True
    count_line_breaks: bool = True
    normalize_line_breaks: bool = True

    def __post_init__(self) -> None:
        if not self.field_id.strip():
            raise ValueError("field_id must not be empty")
        if self.maximum <= 0:
            raise ValueError("maximum must be positive")


@dataclass(frozen=True)
class LimitResult:
    field_id: str
    count: int
    maximum: int
    remaining: int
    valid: bool


def _prepare(text: str, rule: FieldLimit) -> str:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in text):
        raise ValueError(f"{rule.field_id} contains an invalid Unicode surrogate")
    prepared = (
        text.replace("\r\n", "\n").replace("\r", "\n")
        if rule.normalize_line_breaks
        else text
    )
    if rule.mode == CountMode.NORMALIZED_CODEPOINTS:
        prepared = unicodedata.normalize("NFC", prepared)
    if not rule.count_spaces:
        prepared = prepared.replace(" ", "")
    if not rule.count_line_breaks:
        prepared = prepared.replace("\r", "").replace("\n", "")
    return prepared


def validate_limit(text: str, rule: FieldLimit) -> LimitResult:
    prepared = _prepare(text, rule)
    count = (
        len(prepared.encode("utf-16-le")) // 2
        if rule.mode == CountMode.UTF16_CODE_UNITS
        else len(prepared)
    )
    return LimitResult(
        field_id=rule.field_id,
        count=count,
        maximum=rule.maximum,
        remaining=rule.maximum - count,
        valid=count <= rule.maximum,
    )


def require_within_limit(text: str, rule: FieldLimit) -> LimitResult:
    result = validate_limit(text, rule)
    if not result.valid:
        raise ValueError(
            f"{rule.field_id} exceeds the character limit by {-result.remaining} characters"
        )
    return result
