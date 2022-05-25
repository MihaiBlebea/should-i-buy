from __future__ import annotations
from yahoo_fin_api import Ticker

def fmt_amount(amount: int | float)-> str:
	prefix = "-" if amount < 0 else ""

	if abs(amount) > 1_000_000_000:
		return f"{prefix}${abs(round(amount / 1_000_000_000, 2))}b"

	if abs(amount) > 1_000_000:
		return f"{prefix}${abs(round(amount / 1_000_000, 2))}m"

	if abs(amount) > 1_000:
		return f"{prefix}${abs(round(amount / 1_000, 2))}k"

	return f"{prefix}${abs(round(amount, 2))}"

def current_price(ticker: Ticker)-> float:
	if ticker.financial_data is None:
		raise Exception("financial_data not found")

	if ticker.financial_data.current_price is None:
		raise Exception("current_price not found")

	return ticker.financial_data.current_price

def fair_share_price(ticker: Ticker, min_rate_return: float, growth_rate: float, margin_of_safety: float)-> float:
	if ticker.key_statistics is None or ticker.summary_detail is None:
		raise Exception("key_statistics or summary_detail not found")

	eps = ticker.key_statistics.trailing_eps
	if eps is None:
		raise Exception("eps not found")

	pe_ratio = ticker.summary_detail.forward_pe
	if pe_ratio is None:
		raise Exception("pe_ratio not found")

	future_eps = eps
	for i in range(10):
		if i == 0:
			continue

		future_eps = future_eps + (future_eps * growth_rate)

	fair_share_price = future_eps * pe_ratio
	for i in range(10):
		if i == 0:
			continue

		fair_share_price = fair_share_price / (1 + min_rate_return)

	return fair_share_price