from ai.backend_adapter import as_backend_match_payload
from ai.contracts import EvidenceState, MatchFactor, MatchResult


def test_adapter_preserves_review_and_evidence_states() -> None:
    result = MatchResult(
        score=68,
        factors=(
            MatchFactor(
                name="geography",
                score=90,
                rationale="Synthetic verified country alignment",
                evidence_state=EvidenceState.VERIFIED,
                source_reference="synthetic:eligibility:1",
            ),
        ),
        missing_information=("Synthetic co-funding evidence",),
        exclusion_risks=("Synthetic legal-form review",),
        requires_human_review=True,
    )
    payload = as_backend_match_payload(
        result,
        tenant_id="00000000-0000-0000-0000-000000000001",
        opportunity_id="00000000-0000-0000-0000-000000000002",
        model_provider="synthetic-provider",
        model_id="synthetic-model",
        prompt_version="match-v1",
    )

    assert payload["requires_human_review"] is True
    assert payload["factors"][0]["evidence_state"] == "verified"
    assert payload["exclusion_risks"] == ["Synthetic legal-form review"]
