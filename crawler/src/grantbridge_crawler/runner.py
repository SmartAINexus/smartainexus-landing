from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from .errors import NavigationError
from .models import FundingOpportunity
from .parser import DataAttributeOpportunityParser
from .policy import CrawlPolicy
from .upsert import OpportunityRepository, UpsertResult


class PageLoader(Protocol):
    async def load(self, url: str) -> str: ...


class PlaywrightPageLoader:
    """Production loader. Policy authorization must happen before calling load."""

    def __init__(
        self, *, policy: CrawlPolicy, timeout_ms: int = 30_000, user_agent: str
    ) -> None:
        self.policy = policy
        self.timeout_ms = timeout_ms
        self.user_agent = user_agent

    async def load(self, url: str) -> str:
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                try:
                    context = await browser.new_context(user_agent=self.user_agent)
                    page = await context.new_page()

                    async def guard_navigation(route: object) -> None:
                        request = route.request
                        if request.resource_type == "document":
                            try:
                                self.policy.authorize(request.url)
                            except Exception:
                                await route.abort("blockedbyclient")
                                return
                        await route.continue_()

                    await page.route("**/*", guard_navigation)
                    response = await page.goto(
                        url, wait_until="domcontentloaded", timeout=self.timeout_ms
                    )
                    if response is None or not response.ok:
                        status = response.status if response else "no response"
                        raise NavigationError(f"Approved source returned {status}")
                    return await page.content()
                finally:
                    await browser.close()
        except NavigationError:
            raise
        except Exception as exc:
            raise NavigationError(f"Playwright navigation failed: {exc}") from exc


@dataclass(frozen=True, slots=True)
class CrawlOutcome:
    opportunity: FundingOpportunity
    upsert_result: UpsertResult


class FundingCrawler:
    def __init__(
        self,
        *,
        policy: CrawlPolicy,
        loader: PageLoader,
        parser: DataAttributeOpportunityParser,
        repository: OpportunityRepository,
    ) -> None:
        self.policy = policy
        self.loader = loader
        self.parser = parser
        self.repository = repository

    async def crawl(self, url: str) -> list[CrawlOutcome]:
        approval = self.policy.authorize(url)  # Must precede all network activity.
        html = await self.loader.load(url)
        records = self.parser.parse(
            html,
            source_url=url,
            retrieved_at=datetime.now(timezone.utc),
            approval=approval,
        )
        outcomes = []
        for record in records:
            outcomes.append(CrawlOutcome(record, await self.repository.upsert(record)))
        return outcomes
