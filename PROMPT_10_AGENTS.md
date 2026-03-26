# 10-Agent Same-File Prompt

You have access to the SemLock MCP server for repo `/Users/prittamravi/semlock-billing-demo`.

Spawn 10 worker agents in parallel.

All workers must follow these rules:

1. Work only in `billing/charge_pipeline.py`.
2. Before reading or editing, use SemLock on only the assigned top-level function:
   - `list_regions("billing/charge_pipeline.py")`
   - `acquire_locks(...)` for the assigned region only
   - `get_region(...)`
   - `commit_region(...)` with the full replacement text for that function
3. Do not edit imports, constants, headers, signatures, or any other function.
4. Keep the file valid Python.
5. If a retryable SemLock error occurs, retry a few times and report what happened.

Worker assignments:

- Worker 1 owns `classify_retry_window`
  Change only the implementation so VIP charges with `retry_count >= DEFAULT_RETRY_LIMIT - 1` return `"manual_review"` before the existing fallback logic.

- Worker 2 owns `apply_retry_backoff`
  Change only the implementation so the delay mapping becomes:
  - `"immediate"` -> `20`
  - `"short_delay"` -> `240`
  - `"long_delay"` -> `720`
  - manual review still returns `0`

- Worker 3 owns `should_hold_for_fraud`
  Change only the implementation so the threshold is reduced by `3` more points when `attempt.retry_count > 0`.

- Worker 4 owns `compute_tax_buffer`
  Change only the implementation so the rounded tax amount is clamped with `max(DEFAULT_TAX_BUFFER_CENTS, ...)` before adding `DEFAULT_TAX_BUFFER_CENTS`.

- Worker 5 owns `estimate_capture_amount`
  Change only the implementation so VIP charges add an extra `15` cents before returning the capture amount.

- Worker 6 owns `reconcile_webhook_event`
  Change only the implementation so normalized event names replace spaces with underscores, and duplicates return `"duplicate_replayed"`.

- Worker 7 owns `build_customer_notice`
  Change only the implementation so the retry message reads:
  `"Charge <id> is scheduled to retry after <delay> seconds for customer <customer_id>."`

- Worker 8 owns `reserve_ledger_code`
  Change only the implementation so there is a highest-priority branch:
  `if attempt.is_vip and attempt.risk_score >= VIP_REVIEW_SCORE: return "vip_manual_review"`

- Worker 9 owns `route_charge_outcome`
  Change only the implementation so non-fraud, non-manual-review charges with retry window `"short_delay"` return `"retry_soon_queue"`; otherwise keep the existing `"retry_queue"` behavior.

- Worker 10 owns `summarize_charge_attempt`
  Change only the implementation so the returned dict also includes `"retry_delay_seconds": delay_seconds`.

After all 10 workers finish:

1. Show the final diff for `billing/charge_pipeline.py`.
2. Confirm that all 10 workers used SemLock on distinct regions in the same file.
3. Report any lock conflicts, stale-hash retries, or semantic rejections that occurred.
