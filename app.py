import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
SMU_ORANGE = "#F37021"
SMU_BLUE = "#214A9A"
SMU_LIGHT_GREY = "#F5F5F5"
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
responses = len(df)

employment_rate = round(
    (
        df["Employment_Status"]
        .str.contains("Employed", case=False, na=False)
    ).mean() * 100,
    1
)

preparedness_rate = round(
    (
        df["Workplace_Preparedness"]
        .str.contains("Yes", case=False, na=False)
    ).mean() * 100,
    1
)

connected_rate = round(
    (
        df["Stay_Connected"]
        .str.contains("Yes", case=False, na=False)
    ).mean() * 100,
    1
)
st.title("🎓 SMU Alumni Graduate Outcomes Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Responses", f"{responses:,}")
col2.metric("Employment Rate", f"{employment_rate}%")
col3.metric("Preparedness", f"{preparedness_rate}%")
col4.metric("Stay Connected", f"{connected_rate}%")
st.sidebar.header("Filters")

school = st.sidebar.multiselect(
    "School",
    sorted(df["School"].dropna().unique()),
    default=sorted(df["School"].dropna().unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

ethnicity = st.sidebar.multiselect(
    "Ethnicity",
    sorted(df["Ethnicity"].dropna().unique()),
    default=sorted(df["Ethnicity"].dropna().unique())
)
filtered = df[
    (df["School"].isin(school))
    &
    (df["Gender"].isin(gender))
    &
    (df["Ethnicity"].isin(ethnicity))
]
st.subheader("Employment Status")
emp = (
    filtered["Employment_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

emp.columns = ["Status","Percentage"]
fig = px.pie(
    emp,
    names="Status",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_BLUE, SMU_ORANGE]
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.info(f"""
A total of {responses:,} alumni responses were analysed.

The current employment rate is {employment_rate}%.

The dashboard enables executive analysis of graduate outcomes by:
• School
• Gender
• Ethnicity
• Qualification Group
• Qualification

Use the filters on the left to explore outcomes.
""")

st.write(df.columns.tolist())

st.dataframe(
    df,
    use_container_width=True
)
