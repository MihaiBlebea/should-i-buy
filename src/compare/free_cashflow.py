from __future__ import annotations
from typing import List, Tuple
from yahoo_fin_api import Ticker
from src.compare.utils import fmt_amount

Result = List[Tuple[int | float, str]]

class FreeCashFlowIndicator:

	def get_title(self)-> str:
		return "Free cashflow"

	def execute(self, tickers: List[Ticker])-> Result:
		for ticker in tickers:
			fcf = ticker.financial_data.free_cash_flow
			yield (fcf, fmt_amount(fcf))