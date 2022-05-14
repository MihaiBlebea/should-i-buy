from prettytable import PrettyTable
from yahoo_fin_api import Client, YahooFinApi, Ticker
import click
from pprint import pprint

from src.utils import fmt_amount


@click.command("compare")
@click.option("--symbols", "-s", multiple=True, help="Symbol to analyse")
def main(symbols: list):
	yf_api = YahooFinApi(Client())
	tickers = yf_api.get_all(symbols)

	table = PrettyTable(["Symbol", "Profit Margin", "Free CF"])
	table.align = "l"

	for t in tickers:
		profit_margin = round(t.financial_data.profit_margins * 100, 2)
		free_cashflow = t.financial_data.free_cash_flow
		symbol = t.symbol
		table.add_row([symbol, f"{profit_margin}%", fmt_amount(free_cashflow)])

	print(table)

if __name__ == "__main__":
	main()