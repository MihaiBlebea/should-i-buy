from __future__ import annotations
from typing import Protocol, List, Tuple
from yahoo_fin_api import Ticker, YahooFinApi, Client
from src.compare.free_cashflow import FreeCashFlowIndicator


Result = List[Tuple[int | float, str]]

class Indicator(Protocol):
    def get_title(self)-> str:
        ...

    def execute(self, tickers: List[Ticker])-> Result:
        ...

class Service:
    def __init__(self)-> None:
        self.indicators : List[Indicator] = []
        self.symbols : List[str] = []

        self.yf = YahooFinApi(Client())
    
    def add_indicators(self, indicators: List[Indicator])-> None:
        [self.indicators.append(indicator) for indicator in indicators]

    def add_selected_symbols(self, symbols: List[str]):
        [self.symbols.append(symbol.upper()) for symbol in symbols]

    def get_titles(self)-> List[str]:
        return [indicator.get_title() for indicator in self.indicators]

    def calculate(self)-> dict:
        tickers = self.yf.get_all(self.symbols)

        data = []
        for t in tickers:
            data.append({
                "symbol": t.symbol,
                "title": t.title,
                "indicators": []
            })

        for indicator in self.indicators:
            res = list(indicator.execute(tickers))
            for index, d in enumerate(data):
                d["indicators"].append({
                    "value": res[index][0],
                    "fmt": res[index][1]
                })

        return data


if __name__ == "__main__":
    from src.compare.free_cashflow import FreeCashFlowIndicator
    s = Service()
    s.add_indicators([FreeCashFlowIndicator()])
    s.add_stocks(["AAPL", "TSLA"])
    result = s.calculate()
    print(result)