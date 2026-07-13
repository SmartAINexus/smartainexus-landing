# GrantBridge AI contracts

This package contains provider-neutral AI contracts. It performs no external
model call and accepts no raw identity, banking, or uploaded-document content.

## Safety baseline

- Inputs are minimized and tenant-scoped before entering the AI boundary.
- Prompts require explicit uncertainty and prohibit fabricated facts.
- Outputs are drafts until human review.
- Character limits are hard validation rules, not suggestions.
- Structured draft fields must exactly match configured rules; missing or extra fields fail closed.
- Over-limit output is rejected without silent truncation or rewriting.
- Per-field counting can use Unicode code points, NFC-normalized code points, or UTF-16 code units.
- CRLF normalization is explicit and can be disabled for portals that count both code units.
- Invalid Unicode surrogate code points are rejected in every count mode.
- Strict JSON parsing retains and rejects duplicate output field names.
- `count_spaces=false` ignores only ASCII space (U+0020); tabs and nonbreaking spaces still count.
- A future provider must contractually disable training on customer data and
  meet the approved EU data-processing requirements.

Run the standard-library tests with:

```bash
python -m unittest discover -s ai/tests -v
```
