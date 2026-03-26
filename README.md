# SemLock Billing Demo

This is a standalone Git-backed demo repo for testing SemLock on a realistic
same-file workflow.

The hot file is:

- `billing/charge_pipeline.py`

It contains 10 top-level functions that multiple agents can edit in parallel.

To run the SemLock MCP server against this repo from the SemLock workspace:

```bash
cd /Users/prittamravi/SemLock
uv run semlock-mcp --repo-root /Users/prittamravi/semlock-billing-demo
```

Suggested 10-agent prompt:

- See `TASKS.md`
