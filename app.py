import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SMU Alumni Executive Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_excel(
        "SMU_Alumni_Short_Survey_ANALYTICS_READY.xlsx"
    )

df = load_data()

df.columns = [
    'ID',
    'Ethnicity',
    'Gender',
    'School',
    'Qualification_Group',
    'Qualification',
    'Graduation_Year',
    'Employment_Status',
    'Employment_Sector',
    'Time_To_Employment',
    'Qualification_Relevance',
    'Workplace_Preparedness',
    'Alumni_Engagement_Interest',
    'Stay_Connected'
]

st.title("SMU Alumni Executive Dashboard")

st.subheader("Dataset Overview")

st.write(f"Number of Responses: {df.shape[0]:,}")
st.write(f"Number of Variables: {df.shape[1]}")

st.write(df.columns.tolist())

st.dataframe(
    df,
    use_container_width=True
)
