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

## Claude CLI Benchmark Runs

SemLock-enabled run:

```bash
cd /Users/prittamravi/semlock-billing-demo
git reset --hard HEAD

/usr/bin/time -p sh -c '
  claude -p \
    --permission-mode bypassPermissions \
    "$(cat /Users/prittamravi/semlock-billing-demo/PROMPT_10_AGENTS.md)"
' | tee /Users/prittamravi/semlock-billing-demo/claude_10_agent_with_semlock.log
```

No-SemLock run:

```bash
cd /Users/prittamravi/semlock-billing-demo
git reset --hard HEAD

/usr/bin/time -p sh -c '
  claude -p \
    --permission-mode bypassPermissions \
    --strict-mcp-config \
    --mcp-config /Users/prittamravi/semlock-billing-demo/empty_mcp.json \
    -- \
    "$(cat /Users/prittamravi/semlock-billing-demo/PROMPT_10_AGENTS_NO_SEMLOCK.md)"
' | tee /Users/prittamravi/semlock-billing-demo/claude_10_agent_no_semlock.log
```
