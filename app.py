import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================

# PAGE CONFIG

# ==================================================


st.title("🎓 SMU Alumni Graduate Outcomes Dashboard")

st.caption(
    "Prepared by Benjamin Ntshabele | Institutional Researcher | Academic Planning and Quality Assurance Department"
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


qualification = st.sidebar.multiselect(
    "Qualification",
    options=sorted(df["Qualification"].dropna().unique()),
    default=sorted(df["Qualification"].dropna().unique()),
    key="qualification_filter"
)


graduation_year = st.sidebar.multiselect(
    "Graduation Year",
    options=sorted(df["Graduation_Year"].dropna().unique()),
    default=sorted(df["Graduation_Year"].dropna().unique()),
    key="graduation_year_filter"
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


filtered = df[
    (df["School"].isin(school))
    &
    (df["Gender"].isin(gender))
    &
    (df["Qualification"].isin(qualification))
    &
    (df["Graduation_Year"].isin(graduation_year))
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
# EXECUTIVE INSIGHTS
# ==================================================

top_school = filtered["School"].mode()[0]

top_qualification_group = filtered["Qualification_Group"].mode()[0]

st.success(
    f"""
    EXECUTIVE INSIGHTS

    • Total responses analysed: {responses:,}

    • Employment rate: {employment_rate}%

    • Largest respondent group: {top_school}

    • Most common qualification group: {top_qualification_group}

    • Dashboard reflects graduate profile, employability and alumni engagement outcomes.
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


fig_eth.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_eth,
    width="stretch",
    key="ethnicity_chart"
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

# ==================================================

# TAB 3 - EMPLOYABILITY

# ==================================================

with tab3:


    st.header("Employability")

# Employment Status

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

# Employment Sector

st.subheader("Employment Sector")

sector_counts = filtered["Employment_Sector"].value_counts()


sector_df = pd.DataFrame({
    "Sector": sector_counts.index,
    "Count": sector_counts.values,
    "Percentage": (
        sector_counts.values / sector_counts.sum() * 100
    ).round(1)
})


fig_sector = px.bar(
    sector_df,
    x="Percentage",
    y="Sector",
    orientation="h",
    text="Percentage",
    hover_data=["Count"],
    color_discrete_sequence=[SMU_ORANGE]
)

fig_sector.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_sector,
    width="stretch",
    key="sector_chart"
)

# Time to Employment

st.subheader("Time to Employment")

time_df = (
    filtered["Time_To_Employment"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

time_df.columns = ["Time", "Percentage"]

fig_time = px.bar(
    time_df,
    x="Time",
    y="Percentage",
    text="Percentage",
    color_discrete_sequence=[SMU_BLUE]
)

fig_time.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_time,
    width="stretch",
    key="time_chart"
)

# Qualification Relevance

st.subheader("Extent to which SMU Qualification Supports Current Employment")

rel_df = (
    filtered["Qualification_Relevance"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

rel_df.columns = ["Qualification Relevance", "Percentage"]

fig_rel = px.pie(
    rel_df,
    names="Qualification Relevance",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_BLUE, SMU_ORANGE]
)

st.plotly_chart(
    fig_rel,
    width="stretch",
    key="relevance_chart"
)



with tab4:


    st.header("Graduate Outcomes")

# Workplace Preparedness

st.subheader("Workplace Preparedness")

prep_df = (
    filtered["Workplace_Preparedness"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

prep_df.columns = ["Response", "Percentage"]

fig_prep = px.pie(
    prep_df,
    names="Response",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_BLUE, SMU_ORANGE]
)

st.plotly_chart(
    fig_prep,
    width="stretch",
    key="preparedness_chart"
)

# Alumni Engagement Interest

st.subheader("Alumni Engagement Interest")

engage_df = (
    filtered["Alumni_Engagement_Interest"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

engage_df.columns = ["Response", "Percentage"]

fig_engage = px.bar(
    engage_df,
    x="Response",
    y="Percentage",
    text="Percentage",
    color_discrete_sequence=[SMU_ORANGE]
)

fig_engage.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_engage,
    width="stretch",
    key="engagement_chart"
)

# Stay Connected

st.subheader("Stay Connected with SMU")

connect_df = (
    filtered["Stay_Connected"]
    .value_counts(normalize=True)
    .mul(100)
    .reset_index()
)

connect_df.columns = ["Response", "Percentage"]

fig_connect = px.pie(
    connect_df,
    names="Response",
    values="Percentage",
    hole=0.5,
    color_discrete_sequence=[SMU_BLUE, SMU_ORANGE]
)

st.plotly_chart(
    fig_connect,
    width="stretch",
    key="connect_chart"
)



