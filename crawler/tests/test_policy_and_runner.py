import asyncio
from datetime import datetime

import pytest

from grantbridge_crawler.errors import PolicyDeniedError
from grantbridge_crawler.parser import DataAttributeOpportunityParser
from grantbridge_crawler.policy import CrawlPolicy, SourceApproval
from grantbridge_crawler.runner import FundingCrawler
from grantbridge_crawler.upsert import InMemoryOpportunityRepository, UpsertResult


class FixtureLoader:
    def __init__(self, html: str) -> None:
        self.html = html
        self.calls = 0

    async def load(self, url: str) -> str:
        self.calls += 1
        return self.html


def approved_source(**changes: object) -> SourceApproval:
    values = dict(
        host="funding.example.test",
        approval_id="fixture-approval",
        official_source=True,
        terms_approved=True,
        terms_evidence="fixture terms decision",
        robots_allowed=True,
        robots_evidence="fixture robots decision",
        allowed_path_prefixes=("/calls",),
    )
    values.update(changes)
    return SourceApproval(**values)


def test_denies_unknown_host() -> None:
    with pytest.raises(PolicyDeniedError, match="not allowlisted"):
        CrawlPolicy([approved_source()]).authorize("https://unknown.example.test/calls")


@pytest.mark.parametrize(
    "change",
    [
        {"official_source": False},
        {"terms_approved": False},
        {"terms_evidence": ""},
        {"robots_allowed": False},
        {"robots_evidence": ""},
    ],
)
def test_denies_each_unresolved_source_gate(change: dict[str, object]) -> None:
    with pytest.raises(PolicyDeniedError):
        CrawlPolicy([approved_source(**change)]).authorize(
            "https://funding.example.test/calls/open"
        )


def test_policy_denial_happens_before_loader_navigation() -> None:
    loader = FixtureLoader("<html></html>")
    crawler = FundingCrawler(
        policy=CrawlPolicy([]),
        loader=loader,
        parser=DataAttributeOpportunityParser(),
        repository=InMemoryOpportunityRepository(),
    )
    async def scenario() -> None:
        with pytest.raises(PolicyDeniedError):
            await crawler.crawl("https://funding.example.test/calls")
        assert loader.calls == 0

    asyncio.run(scenario())


def test_fixture_runner_parses_and_upserts_without_network() -> None:
    html = """<article data-opportunity><span data-field='identifier'>SYN-RUNNER-1</span><h2 data-field='title'>Synthetic call</h2>
    <span data-field='funder'>Synthetic funder</span>
    <p data-field='description'>Synthetic description</p>
    <time data-field='deadline' datetime='2026-09-30T17:00:00+03:00'></time>
    <span data-field='timezone'>Europe/Bucharest</span>
    <li data-field='eligibility'>Romanian nonprofits</li></article>"""
    loader = FixtureLoader(html)
    crawler = FundingCrawler(
        policy=CrawlPolicy([approved_source()]),
        loader=loader,
        parser=DataAttributeOpportunityParser(),
        repository=InMemoryOpportunityRepository(),
    )
    async def scenario() -> None:
        outcomes = await crawler.crawl("https://funding.example.test/calls/open")
        assert loader.calls == 1
        assert outcomes[0].upsert_result == UpsertResult.INSERTED
        assert isinstance(outcomes[0].opportunity.deadline, datetime)

    asyncio.run(scenario())
