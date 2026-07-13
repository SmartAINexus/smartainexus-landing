from datetime import datetime, timezone
from pathlib import Path

import pytest

from grantbridge_crawler.errors import ParseError
from grantbridge_crawler.parser import DataAttributeOpportunityParser
from grantbridge_crawler.policy import SourceApproval

FIXTURE = Path(__file__).parent / "fixtures" / "official_opportunities.html"


def approval() -> SourceApproval:
    return SourceApproval(
        host="funding.example.test",
        approval_id="synthetic-fixture-only",
        official_source=True,
        terms_approved=True,
        terms_evidence="fixture:terms-approved",
        robots_allowed=True,
        robots_evidence="fixture:robots-allowed",
    )


def test_parses_structured_records_with_provenance() -> None:
    records = DataAttributeOpportunityParser().parse(
        FIXTURE.read_text(encoding="utf-8"),
        source_url="https://funding.example.test/calls",
        retrieved_at=datetime(2026, 7, 13, tzinfo=timezone.utc),
        approval=approval(),
    )
    assert len(records) == 2
    assert records[0].title == "Community Green Transition 2026"
    assert records[0].funder == "Synthetic Romanian Public Authority"
    assert records[0].description.startswith("Synthetic programme")
    assert records[0].deadline.isoformat() == "2026-09-30T17:00:00+03:00"
    assert records[0].timezone == "Europe/Bucharest"
    assert len(records[0].eligibility) == 2
    assert records[0].provenance.allowlist_approval_id == "synthetic-fixture-only"
    assert len(records[0].normalized_hash) == 64


def test_rejects_missing_timezone_and_offset() -> None:
    html = """<article data-opportunity><h2 data-field='title'>Call</h2>
    <span data-field='funder'>Synthetic funder</span>
    <p data-field='description'>Synthetic description</p>
    <time data-field='deadline' datetime='2026-09-30T17:00:00'></time>
    <li data-field='eligibility'>Nonprofits</li></article>"""
    with pytest.raises(ParseError):
        DataAttributeOpportunityParser().parse(
            html,
            source_url="https://funding.example.test/calls",
            retrieved_at=datetime.now(timezone.utc),
            approval=approval(),
        )
