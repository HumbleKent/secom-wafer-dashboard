import streamlit as st
import pandas as pd
import numpy as np

# 1. Set up the title of your web page
st.title("🎛️ Semiconductor Wafer Anomaly Simulator")
st.write("Adjust the factory sensor threshold to see how it impacts chip failures.")

# 2. Create an interactive slider on the website sidebar
# Arguments: (Label, Min Value, Max Value, Default Value)
sensor_threshold = st.sidebar.slider("Chamber Pressure Threshold (PSI)", 0, 100, 45)

# 3. Simulate some mock SECOM factory data
np.random.seed(42)
chart_data = pd.DataFrame(
    np.random.randn(50, 2) + [50, 50],
    columns=['Actual Pressure', 'Sensor Tolerance']
)
# Make the tolerance line react dynamically to the user's slider input
chart_data['Sensor Tolerance'] = sensor_threshold

# 4. Display a beautiful, interactive line chart on the website
st.line_chart(chart_data)

# 5. Add a conditional alert based on the user's input
if sensor_threshold > 75:
    st.error("⚠️ CRITICAL WARNING: High failure risk! Yield rate may drop below 90%.")
else:
    st.success("✅ Factory parameters are within optimal safety margins.")