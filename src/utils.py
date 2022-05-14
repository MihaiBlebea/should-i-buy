from __future__ import annotations


def fmt_amount(amount: int | float)-> str:
	prefix = "-" if amount < 0 else ""

	if abs(amount) > 1_000_000_000:
		return f"{prefix}${abs(round(amount / 1_000_000_000, 2))}b"

	if abs(amount) > 1_000_000:
		return f"{prefix}${abs(round(amount / 1_000_000, 2))}m"

	if abs(amount) > 1_000:
		return f"{prefix}${abs(round(amount / 1_000, 2))}k"

	return f"{prefix}${abs(round(amount, 2))}"