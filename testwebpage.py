import streamlit as st
import pandas as pd
import numpy as np

# Set up page config for a professional look
st.set_page_config(page_title="Semiconductor Yield Analytics", layout="wide")

st.title("🏭 Automated Wafer Fault & Yield Analytics Hub")
st.markdown("---")

# --- DATA LOADING ---
# Loading a hosted copy of the SECOM dataset directly via URL for seamless deployment
@st.cache_data
def load_secom_data():
    # Load features (590 sensors)
    features_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom.data"
    df = pd.read_csv(features_url, sep=r"\s+", header=None)
    
    # Load labels (-1 = Pass, 1 = Fail)
    labels_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/secom/secom_labels.data"
    labels = pd.read_csv(labels_url, sep=r"\s+", header=None, names=["Result", "Timestamp"])
    
    df['Result'] = labels['Result']
    # Clean missing values quickly by filling with the column average (Standard factory practice)
    df = df.fillna(df.mean())
    return df

try:
    data = load_secom_data()
    st.sidebar.success("✅ Real SECOM Dataset Loaded Successfully!")
except Exception as e:
    st.error("Data loading failed. Using simulated backup environment.")
    # Backup fake data if the university server goes down
    data = pd.DataFrame(np.random.randn(100, 10), columns=[f"Sensor_{i}" for i in range(10)])
    data['Result'] = np.random.choice([-1, 1], size=100, p=[0.93, 0.07])

# --- FEATURE C: THE YIELD & FINANCIAL CALCULATOR (Sidebar) ---
st.sidebar.header("💰 Factory Financial Calculator")
st.sidebar.markdown("Calculate the daily financial impact of your current wafer defect rate.")

wafer_cost = st.sidebar.number_input("Cost Per Silicon Wafer ($)", min_value=100, max_value=5000, value=750)
daily_production = st.sidebar.slider("Daily Wafer Production Volume", 100, 5000, 1000)

# Calculate metrics based on the actual dataset failure rate (~7%)
total_wafers = len(data)
failed_wafers = len(data[data['Result'] == 1])
actual_fail_rate = failed_wafers / total_wafers

simulated_fails = int(daily_production * actual_fail_rate)
daily_loss = simulated_fails * wafer_cost

st.sidebar.metric(label="Predicted Daily Failed Wafers", value=f"{simulated_fails} units")
st.sidebar.metric(label="Estimated Daily Revenue Loss", value=f"${daily_loss:,}", delta="-Financial Impact", delta_color="inverse")


# --- LAYOUT SETUP ---
# Splitting the main screen into two clear columns for Feature A and Feature B
col1, col2 = st.columns([1, 1])

with col1:
    # --- FEATURE A: THE FAIL VS. PASS FILTER & DISTRIBUTION ---
    st.header("🔍 Wafer Quality Filter")
    st.markdown("Toggle between baseline passing wafers and critical production anomalies.")
    
    # Dropdown menu selection
    filter_choice = st.selectbox(
        "Select Wafer Status to Inspect:",
        ["All Production Wafers", "Passing Wafers Only (Optimal)", "Failed Wafers Only (Anomalies)"]
    )
    
    # Filter the pandas dataframe based on selection
    if filter_choice == "Passing Wafers Only (Optimal)":
        filtered_data = data[data['Result'] == -1]
    elif filter_choice == "Failed Wafers Only (Anomalies)":
        filtered_data = data[data['Result'] == 1]
    else:
        filtered_data = data

    st.dataframe(filtered_data.head(100), height=300)
    st.caption(f"Showing {len(filtered_data)} rows matching your selection criteria.")

with col2:
    # --- FEATURE B: SENSOR TOP CORRELATION CHART ---
    st.header("📈 Root-Cause Sensor Correlation")
    st.markdown("Automatically calculates which hardware sensors have the highest correlation to microchip failure.")
    
    # Calculate Pearson correlation dynamically against the 'Result' column
    correlations = data.corr()['Result'].drop('Result').abs().sort_values(ascending=False)
    top_5_sensors = correlations.head(5)
    
    # Convert series to a dataframe for Streamlit charting
    chart_df = pd.DataFrame({
        'Sensor ID': [f"Sensor {idx}" for idx in top_5_sensors.index],
        'Anomalous Correlation Score': top_5_sensors.values
    }).set_index('Sensor ID')
    
    # Render an interactive bar chart
    st.bar_chart(chart_df)
    st.info("💡 **Insight for Recruiters:** Sensor " + str(top_5_sensors.index[0]) + " exhibits the highest mathematical correlation to defect rates. This implies a hardware calibration drift in that specific chamber stage.")
