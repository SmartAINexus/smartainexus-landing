import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).parents[1]
I18N_SOURCE = REPO_ROOT / "src" / "i18n" / "index.ts"
PAGE_SOURCE = REPO_ROOT / "app" / "page.tsx"

EU_OFFICIAL_LOCALES = {
    "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga", "hr",
    "hu", "it", "lt", "lv", "mt", "nl", "pl", "pt", "ro", "sk", "sl", "sv",
}


def test_all_24_eu_official_languages_are_declared_and_selectable() -> None:
    i18n = I18N_SOURCE.read_text(encoding="utf-8")
    page = PAGE_SOURCE.read_text(encoding="utf-8")
    declaration = re.search(r"export const locales = \[(.*?)\] as const", i18n)

    assert declaration is not None
    declared = set(re.findall(r'"([a-z]{2})"', declaration.group(1)))
    assert declared == EU_OFFICIAL_LOCALES
    assert "locales.map" in page
    assert "localeMetadata[x].reviewStatus" in page


def test_every_locale_has_metadata_and_translation_review_status() -> None:
    i18n = I18N_SOURCE.read_text(encoding="utf-8")
    metadata_source = i18n.split("export const localeMetadata", maxsplit=1)[1]

    for locale in EU_OFFICIAL_LOCALES:
        entry = re.search(rf"\b{locale}:\{{([^}}]+)\}}", metadata_source)
        assert entry is not None
        metadata = entry.group(1)
        assert "nativeName:" in metadata
        assert "intlLocale:" in metadata
        assert 'direction:"ltr"' in metadata
        expected_status = "human-reviewed" if locale == "en" else "draft"
        assert f'reviewStatus:"{expected_status}"' in metadata


def _mojibake_windows(source: str) -> list[str]:
    """Find short sequences that are valid UTF-8 bytes misread as a legacy encoding."""

    suspicious: list[str] = []
    for start in range(len(source)):
        for width in (2, 3, 4):
            window = source[start : start + width]
            if len(window) != width or not any(ord(char) > 127 for char in window):
                continue
            for legacy_encoding in ("cp1252", "latin-1"):
                try:
                    repaired = window.encode(legacy_encoding).decode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    continue
                if repaired != window and any(ord(char) > 127 for char in repaired):
                    suspicious.append(window)
                    break
    return suspicious


def test_user_facing_sources_are_valid_utf8_without_common_mojibake() -> None:
    sources = [
        I18N_SOURCE.read_text(encoding="utf-8"),
        PAGE_SOURCE.read_text(encoding="utf-8"),
    ]
    for source in sources:
        assert _mojibake_windows(source) == []


@pytest.mark.parametrize(
    "corrupted",
    ["Ã¼", "Ã§", "Ä", "Å¡", "È™", "È›", "â‚¬", "â€”", "Â·", "ÐŸ", "Î“"],
)
def test_mojibake_detector_covers_supported_language_failure_patterns(
    corrupted: str,
) -> None:
    assert _mojibake_windows(corrupted)


@pytest.mark.parametrize(
    "valid",
    ["ü", "ç", "č", "š", "ș", "ț", "€", "—", "·", "П", "Γ", "Română", "Magyar", "Français"],
)
def test_mojibake_detector_accepts_valid_eu_language_text(valid: str) -> None:
    assert _mojibake_windows(valid) == []
