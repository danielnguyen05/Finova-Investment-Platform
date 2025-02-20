from flask import Flask, request, jsonify, send_from_directory, render_template
import numpy as np
import os
import subprocess  # ✅ Added to run `main.py` when user selects a company
from ai import get_response  # ✅ Import AI response function

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
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")  # ✅ Ensure demo.html has chatbot UI

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Processes user messages and returns AI responses."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Error: No message received"}), 400

        user_message = data["message"]
        ai_response = get_response(user_message)  # ✅ Call AI model
        return jsonify({"response": ai_response})

    except Exception as e:
        print("Chat API error:", str(e))
        return jsonify({"response": "Error: AI is not available."}), 500

# ✅ API Endpoint: Get Company Overview
@app.route('/api/company/<symbol>', methods=['GET'])
def get_company(symbol):
    data = get_company_overview(symbol)
    if not data:
        return jsonify({"error": f"Failed to fetch company overview for {symbol}"}), 404
    return jsonify(data)

# ✅ API Endpoint: Get Dividend Information
@app.route('/api/dividends/<symbol>', methods=['GET'])
def get_dividends(symbol):
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

@app.route("/api/plot/investment", methods=["POST"])
def generate_investment_plot():
    """Creates and saves an investment growth plot."""
    data = request.json
    principal = float(data["principal"])
    aggro = data["aggro"]
    symbol = data["symbol"]

    subprocess.run(["python", "main.py", symbol, str(principal), aggro], check=True)

    investment_path = os.path.join(STATIC_FOLDER, "investment_growth.html")

    if os.path.exists(investment_path):
        return jsonify({
            "message": "Investment growth plot saved.",
            "graph_url": "/static/investment_growth.html"
        })
    else:
        return jsonify({"error": "Graph generation failed"}), 500

# ✅ API Endpoint: Get Economic Data
@app.route('/api/economic', methods=['GET'])
def get_economic():
    data = get_real_gdp()
    if not data:
        return jsonify({"error": "Failed to fetch economic data"}), 404
    return jsonify(data)

# ✅ API Endpoint: Generate Dividend Overlay Plot
@app.route('/api/plot/dividends/<symbol>', methods=['GET'])
def generate_dividend_plot(symbol):
    save_path = plot_dividends_overlay([symbol])

    if os.path.exists(save_path):
        return jsonify({
            "message": f"Dividend overlay plot for {symbol} saved.",
            "image_url": f"/static/company_dividends_plot.png"
        })
    else:
        return jsonify({"error": "Graph generation failed"}), 500

STATIC_FOLDER = os.path.join(os.getcwd(), "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route("/api/graphs", methods=["POST"])
def generate_graphs():
    data = request.json
    company = data.get("company")

    if not company:
        return jsonify({"error": "Company not provided"}), 400

    subprocess.run(["python", "main.py", company], check=True)

    dividends_path = os.path.join(STATIC_FOLDER, "company_dividends_plot.png")
    gdp_path = os.path.join(STATIC_FOLDER, "real_gdp_plot.png")
    gdp_per_capita_path = os.path.join(STATIC_FOLDER, "real_gdp_per_capita_plot.png")

    if not (os.path.exists(dividends_path) and os.path.exists(gdp_path) and os.path.exists(gdp_per_capita_path)):
        return jsonify({"error": "Graphs not generated. Check main.py."}), 500

    return jsonify({
        "message": f"Graphs updated successfully for {company}",
        "dividends_url": f"/static/company_dividends_plot.png?{os.path.getmtime(dividends_path)}",
        "gdp_url": f"/static/real_gdp_plot.png?{os.path.getmtime(gdp_path)}",
        "gdp_per_capita_url": f"/static/real_gdp_per_capita_plot.png?{os.path.getmtime(gdp_per_capita_path)}"
    }), 200

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
