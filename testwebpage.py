import streamlit as st
import pandas as pd

st.title("📊 Real-Time Wafer Quality Analytics")

# Load the real dataset from your GitHub folder
@st.cache_data # This keeps the website fast
def load_data():
    # SECOM data is space-separated
    df = pd.read_csv("secom.data", sep=r"\s+", header=None)
    labels = pd.read_csv("secom_labels.data", sep=r"\s+", header=None, names=["Result", "Timestamp"])
    df['Result'] = labels['Result']
    return df

data = load_data()
st.write(f"Successfully loaded {data.shape[0]} wafer records with {data.shape[1]-1} sensor features.")
