import streamlit as st
import pandas as pd

# Define default PRN rates for each state
base_rates = {
    'CA': 115,
    'CT': 110,
    'IN': 90,
    'KY': 90,
    'ME': 95,
    'NY': 105,
    'OH': 95,
    'VA': 100
}

st.title("NP Assignment & Revenue Target Calculator")
st.markdown("""
Easily calculate how many Nurse Practitioners (NPs) on assignment you need to reach a revenue target.
Includes adjustable availability, revenue goals, and built-in profit analysis by state.
""")

# Sidebar - Inputs
st.sidebar.header("Settings")
target_revenue = st.sidebar.number_input("Annual Revenue Goal ($)", value=2_000_000, step=100_000)
assessments_per_day = st.sidebar.slider("Assessments per Day", 1, 10, 6)
days_per_week = st.sidebar.slider("Days Worked per Week", 1, 7, 2)
weeks_per_year = st.sidebar.number_input("Weeks Worked per Year", value=52, step=1)
markup = st.sidebar.slider("Markup %", 0, 100, 35)

# Sidebar - NP availability per state
st.sidebar.header("NPs Available per State")
np_available = {state: st.sidebar.number_input(f"{state} NPs", min_value=0, value=0, step=1) for state in base_rates.keys()}

# Compute assessments per year per provider
assessments_per_year = assessments_per_day * days_per_week * weeks_per_year

# Build calculation table
data = []
for state, rate in base_rates.items():
    bill_rate = rate * (1 + markup / 100)
    annual_revenue_per_provider = bill_rate * assessments_per_year
    providers_needed = target_revenue / annual_revenue_per_provider
    np_count = np_available[state]
    total_revenue = annual_revenue_per_provider * np_count
    provider_cost = rate * assessments_per_year
    annual_cost_all = provider_cost * np_count
    profit = total_revenue - annual_cost_all

    data.append({
        "State": state,
        "Base Rate": rate,
        "Bill Rate": round(bill_rate, 2),
        "Revenue/Assessment": round(bill_rate, 2),
        "Annual Revenue/Provider": round(annual_revenue_per_provider, 2),
        "Providers Needed for Goal": round(providers_needed, 2),
        "Available Providers": np_count,
        "Total Revenue (Available)": round(total_revenue, 2),
        "Total Cost (Available)": round(annual_cost_all, 2),
        "Total Profit (Available)": round(profit, 2)
    })

results_df = pd.DataFrame(data)

st.subheader("Results by State")
st.dataframe(results_df)

# Visuals
st.bar_chart(results_df.set_index("State")["Providers Needed for Goal"])
st.bar_chart(results_df.set_index("State")["Total Profit (Available)"])

# Additional Idea
st.markdown("""
### 🚀 Additional Ideas
- Allow CSV upload for batch NP scheduling inputs
- Add part-time vs full-time weighting logic
- Enable export to Excel or PDF
- Display national averages or benchmarks for reference
""")