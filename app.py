# import streamlit as st
# import pandas as pd
# import plotly.express as px

# from src.data_generator import generate_claims
# from src.fraud_detection import apply_all_models

# # -------------------------------------------------------
# # Page Configuration
# # -------------------------------------------------------

# st.set_page_config(
#     page_title="Healthcare Fraud Detection",
#     page_icon="🏥",
#     layout="wide"
# )

# st.title("🏥 Healthcare Insurance Claim Fraud Detection")
# st.markdown(
#     "### AI-Powered Fraud Analytics Dashboard"
# )

# # -------------------------------------------------------
# # Load Data
# # -------------------------------------------------------

# @st.cache_data
# def load_data():
#     df = generate_claims(10000)
#     df, provider = apply_all_models(df)
#     return df, provider

# df, provider = load_data()

# # -------------------------------------------------------
# # KPI Calculations
# # -------------------------------------------------------

# total_claims = len(df)

# fraud_claims = int(df["iforest_anomaly"].sum())

# fraud_rate = (
#     fraud_claims / total_claims
# ) * 100

# provider_count = df["provider_name"].nunique()

# total_billed = df["billed_amount"].sum()

# total_paid = df["paid_amount"].sum()

# # -------------------------------------------------------
# # KPI Cards
# # -------------------------------------------------------

# col1, col2, col3, col4 = st.columns(4)

# col1.metric(
#     "Total Claims",
#     f"{total_claims:,}"
# )

# col2.metric(
#     "Fraud Detected",
#     fraud_claims
# )

# col3.metric(
#     "Fraud %",
#     f"{fraud_rate:.2f}%"
# )

# col4.metric(
#     "Providers",
#     provider_count)

# st.divider()

# col5, col6 = st.columns(2)

# col5.metric(
#     "Total Billed",
#     f"₹ {total_billed:,.0f}"
# )

# col6.metric(
#     "Total Paid",
#     f"₹ {total_paid:,.0f}"
# )

# st.divider()

# st.subheader("Claims Preview")

# st.dataframe(df.head(20), use_container_width=True)

# # -------------------------------------------------------
# # Fraud by Provider
# # -------------------------------------------------------

# st.divider()

# st.subheader("🏥 Fraud Detected by Provider")

# provider_chart = (
#     df.groupby("provider_name")["iforest_anomaly"]
#       .sum()
#       .reset_index()
#       .sort_values("iforest_anomaly", ascending=False)
# )

# fig = px.bar(
#     provider_chart,
#     x="provider_name",
#     y="iforest_anomaly",
#     color="iforest_anomaly",
#     title="Fraud Detected by Provider",
#     labels={
#         "provider_name": "Provider",
#         "iforest_anomaly": "Fraud Cases"
#     }
# )

# st.plotly_chart(fig, use_container_width=True)
# # -------------------------------------------------------
# # Dashboard Charts
# # -------------------------------------------------------

# st.divider()

# col1, col2 = st.columns(2)

# # -----------------------------------
# # Fraud by Provider
# # -----------------------------------
# with col1:

#     st.subheader("🏥 Fraud Detected by Provider")

#     provider_chart = (
#         df.groupby("provider_name")["iforest_anomaly"]
#           .sum()
#           .reset_index()
#           .sort_values("iforest_anomaly", ascending=False)
#     )

#     fig1 = px.bar(
#         provider_chart,
#         x="provider_name",
#         y="iforest_anomaly",
#         color="iforest_anomaly",
#         title="Fraud Cases by Provider",
#         labels={
#             "provider_name": "Provider",
#             "iforest_anomaly": "Fraud Cases"
#         }
#     )

#     st.plotly_chart(fig1, use_container_width=True)

# # -----------------------------------
# # Claim Type Distribution
# # -----------------------------------
# with col2:

#     st.subheader("📋 Claim Type Distribution")

#     claim_chart = (
#         df["claim_type"]
#         .value_counts()
#         .reset_index()
#     )

#     claim_chart.columns = ["Claim Type", "Count"]

#     fig2 = px.pie(
#         claim_chart,
#         names="Claim Type",
#         values="Count",
#         title="Claim Type Distribution"
#     )

#     st.plotly_chart(fig2, use_container_width=True)
# # import streamlit as st
# from services.llm import ask_llm
# response = ask_llm(
#     "Explain health insurance fraud in simple terms."
# )

# print(response)
# # st.set_page_config(page_title="Test")

# # st.title("✅ Streamlit is Working!")

# # st.write("If you can see this page, Streamlit is working correctly.")


import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_generator import generate_claims
from src.fraud_detection import apply_all_models
from services.llm import ask_llm

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Healthcare Fraud Detection",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Insurance Claim Fraud Detection")
st.markdown("### AI-Powered Fraud Analytics Dashboard")

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

@st.cache_data
def load_data():
    df = generate_claims(10000)
    df, provider = apply_all_models(df)
    return df, provider


df, provider = load_data()

# -------------------------------------------------------
# KPI Calculations
# -------------------------------------------------------

total_claims = len(df)

fraud_claims = int(df["iforest_anomaly"].sum())

fraud_rate = (fraud_claims / total_claims) * 100

provider_count = df["provider_name"].nunique()

total_billed = df["billed_amount"].sum()

total_paid = df["paid_amount"].sum()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Claims", f"{total_claims:,}")

col2.metric("Fraud Detected", fraud_claims)

col3.metric("Fraud %", f"{fraud_rate:.2f}%")

col4.metric("Providers", provider_count)

st.divider()

col5, col6 = st.columns(2)

col5.metric("Total Billed", f"₹ {total_billed:,.0f}")

col6.metric("Total Paid", f"₹ {total_paid:,.0f}")

st.divider()

# -------------------------------------------------------
# Claims Preview
# -------------------------------------------------------

st.subheader("Claims Preview")

st.dataframe(df.head(20), use_container_width=True)

# -------------------------------------------------------
# Charts
# -------------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

# Fraud by Provider

with col1:

    st.subheader("🏥 Fraud Detected by Provider")

    provider_chart = (
        df.groupby("provider_name")["iforest_anomaly"]
        .sum()
        .reset_index()
        .sort_values("iforest_anomaly", ascending=False)
    )

    fig1 = px.bar(
        provider_chart,
        x="provider_name",
        y="iforest_anomaly",
        color="iforest_anomaly",
        title="Fraud Cases by Provider"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Claim Type Distribution

with col2:

    st.subheader("📋 Claim Type Distribution")

    claim_chart = (
        df["claim_type"]
        .value_counts()
        .reset_index()
    )

    claim_chart.columns = ["Claim Type", "Count"]

    fig2 = px.pie(
        claim_chart,
        names="Claim Type",
        values="Count",
        title="Claim Type Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------
# AI Fraud Analysis
# -------------------------------------------------------

st.divider()

st.header("🤖 AI Fraud Analysis")

st.write(
    "Click the button below to let the AI analyze the current fraud statistics."
)

if st.button("Generate AI Analysis"):

    with st.spinner("Analyzing claims using AI..."):

        prompt = f"""
You are an expert Healthcare Insurance Fraud Investigator.

Analyze the following healthcare claim statistics.

Total Claims: {total_claims}

Fraud Claims Detected: {fraud_claims}

Fraud Percentage: {fraud_rate:.2f}%

Total Providers: {provider_count}

Total Billed Amount: ₹{total_billed:,.2f}

Total Paid Amount: ₹{total_paid:,.2f}

Provide your response in the following format:

1. Executive Summary

2. Key Fraud Risks

3. Possible Fraud Patterns

4. Financial Observations

5. Recommendations

Keep the response professional and suitable for senior management.
"""

        response = ask_llm(prompt)

    st.success("Analysis Complete!")

    st.markdown(response)