# OIDC readiness boundary

Status: design and claim-policy code only. Production authentication is not enabled.

Implemented and tested:

- OIDC mode requires an HTTPS issuer, an audience, and a non-empty tenant claim name.
- Already signature-verified claims must match issuer and audience.
- Subject, expiry, and a UUID tenant claim are mandatory.
- Development header authentication remains forbidden in production.
- The API still returns `503 OIDC authentication is not configured` in OIDC mode.

Still required before OIDC can be enabled:

1. Founder-approved identity provider and tenant architecture.
2. Provider discovery metadata and JWKS signature verification.
3. Algorithm allow-list, key rotation, clock-skew, `nbf`, and replay/session policy.
4. Provisioning rule that binds provider identities to GrantBridge NGO tenants.
5. Security and GDPR review with retained evidence.
6. Synthetic end-to-end login tests, then explicit production authorization.

No token may be accepted by merely decoding its payload. The function
`principal_from_verified_claims` is intentionally downstream of a future cryptographic verifier.
