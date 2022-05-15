from __future__ import annotations
from yahoo_fin_api import Client, YahooFinApi
import click
import json
from pathlib import Path

HOME = Path.home()

@click.group()
def cli():
	pass

@cli.command("portfolio")
@click.option("--name", "-n", help="Porfolio name to analyse")
def portfolio(name: str):
	"""Fetch and analyse the portfolio returns and risks"""
	with open(f"{HOME}/.shouldibuy/portfolio.json", "r") as file:
		content = json.loads(file.read())
		if name not in content:
			raise Exception("portfolio name not in portfolios")

		yf_api = YahooFinApi(Client())
		tickers = yf_api.get_all([s for s in list(content[name].keys())])

		print(tickers)

@cli.command("update")
@click.option("--name", "-n", help="Porfolio name to analyse")
@click.option("--symbols", "-s", multiple=True, help="List of symbols")
@click.option("--remove", "-r", default=False, help="Remove the symbol", is_flag=True)
def update(name: str, symbols: list, remove: bool):
	"""Update symbols to a portfolio"""
	with open(f"{HOME}/.shouldibuy/portfolio.json", "r") as file:
		content = json.loads(file.read())
		if remove:
			remove_from_portfolio(content, name, symbols)
			return

		add_to_portfolio(content, name, symbols)

def remove_from_portfolio(content: dict, name: str, symbols: list)-> None:
	for symbol in symbols:
		if ":" in symbol:
			raise Exception("invalid argument in symbol")
		symbol = symbol.upper()
		del content[name][symbol]

	if len(list(content[name].values())) == 0:
		del content[name]

	with open(f"{HOME}/.shouldibuy/portfolio.json", "w") as file:
		file.write(json.dumps(content))

def add_to_portfolio(content: dict, name: str, symbols: list)-> None:
	if name not in content:
		content[name] = {}

	for s in symbols:
		if ":" not in s:
			raise Exception("invalid argument include quantity")

		symbol = s.split(":")[0]
		quantity = float(s.split(":")[1])

		if quantity < 0 or quantity == 0:
			raise Exception("quantify must be positive")

		symbol = symbol.upper()
		content[name][symbol] = quantity

	with open(f"{HOME}/.shouldibuy/portfolio.json", "w") as file:
		file.write(json.dumps(content))

if __name__ == "__main__":
	portfolio()