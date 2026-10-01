import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Patient Health Record Dashboard",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: white;
}


/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f5f7fa !important;
}


/* Sidebar text */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #222222 !important;
}


/* Sidebar select boxes */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: white !important;
    color: #222222 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 7px !important;
}


/* Selected value */
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #222222 !important;
}


/* Dropdown arrow */
section[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #222222 !important;
    color: #222222 !important;
}


/* Dropdown menu */
[data-baseweb="popover"] {
    background-color: white !important;
}


/* Dropdown options */
[data-baseweb="popover"] li {
    background-color: white !important;
    color: #222222 !important;
}


/* Dropdown hover */
[data-baseweb="popover"] li:hover {
    background-color: #eaf2fb !important;
    color: #222222 !important;
}


/* KPI cards */
[data-testid="stMetric"] {
    background-color: #f8fbff !important;
    border: 1px solid #d8e2ec !important;
    border-radius: 8px !important;
    padding: 12px !important;
}


/* KPI label */
[data-testid="stMetricLabel"] {
    color: #555555 !important;
}


/* KPI value */
[data-testid="stMetricValue"] {
    color: #1f4e79 !important;
}


/* Headings */
h1,
h2,
h3 {
    color: #1f4e79 !important;
}


/* Normal text */
p {
    color: #333333;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("patient_dashboard_data.csv")

    # Create age group if not already available
    if "age_group" not in df.columns:

        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 18, 35, 50, 65, 100],
            labels=[
                "0-18",
                "19-35",
                "36-50",
                "51-65",
                "66+"
            ]
        )

    return df


data = load_data()


# =========================================================
# CHART FORMAT
# =========================================================

def format_chart(fig, x_title, y_title):

    fig.update_layout(

        template="simple_white",

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            family="Arial",
            size=13,
            color="#222222"
        ),

        xaxis=dict(

            title=x_title,

            title_font=dict(
                color="#222222",
                size=14
            ),

            tickfont=dict(
                color="#222222",
                size=12
            ),

            showline=True,

            linecolor="#333333",

            tickcolor="#333333",

            gridcolor="#eeeeee"
        ),

        yaxis=dict(

            title=y_title,

            title_font=dict(
                color="#222222",
                size=14
            ),

            tickfont=dict(
                color="#222222",
                size=12
            ),

            showline=True,

            linecolor="#333333",

            tickcolor="#333333",

            gridcolor="#eeeeee"
        ),

        title=dict(
            font=dict(
                color="#1f4e79",
                size=18
            )
        ),

        margin=dict(
            l=75,
            r=30,
            t=70,
            b=80
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_color="#222222"
        )
    )

    return fig


# =========================================================
# SIDEBAR FILTERS
# =========================================================

with st.sidebar:

    st.header("Dashboard Filters")

    st.write(
        "Select values to filter the dashboard."
    )

    st.divider()


    # -----------------------------------------------------
    # INSURANCE FILTER
    # -----------------------------------------------------

    insurance_values = sorted(
        data["insurance_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    insurance = st.selectbox(
        "Insurance Type",
        ["All"] + insurance_values
    )


    # -----------------------------------------------------
    # ADMISSION FILTER
    # -----------------------------------------------------

    admission_values = sorted(
        data["admit_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    admission = st.selectbox(
        "Admission Type",
        ["All"] + admission_values
    )


    # -----------------------------------------------------
    # HOSPITAL FILTER
    # -----------------------------------------------------

    hospital_values = sorted(
        data["hospital_tier"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    hospital = st.selectbox(
        "Hospital Tier",
        ["All"] + hospital_values
    )


    # -----------------------------------------------------
    # AGE FILTER
    # -----------------------------------------------------

    age_values = [
        "All",
        "0-18",
        "19-35",
        "36-50",
        "51-65",
        "66+"
    ]

    age = st.selectbox(
        "Age Group",
        age_values
    )


    # -----------------------------------------------------
    # GENDER FILTER
    # -----------------------------------------------------

    gender_values = sorted(
        data["gender"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    gender = st.selectbox(
        "Gender",
        ["All"] + gender_values
    )


# =========================================================
# APPLY FILTERS
# =========================================================

df = data.copy()


# Insurance

if insurance != "All":

    df = df[
        df["insurance_type"].astype(str) == insurance
    ]


# Admission

if admission != "All":

    df = df[
        df["admit_type"].astype(str) == admission
    ]


# Hospital tier

if hospital != "All":

    df = df[
        df["hospital_tier"].astype(str) == hospital
    ]


# Age

if age != "All":

    df = df[
        df["age_group"].astype(str) == age
    ]


# Gender

if gender != "All":

    df = df[
        df["gender"].astype(str) == gender
    ]


# =========================================================
# HEADER
# =========================================================

st.title(
    "Patient Health Record Dashboard"
)

st.write(
    "Analysis of hospital admissions and 30-day readmissions."
)

st.divider()


# =========================================================
# SUMMARY
# =========================================================

st.header("Summary")


total_admissions = len(df)


total_readmissions = int(
    df["readmitted_30d"].sum()
)


if len(df) > 0:

    readmission_rate = (
        df["readmitted_30d"].mean() * 100
    )

    avg_los = (
        df["los_days"].mean()
    )

    avg_cost = (
        df["total_cost_inr"].mean()
    )

else:

    readmission_rate = 0

    avg_los = 0

    avg_cost = 0


# =========================================================
# KPI CARDS
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "Total Admissions",
        f"{total_admissions:,}"
    )


with c2:

    st.metric(
        "Readmissions",
        f"{total_readmissions:,}"
    )


with c3:

    st.metric(
        "Readmission Rate",
        f"{readmission_rate:.2f}%"
    )


with c4:

    st.metric(
        "Average LOS",
        f"{avg_los:.2f} days"
    )


with c5:

    st.metric(
        "Average Cost",
        f"₹{avg_cost:,.0f}"
    )


# =========================================================
# READMISSION ANALYSIS
# =========================================================

st.divider()

st.header("Readmission Analysis")


col1, col2 = st.columns(2)


# =========================================================
# AGE GROUP
# =========================================================

with col1:

    age_data = (
        df.groupby(
            "age_group",
            observed=False
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    age_data["readmitted_30d"] = (
        age_data["readmitted_30d"] * 100
    )

    fig_age = px.bar(

        age_data,

        x="age_group",

        y="readmitted_30d",

        title="Readmission Rate by Age Group",

        text="readmitted_30d",

        labels={
            "age_group": "Age Group",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_age.update_traces(

        marker_color="#4F81BD",

        texttemplate="%{text:.2f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_age = format_chart(
        fig_age,
        "Age Group",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


# =========================================================
# INSURANCE
# =========================================================

with col2:

    insurance_data = (
        df.groupby(
            "insurance_type"
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    insurance_data["readmitted_30d"] = (
        insurance_data["readmitted_30d"] * 100
    )

    fig_insurance = px.bar(

        insurance_data,

        x="insurance_type",

        y="readmitted_30d",

        title="Readmission Rate by Insurance Type",

        text="readmitted_30d",

        labels={
            "insurance_type": "Insurance Type",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_insurance.update_traces(

        marker_color="#70AD47",

        texttemplate="%{text:.2f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_insurance = format_chart(
        fig_insurance,
        "Insurance Type",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_insurance,
        use_container_width=True
    )


# =========================================================
# PATIENT HISTORY
# =========================================================

st.header("Patient History")


col3, col4 = st.columns(2)


# =========================================================
# PREVIOUS ADMISSIONS
# =========================================================

with col3:

    previous_data = (
        df.groupby(
            "prev_admissions"
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    previous_data["readmitted_30d"] = (
        previous_data["readmitted_30d"] * 100
    )

    fig_previous = px.bar(

        previous_data,

        x="prev_admissions",

        y="readmitted_30d",

        title="Previous Admissions vs Readmission",

        text="readmitted_30d",

        labels={
            "prev_admissions": "Previous Admissions",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_previous.update_traces(

        marker_color="#ED7D31",

        texttemplate="%{text:.1f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_previous = format_chart(
        fig_previous,
        "Previous Admissions",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_previous,
        use_container_width=True
    )


# =========================================================
# COMORBIDITY
# =========================================================

with col4:

    comorbidity_data = (
        df.groupby(
            "comorbidity_count"
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    comorbidity_data["readmitted_30d"] = (
        comorbidity_data["readmitted_30d"] * 100
    )

    fig_comorbidity = px.bar(

        comorbidity_data,

        x="comorbidity_count",

        y="readmitted_30d",

        title="Comorbidity Count vs Readmission",

        text="readmitted_30d",

        labels={
            "comorbidity_count": "Comorbidity Count",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_comorbidity.update_traces(

        marker_color="#A5A5A5",

        texttemplate="%{text:.1f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_comorbidity = format_chart(
        fig_comorbidity,
        "Comorbidity Count",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_comorbidity,
        use_container_width=True
    )


# =========================================================
# HOSPITAL ANALYSIS
# =========================================================

st.header("Hospital Analysis")


col5, col6 = st.columns(2)


# =========================================================
# HOSPITAL TIER
# =========================================================

with col5:

    hospital_data = (
        df.groupby(
            "hospital_tier"
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    hospital_data["readmitted_30d"] = (
        hospital_data["readmitted_30d"] * 100
    )

    fig_hospital = px.bar(

        hospital_data,

        x="hospital_tier",

        y="readmitted_30d",

        title="Readmission Rate by Hospital Tier",

        text="readmitted_30d",

        labels={
            "hospital_tier": "Hospital Tier",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_hospital.update_traces(

        marker_color="#5B9BD5",

        texttemplate="%{text:.2f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_hospital = format_chart(
        fig_hospital,
        "Hospital Tier",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_hospital,
        use_container_width=True
    )


# =========================================================
# WARD TYPE
# =========================================================

with col6:

    ward_data = (
        df.groupby(
            "ward_type"
        )["readmitted_30d"]
        .mean()
        .reset_index()
    )

    ward_data["readmitted_30d"] = (
        ward_data["readmitted_30d"] * 100
    )

    fig_ward = px.bar(

        ward_data,

        x="ward_type",

        y="readmitted_30d",

        title="Readmission Rate by Ward Type",

        text="readmitted_30d",

        labels={
            "ward_type": "Ward Type",
            "readmitted_30d": "Readmission Rate (%)"
        }
    )

    fig_ward.update_traces(

        marker_color="#FFC000",

        texttemplate="%{text:.2f}%",

        textposition="outside",

        textfont=dict(
            color="#222222",
            size=12
        )
    )

    fig_ward = format_chart(
        fig_ward,
        "Ward Type",
        "Readmission Rate (%)"
    )

    st.plotly_chart(
        fig_ward,
        use_container_width=True
    )


# =========================================================
# COST ANALYSIS
# =========================================================

st.header("Treatment Cost Analysis")


cost_data = (
    df.groupby(
        "insurance_type"
    )[
        [
            "total_cost_inr",
            "out_of_pocket_inr"
        ]
    ]
    .mean()
    .reset_index()
)


cost_data = cost_data.melt(

    id_vars="insurance_type",

    var_name="Cost Type",

    value_name="Average Cost"
)


fig_cost = px.bar(

    cost_data,

    x="insurance_type",

    y="Average Cost",

    color="Cost Type",

    barmode="group",

    title="Average Cost by Insurance Type",

    text="Average Cost",

    labels={
        "insurance_type": "Insurance Type",
        "Average Cost": "Average Cost (INR)",
        "Cost Type": "Cost Type"
    },

    color_discrete_sequence=[
        "#4472C4",
        "#ED7D31"
    ]
)


fig_cost.update_traces(

    texttemplate="₹%{text:,.0f}",

    textposition="outside",

    textfont=dict(
        color="#222222",
        size=11
    )
)


fig_cost = format_chart(
    fig_cost,
    "Insurance Type",
    "Average Cost (INR)"
)


st.plotly_chart(
    fig_cost,
    use_container_width=True
)


# =========================================================
# CLINICAL INFORMATION
# =========================================================

st.header("Clinical Information")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Average HbA1c",
        f"{df['hba1c'].mean():.2f}"
    )


with c2:

    st.metric(
        "Average Creatinine",
        f"{df['creatinine'].mean():.2f}"
    )


with c3:

    st.metric(
        "Average Haemoglobin",
        f"{df['haemoglobin'].mean():.2f}"
    )


with c4:

    st.metric(
        "Average Systolic BP",
        f"{df['systolic_bp'].mean():.2f}"
    )


# =========================================================
# OBSERVATIONS
# =========================================================

st.divider()

st.header("Observations")


if len(df) > 0:

    age_rates = (
        df.groupby(
            "age_group",
            observed=False
        )["readmitted_30d"]
        .mean()
        .dropna()
    )


    previous_rates = (
        df.groupby(
            "prev_admissions"
        )["readmitted_30d"]
        .mean()
    )


    if len(age_rates) > 0:

        highest_age = age_rates.idxmax()

        st.write(
            f"• Highest observed readmission rate "
            f"among age groups: **{highest_age}**."
        )


    if len(previous_rates) > 0:

        highest_previous = previous_rates.idxmax()

        st.write(
            f"• Highest observed readmission rate "
            f"for previous admissions: **{highest_previous}**."
        )


    st.write(
        f"• Records after applying filters: "
        f"**{len(df):,}**."
    )


# =========================================================
# DOWNLOAD
# =========================================================

st.divider()

st.header("Download Data")


csv_file = df.to_csv(
    index=False
)


st.download_button(

    label="Download Filtered CSV",

    data=csv_file,

    file_name="filtered_patient_data.csv",

    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Patient Health Record Dashboard | P_090"
)
