import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
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

st.markdown(
    """
    <style>

    /* Main App */
    .stApp {
        background-color: #0b0f14;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11161d;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(
            135deg,
            #1c222b,
            #12171d
        );

        border: 1px solid #303640;
        border-radius: 15px;

        padding: 20px;

        text-align: center;

        box-shadow: 0px 5px 18px rgba(0, 0, 0, 0.30);

        min-height: 130px;
    }

    .kpi-icon {
        font-size: 25px;
    }

    .kpi-title {
        color: #a7adb7;
        font-size: 14px;
        margin-top: 5px;
    }

    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Section Titles */
    .section-title {
        color: white;
        font-size: 21px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* Information Box */
    .info-box {
        background-color: #151b23;
        border-left: 4px solid #e23744;

        padding: 15px;

        border-radius: 8px;

        color: #d7dbe0;

        margin-bottom: 20px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777f8a;
        padding: 25px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv("Zomato_Data.csv")

    except FileNotFoundError:

        st.error(
            "❌ Zomato_Data.csv file nahi mili. "
            "CSV file ko app.py ke same folder mein rakho."
        )

        st.stop()

    # -----------------------------------------------------
    # Clean column names
    # -----------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # -----------------------------------------------------
    # Check important columns
    # -----------------------------------------------------

    required_columns = [
        "name",
        "location",
        "rate",
        "votes",
        "approx_cost"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            "❌ CSV mein ye columns missing hain: "
            + ", ".join(missing_columns)
        )

        st.write("Available columns:", list(df.columns))

        st.stop()

    # -----------------------------------------------------
    # Clean Restaurant Name
    # -----------------------------------------------------

    df["name"] = (
        df["name"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # Clean Location
    # -----------------------------------------------------

    df["location"] = (
        df["location"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # Clean Cost
    # -----------------------------------------------------

    df["approx_cost"] = (
        df["approx_cost"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["approx_cost"] = pd.to_numeric(
        df["approx_cost"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Clean Votes
    # -----------------------------------------------------

    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["votes"] = df["votes"].fillna(0)

    # -----------------------------------------------------
    # Extract Numeric Rating
    # Example:
    # 4.1/5 -> 4.1
    # NEW   -> NaN
    # -     -> NaN
    # -----------------------------------------------------

    df["rating"] = (
        df["rate"]
        .astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
    )

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # Remove invalid records
    # -----------------------------------------------------

    df = df.dropna(
        subset=[
            "name",
            "location",
            "rating",
            "approx_cost"
        ]
    )

    # -----------------------------------------------------
    # Rating range validation
    # -----------------------------------------------------

    df = df[
        (df["rating"] >= 0) &
        (df["rating"] <= 5)
    ]

    # -----------------------------------------------------
    # Cost validation
    # -----------------------------------------------------

    df = df[
        df["approx_cost"] >= 0
    ]

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h2 style="color:#e23744;">
        🔎 Dashboard Filters
    </h2>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Location Filter
# ---------------------------------------------------------

locations = sorted(
    df["location"]
    .dropna()
    .unique()
    .tolist()
)

selected_location = st.sidebar.selectbox(
    "📍 Select Location",
    ["All Locations"] + locations
)


# ---------------------------------------------------------
# Rating Filter
# ---------------------------------------------------------

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# ---------------------------------------------------------
# Cost Filter
# ---------------------------------------------------------

max_dataset_cost = int(
    df["approx_cost"].max()
)

selected_max_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=max_dataset_cost,
    value=max_dataset_cost,
    step=100
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# Location filter

if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]


# Rating filter

filtered_df = filtered_df[
    filtered_df["rating"] >= min_rating
]


# Cost filter

filtered_df = filtered_df[
    filtered_df["approx_cost"] <= selected_max_cost
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        color:#e23744;
        font-size:42px;
        margin-bottom:0px;
    ">
        🍽️ Zomato Restaurant Analytics
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#9da4ae;
        font-size:16px;
        margin-top:5px;
    ">
        Restaurant Ratings • Pricing • Popularity • Customer Analysis
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Current filters ke according koi data available nahi hai. "
        "Please filters ko change karo."
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_restaurants = len(filtered_df)

average_rating = filtered_df["rating"].mean()

total_votes = filtered_df["votes"].sum()

average_cost = filtered_df["approx_cost"].mean()


# =========================================================
# KPI CARDS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                🏪
            </div>

            <div class="kpi-title">
                Total Restaurants
            </div>

            <div class="kpi-value">
                {total_restaurants:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                ⭐
            </div>

            <div class="kpi-title">
                Average Rating
            </div>

            <div class="kpi-value">
                {average_rating:.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                🗳️
            </div>

            <div class="kpi-title">
                Total Votes
            </div>

            <div class="kpi-value">
                {int(total_votes):,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">
                💰
            </div>

            <div class="kpi-title">
                Average Cost
            </div>

            <div class="kpi-value">
                ₹{average_cost:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# FILTER SUMMARY
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📊 Analysis Overview
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="info-box">

        <b>📍 Location:</b>
        {selected_location}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        <b>⭐ Minimum Rating:</b>
        {min_rating}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        <b>💰 Maximum Cost:</b>
        ₹{selected_max_cost:,}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        <b>🏪 Records:</b>
        {len(filtered_df):,}

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHART 1 + CHART 2
# =========================================================

chart1, chart2 = st.columns(2)


# =========================================================
# AVERAGE COST BY LOCATION
# =========================================================

with chart1:

    st.markdown(
        """
        <div class="section-title">
            📍 Average Cost by Location
        </div>
        """,
        unsafe_allow_html=True
    )

    location_cost = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_location = px.bar(
        location_cost,
        x="approx_cost",
        y="location",
        orientation="h",
        color="approx_cost",
        color_continuous_scale="Reds",
        template="plotly_dark",
        labels={
            "approx_cost": "Average Cost (₹)",
            "location": "Location"
        }
    )

    fig_location.update_layout(
        height=450,
        showlegend=False,
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_location,
        use_container_width=True
    )


# =========================================================
# RATING DISTRIBUTION
# =========================================================

with chart2:

    st.markdown(
        """
        <div class="section-title">
            ⭐ Rating Distribution
        </div>
        """,
        unsafe_allow_html=True
    )

    fig_rating = px.histogram(
        filtered_df,
        x="rating",
        nbins=15,
        color_discrete_sequence=["#e23744"],
        template="plotly_dark",
        labels={
            "rating": "Rating"
        }
    )

    fig_rating.update_layout(
        height=450,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


# =========================================================
# CHART 3 + CHART 4
# =========================================================

chart3, chart4 = st.columns(2)


# =========================================================
# MOST POPULAR RESTAURANTS
# =========================================================

with chart3:

    st.markdown(
        """
        <div class="section-title">
            🔥 Most Popular Restaurants
        </div>
        """,
        unsafe_allow_html=True
    )

    popular_restaurants = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_votes = px.bar(
        popular_restaurants,
        x="votes",
        y="name",
        orientation="h",
        color="votes",
        color_continuous_scale="Oranges",
        template="plotly_dark",
        labels={
            "votes": "Total Votes",
            "name": "Restaurant"
        }
    )

    fig_votes.update_layout(
        height=450,
        showlegend=False,
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_votes,
        use_container_width=True
    )


# =========================================================
# COST VS RATING
# =========================================================

with chart4:

    st.markdown(
        """
        <div class="section-title">
            💰 Cost vs Rating
        </div>
        """,
        unsafe_allow_html=True
    )

    scatter_data = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()

    fig_scatter = px.scatter(
        scatter_data,
        x="approx_cost",
        y="rating",
        size="votes",
        color="rating",
        hover_name="name",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        labels={
            "approx_cost": "Approx Cost (₹)",
            "rating": "Rating",
            "votes": "Votes"
        }
    )

    fig_scatter.update_layout(
        height=450,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# =========================================================
# TOP RATED RESTAURANTS
# =========================================================

st.markdown(
    """
    <div class="section-title">
        🏆 Top Rated Restaurants
    </div>
    """,
    unsafe_allow_html=True
)

top_rated = (
    filtered_df[
        [
            "name",
            "location",
            "rating",
            "votes",
            "approx_cost"
        ]
    ]
    .sort_values(
        by=["rating", "votes"],
        ascending=[False, False]
    )
    .head(15)
    .copy()
)


# Rename columns for display

top_rated = top_rated.rename(
    columns={
        "name": "Restaurant",
        "location": "Location",
        "rating": "Rating",
        "votes": "Votes",
        "approx_cost": "Approx Cost (₹)"
    }
)


st.dataframe(
    top_rated,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DATASET SUMMARY
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="section-title">
        📁 Dataset Summary
    </div>
    """,
    unsafe_allow_html=True
)

summary1, summary2, summary3, summary4 = st.columns(4)


with summary1:

    st.metric(
        "Dataset Rows",
        f"{len(df):,}"
    )


with summary2:

    st.metric(
        "Unique Restaurants",
        f"{df['name'].nunique():,}"
    )


with summary3:

    st.metric(
        "Unique Locations",
        f"{df['location'].nunique():,}"
    )


with summary4:

    st.metric(
        "Average Dataset Rating",
        f"{df['rating'].mean():.2f}"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🍽️ <b>Zomato Restaurant Analytics Dashboard</b>

        <br><br>

        Built with
        <b>Python</b> •
        <b>Pandas</b> •
        <b>Plotly</b> •
        <b>Streamlit</b>

        <br><br>

        Made with ❤️ by Atharv

    </div>
    """,
    unsafe_allow_html=True
)
