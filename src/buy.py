from __future__ import annotations
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


@click.command()
@click.option("--symbol", default="AAPL", help="Symbol to analyse")
def main(symbol: str):

	yf_api = YahooFinApi(Client())
	ticker = yf_api.get_all([symbol])[0]

	print(f"Results for {ticker.title}:")

	print(f"\t- current price {fmt_amount(current_price(ticker))}")

	growth_rate = ticker.financial_data.earnings_growth
	print(f"\t- fair price {fmt_amount(fair_share_price(ticker, MIN_RATE_RETURN, growth_rate, 0))}")

	if ticker.financial_data.profit_margins < MIN_PROFIT_MARGIN:
		profit_margins = round(ticker.financial_data.profit_margins * 100, 2)
		print(f"\t- profit margins {profit_margins}% is too low")

	forward_pe = ticker.summary_detail.forward_pe
	trailing_pe = ticker.summary_detail.trailing_pe
	if forward_pe < trailing_pe:
		print(f"\t- forward PE is lower than trailing PE ({forward_pe} to {trailing_pe})")

	beta = ticker.summary_detail.beta
	if beta is not None and beta > MAX_BETA:
		print(f"\t- beta is too high {beta}")

	print("\nBalance sheet:")
	for bs in ticker.get_balance_sheets():
		diff = bs.total_current_assets - bs.total_current_liabilities

		print(f"- {bs.fmt_end_date()}:")
		print(f"\t- Assets {fmt_amount(bs.total_current_assets)}")
		print(f"\t- Liabilities {fmt_amount(bs.total_current_liabilities)}")
		print(f"\t- Diff {fmt_amount(diff)}")

	print("\nCashflow:")
	for cf in ticker.get_cashflows():

		print(f"- {cf.fmt_end_date()}:")
		print(f"\t- Operating {fmt_amount(cf.total_cash_from_operating_activities)}")
		print(f"\t- Investing {fmt_amount(cf.total_cashflows_from_investing_activities)}")
		print(f"\t- Financing {fmt_amount(cf.total_cash_from_financing_activities)}")

if __name__ == "__main__":
	main()