import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Zomato Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0b0f14;
        color: #ffffff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #11161d;
        border-right: 1px solid #2a3038;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #171d25, #10151b);
        border: 1px solid #292f38;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
    }

    .kpi-title {
        color: #a7adb7;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }

    .kpi-icon {
        font-size: 25px;
    }

    /* Section title */
    .section-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Info box */
    .info-box {
        background: #151b23;
        border-left: 4px solid #e23744;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777f8a;
        padding: 20px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD & CLEAN DATA
# =========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("Zomato_Data.csv")

    # Remove commas from cost
    df["approx_cost"] = (
        df["approx_cost"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["approx_cost"] = pd.to_numeric(
        df["approx_cost"],
        errors="coerce"
    )

    # Extract numeric rating
    df["rating"] = (
        df
