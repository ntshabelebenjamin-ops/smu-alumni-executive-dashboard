import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SMU Alumni Executive Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_excel(
        "SMU_Alumni_Short_Survey_ANALYTICS_READY.xlsx"
    )

df = load_data()

# ---------------------------------------------------
# RENAME COLUMNS
# ---------------------------------------------------

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

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

responses = len(df)

employment_rate = round(
    (df["Employment_Status"]
     .str.contains("Employed", case=False, na=False)
    ).mean() * 100,
    1
)

# ---------------------------------------------------
# ADD TABS HERE
# ---------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Graduate Profile",
    "Employability",
    "Graduate Outcomes"
])

# ---------------------------------------------------
# TAB 1
# ---------------------------------------------------

with tab1:

    st.header("Executive Overview")

    col1, col2 = st.columns(2)

    col1.metric("Responses", responses)
    col2.metric("Employment Rate", f"{employment_rate}%")

# ---------------------------------------------------
# TAB 2
# ---------------------------------------------------

with tab2:

    st.header("Graduate Profile")

    st.write("Graduate profile charts will go here.")

# ---------------------------------------------------
# TAB 3
# ---------------------------------------------------

with tab3:

    st.header("Employability")

    st.write("Employability charts will go here.")

# ---------------------------------------------------
# TAB 4
# ---------------------------------------------------

with tab4:

    st.header("Graduate Outcomes")

    st.write("Graduate outcomes charts will go here.")

with tab2:

    st.header("Graduate Profile")

    col1, col2 = st.columns(2)

    # SCHOOL DISTRIBUTION
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

    with col1:
        st.subheader("School Distribution")
        st.plotly_chart(fig_school, use_container_width=True)

    # GENDER DISTRIBUTION
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

    fig_gender.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    with col2:
        st.subheader("Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)
