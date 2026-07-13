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

    def test_platform_can_preserve_crlf_as_two_characters(self) -> None:
        normalized = validate_limit("a\r\nb", FieldLimit("normalized", 3))
        preserved = validate_limit(
            "a\r\nb", FieldLimit("preserved", 4, normalize_line_breaks=False)
        )
        self.assertEqual(normalized.count, 3)
        self.assertEqual(preserved.count, 4)

    def test_lone_surrogate_is_rejected_in_every_count_mode(self) -> None:
        for mode in CountMode:
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(ValueError, "invalid Unicode surrogate"):
                    validate_limit("\ud800", FieldLimit("invalid", 10, mode=mode))

    def test_zwj_sequence_has_explicit_codepoint_and_utf16_counts(self) -> None:
        family = "👩‍👩‍👧‍👦"
        codepoints = validate_limit(family, FieldLimit("family", 20))
        utf16 = validate_limit(
            family, FieldLimit("family", 20, mode=CountMode.UTF16_CODE_UNITS)
        )
        self.assertEqual(codepoints.count, 7)
        self.assertEqual(utf16.count, 11)

    def test_count_spaces_false_removes_only_ascii_space(self) -> None:
        result = validate_limit(
            "a \t\u00a0b", FieldLimit("spacing", 10, count_spaces=False)
        )
        self.assertEqual(result.count, 4)


if __name__ == "__main__":
    unittest.main()
