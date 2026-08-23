import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Zomato Restaurant Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================= GLOBAL ================= */

.stApp {
    background: #0b0f14;
    color: white;
}

.block-container {
    max-width: 100% !important;
    padding-top: 0.5rem !important;
    padding-bottom: 0.3rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #151a21 !important;
    border-right: 1px solid #303640;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

section[data-testid="stSidebar"] h2 {
    color: #e23744 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
    margin-bottom: 4px !important;
}

section[data-testid="stSidebar"] p {
    color: #aab3bf !important;
    font-size: 13px !important;
}

section[data-testid="stSidebar"] label {
    color: #f5f5f5 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="select"] > div {
    background: #0c1016 !important;
    border: 1px solid #343b46 !important;
    border-radius: 8px !important;
    min-height: 40px !important;
}


/* ================= HEADER ================= */

.zomato-header {
    text-align: center;
    padding: 2px 0 3px 0;
}

.zomato-title {
    color: #e23744;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1px;
    margin: 0;
}

.zomato-subtitle {
    color: #9da7b4;
    font-size: 12px;
    margin-top: 5px;
}


/* ================= DIVIDER ================= */

hr {
    border-color: #303640 !important;
    margin: 6px 0 !important;
}


/* ================= SECTION ================= */

.section-title {
    color: white;
    font-size: 17px;
    font-weight: 800;
    margin: 4px 0 5px 0;
}


/* ================= KPI ================= */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1c222b,
        #151a21
    );

    border: 1px solid #353d49;
    border-radius: 11px;

    padding: 8px 12px !important;

    min-height: 70px !important;

    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #aeb7c3 !important;
    font-size: 11px !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 23px !important;
    font-weight: 800 !important;
}


/* ================= CHARTS ================= */

div[data-testid="stPlotlyChart"] {
    background: #11161d;
    border: 1px solid #303844;
    border-radius: 10px;
    padding: 0 !important;
    margin: 0 !important;
}


/* ================= COLUMNS ================= */

div[data-testid="column"] {
    padding-left: 4px !important;
    padding-right: 4px !important;
}


/* ================= FILTER INFO ================= */

.filter-info {
    text-align: center;
    color: #7f8997;
    font-size: 10px;
    margin: 3px 0;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #697381;
    font-size: 9px;
    margin-top: 3px;
}


/* ================= HIDE STREAMLIT FOOTER ================= */

footer {
    visibility: hidden;
}


/* =====================================================
   PRINT / SCREENSHOT FIX
   ===================================================== */

@media print {

    @page {
        size: landscape;
        margin: 0;
    }

    html,
    body {
        width: 100%;
        height: 100%;
        overflow: hidden !important;
    }

    .stApp {
        width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }

    section[data-testid="stSidebar"] {
        display: block !important;
    }

    .block-container {
        padding: 5px !important;
        margin: 0 !important;
    }

    div[data-testid="stPlotlyChart"] {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }

    [data-testid="stMetric"] {
        break-inside: avoid !important;
        page-break-inside: avoid !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Zomato_Data.csv")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # Required columns
    required_columns = [
        "name",
        "location",
        "rate",
        "votes",
        "approx_cost"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(
            f"Required columns missing: {missing}"
        )
        st.stop()

    # Restaurant name
    df["name"] = (
        df["name"]
        .astype(str)
        .str.strip()
    )

    # Location
    df["location"] = (
        df["location"]
        .astype(str)
        .str.strip()
    )

    # Cost cleaning
    df["approx_cost"] = (
        df["approx_cost"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip()
    )

    df["approx_cost"] = pd.to_numeric(
        df["approx_cost"],
        errors="coerce"
    )

    # Votes
    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    ).fillna(0)

    # Rating
    df["rating"] = (
        df["rate"]
        .astype(str)
        .str.extract(
            r"(\d+(?:\.\d+)?)",
            expand=False
        )
    )

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "name",
            "location",
            "rating",
            "approx_cost"
        ]
    )

    df = df[
        (df["rating"] >= 0) &
        (df["rating"] <= 5)
    ]

    df = df[
        df["approx_cost"] >= 0
    ]

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## 🔎 Dashboard Filters"
)

st.sidebar.caption(
    "Use filters to explore restaurant data."
)

st.sidebar.divider()


# Location
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


# Minimum rating
min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# Maximum cost
max_cost = int(
    df["approx_cost"].max()
)

selected_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=max_cost,
    value=max_cost,
    step=100
)


# Online order
if "online_order" in df.columns:

    online_options = sorted(
        df["online_order"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_online = st.sidebar.selectbox(
        "🛵 Online Order",
        ["All"] + online_options
    )

else:
    selected_online = "All"


# Table booking
if "book_table" in df.columns:

    booking_options = sorted(
        df["book_table"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_booking = st.sidebar.selectbox(
        "🍽️ Table Booking",
        ["All"] + booking_options
    )

else:
    selected_booking = "All"


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]


filtered_df = filtered_df[
    filtered_df["rating"] >= min_rating
]


filtered_df = filtered_df[
    filtered_df["approx_cost"] <= selected_cost
]


if (
    "online_order" in filtered_df.columns
    and selected_online != "All"
):

    filtered_df = filtered_df[
        filtered_df["online_order"]
        .astype(str)
        == selected_online
    ]


if (
    "book_table" in filtered_df.columns
    and selected_booking != "All"
):

    filtered_df = filtered_df[
        filtered_df["book_table"]
        .astype(str)
        == selected_booking
    ]


# =========================================================
# EMPTY DATA
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Selected filters ke according data available nahi hai."
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="zomato-header">

        <div class="zomato-title">
            🍽️ ZOMATO RESTAURANT ANALYTICS
        </div>

        <div class="zomato-subtitle">
            Restaurant Ratings • Pricing • Popularity • Customer Analysis
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_restaurants = len(filtered_df)

average_rating = filtered_df["rating"].mean()

total_votes = filtered_df["votes"].sum()

average_cost = filtered_df["approx_cost"].mean()


# =========================================================
# KPI TITLE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📊 Key Performance Indicators
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4 = st.columns(4)


with k1:
    st.metric(
        "🏪 Total Restaurants",
        f"{total_restaurants:,}"
    )


with k2:
    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}"
    )


with k3:
    st.metric(
        "🗳️ Total Votes",
        f"{int(total_votes):,}"
    )


with k4:
    st.metric(
        "💰 Average Cost",
        f"₹{average_cost:,.0f}"
    )


# =========================================================
# FILTER SUMMARY
# =========================================================

st.markdown(
    f"""
    <div class="filter-info">

        📍 {selected_location}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        ⭐ Rating ≥ {min_rating:.1f}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        💰 Cost ≤ ₹{selected_cost:,}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        📊 {len(filtered_df):,} Records

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHART TITLE
# =========================================================

st.markdown(
    """
    <div class="section-title">
        📈 Restaurant Performance Analysis
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHART ROW 1
# =========================================================

chart1, chart2 = st.columns(2)


# =========================================================
# CHART 1 - LOCATION COST
# =========================================================

with chart1:

    location_cost = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )

    fig1 = px.bar(
        location_cost,
        x="approx_cost",
        y="location",
        orientation="h",
        color="approx_cost",
        color_continuous_scale=[
            "#8b1e25",
            "#e23744",
            "#ff6b6b"
        ],
        template="plotly_dark",
        labels={
            "approx_cost": "Average Cost",
            "location": ""
        }
    )

    fig1.update_layout(
        title={
            "text": "💰 Average Cost by Location",
            "font": {
                "size": 12
            }
        },
        height=155,
        margin=dict(
            l=5,
            r=5,
            t=32,
            b=5
        ),
        coloraxis_showscale=False,
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=8)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# CHART 2 - RATING
# =========================================================

with chart2:

    fig2 = px.histogram(
        filtered_df,
        x="rating",
        nbins=10,
        color_discrete_sequence=["#e23744"],
        template="plotly_dark"
    )

    fig2.update_layout(
        title={
            "text": "⭐ Rating Distribution",
            "font": {
                "size": 12
            }
        },
        height=155,
        margin=dict(
            l=5,
            r=5,
            t=32,
            b=5
        ),
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=8),
        bargap=0.08
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# CHART ROW 2
# =========================================================

chart3, chart4 = st.columns(2)


# =========================================================
# CHART 3 - POPULAR RESTAURANTS
# =========================================================

with chart3:

    popular = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )

    fig3 = px.bar(
        popular,
        x="votes",
        y="name",
        orientation="h",
        color="votes",
        color_continuous_scale=[
            "#7c2d12",
            "#ea580c",
            "#fb923c"
        ],
        template="plotly_dark",
        labels={
            "votes": "Votes",
            "name": ""
        }
    )

    fig3.update_layout(
        title={
            "text": "🔥 Most Popular Restaurants",
            "font": {
                "size": 12
            }
        },
        height=155,
        margin=dict(
            l=5,
            r=5,
            t=32,
            b=5
        ),
        coloraxis_showscale=False,
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=8)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# CHART 4 - COST VS RATING
# =========================================================

with chart4:

    scatter_data = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()

    if len(scatter_data) > 700:

        scatter_data = scatter_data.sample(
            700,
            random_state=42
        )

    fig4 = px.scatter(
        scatter_data,
        x="approx_cost",
        y="rating",
        size="votes",
        color="rating",
        hover_name="name",
        color_continuous_scale=[
            "#ef4444",
            "#facc15",
            "#22c55e"
        ],
        template="plotly_dark",
        labels={
            "approx_cost": "Cost ₹",
            "rating": "Rating"
        }
    )

    fig4.update_layout(
        title={
            "text": "🎯 Cost vs Rating",
            "font": {
                "size": 12
            }
        },
        height=155,
        margin=dict(
            l=5,
            r=5,
            t=32,
            b=5
        ),
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=8)
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# FINAL FOOTER
# =========================================================

st.markdown(
    f"""
    <div class="footer">

        🍽️ Zomato Restaurant Analytics
        &nbsp; • &nbsp;
        Dataset: {len(df):,} rows
        &nbsp; • &nbsp;
        Filtered: {len(filtered_df):,} rows
        &nbsp; • &nbsp;
        Locations: {df["location"].nunique()}

    </div>
    """,
    unsafe_allow_html=True
)
