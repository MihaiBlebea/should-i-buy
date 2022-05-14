from __future__ import annotations
from typing import List, Protocol
import click
from yahoo_fin_api import Client, YahooFinApi, Ticker

MIN_PROFIT_MARGIN = 0.1
MAX_BETA = 3
MIN_RATE_RETURN = 0.066

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

class Indicator(Protocol):
	def execute(self, ticker: Ticker)-> str:
		...

class Service:
	def __init__(self, *args: Indicator) -> None:
		self.indicators = args

	def execute(self, symbol)-> None:
		yf_api = YahooFinApi(Client())
		ticker = yf_api.get_all([symbol])[0]

		print(f"Results for {ticker.title}:")

		for indicator in self.indicators:
			res = indicator.execute(ticker)
			if res is None:
				continue
			print(res)

class GrowthRateIndicator:
	def execute(self, ticker: Ticker)-> str:
		growth_rate = ticker.financial_data.earnings_growth
		if growth_rate < 0:
			return f"\t- growth rate is negative {growth_rate * 100}%"
		else:
			return f"\t- growth rate is positive {growth_rate * 100}%"

class FreeCashFlowIndicator:
	def execute(self, ticker: Ticker)-> str:
		fcf = ticker.financial_data.free_cash_flow
		if fcf > 0:
			return f"\t- free cash flow is positive {fmt_amount(fcf)}"
		else:
			return f"\t- free cash flow is negative {fmt_amount(fcf)}"

class BetaIndicator:
	def execute(self, ticker: Ticker)-> str:
		beta = ticker.summary_detail.beta
		if beta is None:
			return None
		beta = round(beta, 2)

		if beta > MAX_BETA:
			return f"\t- beta is too high {beta}"
		else:
			return f"\t- beta is acceptable {beta}"

class FairPriceIndicator:
	def execute(self, ticker: Ticker)-> str:
		price = current_price(ticker)
		growth_rate = ticker.financial_data.earnings_growth
		fair_price = fair_share_price(ticker, MIN_RATE_RETURN, growth_rate, 0)

		if price < fair_price:
			return f"\t- undervalued - current price {fmt_amount(price)} is lower than the fair price {fmt_amount(fair_price)}"
		else:
			return f"\t- overvalued - current price {fmt_amount(price)} is higher than the fair price {fmt_amount(fair_price)}"

class ProfitMarginIndicator:
	def execute(self, ticker: Ticker)-> str:
		profit_margin = ticker.financial_data.profit_margins
		profit_margin_fmt = round(profit_margin * 100, 2)

		if profit_margin < MIN_PROFIT_MARGIN:
			return f"\t- profit margin {profit_margin_fmt}% is too low"
		else:
			return f"\t- profit margin {profit_margin_fmt}% is ok"

class PricePerEarningIndicator:
	def execute(self, ticker: Ticker)-> str:
		forward_pe = ticker.summary_detail.forward_pe
		trailing_pe = ticker.summary_detail.trailing_pe
		if forward_pe < trailing_pe:
			return f"\t- forward PE is lower than trailing PE ({forward_pe} to {trailing_pe})"
		else:
			return f"\t- forward PE is higher than trailing PE ({forward_pe} to {trailing_pe})"

class AssetsLiabilitiesIndicator:
	def execute(self, ticker: Ticker)-> str:
		has_more_assets = True
		negative_years = 0
		for bs in ticker.get_balance_sheets():
			diff = bs.total_current_assets - bs.total_current_liabilities
			if diff < 0:
				has_more_assets = False
				negative_years += 1

		return "\t- has more assets than liabilities over last 4 years" \
			if has_more_assets \
			else f"\t- has more liabilities than assets in {negative_years} of the last 4 years"

@click.command()
@click.option("--symbol", default="AAPL", help="Symbol to analyse")
def main(symbol: str):
	Service(
		FairPriceIndicator(),
		GrowthRateIndicator(),
		FreeCashFlowIndicator(),
		BetaIndicator(),
		ProfitMarginIndicator(),
		PricePerEarningIndicator(),
		AssetsLiabilitiesIndicator()
	).execute(symbol)


if __name__ == "__main__":
	main()