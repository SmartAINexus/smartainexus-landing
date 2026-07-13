# GrantBridge Europe – development shift handover – 2026-07-13 06:57 EEST

## Current baseline

- Branch: `develop/grantbridge-mvp-2026-07-13`
- Baseline commit before this handover: `c6e79d2`
- Pilot: Romania
- Planned operator: Szökőcs Green SRL, Sălaj County, Romania
- Data posture: synthetic data only
- Production launch: not authorized
- Plesk/CentOS 7 server: STOP-SHIP for GrantBridge deployment or service changes

## Implemented program code

- Next.js synthetic Romanian-pilot frontend with all 24 EU official language selectors and explicit
  translation review status.
- FastAPI, SQLAlchemy and Alembic backend foundation for NGO tenants, grants, global official-source
  opportunities, append-only observations and tenant-scoped match history.
- Crawler policy gates, deterministic source identity and content hashing; expected unique-key races
  are recovered idempotently by backend ingestion.
- Opportunity ingestion preserves content/provenance snapshots, validates stable identity and handles
  expected concurrent unique-key races without swallowing unrelated integrity failures.
- Persisted backend opportunity matches are append-only auditable drafts, and backend schema/storage
  always require human review. AI `MatchResult` defaults to review and forces it when exclusion risks
  exist.
- Structured AI draft guard enforces exact per-field schemas and hard character limits without silent
  truncation. Supported counting policies include Unicode code points, NFC-normalized code points,
  UTF-16 code units and configurable CRLF handling.
- Provider-neutral OIDC readiness contract validates issuer, audience, subject, expiry and tenant UUID
  only after a future cryptographic verifier. OIDC API access remains fail-closed with HTTP 503.

## Retained verification evidence

- Local crawler suite: 16 passed.
- Local backend suite: 38 passed; one non-blocking Starlette/httpx deprecation warning.
- Local AI suite: 20 passed.
- Local handover review with `PYTHONPATH` set to `backend;.` and command
  `python -m pytest integration_tests -q`: 30 passed in 1.44 seconds. This invocation includes
  synthetic integration plus parameterized 24-language/source-integrity cases.
- Fresh disposable SQLite `alembic upgrade head`: passed through revisions 0001, 0002 and 0003;
  schema inspection confirmed `content_snapshot` on `opportunity_observations`.
- Independent reviewer/tester verdicts: PASS for identity/history, 24-language QA, concurrent ingestion,
  OIDC readiness and character-limit enforcement after findings were corrected.
- GitHub Actions frontend lint/build and backend/crawler/AI/integration jobs passed with retained runs:
  - `ce757f5`: https://github.com/SmartAINexus/smartainexus-landing/actions/runs/29221331205
  - `00754b9`: https://github.com/SmartAINexus/smartainexus-landing/actions/runs/29221652467
  - `708ee4a`: https://github.com/SmartAINexus/smartainexus-landing/actions/runs/29222040855
  - `91c6288`: https://github.com/SmartAINexus/smartainexus-landing/actions/runs/29222276150
  - `c6e79d2`: https://github.com/SmartAINexus/smartainexus-landing/actions/runs/29222641701

## Not implemented or not verified

- No production identity provider, JWKS signature verifier or live login flow is connected.
- No provider, contract, payment, real personal data or real NGO data was used.
- No production PostgreSQL instance has been provisioned; PostgreSQL upgrade/downgrade rehearsal is
  still required in a disposable approved environment.
- No GrantBridge component was deployed to the current Plesk/CentOS 7 server.
- The 23 non-English translation sets are marked draft until human linguistic review; selector and
  source-integrity coverage do not constitute linguistic approval.
- The UI is still a synthetic demonstration and is not yet connected to live backend workflows.

## Next safe work package

Connect the synthetic frontend profile and opportunity feed to a typed, mocked API boundary with
loading/error/empty states and browser-level tests. Keep all data synthetic and do not enable OIDC,
production deployment or real uploads.

## Founder decision required now

None. Identity-provider selection, paid infrastructure, production database, real-data processing and
production launch remain reserved for later explicit Founder approval.
