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

/* ---------- MAIN ---------- */

.stApp {
    background-color: #0b0f14;
    color: white;
}

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background-color: #151a21 !important;
    border-right: 1px solid #303640;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

section[data-testid="stSidebar"] h2 {
    color: #e23744 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
    margin-bottom: 3px !important;
}

section[data-testid="stSidebar"] p {
    color: #aeb7c3 !important;
    font-size: 12px !important;
}

section[data-testid="stSidebar"] label {
    color: white !important;
    font-size: 13px !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"]
div[data-baseweb="select"] > div {
    background-color: #0c1016 !important;
    border: 1px solid #353c47 !important;
    border-radius: 8px !important;
}


/* ---------- TITLE ---------- */

.dashboard-title {
    text-align: center;
    color: #e23744;
    font-size: 36px;
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
    padding: 0;
}

.dashboard-subtitle {
    text-align: center;
    color: #9da7b4;
    font-size: 12px;
    margin-top: 4px;
    margin-bottom: 5px;
}


/* ---------- SECTION HEADINGS ---------- */

.section-heading {
    color: white;
    font-size: 16px;
    font-weight: 800;
    margin-top: 3px;
    margin-bottom: 5px;
}


/* ---------- KPI CARDS ---------- */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1d242e,
        #151a21
    );

    border: 1px solid #353d49;
    border-radius: 11px;

    padding: 8px 12px !important;

    min-height: 65px !important;

    box-shadow: 0 3px 10px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #aeb7c3 !important;
    font-size: 11px !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 22px !important;
    font-weight: 800 !important;
}


/* ---------- CHART ---------- */

div[data-testid="stPlotlyChart"] {
    background-color: #11161d;
    border: 1px solid #303844;
    border-radius: 10px;
    padding: 0 !important;
    margin: 0 !important;
}


/* ---------- COLUMNS ---------- */

div[data-testid="column"] {
    padding-left: 3px !important;
    padding-right: 3px !important;
}


/* ---------- SMALL INFO ---------- */

.small-info {
    text-align: center;
    color: #7f8997;
    font-size: 10px;
    margin-top: 2px;
    margin-bottom: 3px;
}


/* ---------- HIDE FOOTER ---------- */

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

    # Required columns
    required_columns = [
        "name",
        "location",
        "rate",
        "votes",
        "approx_cost"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            f"❌ These columns are missing: {missing_columns}"
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

    # Cost
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

    # Valid rating
    df = df[
        (df["rating"] >= 0) &
        (df["rating"] <= 5)
    ]

    # Valid cost
    df = df[
        df["approx_cost"] >= 0
    ]

    return df


# =========================================================
# DATA
# =========================================================

df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🔎 Dashboard Filters")

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
    "📍 Location",
    ["All Locations"] + locations
)


# Minimum rating
minimum_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# Maximum cost
maximum_cost = int(
    df["approx_cost"].max()
)

selected_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=maximum_cost,
    value=maximum_cost,
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
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


# Location filter
if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]


# Rating filter
filtered_df = filtered_df[
    filtered_df["rating"] >= minimum_rating
]


# Cost filter
filtered_df = filtered_df[
    filtered_df["approx_cost"] <= selected_cost
]


# Online order filter
if (
    "online_order" in filtered_df.columns
    and selected_online != "All"
):

    filtered_df = filtered_df[
        filtered_df["online_order"]
        .astype(str)
        == selected_online
    ]


# Table booking filter
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
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Selected filters ke according koi data nahi mila."
    )

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">'
    '🍽️ ZOMATO RESTAURANT ANALYTICS'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Restaurant Ratings • Pricing • Popularity • Customer Analysis'
    '</div>',
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
# KPI HEADING
# =========================================================

st.markdown(
    '<div class="section-heading">'
    '📊 Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI ROW
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "🏪 Total Restaurants",
        f"{total_restaurants:,}"
    )


with kpi2:

    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}"
    )


with kpi3:

    st.metric(
        "🗳️ Total Votes",
        f"{int(total_votes):,}"
    )


with kpi4:

    st.metric(
        "💰 Average Cost",
        f"₹{average_cost:,.0f}"
    )


# =========================================================
# FILTER SUMMARY
# =========================================================

st.markdown(
    f'<div class="small-info">'
    f'📍 {selected_location}'
    f' &nbsp; | &nbsp; '
    f'⭐ Rating ≥ {minimum_rating:.1f}'
    f' &nbsp; | &nbsp; '
    f'💰 Cost ≤ ₹{selected_cost:,}'
    f' &nbsp; | &nbsp; '
    f'📊 {len(filtered_df):,} Records'
    f'</div>',
    unsafe_allow_html=True
)


# =========================================================
# GRAPH HEADING
# =========================================================

st.markdown(
    '<div class="section-heading">'
    '📈 Restaurant Performance Analysis'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GRAPH 1 + GRAPH 2
# =========================================================

graph1, graph2 = st.columns(2)


# =========================================================
# GRAPH 1
# =========================================================

with graph1:

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
            "#7f1d1d",
            "#e23744",
            "#ff6b6b"
        ],
        template="plotly_dark",
        labels={
            "approx_cost": "Average Cost ₹",
            "location": ""
        }
    )

    fig1.update_layout(
        title={
            "text": "💰 Average Cost by Location",
            "font": {
                "size": 13,
                "color": "white"
            }
        },
        height=180,
        margin=dict(
            l=5,
            r=5,
            t=35,
            b=5
        ),
        coloraxis_showscale=False,
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=9)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# GRAPH 2
# =========================================================

with graph2:

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
                "size": 13,
                "color": "white"
            }
        },
        height=180,
        margin=dict(
            l=5,
            r=5,
            t=35,
            b=5
        ),
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=9),
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
# GRAPH 3 + GRAPH 4
# =========================================================

graph3, graph4 = st.columns(2)


# =========================================================
# GRAPH 3
# =========================================================

with graph3:

    popular_restaurants = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )

    fig3 = px.bar(
        popular_restaurants,
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
                "size": 13,
                "color": "white"
            }
        },
        height=180,
        margin=dict(
            l=5,
            r=5,
            t=35,
            b=5
        ),
        coloraxis_showscale=False,
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=9)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# GRAPH 4
# =========================================================

with graph4:

    scatter_data = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()

    # Keep dashboard fast
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
                "size": 13,
                "color": "white"
            }
        },
        height=180,
        margin=dict(
            l=5,
            r=5,
            t=35,
            b=5
        ),
        paper_bgcolor="#11161d",
        plot_bgcolor="#11161d",
        font=dict(size=9)
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# FINAL SMALL INFO
# =========================================================

st.markdown(
    f'<div class="small-info">'
    f'🍽️ Zomato Restaurant Analytics'
    f' &nbsp; • &nbsp; '
    f'Dataset: {len(df):,} rows'
    f' &nbsp; • &nbsp; '
    f'Filtered: {len(filtered_df):,} rows'
    f' &nbsp; • &nbsp; '
    f'Locations: {df["location"].nunique()}'
    f'</div>',
    unsafe_allow_html=True
)
