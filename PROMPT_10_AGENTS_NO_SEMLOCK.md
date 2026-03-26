# 10-Agent Same-File Prompt Without SemLock

You are working in the repo `/Users/prittamravi/semlock-billing-demo`.

Spawn 10 worker agents in parallel.

Do not use SemLock or any MCP locking tools.

All workers must follow these rules:

1. Work only in `billing/charge_pipeline.py`.
2. Each worker owns exactly one assigned top-level function and must edit only that function body.
3. Do not edit imports, constants, headers, signatures, or any other function.
4. Keep the file valid Python.
5. Before each edit attempt, re-read the latest `billing/charge_pipeline.py` from disk so the worker is not editing an old snapshot.
6. If a worker notices its change was lost or overwritten, it must retry by re-reading the latest file and applying only its assigned change again.
7. Keep retrying until all 10 assigned changes are present in the final file.
8. Do not introduce any changes beyond the 10 assigned function-body edits below.

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
2. Confirm whether all 10 assigned edits are present in the final file.
3. Report how many retries were needed because another worker overwrote or displaced a change.
