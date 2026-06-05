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
df.columns.tolist()
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
st.write(df.columns.tolist())
responses = len(df)

employment_rate = round(
    (
        df["Employment_Status"]
        .str.contains("Employed", case=False, na=False)
    ).mean() * 100,
    1
)

col1, col2 = st.columns(2)

col1.metric(
    "Responses",
    f"{responses:,}"
)

col2.metric(
    "Employment Rate",
    f"{employment_rate}%"
)
