from flask import Flask, jsonify, send_from_directory, request
from pathlib import Path
import json
from src.score import *

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
	# with open(f"{cwd}/../webapp/mock/compare.json") as file:
	# 	compare_data = json.loads(file.read())
	symbols = request.args.get("symbols").split(",")\
		if request.args.get("symbols") is not None\
		else []

	symbols = [symbol.strip().upper() for symbol in symbols]
	
	results = []

	for symbol in symbols:
		res = Service(
			FairPriceIndicator(),
			GrowthRateIndicator(),
			FreeCashFlowIndicator(),
			BetaIndicator(),
			ProfitMarginIndicator(),
			PricePerEarningIndicator(),
			AssetsLiabilitiesIndicator()
		).execute(symbol)
		print(res)

	return jsonify({})

@app.route("/api/v1/stocks")
def stocks():
	with open(f"{cwd}/../webapp/mock/stocks.json") as file:
		stocks_data = json.loads(file.read())

		return jsonify(stocks_data)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)