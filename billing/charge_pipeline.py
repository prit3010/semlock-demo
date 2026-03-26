"""Shared billing charge pipeline hot file for SemLock demos."""

from __future__ import annotations

from billing.config import (
    DEFAULT_RETRY_LIMIT,
    DEFAULT_TAX_BUFFER_CENTS,
    HIGH_RISK_SCORE,
    VIP_LEDGER_THRESHOLD_CENTS,
    VIP_REVIEW_SCORE,
)
from billing.models import ChargeAttempt


def classify_retry_window(attempt: ChargeAttempt) -> str:
    if attempt.retry_count >= DEFAULT_RETRY_LIMIT:
        return "manual_review"
    if attempt.retry_count == 0:
        return "immediate"
    if attempt.retry_count == 1:
        return "short_delay"
    return "long_delay"

def apply_retry_backoff(attempt: ChargeAttempt) -> int:
    window = classify_retry_window(attempt)
    if window == "immediate":
        return 30
    if window == "short_delay":
        return 300
    if window == "long_delay":
        return 900
    return 0

def should_hold_for_fraud(attempt: ChargeAttempt) -> bool:
    threshold = VIP_REVIEW_SCORE if attempt.is_vip else HIGH_RISK_SCORE
    return attempt.risk_score >= threshold

def compute_tax_buffer(amount_cents: int, jurisdiction_rate: float) -> int:
    return round(amount_cents * jurisdiction_rate) + DEFAULT_TAX_BUFFER_CENTS


def estimate_capture_amount(attempt: ChargeAttempt, jurisdiction_rate: float) -> int:
    tax_buffer = compute_tax_buffer(attempt.amount_cents, jurisdiction_rate)
    return attempt.amount_cents + tax_buffer

def reconcile_webhook_event(event_name: str, seen_before: bool) -> str:
    normalized = event_name.strip().lower()
    if seen_before:
        return "duplicate"
    return normalized


def build_customer_notice(attempt: ChargeAttempt, delay_seconds: int) -> str:
    retry_window = classify_retry_window(attempt)
    if retry_window == "manual_review":
        return f"Charge {attempt.charge_id} requires manual review."
    return f"Charge {attempt.charge_id} will retry in {delay_seconds} seconds."

def reserve_ledger_code(attempt: ChargeAttempt) -> str:
    if attempt.is_vip and attempt.amount_cents >= VIP_LEDGER_THRESHOLD_CENTS:
        return "vip_priority_hold"
    if attempt.amount_cents >= VIP_LEDGER_THRESHOLD_CENTS:
        return "large_charge_hold"
    return "standard_retry_hold"

def route_charge_outcome(attempt: ChargeAttempt) -> str:
    if should_hold_for_fraud(attempt):
        return "risk_hold"
    retry_window = classify_retry_window(attempt)
    if retry_window == "manual_review":
        return "manual_review"
    return "retry_queue"

def summarize_charge_attempt(
    attempt: ChargeAttempt,
    jurisdiction_rate: float,
) -> dict[str, object]:
    delay_seconds = apply_retry_backoff(attempt)
    return {
        "charge_id": attempt.charge_id,
        "route": route_charge_outcome(attempt),
        "capture_amount_cents": estimate_capture_amount(attempt, jurisdiction_rate),
        "ledger_code": reserve_ledger_code(attempt),
        "customer_notice": build_customer_notice(attempt, delay_seconds),
    }
