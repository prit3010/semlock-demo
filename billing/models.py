"""Domain models for the billing demo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ChargeAttempt:
    """One charge attempt waiting to be retried or reviewed."""

    charge_id: str
    customer_id: str
    amount_cents: int
    currency: str
    risk_score: int
    retry_count: int
    is_vip: bool = False
