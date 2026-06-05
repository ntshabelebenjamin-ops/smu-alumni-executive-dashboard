import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_excel(
        "SMU_Alumni_Short_Survey_ANALYTICS_READY.xlsx"
    )

df = load_data()
st.title("SMU Alumni Executive Dashboard")

st.success("Data loaded successfully")

st.write("Number of Responses:", len(df))

st.write("Columns:")
st.write(df.columns.tolist())

st.dataframe(df.head())
streamlit run app.py
df.columns.tolist()
