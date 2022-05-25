from flask import Flask, jsonify, send_from_directory, request
from pathlib import Path
import json
from yahoo_fin_api import Universe
from src.compare import Service, FreeCashFlowIndicator

cwd = Path(__file__).parent

app = Flask(__name__)

@app.route("/<path:path>")
def static_assets(path):
	return send_from_directory(f"{cwd}/../webapp/dist", path)

@app.route("/")
def index():
	return send_from_directory(f"{cwd}/../webapp/dist", "index.html")

@app.route("/api/v1/compare")
def compare(methods=["GET"]):
	symbols = request.args.get("symbols").split(",")\
		if request.args.get("symbols") is not None\
		else []

	symbols = [symbol.strip().upper() for symbol in symbols]
	
	service = Service()
	service.add_indicators([FreeCashFlowIndicator()])
	service.add_selected_symbols(symbols)

	body = {
		"indictors": service.get_titles(),
		"symbols": service.calculate()
	}

	return jsonify(body)

@app.route("/api/v1/stocks")
def stocks():
	stocks = [
		{"title": symbol, "symbol": symbol} for symbol in Universe.get_freetrade_universe()
	]
	return jsonify({
		"stocks": stocks
	})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)