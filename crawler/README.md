# GrantBridge Europe crawler

Policy-gated Python/Playwright architecture for importing opportunities from official funding sources. This package currently contains no configured live source and the test suite performs no network access.

## Safety boundary

Navigation is fail-closed. `CrawlPolicy.authorize()` runs before the page loader and requires all of the following for the exact hostname and path:

1. explicit allowlist record and approval ID;
2. source recorded as official;
3. documented terms/licence approval;
4. documented robots.txt approval;
5. HTTPS and an approved path prefix.

An empty, missing or negative decision denies crawling. A production approval record must point to retained legal/compliance evidence; the synthetic values in tests are not approval for any real source. The Playwright loader routes every document navigation, including redirects, through the same policy before allowing the request.

## Architecture

- `policy.py`: pre-navigation robots/terms/allowlist gates.
- `runner.py`: orchestration plus an injectable Playwright page loader.
- `parser.py`: deterministic reference parser. Real sources should receive dedicated adapters implementing the same output contract.
- `models.py`: title, offset-aware deadline, IANA timezone, eligibility, source URL and provenance schema.
- `dedupe.py`: NFKC/case/whitespace normalization, tracking-free canonical URLs and SHA-256 content hashes.
- `upsert.py`: async repository protocol and in-memory reference implementation.
- `tests/fixtures`: synthetic HTML only.

The crawler does not infer a timezone from server or browser locale. Both an offset-aware deadline and an explicit valid IANA timezone are required. Invalid or incomplete records fail parsing instead of being published.

## Installation and tests

Use a Python 3.11+ virtual environment. Installing dependencies and browsers is an explicit environment setup step and was not performed by this implementation:

```text
python -m pip install -e ".[test]"
python -m playwright install chromium
python -m pytest
```

The tests cover fixture parsing, required fields, provenance, policy denial before navigation, URL/content normalization, hash deduplication and the upsert contract.

## Adding an official source

1. Obtain and retain ownership, robots.txt, terms/licence and path-scope evidence.
2. Record a narrowly scoped `SourceApproval`; never use wildcard hosts.
3. Implement a source-specific parser with fixture snapshots containing no personal data.
4. Add golden, malformed-input, deadline/timezone and deduplication tests.
5. Test redirects so every destination is re-authorized.
6. Have a separate compliance/source reviewer approve the adapter and evidence.
7. Only then wire the adapter to `PlaywrightPageLoader` and a production `OpportunityRepository`.

## Upsert contract

`OpportunityRepository.upsert()` accepts one fully validated `FundingOpportunity` and returns `inserted`, `unchanged` or `updated`. The normalized hash is the idempotency key. Production repositories should additionally retain observation history and provenance rather than overwriting evidence.

## Error handling

- `PolicyDeniedError`: source approval gate failed; no navigation should occur.
- `NavigationError`: an approved page could not be loaded or returned a failing response.
- `ParseError`: no valid record or a required structured field is missing/invalid.

Errors are explicit and suitable for a quarantine/dead-letter workflow. They must not silently activate a funding opportunity.
