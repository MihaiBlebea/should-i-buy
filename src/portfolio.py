from __future__ import annotations
from yahoo_fin_api import Client, YahooFinApi
import click
import json

@click.group()
def cli():
	pass

@cli.command("portfolio")
@click.option("--name", "-n", help="Porfolio name to analyse")
def portfolio(name: str):
	"""Fetch and analyse the portfolio returns and risks"""
	with open("$HOME/.shouldibuy/portfolio.json", "r") as file:
		print(file)
	# yf_api = YahooFinApi(Client())
	# tickers = yf_api.get_all(symbols)

if __name__ == "__main__":
	portfolio()