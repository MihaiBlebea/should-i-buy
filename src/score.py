from __future__ import annotations
from typing import List, Protocol
from dataclasses import dataclass
import click
from yahoo_fin_api import Client, YahooFinApi, Ticker
from src.utils import fmt_amount


MIN_PROFIT_MARGIN = 0.1
MAX_BETA = 3
MIN_RATE_RETURN = 0.066


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
	def execute(self, ticker: Ticker)-> Result | None:
		...

@dataclass
class Result:
	raw: int | float
	fmt: str

class Service:
	def __init__(self, *args: Indicator) -> List[Result]:
		self.indicators = args

	def execute(self, symbol)-> None:
		yf_api = YahooFinApi(Client())
		ticker = yf_api.get_all([symbol])[0]

		results = []
		for indicator in self.indicators:
			res = indicator.execute(ticker)
			if res is None:
				continue
			results.append(res)
		return results

class GrowthRateIndicator:
	def execute(self, ticker: Ticker)-> Result:
		growth_rate = ticker.financial_data.earnings_growth
		return Result(growth_rate, f"{growth_rate * 100}%")

class FreeCashFlowIndicator:
	def execute(self, ticker: Ticker)-> Result:
		fcf = ticker.financial_data.free_cash_flow
		return Result(fcf, fmt_amount(fcf))

class BetaIndicator:
	def execute(self, ticker: Ticker)-> Result | None:
		beta = ticker.summary_detail.beta
		if beta is None:
			return None
		beta = round(beta, 2)
		return Result(beta, f"{beta}")

class FairPriceIndicator:
	def execute(self, ticker: Ticker)-> Result:
		# price = current_price(ticker)
		growth_rate = ticker.financial_data.earnings_growth
		fair_price = fair_share_price(ticker, MIN_RATE_RETURN, growth_rate, 0)
		return Result(fair_price, fmt_amount(fair_price))

class ProfitMarginIndicator:
	def execute(self, ticker: Ticker)-> Result:
		profit_margin = ticker.financial_data.profit_margins
		profit_margin_fmt = f"{round(profit_margin * 100, 2)}%"
		return Result(profit_margin, profit_margin_fmt)

class PricePerEarningIndicator:
	def execute(self, ticker: Ticker)-> Result:
		forward_pe = ticker.summary_detail.forward_pe
		trailing_pe = ticker.summary_detail.trailing_pe
		return Result(forward_pe - trailing_pe, f"{forward_pe}/{trailing_pe}")

class AssetsLiabilitiesIndicator:
	def execute(self, ticker: Ticker)-> Result:
		has_more_assets = True
		negative_years = 0
		for bs in ticker.get_balance_sheets():
			diff = bs.total_current_assets - bs.total_current_liabilities
			if diff < 0:
				has_more_assets = False
				negative_years += 1
		return Result(has_more_assets, has_more_assets)

@click.group()
def cli():
	pass

@cli.command("score")
@click.option("--symbol", "-s", default="AAPL", help="Symbol to analyse")
def score(symbol: str):
	"""Score a symbol based on indicators"""
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
	score()