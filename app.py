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

/* ======================================================
   MAIN PAGE
   ====================================================== */

.stApp {
    background: #0b0f14;
}

.block-container {
    max-width: 100%;
    padding-top: 0.45rem;
    padding-bottom: 0.2rem;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
}


/* ======================================================
   SIDEBAR
   ====================================================== */

section[data-testid="stSidebar"] {
    background: #151a21;
    border-right: 1px solid #303640;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
    padding-left: 0.9rem;
    padding-right: 0.9rem;
}


/* Sidebar heading */

section[data-testid="stSidebar"] h2 {
    color: #e23744 !important;
    font-size: 21px !important;
    font-weight: 800 !important;
    margin-bottom: 4px !important;
}


/* Sidebar description */

section[data-testid="stSidebar"] p {
    color: #aeb7c3 !important;
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
    background-color: #0d1117 !important;
    border: 1px solid #353c47 !important;
    border-radius: 8px !important;
    min-height: 38px !important;
}


/* Slider */

section[data-testid="stSidebar"] .stSlider {
    padding-top: 0px;
    padding-bottom: 5px;
}


/* ======================================================
   ZOMATO HEADER
   ====================================================== */

.zomato-title {
    text-align: center;
    color: #e23744;
    font-size: 39px;
    line-height: 1.05;
    font-weight: 900;
    letter-spacing: -1px;
    margin-top: 0px;
    margin-bottom: 2px;
}

.zomato-subtitle {
    text-align: center;
    color: #aeb7c3;
    font-size: 12px;
    margin-bottom: 5px;
}


/* ======================================================
   DIVIDER
   ====================================================== */

hr {
    border-color: #303640 !important;
    margin-top: 5px !important;
    margin-bottom: 7px !important;
}


/* ======================================================
   SECTION TITLE
   ====================================================== */

.section-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 800;
    margin-top: 3px;
    margin-bottom: 5px;
}


/* ======================================================
   KPI CARDS
   ====================================================== */

[data-testid="stMetric"] {

    background: linear-gradient(
        145deg,
        #1b212a,
        #151a21
    );

    border: 1px solid #343c47;

    border-radius: 11px;

    padding: 8px 12px;

    min-height: 68px;

    box-shadow:
        0 4px 10px rgba(0,0,0,0.22);
}


/* KPI label */

[data-testid="stMetricLabel"] {
    color: #aeb7c3 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
}


/* KPI value */

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: 800 !important;
}


/* ======================================================
   CHART CONTAINER
   ====================================================== */

div[data-testid="stPlotlyChart"] {

    background: #11161d;

    border: 1px solid #2c343f;

    border-radius: 10px;

    padding: 2px;

    margin-bottom: 5px;
}


/* ======================================================
   SMALL TEXT
   ====================================================== */

.small-info {
    text-align: center;
    color: #8993a1;
    font-size: 10px;
    margin-top: 1px;
}


/* ======================================================
   HIDE FOOTER
   ====================================================== */

footer {
    visibility: hidden;
}


/* ======================================================
   REDUCE COLUMN GAP
   ====================================================== */

div[data-testid="column"] {
    padding-left: 3px !important;
    padding-right: 3px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("Zomato_Data.csv")

    except FileNotFoundError:

        st.error(
            "❌ Zomato_Data.csv nahi mili. "
            "CSV ko app.py ke same folder mein rakho."
        )

        st.stop()


    # Clean column names

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


    # Required columns

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
            "❌ Required columns missing hain:"
        )

        st.write(missing)

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
    )


    df["approx_cost"] = pd.to_numeric(
        df["approx_cost"],
        errors="coerce"
    )


    # Votes

    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["votes"] = df["votes"].fillna(0)


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


    # Remove invalid data

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

st.sidebar.markdown(
    "## 🔎 Dashboard Filters"
)

st.sidebar.caption(
    "Use filters to explore restaurant performance."
)

st.sidebar.divider()


# =========================================================
# LOCATION
# =========================================================

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


# =========================================================
# RATING
# =========================================================

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# =========================================================
# COST
# =========================================================

maximum_cost = int(
    df["approx_cost"].max()
)


selected_max_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=maximum_cost,
    value=maximum_cost,
    step=100
)


# =========================================================
# ONLINE ORDER
# =========================================================

if "online_order" in df.columns:

    online_values = sorted(
        df["online_order"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_online = st.sidebar.selectbox(
        "🛵 Online Order",
        ["All"] + online_values
    )

else:

    selected_online = "All"


# =========================================================
# TABLE BOOKING
# =========================================================

if "book_table" in df.columns:

    table_values = sorted(
        df["book_table"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_table = st.sidebar.selectbox(
        "🍽️ Table Booking",
        ["All"] + table_values
    )

else:

    selected_table = "All"


# =========================================================
# APPLY FILTERS
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
    and selected_table != "All"
):

    filtered_df = filtered_df[
        filtered_df["book_table"]
        .astype(str)
        == selected_table
    ]


# =========================================================
# EMPTY DATA
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Current filters ke according koi data nahi mila."
    )

    st.stop()


# =========================================================
# ZOMATO HEADER
# =========================================================

st.markdown(
    '<div class="zomato-title">'
    '🍽️ ZOMATO RESTAURANT ANALYTICS'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="zomato-subtitle">'
    'Restaurant Ratings • Pricing • Popularity • Customer Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_restaurants = len(filtered_df)

average_rating = (
    filtered_df["rating"].mean()
)

total_votes = (
    filtered_df["votes"].sum()
)

average_cost = (
    filtered_df["approx_cost"].mean()
)


# =========================================================
# KPI TITLE
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI ROW
# =========================================================

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
# FILTER SUMMARY
# =========================================================

st.markdown(
    f"""
    <div class="small-info">
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
    '<div class="section-title">'
    '📈 Restaurant Performance Analysis'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CHART 1 + CHART 2
# =========================================================

col1, col2 = st.columns(
    2,
    gap="small"
)


# =========================================================
# LOCATION COST
# =========================================================

with col1:

    location_cost = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(7)
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
            "approx_cost": "Avg Cost ₹",
            "location": ""
        }
    )


    fig1.update_layout(
        height=205,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=9
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
# RATING DISTRIBUTION
# =========================================================

with col2:

    fig2 = px.histogram(
        filtered_df,
        x="rating",
        nbins=12,
        color_discrete_sequence=[
            "#e23744"
        ],
        template="plotly_dark",
        labels={
            "rating": "Rating"
        }
    )


    fig2.update_layout(
        height=205,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=9
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

col3, col4 = st.columns(
    2,
    gap="small"
)


# =========================================================
# MOST POPULAR
# =========================================================

with col3:

    popular = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(7)
        .reset_index()
    )


    fig3 = px.bar(
        popular,
        x="votes",
        y="name",
        orientation="h",
        color="votes",
        color_continuous_scale=[
            "#78350f",
            "#f97316",
            "#fb923c"
        ],
        template="plotly_dark",
        labels={
            "votes": "Votes",
            "name": ""
        }
    )


    fig3.update_layout(
        height=205,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=9
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
# COST VS RATING
# =========================================================

with col4:

    scatter_df = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()


    # Limit points for faster and cleaner display

    if len(scatter_df) > 1200:

        scatter_df = (
            scatter_df
            .sample(
                1200,
                random_state=42
            )
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
        height=205,
        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            size=9
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
# BOTTOM SUMMARY
# =========================================================

st.markdown(
    f"""
    <div class="small-info">
        🍽️ Zomato Restaurant Analytics
        &nbsp; | &nbsp;
        Dataset: {len(df):,} rows
        &nbsp; | &nbsp;
        Filtered: {len(filtered_df):,}
        &nbsp; | &nbsp;
        Locations: {df["location"].nunique()}
        &nbsp; | &nbsp;
        Restaurants: {df["name"].nunique():,}
    </div>
    """,
    unsafe_allow_html=True
)
