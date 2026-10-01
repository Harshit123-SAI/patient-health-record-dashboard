import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Patient Health Dashboard",
    page_icon="🏥",
    layout="wide"
)

data = pd.read_csv("patient_dashboard_data.csv")

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #06142f, #0a1f4d, #10143b);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #06132d, #0a2452);
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1500px;
}

.hero {
    background: linear-gradient(
        100deg,
        #123c9c,
        #6335b5,
        #087f91
    );

    padding: 30px;
    border-radius: 22px;
    margin-bottom: 25px;

    box-shadow: 0 10px 35px rgba(0,0,0,0.4);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
}

.hero-sub {
    font-size: 16px;
    color: #dce9ff;
    margin-top: 8px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    color: white;
    min-height: 125px;

    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

.blue {
    background: linear-gradient(135deg,#1674e8,#123b9e);
}

.purple {
    background: linear-gradient(135deg,#a348ec,#4b238e);
}

.green {
    background: linear-gradient(135deg,#00b8a9,#08746c);
}

.orange {
    background: linear-gradient(135deg,#f6a62b,#a75812);
}

.card-title {
    font-size: 15px;
}

.card-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.section {
    background: rgba(8,30,70,0.75);
    border: 1px solid rgba(80,150,255,0.35);

    border-radius: 20px;
    padding: 20px;
    margin-top: 25px;

    box-shadow: 0 8px 28px rgba(0,0,0,0.25);
}

.small-card {
    background: linear-gradient(135deg,#182d70,#26366f);

    border-radius: 16px;
    padding: 17px;

    border: 1px solid rgba(130,160,255,0.35);
}

.small-title {
    font-size: 13px;
    color: #b9ceff;
}

.small-value {
    font-size: 23px;
    font-weight: 700;
    margin-top: 5px;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #9fc6ff;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 🏥 Patient Analytics")
st.sidebar.caption("Interactive healthcare dashboard")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🔎 Filters")

insurance = st.sidebar.multiselect(
    "Insurance Type",
    sorted(data["insurance_type"].unique()),
    default=sorted(data["insurance_type"].unique())
)

admission = st.sidebar.multiselect(
    "Admission Type",
    sorted(data["admit_type"].unique()),
    default=sorted(data["admit_type"].unique())
)

tier = st.sidebar.multiselect(
    "Hospital Tier",
    sorted(data["hospital_tier"].unique()),
    default=sorted(data["hospital_tier"].unique())
)


filtered = data[
    data["insurance_type"].isin(insurance)
    &
    data["admit_type"].isin(admission)
    &
    data["hospital_tier"].isin(tier)
]


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">

<div class="hero-title">
 Patient Health Record Dashboard
</div>

<div class="hero-sub">
Patient admission, readmission and healthcare analytics
</div>

</div>
""", unsafe_allow_html=True)


# ---------------- KPI ----------------

st.markdown("## 📊 Key Performance Indicators")

total = len(filtered)

readmissions = int(
    filtered["readmitted_30d"].sum()
)

rate = (
    filtered["readmitted_30d"].mean() * 100
)

avg_los = filtered["los_days"].mean()


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(f"""
    <div class="card blue">

    <div class="card-title">
    👥 Total Admissions
    </div>

    <div class="card-value">
    {total:,}
    </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="card purple">

    <div class="card-title">
    ↩️ Readmissions
    </div>

    <div class="card-value">
    {readmissions:,}
    </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="card green">

    <div class="card-title">
    📈 Readmission Rate
    </div>

    <div class="card-value">
    {rate:.2f}%
    </div>

    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="card orange">

    <div class="card-title">
    🛏️ Average LOS
    </div>

    <div class="card-value">
    {avg_los:.2f} days
    </div>

    </div>
    """, unsafe_allow_html=True)


# ---------------- READMISSION ----------------

st.markdown("""
<div class="section">
<h2>📊 Readmission Analysis</h2>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)


# Age

with col1:

    age = (
        filtered
        .groupby("age_group", observed=False)
        ["readmitted_30d"]
        .mean() * 100
    )

    fig = px.bar(
        x=age.index,
        y=age.values,
        title="Readmission by Age Group",
        labels={
            "x": "Age Group",
            "y": "Readmission Rate (%)"
        },
        color=age.values,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Insurance

with col2:

    insurance_rate = (
        filtered
        .groupby("insurance_type")
        ["readmitted_30d"]
        .mean() * 100
    )

    fig = px.pie(
        values=insurance_rate.values,
        names=insurance_rate.index,
        hole=0.55,
        title="Readmission by Insurance"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


col3, col4 = st.columns(2)


# Admission Type

with col3:

    admission_rate = (
        filtered
        .groupby("admit_type")
        ["readmitted_30d"]
        .mean() * 100
    )

    fig = px.bar(
        x=admission_rate.index,
        y=admission_rate.values,
        title="Readmission by Admission Type",
        color=admission_rate.values,
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Hospital Tier

with col4:

    tier_rate = (
        filtered
        .groupby("hospital_tier")
        ["readmitted_30d"]
        .mean() * 100
    )

    fig = px.bar(
        x=tier_rate.index,
        y=tier_rate.values,
        title="Readmission by Hospital Tier",
        color=tier_rate.values,
        color_continuous_scale="Purples"
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------- COST ----------------

st.markdown("""
<div class="section">
<h2>💰 Cost Analysis</h2>
</div>
""", unsafe_allow_html=True)


avg_cost = filtered["total_cost_inr"].mean()

avg_oop = filtered["out_of_pocket_inr"].mean()


c1, c2 = st.columns(2)


with c1:

    st.markdown(f"""
    <div class="small-card">

    <div class="small-title">
    💰 Average Treatment Cost
    </div>

    <div class="small-value">
    ₹{avg_cost:,.2f}
    </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="small-card">

    <div class="small-title">
    💳 Average Out-of-Pocket Cost
    </div>

    <div class="small-value">
    ₹{avg_oop:,.2f}
    </div>

    </div>
    """, unsafe_allow_html=True)


cost = (
    filtered
    .groupby("insurance_type")
    [["total_cost_inr",
      "out_of_pocket_inr"]]
    .mean()
    .reset_index()
)


cost = cost.rename(
    columns={
        "total_cost_inr": "Treatment Cost",
        "out_of_pocket_inr": "Out-of-Pocket"
    }
)


cost_long = cost.melt(
    id_vars="insurance_type",
    var_name="Cost Type",
    value_name="Amount"
)


fig = px.bar(
    cost_long,
    x="insurance_type",
    y="Amount",
    color="Cost Type",
    barmode="group",
    title="Average Cost by Insurance Type"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------- CLINICAL ----------------

st.markdown("""
<div class="section">
<h2>🩺 Clinical Analysis</h2>
</div>
""", unsafe_allow_html=True)


clinical = {
    "HbA1c": filtered["hba1c"].mean(),
    "Creatinine": filtered["creatinine"].mean(),
    "Haemoglobin": filtered["haemoglobin"].mean(),
    "Systolic BP": filtered["systolic_bp"].mean()
}


cols = st.columns(4)


for col, (name, value) in zip(
    cols,
    clinical.items()
):

    with col:

        st.markdown(f"""
        <div class="small-card">

        <div class="small-title">
        🩺 {name}
        </div>

        <div class="small-value">
        {value:.2f}
        </div>

        </div>
        """, unsafe_allow_html=True)


clinical_df = pd.DataFrame({
    "Indicator": list(clinical.keys()),
    "Average Value": list(clinical.values())
})


fig = px.bar(
    clinical_df,
    x="Indicator",
    y="Average Value",
    color="Average Value",
    color_continuous_scale="Viridis",
    title="Clinical Indicator Comparison"
)


fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------- DOWNLOAD ----------------

st.markdown("""
<div class="section">

<h2>📥 Download Data</h2>

<p>
Download the filtered patient dataset for further analysis.
</p>

</div>
""", unsafe_allow_html=True)


st.download_button(
    "⬇️ Download Filtered Patient Data",
    filtered.to_csv(index=False),
    "filtered_patient_data.csv",
    use_container_width=True
)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">

Patient Health Record Dashboard
<br><br>

<b>
Better Data → Better Insights → Better Healthcare
</b>

</div>
""", unsafe_allow_html=True)
