from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from html.parser import HTMLParser
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .dedupe import content_hash, source_key
from .errors import ParseError
from .models import FundingOpportunity, Provenance
from .policy import SourceApproval


class _OpportunityHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: list[dict[str, object]] = []
        self._record: dict[str, object] | None = None
        self._record_tag: str | None = None
        self._field: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        # Boolean HTML attributes are represented as ``None`` by HTMLParser.
        # Membership, rather than the attribute value, therefore identifies a
        # record container such as ``<article data-opportunity>``.
        if "data-opportunity" in values:
            self._record = {}
            self._record_tag = tag
        if self._record is not None and values.get("data-field"):
            self._field = values["data-field"]
            self._buffer = []
            if self._field == "deadline":
                self._record["deadline"] = values.get("datetime", "")

    def handle_data(self, data: str) -> None:
        if self._field:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._record is not None and self._field:
            text = " ".join("".join(self._buffer).split())
            if self._field == "eligibility":
                self._record.setdefault("eligibility", []).append(text)
            elif self._field != "deadline" or not self._record.get("deadline"):
                self._record[self._field] = text
            self._field = None
            self._buffer = []
        if tag == self._record_tag and self._record is not None:
            self.records.append(self._record)
            self._record = None
            self._record_tag = None


class DataAttributeOpportunityParser:
    """Reference parser for source adapters and deterministic HTML fixtures."""

    name = "data-attribute-opportunity-parser"
    version = "1.0"

    def parse(
        self,
        html: str,
        *,
        source_url: str,
        retrieved_at: datetime,
        approval: SourceApproval,
    ) -> list[FundingOpportunity]:
        collector = _OpportunityHTMLParser()
        collector.feed(html)
        results: list[FundingOpportunity] = []
        for index, raw in enumerate(collector.records, start=1):
            try:
                source_identifier = str(raw["identifier"]).strip()
                title = str(raw["title"]).strip()
                funder = str(raw["funder"]).strip()
                description = str(raw["description"]).strip()
                timezone = str(raw["timezone"]).strip()
                ZoneInfo(timezone)
                deadline = datetime.fromisoformat(str(raw["deadline"]).strip())
                eligibility = tuple(
                    item.strip() for item in raw.get("eligibility", []) if str(item).strip()
                )
                if not source_identifier or not title or not funder or not description or not eligibility or deadline.tzinfo is None:
                    raise ValueError("required field is blank or deadline has no UTC offset")
            except (KeyError, ValueError, ZoneInfoNotFoundError) as exc:
                raise ParseError(f"Invalid opportunity record #{index}: {exc}") from exc
            provenance = Provenance(
                source_url=source_url,
                retrieved_at=retrieved_at,
                parser_name=self.name,
                parser_version=self.version,
                official_source=approval.official_source,
                allowlist_approval_id=approval.approval_id,
                robots_evidence=approval.robots_evidence,
                terms_evidence=approval.terms_evidence,
            )
            opportunity = FundingOpportunity(
                source_identifier=source_identifier,
                title=title,
                funder=funder,
                description=description,
                deadline=deadline,
                timezone=timezone,
                eligibility=eligibility,
                source_url=source_url,
                provenance=provenance,
            )
            results.append(
                replace(
                    opportunity,
                    source_key=source_key(opportunity),
                    content_hash=content_hash(opportunity),
                )
            )
        if not results:
            raise ParseError("No opportunity records found")
        return results
