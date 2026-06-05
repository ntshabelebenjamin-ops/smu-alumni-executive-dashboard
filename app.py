import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================

# PAGE CONFIG

# ==================================================

st.set_page_config(
page_title="SMU Alumni Executive Dashboard",
layout="wide"
)

# ==================================================

# SMU COLOURS

# ==================================================

SMU_BLUE = "#214A9A"
SMU_ORANGE = "#F37021"


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_excel(
        "SMU_Alumni_Short_Survey_ANALYTICS_READY.xlsx"
    )

df = load_data()

# ==================================================

# RENAME COLUMNS

# ==================================================

df.columns = [
"ID",
"Ethnicity",
"Gender",
"School",
"Qualification_Group",
"Qualification",
"Graduation_Year",
"Employment_Status",
"Employment_Sector",
"Time_To_Employment",
"Qualification_Relevance",
"Workplace_Preparedness",
"Alumni_Engagement_Interest",
"Stay_Connected"
]

# ==================================================

# SIDEBAR FILTERS

# ==================================================

st.sidebar.header("Filters")

school = st.sidebar.multiselect(
"School",
options=sorted(df["School"].dropna().unique()),
default=sorted(df["School"].dropna().unique()),
key="school_filter"
)

gender = st.sidebar.multiselect(
"Gender",
options=sorted(df["Gender"].dropna().unique()),
default=sorted(df["Gender"].dropna().unique()),
key="gender_filter"
)

ethnicity = st.sidebar.multiselect(
"Ethnicity",
options=sorted(df["Ethnicity"].dropna().unique()),
default=sorted(df["Ethnicity"].dropna().unique()),
key="ethnicity_filter"
)

# ==================================================

# FILTERED DATA

# ==================================================

filtered = df[
(df["School"].isin(school))
&
(df["Gender"].isin(gender))
&
(df["Ethnicity"].isin(ethnicity))
]

# ==================================================

# KPI CALCULATIONS

# ==================================================

responses = len(filtered)

employment_rate = round(
(
filtered["Employment_Status"]
.astype(str)
.str.contains("Employed", case=False, na=False)
).mean() * 100,
1
)

# ==================================================

# TITLE

# ==================================================

st.title("🎓 SMU Alumni Graduate Outcomes Dashboard")

# ==================================================

# TABS

# ==================================================

tab1, tab2, tab3, tab4 = st.tabs([
"Executive Overview",
"Graduate Profile",
"Employability",
"Graduate Outcomes"
])

# ==================================================

# TAB 1 - EXECUTIVE OVERVIEW

# ==================================================

with tab1:


   col1, col2 = st.columns(2)

   col1.metric("Responses", f"{responses:,}")
   col2.metric("Employment Rate", f"{employment_rate}%")

   st.info(
    f"""
    A total of {responses:,} alumni responses are included in the analysis.

    Current employment rate: {employment_rate}%
    """
)


# ==================================================

# TAB 2 - GRADUATE PROFILE

# ==================================================

with tab2:


    st.header("Graduate Profile")

# School Distribution

school_df = (
    filtered["School"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

school_df.columns = ["School", "Percentage"]

fig_school = px.bar(
    school_df,
    x="Percentage",
    y="School",
    orientation="h",
    text="Percentage",
    color_discrete_sequence=[SMU_BLUE]
)

fig_school.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="inside"
)

st.plotly_chart(
    fig_school,
    width="stretch",
    key="school_chart"
)

# Gender Distribution

st.subheader("Gender Distribution")

gender_df = (
    filtered["Gender"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

gender_df.columns = ["Gender", "Percentage"]

fig_gender = px.pie(
    gender_df,
    names="Gender",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_ORANGE, SMU_BLUE]
)

st.plotly_chart(
    fig_gender,
    width="stretch",
    key="gender_chart"
)

# Ethnicity Distribution

st.subheader("Ethnicity Distribution")

eth_df = (
    filtered["Ethnicity"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

eth_df.columns = ["Ethnicity", "Percentage"]

fig_eth = px.bar(
    eth_df,
    x="Ethnicity",
    y="Percentage",
    text="Percentage",
    color_discrete_sequence=[SMU_ORANGE]
)

st.plotly_chart(
    fig_eth,
    width="stretch",
    key="ethnicity_chart"
)

# Qualification Group Distribution

st.subheader("Qualification Group Distribution")

qg_df = (
    filtered["Qualification_Group"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

qg_df.columns = ["Qualification_Group", "Percentage"]

fig_qg = px.bar(
    qg_df,
    x="Qualification_Group",
    y="Percentage",
    text="Percentage",
    color_discrete_sequence=[SMU_BLUE]
)

fig_qg.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_qg,
    width="stretch",
    key="qualification_group_chart"
)

# Top Qualifications

st.subheader("Top Qualifications")

qual_df = (
    filtered["Qualification"]
    .value_counts()
    .head(15)
    .reset_index()
)

qual_df.columns = ["Qualification", "Responses"]

fig_qual = px.bar(
    qual_df,
    x="Responses",
    y="Qualification",
    orientation="h",
    color_discrete_sequence=[SMU_ORANGE]
)

st.plotly_chart(
    fig_qual,
    width="stretch",
    key="qualification_chart"
)

# Graduation Year Distribution

st.subheader("Graduation Year Distribution")

year_df = (
    filtered["Graduation_Year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_df.columns = ["Graduation_Year", "Responses"]

fig_year = px.line(
    year_df,
    x="Graduation_Year",
    y="Responses",
    markers=True
)

st.plotly_chart(
    fig_year,
    width="stretch",
    key="graduation_year_chart"
)



# ==================================================

# TAB 3 - EMPLOYABILITY

# ==================================================

with tab3:


    st.header("Employability")

emp_df = (
    filtered["Employment_Status"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

emp_df.columns = ["Status", "Percentage"]

fig_emp = px.pie(
    emp_df,
    names="Status",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_BLUE, SMU_ORANGE]
)

st.plotly_chart(
    fig_emp,
    width="stretch",
    key="employment_chart"
)


# ==================================================

# TAB 4 - GRADUATE OUTCOMES

# ==================================================

with tab4:


    st.header("Graduate Outcomes")

    st.write("Graduate outcomes visuals coming next.")

