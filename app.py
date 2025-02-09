from flask import Flask, request, jsonify, render_template
import numpy as np

# Import all the necessary functions from your existing modules
from Corporate_Information.data_ci import get_company_overview
from Corporate_Information.graph_ci import plot_dividends_overlay
from Economic_Indicators.data_ei import get_real_gdp
from Economic_Indicators.graph_ei import plot_real_gdp
from Portfolio_Building.get_weights import get_weights_given_aggressiveness
from Portfolio_Building.plot_ror import plot_value_given_aggro_and_principal
from Corporate_Information.graph_ci import plot_dividends_overlay
from Economic_Indicators.graph_ei import plot_real_gdp, plot_real_gdp_per_capita
from Economic_Indicators.data_ei import get_real_gdp, get_real_gdp_per_capita

app = Flask(__name__)

@app.route("/")
def index():
    '''
    Opens the template index.html

    Inputs;
    None

    Returns:
    output: string
    '''
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ✅ Route: Serve Demo Page
@app.route("/demo")
def demo():
    return render_template("demo.html")

# ✅ Route: Serve Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ✅ API Endpoint: Get Company Overview
@app.route('/api/company/<symbol>', methods=['GET'])
def get_company(symbol):
    """Fetches company overview data for a given stock symbol."""
    data = get_company_overview(symbol)
    if not data:
        return jsonify({"error": f"Failed to fetch company overview for {symbol}"}), 404
    return jsonify(data)

# ✅ API Endpoint: Get Dividend Information
@app.route('/api/dividends/<symbol>', methods=['GET'])
def get_dividends(symbol):
    """Fetches dividend information for a given stock symbol."""
    dividends = get_dividends(symbol)
    if not dividends or "data" not in dividends:
        return jsonify({"error": f"Failed to fetch dividend data for {symbol}"}), 404

    dividend_data = dividends["data"]
    most_recent = max(dividend_data, key=lambda d: d["ex_dividend_date"])
    highest_paying = max(dividend_data, key=lambda d: float(d["amount"]))

    return jsonify({
        "most_recent": most_recent,
        "highest_paying": highest_paying
    })

# ✅ API Endpoint: Get Investment Data
@app.route('/api/investment', methods=['POST'])
def get_investment_data():
    """Calculates investment growth based on user input."""
    data = request.json
    principal = float(data["principal"])
    aggro = data["aggro"]

    _, target_bounds = get_weights_given_aggressiveness(aggro)
    lower_bound, expected_rate, upper_bound = target_bounds

    years = 30
    t = np.arange(0, years + 1, 1)

    return jsonify({
        "t": t.tolist(),
        "expected": (principal * (1 + expected_rate) ** t).tolist(),
        "lower": (principal * (1 + lower_bound) ** t).tolist(),
        "upper": (principal * (1 + upper_bound) ** t).tolist()
    })

# ✅ API Endpoint: Get Economic Data
@app.route('/api/economic', methods=['GET'])
def get_economic():
    """Fetches economic indicators like GDP and inflation."""
    data = get_real_gdp()
    if not data:
        return jsonify({"error": "Failed to fetch economic data"}), 404
    return jsonify(data)

# ✅ API Endpoint: Generate and Save Investment Growth Plot
@app.route('/api/plot/investment', methods=['POST'])
def generate_investment_plot():
    """Creates and saves an investment growth plot."""
    data = request.json
    principal = float(data["principal"])
    aggro = data["aggro"]

    plot_value_given_aggro_and_principal(aggro, principal)

    return jsonify({"message": "Investment growth plot saved."})

# ✅ API Endpoint: Generate Dividend Overlay Plot
@app.route('/api/plot/dividends/<symbol>', methods=['GET'])
def generate_dividend_plot(symbol):
    """Creates and saves a dividend overlay plot."""
    plot_dividends_overlay(symbol)
    return jsonify({"message": f"Dividend overlay plot for {symbol} saved."})


@app.route("/api/graphs", methods=["POST"])
def generate_graphs():
    data = request.json
    company = data.get("company")

    if not company:
        return jsonify({"error": "Company not provided"}), 400

    # Generate graphs based on user selection
    plot_dividends_overlay([company])  # Generates company_dividends_plot.png

    # Fetch economic data and generate graphs
    real_gdp_data = get_real_gdp()
    real_gdp_per_capita_data = get_real_gdp_per_capita()
    plot_real_gdp(real_gdp_data)
    plot_real_gdp_per_capita(real_gdp_per_capita_data)

    return jsonify({"message": "Graphs updated successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)