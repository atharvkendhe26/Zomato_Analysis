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
# CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background: #0b0f14;
}

.block-container {
    max-width: 100%;
    padding-top: 0.25rem !important;
    padding-bottom: 0rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background: #151a21 !important;
    border-right: 1px solid #303640;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem !important;
    padding-left: 0.9rem !important;
    padding-right: 0.9rem !important;
}


/* Sidebar heading */

section[data-testid="stSidebar"] h2 {
    color: #e23744 !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    margin-bottom: 3px !important;
}


/* Sidebar text */

section[data-testid="stSidebar"] p {
    color: #9da7b4 !important;
    font-size: 12px !important;
}


/* Sidebar labels */

section[data-testid="stSidebar"] label {
    color: #f1f3f5 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}


/* Select box */

section[data-testid="stSidebar"]
div[data-baseweb="select"] > div {

    background-color: #0c1016 !important;

    border: 1px solid #353c47 !important;

    border-radius: 8px !important;

    min-height: 38px !important;
}


/* Sliders */

section[data-testid="stSidebar"] .stSlider {
    padding-top: 0 !important;
    padding-bottom: 4px !important;
}


/* =====================================================
   ZOMATO HEADER
   ===================================================== */

.zomato-title {

    text-align: center;

    color: #e23744;

    font-size: 34px;

    line-height: 1;

    font-weight: 900;

    letter-spacing: -0.8px;

    margin: 0 !important;

    padding: 0 !important;
}


.zomato-subtitle {

    text-align: center;

    color: #9da7b4;

    font-size: 11px;

    margin-top: 4px;

    margin-bottom: 5px;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {

    border-color: #303640 !important;

    margin-top: 4px !important;

    margin-bottom: 5px !important;
}


/* =====================================================
   SECTION TITLE
   ===================================================== */

.section-title {

    color: #ffffff;

    font-size: 16px;

    font-weight: 800;

    margin-top: 3px;

    margin-bottom: 4px;
}


/* =====================================================
   KPI CARDS
   ===================================================== */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            135deg,
            #1c222b,
            #151a21
        );

    border: 1px solid #343c47;

    border-radius: 10px;

    padding: 7px 12px !important;

    min-height: 61px !important;

    height: 61px !important;

    box-shadow:
        0 3px 8px rgba(0,0,0,0.25);
}


/* KPI label */

[data-testid="stMetricLabel"] {

    color: #aeb7c3 !important;

    font-size: 10px !important;

    line-height: 1 !important;
}


/* KPI value */

[data-testid="stMetricValue"] {

    color: #ffffff !important;

    font-size: 21px !important;

    font-weight: 800 !important;

    line-height: 1.1 !important;
}


/* =====================================================
   PLOTLY CHART
   ===================================================== */

div[data-testid="stPlotlyChart"] {

    background: #11161d;

    border: 1px solid #2c343f;

    border-radius: 9px;

    padding: 0 !important;

    margin: 0 !important;

}


/* =====================================================
   COLUMNS
   ===================================================== */

div[data-testid="column"] {

    padding-left: 3px !important;

    padding-right: 3px !important;

}


/* =====================================================
   FILTER SUMMARY
   ===================================================== */

.filter-summary {

    text-align: center;

    color: #7f8997;

    font-size: 9px;

    margin-top: 2px;

    margin-bottom: 2px;
}


/* =====================================================
   FOOTER
   ===================================================== */

footer {
    visibility: hidden;
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

    # Check columns
    required = [
        "name",
        "location",
        "rate",
        "votes",
        "approx_cost"
    ]

    missing = [
        c for c in required
        if c not in df.columns
    ]

    if missing:
        st.error(
            f"Missing columns: {missing}"
        )
        st.stop()

    # Name
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

    # Cost
    df["approx_cost"] = (
        df["approx_cost"]
        .astype(str)
        .str.replace(",", "", regex=False)
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
# SIDEBAR FILTERS
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
    .unique()
    .tolist()
)

selected_location = st.sidebar.selectbox(
    "📍 Select Location",
    ["All Locations"] + locations
)


# Rating

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    1.0,
    5.0,
    3.0,
    0.1
)


# Cost

maximum_cost = int(
    df["approx_cost"].max()
)

selected_max_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    0,
    maximum_cost,
    maximum_cost,
    100
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
        filtered_df["location"]
        == selected_location
    ]


filtered_df = filtered_df[
    filtered_df["rating"] >= min_rating
]


filtered_df = filtered_df[
    filtered_df["approx_cost"]
    <= selected_max_cost
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
        "⚠️ No restaurants found for selected filters."
    )

    st.stop()


# =========================================================
# ZOMATO HEADER
# =========================================================

st.markdown(
    """
    <div class="zomato-title">
        🍽️ ZOMATO RESTAURANT ANALYTICS
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="zomato-subtitle">
        Restaurant Ratings • Pricing • Popularity • Customer Analysis
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KPI
# =========================================================

total_restaurants = len(
    filtered_df
)

average_rating = (
    filtered_df["rating"].mean()
)

total_votes = (
    filtered_df["votes"].sum()
)

average_cost = (
    filtered_df["approx_cost"].mean()
)


st.markdown(
    """
    <div class="section-title">
        📊 Key Performance Indicators
    </div>
    """,
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(
    4,
    gap="small"
)


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
# SUMMARY
# =========================================================

st.markdown(
    f"""
    <div class="filter-summary">
        📍 {selected_location}
        &nbsp; • &nbsp;
        ⭐ Rating ≥ {min_rating:.1f}
        &nbsp; • &nbsp;
        💰 Cost ≤ ₹{selected_max_cost:,}
        &nbsp; • &nbsp;
        📊 {len(filtered_df):,} Records
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ANALYSIS TITLE
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
# CHART 1 + CHART 2
# =========================================================

c1, c2 = st.columns(
    2,
    gap="small"
)


# =========================================================
# CHART 1
# =========================================================

with c1:

    location_cost = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(
            ascending=False
        )
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
            "approx_cost": "Cost ₹",
            "location": ""
        }
    )

    fig1.update_layout(
        title={
            "text": "💰 Top Locations by Cost",
            "font": {
                "size": 12,
                "color": "white"
            }
        },
        height=145,
        margin=dict(
            l=5,
            r=5,
            t=30,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=8
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# CHART 2
# =========================================================

with c2:

    fig2 = px.histogram(
        filtered_df,
        x="rating",
        nbins=10,
        color_discrete_sequence=[
            "#e23744"
        ],
        template="plotly_dark"
    )

    fig2.update_layout(
        title={
            "text": "⭐ Rating Distribution",
            "font": {
                "size": 12,
                "color": "white"
            }
        },
        height=145,
        margin=dict(
            l=5,
            r=5,
            t=30,
            b=5
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=8
        ),
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
# CHART 3 + CHART 4
# =========================================================

c3, c4 = st.columns(
    2,
    gap="small"
)


# =========================================================
# CHART 3
# =========================================================

with c3:

    popular = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(
            ascending=False
        )
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
                "size": 12,
                "color": "white"
            }
        },
        height=145,
        margin=dict(
            l=5,
            r=5,
            t=30,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=8
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# CHART 4
# =========================================================

with c4:

    scatter_df = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()


    # Limit points

    if len(scatter_df) > 900:

        scatter_df = scatter_df.sample(
            900,
            random_state=42
        )


    fig4 = px.scatter(
        scatter_df,
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
            "text": "💰 Cost vs Rating",
            "font": {
                "size": 12,
                "color": "white"
            }
        },
        height=145,
        margin=dict(
            l=5,
            r=5,
            t=30,
            b=5
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=8
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# BOTTOM LINE
# =========================================================

st.markdown(
    f"""
    <div class="filter-summary">
        🍽️ Zomato Restaurant Analytics
        &nbsp; | &nbsp;
        Dataset: {len(df):,} rows
        &nbsp; | &nbsp;
        Showing: {len(filtered_df):,}
        &nbsp; | &nbsp;
        Locations: {df["location"].nunique()}
    </div>
    """,
    unsafe_allow_html=True
)
