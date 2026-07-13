from __future__ import annotations

from ai.contracts import MatchResult


def as_backend_match_payload(
    result: MatchResult,
    *,
    tenant_id: str,
    opportunity_id: str,
    model_provider: str,
    model_id: str,
    prompt_version: str,
) -> dict[str, object]:
    """Serialize a reviewed contract shape without adding or inferring facts."""

    return {
        "tenant_id": tenant_id,
        "opportunity_id": opportunity_id,
        "score": result.score,
        "factors": [
            {
                "name": factor.name,
                "score": factor.score,
                "rationale": factor.rationale,
                "evidence_state": factor.evidence_state.value,
                "source_reference": factor.source_reference,
            }
            for factor in result.factors
        ],
        "missing_information": list(result.missing_information),
        "exclusion_risks": list(result.exclusion_risks),
        "requires_human_review": result.requires_human_review,
        "model_provider": model_provider,
        "model_id": model_id,
        "prompt_version": prompt_version,
    }
