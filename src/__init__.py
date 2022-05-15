from src.score import cli as score_cli
from src.compare import cli as compare_cli
from src.portfolio import cli as portfolio_cli

import click

cli = click.CommandCollection(sources=[score_cli, compare_cli, portfolio_cli])

if __name__ == "__main__":
    cli()