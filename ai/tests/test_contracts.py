import unittest

from ai.contracts import EvidenceState, MatchFactor, MatchResult


class ContractTests(unittest.TestCase):
    def test_score_bounds_are_enforced(self) -> None:
        with self.assertRaises(ValueError):
            MatchResult(score=101)

    def test_exclusion_risk_requires_review(self) -> None:
        with self.assertRaises(ValueError):
            MatchResult(
                score=10,
                exclusion_risks=("Applicant type is not verified",),
                requires_human_review=False,
            )

    def test_factor_keeps_evidence_state(self) -> None:
        factor = MatchFactor(
            name="geography",
            score=80,
            rationale="Romania is listed in the supplied evidence.",
            evidence_state=EvidenceState.VERIFIED,
            source_reference="official-call.pdf#section-2",
        )
        self.assertEqual(factor.evidence_state, EvidenceState.VERIFIED)


if __name__ == "__main__":
    unittest.main()
