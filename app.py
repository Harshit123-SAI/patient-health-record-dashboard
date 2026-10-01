import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Patient Health Record Dashboard",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 1.5rem;
}

h1 {
    color: #ffffff;
}

h2, h3 {
    color: #e5e7eb;
}

[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #30363d;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    data = pd.read_csv("patient_dashboard_data.csv")

    patients = pd.read_csv("patients.csv")

    admissions = pd.read_csv("admissions.csv")

    diagnoses = pd.read_csv("diagnoses.csv")

    return data, patients, admissions, diagnoses


data, patients, admissions, diagnoses = load_data()


# =========================================================
# DATE CONVERSION
# =========================================================

if "admit_date" in data.columns:

    data["admit_date"] = pd.to_datetime(
        data["admit_date"],
        errors="coerce"
    )


if "discharge_date" in data.columns:

    data["discharge_date"] = pd.to_datetime(
        data["discharge_date"],
        errors="coerce"
    )


if "admit_date" in admissions.columns:

    admissions["admit_date"] = pd.to_datetime(
        admissions["admit_date"],
        errors="coerce"
    )


if "discharge_date" in admissions.columns:

    admissions["discharge_date"] = pd.to_datetime(
        admissions["discharge_date"],
        errors="coerce"
    )


# =========================================================
# TITLE
# =========================================================

st.title("🏥 Patient Health Record Dashboard")

st.markdown(
    "Interactive analysis of patient demographics, clinical information, "
    "hospital performance, healthcare costs, diagnoses and readmission."
)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🔎 Dashboard Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Patient & Demographic Analysis",
        "Clinical Analysis",
        "Hospital Analysis",
        "Cost Analysis",
        "Disease & Diagnosis Analysis",
        "Monthly Trends",
        "ML Model Analysis",
        "Patient Explorer"
    ]
)


# =========================================================
# FILTERS
# =========================================================

st.sidebar.markdown("---")

st.sidebar.subheader("🎛️ Dashboard Filters")

filtered_data = data.copy()


# ---------------------------------------------------------
# Gender
# ---------------------------------------------------------

if "gender" in data.columns:

    gender_options = ["All"] + sorted(
        data["gender"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_gender = st.sidebar.selectbox(
        "Gender",
        gender_options
    )

    if selected_gender != "All":

        filtered_data = filtered_data[
            filtered_data["gender"].astype(str)
            == selected_gender
        ]


# ---------------------------------------------------------
# Insurance
# ---------------------------------------------------------

if "insurance_type" in data.columns:

    insurance_options = ["All"] + sorted(
        data["insurance_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_insurance = st.sidebar.selectbox(
        "Insurance Type",
        insurance_options
    )

    if selected_insurance != "All":

        filtered_data = filtered_data[
            filtered_data["insurance_type"].astype(str)
            == selected_insurance
        ]


# ---------------------------------------------------------
# Readmission
# ---------------------------------------------------------

if "readmitted_30d" in data.columns:

    readmission_filter = st.sidebar.selectbox(
        "30-Day Readmission",
        [
            "All",
            "Readmitted",
            "Not Readmitted"
        ]
    )

    if readmission_filter == "Readmitted":

        filtered_data = filtered_data[
            filtered_data["readmitted_30d"] == 1
        ]

    elif readmission_filter == "Not Readmitted":

        filtered_data = filtered_data[
            filtered_data["readmitted_30d"] == 0
        ]


# ---------------------------------------------------------
# Hospital Tier
# ---------------------------------------------------------

if "hospital_tier" in data.columns:

    hospital_tier_options = ["All"] + sorted(
        data["hospital_tier"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_hospital_tier = st.sidebar.selectbox(
        "Hospital Tier",
        hospital_tier_options
    )

    if selected_hospital_tier != "All":

        filtered_data = filtered_data[
            filtered_data["hospital_tier"].astype(str)
            == selected_hospital_tier
        ]


# ---------------------------------------------------------
# Admission Type
# ---------------------------------------------------------

if "admit_type" in data.columns:

    admission_type_options = ["All"] + sorted(
        data["admit_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_admission_type = st.sidebar.selectbox(
        "Admission Type",
        admission_type_options
    )

    if selected_admission_type != "All":

        filtered_data = filtered_data[
            filtered_data["admit_type"].astype(str)
            == selected_admission_type
        ]


# ---------------------------------------------------------
# Ward Type
# ---------------------------------------------------------

if "ward_type" in data.columns:

    ward_options = ["All"] + sorted(
        data["ward_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_ward = st.sidebar.selectbox(
        "Ward Type",
        ward_options
    )

    if selected_ward != "All":

        filtered_data = filtered_data[
            filtered_data["ward_type"].astype(str)
            == selected_ward
        ]


# ---------------------------------------------------------
# Discharge Type
# ---------------------------------------------------------

if "discharge_type" in data.columns:

    discharge_options = ["All"] + sorted(
        data["discharge_type"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_discharge = st.sidebar.selectbox(
        "Discharge Type",
        discharge_options
    )

    if selected_discharge != "All":

        filtered_data = filtered_data[
            filtered_data["discharge_type"].astype(str)
            == selected_discharge
        ]


# ---------------------------------------------------------
# Hospital State
# ---------------------------------------------------------

if "hospital_state" in data.columns:

    state_options = ["All"] + sorted(
        data["hospital_state"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_state = st.sidebar.selectbox(
        "Hospital State",
        state_options
    )

    if selected_state != "All":

        filtered_data = filtered_data[
            filtered_data["hospital_state"].astype(str)
            == selected_state
        ]


# ---------------------------------------------------------
# Age Range
# ---------------------------------------------------------

if "age" in data.columns:

    min_age = int(data["age"].min())
    max_age = int(data["age"].max())

    age_range = st.sidebar.slider(
        "Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

    filtered_data = filtered_data[
        filtered_data["age"].between(
            age_range[0],
            age_range[1]
        )
    ]


# ---------------------------------------------------------
# Length of Stay
# ---------------------------------------------------------

if "los_days" in data.columns:

    min_los = int(data["los_days"].min())
    max_los = int(data["los_days"].max())

    los_range = st.sidebar.slider(
        "Length of Stay (Days)",
        min_value=min_los,
        max_value=max_los,
        value=(min_los, max_los)
    )

    filtered_data = filtered_data[
        filtered_data["los_days"].between(
            los_range[0],
            los_range[1]
        )
    ]


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.header("📊 Dashboard Overview")

    total_admissions = len(filtered_data)

    total_patients = patients["patient_id"].nunique()

    if "readmitted_30d" in filtered_data.columns:

        readmission_rate = (
            filtered_data["readmitted_30d"].mean()
            * 100
        )

    else:

        readmission_rate = 0


    if "los_days" in filtered_data.columns:

        avg_los = filtered_data["los_days"].mean()

    else:

        avg_los = 0


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "👥 Total Patients",
        f"{total_patients:,}"
    )


    c2.metric(
        "🏥 Admissions",
        f"{total_admissions:,}"
    )


    c3.metric(
        "🔄 Readmission Rate",
        f"{readmission_rate:.2f}%"
    )


    c4.metric(
        "🛏️ Avg Length of Stay",
        f"{avg_los:.2f} days"
    )


    st.markdown("---")


    # Readmission distribution

    if "readmitted_30d" in filtered_data.columns:

        st.subheader("30-Day Readmission Distribution")

        readmission_counts = (
            filtered_data["readmitted_30d"]
            .value_counts()
            .reset_index()
        )

        readmission_counts.columns = [
            "Readmission",
            "Count"
        ]

        readmission_counts["Readmission"] = (
            readmission_counts["Readmission"]
            .map({
                0: "Not Readmitted",
                1: "Readmitted"
            })
        )

        fig = px.pie(
            readmission_counts,
            names="Readmission",
            values="Count",
            hole=0.45,
            title="30-Day Readmission Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PATIENT & DEMOGRAPHIC ANALYSIS
# =========================================================

elif page == "Patient & Demographic Analysis":

    st.header("👥 Patient & Demographic Analysis")


    col1, col2 = st.columns(2)


    # Age

    with col1:

        if "age_group" in filtered_data.columns:

            age_rate = (
                filtered_data
                .groupby("age_group")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            age_rate["readmitted_30d"] *= 100

            fig = px.bar(
                age_rate,
                x="age_group",
                y="readmitted_30d",
                title="Age Group vs Readmission Rate",
                labels={
                    "age_group": "Age Group",
                    "readmitted_30d": "Readmission Rate (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif "age" in filtered_data.columns:

            fig = px.histogram(
                filtered_data,
                x="age",
                color="readmitted_30d",
                nbins=30,
                title="Age Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Gender

    with col2:

        if "gender" in filtered_data.columns:

            gender_rate = (
                filtered_data
                .groupby("gender")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            gender_rate["readmitted_30d"] *= 100

            fig = px.bar(
                gender_rate,
                x="gender",
                y="readmitted_30d",
                title="Gender vs Readmission Rate",
                labels={
                    "readmitted_30d":
                    "Readmission Rate (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Insurance

    if "insurance_type" in filtered_data.columns:

        insurance_rate = (
            filtered_data
            .groupby("insurance_type")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )

        insurance_rate["readmitted_30d"] *= 100

        fig = px.bar(
            insurance_rate,
            x="insurance_type",
            y="readmitted_30d",
            title="Insurance Type vs Readmission",
            labels={
                "readmitted_30d":
                "Readmission Rate (%)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# CLINICAL ANALYSIS
# =========================================================

elif page == "Clinical Analysis":

    st.header("🩺 Clinical Analysis")


    col1, col2 = st.columns(2)


    # Comorbidity

    with col1:

        if "comorbidity_count" in filtered_data.columns:

            temp = (
                filtered_data
                .groupby("comorbidity_count")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            temp["readmitted_30d"] *= 100

            fig = px.bar(
                temp,
                x="comorbidity_count",
                y="readmitted_30d",
                title="Comorbidity Count vs Readmission",
                labels={
                    "comorbidity_count":
                    "Comorbidity Count",
                    "readmitted_30d":
                    "Readmission Rate (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Previous Admissions

    with col2:

        if "prev_admissions" in filtered_data.columns:

            temp = (
                filtered_data
                .groupby("prev_admissions")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            temp["readmitted_30d"] *= 100

            fig = px.bar(
                temp,
                x="prev_admissions",
                y="readmitted_30d",
                title="Previous Admissions vs Readmission",
                labels={
                    "prev_admissions":
                    "Previous Admissions",
                    "readmitted_30d":
                    "Readmission Rate (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    col1, col2 = st.columns(2)


    # Charlson

    with col1:

        if "charlson_index" in filtered_data.columns:

            temp = (
                filtered_data
                .groupby("charlson_index")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            temp["readmitted_30d"] *= 100

            fig = px.bar(
                temp,
                x="charlson_index",
                y="readmitted_30d",
                title="Charlson Index vs Readmission",
                labels={
                    "readmitted_30d":
                    "Readmission Rate (%)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # LOS

    with col2:

        if "los_days" in filtered_data.columns:

            temp = (
                filtered_data
                .groupby("readmitted_30d")
                ["los_days"]
                .mean()
                .reset_index()
            )

            temp["Status"] = temp[
                "readmitted_30d"
            ].map({
                0: "Not Readmitted",
                1: "Readmitted"
            })

            fig = px.bar(
                temp,
                x="Status",
                y="los_days",
                title="Average Length of Stay",
                labels={
                    "los_days":
                    "Average LOS (Days)"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Clinical variables

    clinical_cols = [
        "hba1c",
        "creatinine",
        "haemoglobin",
        "systolic_bp"
    ]

    available_clinical = [
        x for x in clinical_cols
        if x in filtered_data.columns
    ]


    if available_clinical:

        st.subheader("🧪 Clinical Measurements")

        selected_clinical = st.selectbox(
            "Select Clinical Variable",
            available_clinical
        )

        fig = px.box(
            filtered_data,
            x="readmitted_30d",
            y=selected_clinical,
            color="readmitted_30d",
            title=f"{selected_clinical} vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Clinical risk

    if "clinical_risk" in filtered_data.columns:

        risk_rate = (
            filtered_data
            .groupby("clinical_risk")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )

        risk_rate["readmitted_30d"] *= 100

        fig = px.bar(
            risk_rate,
            x="clinical_risk",
            y="readmitted_30d",
            title="Clinical Risk Score vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# HOSPITAL ANALYSIS
# =========================================================

elif page == "Hospital Analysis":

    st.header("🏥 Hospital Analysis")


    # Hospital Tier

    if "hospital_tier" in filtered_data.columns:

        tier_rate = (
            filtered_data
            .groupby("hospital_tier")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )

        tier_rate["readmitted_30d"] *= 100

        fig = px.bar(
            tier_rate,
            x="hospital_tier",
            y="readmitted_30d",
            title="Hospital Tier vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Hospital State

    if "hospital_state" in filtered_data.columns:

        state_rate = (
            filtered_data
            .groupby("hospital_state")
            ["readmitted_30d"]
            .mean()
            .reset_index()
            .sort_values(
                "readmitted_30d",
                ascending=False
            )
        )

        state_rate["readmitted_30d"] *= 100

        fig = px.bar(
            state_rate,
            x="hospital_state",
            y="readmitted_30d",
            title="Hospital State vs Readmission",
            labels={
                "hospital_state": "State",
                "readmitted_30d":
                "Readmission Rate (%)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Hospital Beds

    if "hospital_beds" in filtered_data.columns:

        fig = px.scatter(
            filtered_data,
            x="hospital_beds",
            y="readmitted_30d",
            title="Hospital Beds vs Readmission",
            labels={
                "hospital_beds": "Hospital Beds",
                "readmitted_30d":
                "30-Day Readmission"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    col1, col2 = st.columns(2)


    # Ward

    with col1:

        if "ward_type" in filtered_data.columns:

            ward_rate = (
                filtered_data
                .groupby("ward_type")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            ward_rate["readmitted_30d"] *= 100

            fig = px.bar(
                ward_rate,
                x="ward_type",
                y="readmitted_30d",
                title="Ward Type vs Readmission"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Discharge

    with col2:

        if "discharge_type" in filtered_data.columns:

            discharge_rate = (
                filtered_data
                .groupby("discharge_type")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )

            discharge_rate["readmitted_30d"] *= 100

            fig = px.bar(
                discharge_rate,
                x="discharge_type",
                y="readmitted_30d",
                title="Discharge Type vs Readmission"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Admission Type

    if "admit_type" in filtered_data.columns:

        admission_rate = (
            filtered_data
            .groupby("admit_type")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )

        admission_rate["readmitted_30d"] *= 100

        fig = px.bar(
            admission_rate,
            x="admit_type",
            y="readmitted_30d",
            title="Admission Type vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# COST ANALYSIS
# =========================================================

elif page == "Cost Analysis":

    st.header("💰 Healthcare Cost Analysis")


    cost_cols = [
        "total_cost_inr",
        "govt_subsidy_inr",
        "out_of_pocket_inr"
    ]

    available_costs = [
        x for x in cost_cols
        if x in filtered_data.columns
    ]


    if available_costs:

        selected_cost = st.selectbox(
            "Select Cost Variable",
            available_costs
        )


        col1, col2 = st.columns(2)


        with col1:

            fig = px.histogram(
                filtered_data,
                x=selected_cost,
                nbins=40,
                title=f"{selected_cost} Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with col2:

            fig = px.box(
                filtered_data,
                x="readmitted_30d",
                y=selected_cost,
                color="readmitted_30d",
                title=f"{selected_cost} vs Readmission"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    if "cost_category" in filtered_data.columns:

        cost_rate = (
            filtered_data
            .groupby("cost_category")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )

        cost_rate["readmitted_30d"] *= 100

        fig = px.bar(
            cost_rate,
            x="cost_category",
            y="readmitted_30d",
            title="Cost Category vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# DISEASE & DIAGNOSIS ANALYSIS
# =========================================================

elif page == "Disease & Diagnosis Analysis":

    st.header("🦠 Disease & Diagnosis Analysis")


    if "diag_category" in diagnoses.columns:

        diagnosis_counts = (
            diagnoses["diag_category"]
            .value_counts()
            .reset_index()
        )

        diagnosis_counts.columns = [
            "diag_category",
            "count"
        ]


        fig = px.bar(
            diagnosis_counts,
            x="diag_category",
            y="count",
            title="Diagnosis Category Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Avoid over-counting
        diagnosis_data = (
            diagnoses[
                [
                    "admission_id",
                    "diag_category"
                ]
            ]
            .drop_duplicates(
                [
                    "admission_id",
                    "diag_category"
                ]
            )
        )


        diagnosis_data = diagnosis_data.merge(
            admissions[
                [
                    "admission_id",
                    "readmitted_30d"
                ]
            ],
            on="admission_id",
            how="left"
        )


        diagnosis_rate = (
            diagnosis_data
            .groupby("diag_category")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )


        diagnosis_rate["readmitted_30d"] *= 100


        fig = px.bar(
            diagnosis_rate,
            x="diag_category",
            y="readmitted_30d",
            title="Diagnosis Category vs Readmission"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Primary Diagnosis

    if "diag_rank" in diagnoses.columns:

        primary = diagnoses[
            diagnoses["diag_rank"] == 1
        ].copy()


        if "diag_category" in primary.columns:

            primary = primary.merge(
                admissions[
                    [
                        "admission_id",
                        "readmitted_30d"
                    ]
                ],
                on="admission_id",
                how="left"
            )


            primary_rate = (
                primary
                .groupby("diag_category")
                ["readmitted_30d"]
                .mean()
                .reset_index()
            )


            primary_rate["readmitted_30d"] *= 100


            fig = px.bar(
                primary_rate,
                x="diag_category",
                y="readmitted_30d",
                title="Primary Diagnosis Category vs Readmission"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # Top diagnoses

        if "diag_desc" in primary.columns:

            top_diagnoses = (
                primary["diag_desc"]
                .value_counts()
                .head(10)
                .reset_index()
            )


            top_diagnoses.columns = [
                "Diagnosis",
                "Count"
            ]


            fig = px.bar(
                top_diagnoses,
                x="Count",
                y="Diagnosis",
                orientation="h",
                title="Top 10 Primary Diagnoses"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Diagnosis Count

    diagnosis_count = (
        diagnoses
        .groupby("admission_id")
        .size()
        .reset_index(
            name="diagnosis_count"
        )
    )


    diagnosis_count = diagnosis_count.merge(
        admissions[
            [
                "admission_id",
                "readmitted_30d"
            ]
        ],
        on="admission_id",
        how="left"
    )


    count_rate = (
        diagnosis_count
        .groupby("diagnosis_count")
        ["readmitted_30d"]
        .mean()
        .reset_index()
    )


    count_rate["readmitted_30d"] *= 100


    fig = px.bar(
        count_rate,
        x="diagnosis_count",
        y="readmitted_30d",
        title="Number of Diagnoses vs Readmission"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MONTHLY TRENDS
# =========================================================

elif page == "Monthly Trends":

    st.header("📅 Monthly Trends")


    if "admit_date" in filtered_data.columns:

        monthly = filtered_data.copy()


        monthly["month"] = (
            monthly["admit_date"]
            .dt.to_period("M")
            .astype(str)
        )


        monthly_rate = (
            monthly
            .groupby("month")
            ["readmitted_30d"]
            .mean()
            .reset_index()
        )


        monthly_rate["readmitted_30d"] *= 100


        fig = px.line(
            monthly_rate,
            x="month",
            y="readmitted_30d",
            markers=True,
            title="Monthly Readmission Rate",
            labels={
                "month": "Month",
                "readmitted_30d":
                "Readmission Rate (%)"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Monthly admissions

        monthly_volume = (
            monthly
            .groupby("month")
            .size()
            .reset_index(
                name="admissions"
            )
        )


        fig = px.line(
            monthly_volume,
            x="month",
            y="admissions",
            markers=True,
            title="Monthly Admission Volume"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# ML MODEL ANALYSIS
# =========================================================

elif page == "ML Model Analysis":

    st.header("🤖 ML Model Analysis")


    st.info(
        "Machine learning was used to analyze 30-day hospital "
        "readmission using patient and admission information."
    )


    st.subheader("📌 Models Used")

    st.write(
        "- Logistic Regression"
    )

    st.write(
        "- Random Forest"
    )


    st.subheader("📊 Evaluation Metrics")

    st.write(
        "The project evaluates models using:"
    )

    st.write(
        "- Accuracy"
    )

    st.write(
        "- Precision"
    )

    st.write(
        "- Recall"
    )

    st.write(
        "- F1 Score"
    )

    st.write(
        "- ROC-AUC"
    )


    # Known Random Forest result from project analysis

    ml_result = pd.DataFrame({

        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC"
        ],

        "Random Forest": [
            88.35,
            57.95,
            5.77,
            10.50,
            73.79
        ]
    })


    fig = px.bar(
        ml_result,
        x="Metric",
        y="Random Forest",
        title="Random Forest Model Performance",
        labels={
            "Random Forest":
            "Score (%)"
        }
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.dataframe(
        ml_result,
        use_container_width=True,
        hide_index=True
    )


    st.warning(
        "The relatively low recall indicates that the current "
        "classification threshold misses a substantial number "
        "of readmitted patients."
    )


# =========================================================
# PATIENT EXPLORER
# =========================================================

elif page == "Patient Explorer":

    st.header("🔎 Patient Explorer")


    st.markdown(
        "Search a Patient ID to view the patient's personal "
        "information, admission history and recorded diseases."
    )


    # -----------------------------------------------------
    # SEARCH PATIENT
    # -----------------------------------------------------

    patient_search = st.text_input(
        "🔍 Enter Patient ID",
        placeholder="Example: P10025"
    )


    patient_ids = (
        patients["patient_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    # If user types ID
    if patient_search.strip() != "":

        search_id = patient_search.strip()

        matching_ids = [
            x for x in patient_ids
            if search_id.lower() in x.lower()
        ]


        if len(matching_ids) == 1:

            selected_patient_id = matching_ids[0]

        elif len(matching_ids) > 1:

            selected_patient_id = st.selectbox(
                "Multiple patients found. Select one:",
                sorted(matching_ids)
            )

        else:

            selected_patient_id = None

            st.error(
                "No patient found with this Patient ID."
            )


    # If search box empty
    else:

        selected_patient_id = st.selectbox(
            "Or select Patient ID",
            sorted(patient_ids)
        )


    # -----------------------------------------------------
    # PATIENT DETAILS
    # -----------------------------------------------------

    if selected_patient_id is not None:

        selected_patient = patients[
            patients["patient_id"].astype(str)
            == selected_patient_id
        ]


        if not selected_patient.empty:

            patient = selected_patient.iloc[0]


            st.markdown("---")

            st.subheader("👤 Patient Information")


            c1, c2, c3, c4 = st.columns(4)


            c1.metric(
                "Patient ID",
                str(patient["patient_id"])
            )


            if "age" in patient.index:

                c2.metric(
                    "Age",
                    str(patient["age"])
                )


            if "gender" in patient.index:

                c3.metric(
                    "Gender",
                    str(patient["gender"])
                )


            if "insurance_type" in patient.index:

                c4.metric(
                    "Insurance",
                    str(patient["insurance_type"])
                )


            # -------------------------------------------------
            # EXTRA PATIENT DETAILS
            # -------------------------------------------------

            extra_cols = [
                "state",
                "bpl_card",
                "comorbidity_count",
                "prev_admissions"
            ]


            available_extra = [
                x for x in extra_cols
                if x in patient.index
            ]


            if available_extra:

                st.subheader("📋 Additional Patient Details")


                detail_data = pd.DataFrame({

                    "Field": [
                        x.replace(
                            "_",
                            " "
                        ).title()
                        for x in available_extra
                    ],

                    "Value": [
                        patient[x]
                        for x in available_extra
                    ]
                })


                st.dataframe(
                    detail_data,
                    use_container_width=True,
                    hide_index=True
                )


            # -------------------------------------------------
            # ADMISSION HISTORY
            # -------------------------------------------------

            st.markdown("---")

            st.subheader("🏥 Admission History")


            patient_admissions = admissions[
                admissions["patient_id"].astype(str)
                == selected_patient_id
            ].copy()


            if patient_admissions.empty:

                st.info(
                    "No admission records found."
                )


            else:

                display_cols = [

                    "admission_id",

                    "admit_date",

                    "discharge_date",

                    "los_days",

                    "admit_type",

                    "ward_type",

                    "hospital_id",

                    "discharge_type",

                    "num_procedures",

                    "charlson_index",

                    "hba1c",

                    "creatinine",

                    "haemoglobin",

                    "systolic_bp",

                    "readmitted_30d",

                    "readmitted_7d"
                ]


                display_cols = [
                    x for x in display_cols
                    if x in patient_admissions.columns
                ]


                history = patient_admissions[
                    display_cols
                ].copy()


                if "readmitted_30d" in history.columns:

                    history["readmitted_30d"] = (
                        history["readmitted_30d"]
                        .map({
                            0: "No",
                            1: "Yes"
                        })
                    )


                if "readmitted_7d" in history.columns:

                    history["readmitted_7d"] = (
                        history["readmitted_7d"]
                        .map({
                            0: "No",
                            1: "Yes"
                        })
                    )


                st.dataframe(
                    history,
                    use_container_width=True,
                    hide_index=True
                )


                c1, c2, c3 = st.columns(3)


                c1.metric(
                    "Total Admissions",
                    len(patient_admissions)
                )


                if "los_days" in patient_admissions.columns:

                    c2.metric(
                        "Average LOS",
                        f"{patient_admissions['los_days'].mean():.2f} days"
                    )


                if "readmitted_30d" in patient_admissions.columns:

                    c3.metric(
                        "30-Day Readmissions",
                        int(
                            patient_admissions[
                                "readmitted_30d"
                            ].sum()
                        )
                    )


            # -------------------------------------------------
            # DISEASE / DIAGNOSIS
            # -------------------------------------------------

            st.markdown("---")

            st.subheader("🦠 Diseases & Diagnoses")


            patient_admission_ids = (
                patient_admissions[
                    "admission_id"
                ].tolist()
            )


            patient_diagnoses = diagnoses[
                diagnoses["admission_id"]
                .isin(patient_admission_ids)
            ].copy()


            if patient_diagnoses.empty:

                st.info(
                    "No diagnosis records found for this patient."
                )


            else:

                diagnosis_cols = [

                    "admission_id",

                    "diag_rank",

                    "icd10_code",

                    "diag_desc",

                    "diag_category"
                ]


                diagnosis_cols = [
                    x for x in diagnosis_cols
                    if x in patient_diagnoses.columns
                ]


                st.dataframe(
                    patient_diagnoses[
                        diagnosis_cols
                    ],
                    use_container_width=True,
                    hide_index=True
                )


                # Diagnosis summary

                if "diag_category" in patient_diagnoses.columns:

                    disease_count = (
                        patient_diagnoses[
                            "diag_category"
                        ]
                        .value_counts()
                        .reset_index()
                    )


                    disease_count.columns = [
                        "Disease Category",
                        "Count"
                    ]


                    fig = px.bar(
                        disease_count,
                        x="Disease Category",
                        y="Count",
                        title="Patient Disease Categories"
                    )


                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )


            # -------------------------------------------------
            # LATEST CLINICAL INFORMATION
            # -------------------------------------------------

            st.markdown("---")

            st.subheader("🩺 Latest Clinical Information")


            if not patient_admissions.empty:

                latest = (
                    patient_admissions
                    .sort_values("admit_date")
                    .iloc[-1]
                )


                clinical_cols = [

                    "hba1c",

                    "creatinine",

                    "haemoglobin",

                    "systolic_bp",

                    "charlson_index",

                    "num_procedures"
                ]


                available_clinical = [
                    x for x in clinical_cols
                    if x in latest.index
                ]


                if available_clinical:

                    metric_cols = st.columns(
                        len(available_clinical)
                    )


                    for i, col in enumerate(
                        available_clinical
                    ):

                        metric_cols[i].metric(
                            col.replace(
                                "_",
                                " "
                            ).title(),
                            str(latest[col])
                        )


            # -------------------------------------------------
            # DOWNLOAD PATIENT RECORD
            # -------------------------------------------------

            st.markdown("---")

            st.subheader("⬇️ Download Patient Record")


            patient_record = patient_admissions.copy()


            if not patient_diagnoses.empty:

                patient_record = patient_record.merge(
                    patient_diagnoses,
                    on="admission_id",
                    how="left",
                    suffixes=(
                        "",
                        "_diagnosis"
                    )
                )


            csv = patient_record.to_csv(
                index=False
            )


            st.download_button(
                label="📥 Download Patient Record",
                data=csv,
                file_name=(
                    f"patient_"
                    f"{selected_patient_id}"
                    f"_record.csv"
                ),
                mime="text/csv"
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Patient Health Record Dashboard | Data Science Project P_090"
)
