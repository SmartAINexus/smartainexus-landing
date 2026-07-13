import unittest

from ai.character_limits import CountMode, FieldLimit, require_within_limit, validate_limit


class CharacterLimitTests(unittest.TestCase):
    def test_exact_limit_is_valid(self) -> None:
        result = validate_limit("12345", FieldLimit("objective", 5))
        self.assertTrue(result.valid)
        self.assertEqual(result.remaining, 0)

    def test_over_limit_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "exceeds the character limit by 1"):
            require_within_limit("123456", FieldLimit("objective", 5))

    def test_hungarian_unicode_is_counted_as_codepoints(self) -> None:
        result = validate_limit("árvíztűrő", FieldLimit("summary", 9))
        self.assertTrue(result.valid)
        self.assertEqual(result.count, 9)

    def test_nfc_normalization_is_explicit(self) -> None:
        decomposed = "e\u0301"
        raw = validate_limit(decomposed, FieldLimit("raw", 1))
        normalized = validate_limit(
            decomposed,
            FieldLimit("normalized", 1, mode=CountMode.NORMALIZED_CODEPOINTS),
        )
        self.assertFalse(raw.valid)
        self.assertTrue(normalized.valid)

    def test_line_break_rule_is_configurable(self) -> None:
        counted = validate_limit("a\nb", FieldLimit("counted", 2))
        ignored = validate_limit(
            "a\nb", FieldLimit("ignored", 2, count_line_breaks=False)
        )
        self.assertFalse(counted.valid)
        self.assertTrue(ignored.valid)


if __name__ == "__main__":
    unittest.main()

