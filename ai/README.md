# GrantBridge AI contracts

This package contains provider-neutral AI contracts. It performs no external
model call and accepts no raw identity, banking, or uploaded-document content.

## Safety baseline

- Inputs are minimized and tenant-scoped before entering the AI boundary.
- Prompts require explicit uncertainty and prohibit fabricated facts.
- Outputs are drafts until human review.
- Character limits are hard validation rules, not suggestions.
- A future provider must contractually disable training on customer data and
  meet the approved EU data-processing requirements.

Run the standard-library tests with:

```bash
python -m unittest discover -s ai/tests -v
```

