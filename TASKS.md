# 10-Agent Same-File Tasks

All agents should work only in:

- `billing/charge_pipeline.py`

Task map:

1. `classify_retry_window`
2. `apply_retry_backoff`
3. `should_hold_for_fraud`
4. `compute_tax_buffer`
5. `estimate_capture_amount`
6. `reconcile_webhook_event`
7. `build_customer_notice`
8. `reserve_ledger_code`
9. `route_charge_outcome`
10. `summarize_charge_attempt`
