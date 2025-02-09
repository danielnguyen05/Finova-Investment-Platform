import os
from Corporate_Information.data_ci import get_company_overview, get_dividends
from Corporate_Information.graph_ci import plot_dividends_overlay
from Economic_Indicators.data_ei import get_real_gdp, get_real_gdp_per_capita
from Economic_Indicators.graph_ei import plot_real_gdp, plot_real_gdp_per_capita
from Portfolio_Building.get_weights import get_weights_given_aggressiveness
from Portfolio_Building.plot_ror import plot_value_given_aggro_and_principal

# ✅ Ensure 'static/' exists
STATIC_FOLDER = os.path.join(os.getcwd(), "static")
os.makedirs(STATIC_FOLDER, exist_ok=True)

def main():
    symbol = "IBM"  # Change this to test different companies

    print("\n📢 Fetching company data...")
    data = get_company_overview(symbol)
    dividends = get_dividends(symbol)

    if data:
        print("\n✅ Company Overview:")
        print(f"📌 Company Name: {data.get('Name')}")
        print(f"📌 Sector: {data.get('Sector')}")
        print(f"📌 Market Capitalisation: {data.get('MarketCapitalization')}")
        print(f"📌 Description: {data.get('Description')}")
    else:
        print(f"\n❌ Failed to fetch company overview for {symbol}")

    if dividends and "data" in dividends:
        dividend_data = dividends["data"]
        most_recent = max(dividend_data, key=lambda d: d["ex_dividend_date"])
        highest_paying = max(dividend_data, key=lambda d: float(d["amount"]))

        print("\n💰 Dividend Information:")
        print(f"📅 Most Recent Dividend - {most_recent['ex_dividend_date']}: ${most_recent['amount']}")
        print(f"🏆 Highest-Paying Dividend - {highest_paying['ex_dividend_date']}: ${highest_paying['amount']}")
    else:
        print(f"\n❌ Failed to fetch dividend data for {symbol}")

    # ✅ Generate and save graphs inside /static/
    print("\n📊 Generating graphs...")

    # 1️⃣ Dividend Trends
    dividends_path = os.path.join(STATIC_FOLDER, "company_dividends_plot.png")
    plot_dividends_overlay([symbol])
    os.rename("company_dividends_plot.png", dividends_path)
    print(f"✅ Dividend graph saved: {dividends_path}")

    # 2️⃣ Real GDP Over Time
    gdp_data = get_real_gdp()
    if gdp_data:
        gdp_path = os.path.join(STATIC_FOLDER, "real_gdp_plot.png")
        plot_real_gdp(gdp_data)
        os.rename("real_gdp_plot.png", gdp_path)
        print(f"✅ Real GDP graph saved: {gdp_path}")
    else:
        print("❌ Failed to fetch GDP data.")

    # 3️⃣ Real GDP Per Capita Over Time
    gdp_per_capita_data = get_real_gdp_per_capita()
    if gdp_per_capita_data:
        gdp_per_capita_path = os.path.join(STATIC_FOLDER, "real_gdp_per_capita_plot.png")
        plot_real_gdp_per_capita(gdp_per_capita_data)
        os.rename("real_gdp_per_capita_plot.png", gdp_per_capita_path)
        print(f"✅ Real GDP per Capita graph saved: {gdp_per_capita_path}")
    else:
        print("❌ Failed to fetch GDP per capita data.")

if __name__ == "__main__":
    main()
