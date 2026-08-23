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

st.markdown(
    """
    <style>

    /* ================= MAIN APP ================= */

    .stApp {
        background-color: #0b0f14;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1600px;
    }


    /* ================= SIDEBAR ================= */

    section[data-testid="stSidebar"] {
        background-color: #151a21;
        border-right: 1px solid #292f38;
    }

    section[data-testid="stSidebar"] h2 {
        color: #e23744 !important;
        font-size: 22px !important;
    }


    /* ================= ZOMATO HEADER ================= */

    .zomato-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        color: #e23744;
        letter-spacing: -1px;
        margin-top: 5px;
        margin-bottom: 2px;
    }

    .zomato-subtitle {
        text-align: center;
        color: #9da7b4;
        font-size: 15px;
        margin-bottom: 10px;
    }


    /* ================= SECTION HEADERS ================= */

    .section-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 700;
        margin-top: 5px;
        margin-bottom: 8px;
    }


    /* ================= KPI CARDS ================= */

    [data-testid="stMetric"] {

        background: linear-gradient(
            135deg,
            #1b2029,
            #151a21
        );

        border: 1px solid #303743;
        border-radius: 14px;

        padding: 14px 18px;

        min-height: 92px;

        box-shadow:
            0 5px 15px rgba(0,0,0,0.25);
    }


    [data-testid="stMetricLabel"] {

        color: #aeb7c3 !important;

        font-size: 14px !important;
        font-weight: 500 !important;
    }


    [data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-size: 27px !important;

        font-weight: 700 !important;
    }


    /* ================= SIDEBAR TEXT ================= */

    section[data-testid="stSidebar"] label {

        color: #e6e9ed !important;

        font-weight: 600 !important;
    }


    /* ================= SELECT BOX ================= */

    div[data-baseweb="select"] > div {

        background-color: #0f1319;

        border: 1px solid #303640;

        border-radius: 8px;
    }


    /* ================= SLIDER ================= */

    .stSlider {

        padding-bottom: 5px;
    }


    /* ================= DIVIDER ================= */

    hr {

        border-color: #303640;

        margin-top: 8px;
        margin-bottom: 10px;
    }


    /* ================= ALERTS ================= */

    .stAlert {

        border-radius: 10px;
    }


    /* ================= FOOTER ================= */

    footer {
        visibility: hidden;
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

    required_columns = [
        "name",
        "location",
        "rate",
        "votes",
        "approx_cost"
    ]


    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]


    if missing_columns:

        st.error(
            "❌ Required columns missing hain:"
        )

        st.write(missing_columns)

        st.write(
            "Available columns:",
            list(df.columns)
        )

        st.stop()


    # =====================================================
    # NAME
    # =====================================================

    df["name"] = (
        df["name"]
        .astype(str)
        .str.strip()
    )


    # =====================================================
    # LOCATION
    # =====================================================

    df["location"] = (
        df["location"]
        .astype(str)
        .str.strip()
    )


    # =====================================================
    # COST
    # =====================================================

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


    # =====================================================
    # VOTES
    # =====================================================

    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["votes"] = df["votes"].fillna(0)


    # =====================================================
    # RATING
    # =====================================================

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


    # =====================================================
    # REMOVE INVALID DATA
    # =====================================================

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


# Load

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


# =========================================================
# LOCATION FILTER
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
# RATING FILTER
# =========================================================

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# =========================================================
# COST FILTER
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


# Location

if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]


# Rating

filtered_df = filtered_df[
    filtered_df["rating"] >= min_rating
]


# Cost

filtered_df = filtered_df[
    filtered_df["approx_cost"] <= selected_max_cost
]


# Online order

if (
    "online_order" in filtered_df.columns
    and selected_online != "All"
):

    filtered_df = filtered_df[
        filtered_df["online_order"]
        .astype(str)
        == selected_online
    ]


# Table booking

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
        "⚠️ Current filters ke according koi restaurant nahi mila."
    )

    st.info(
        "Location, Rating ya Cost filter change karke try karein."
    )

    st.stop()


# =========================================================
# MAIN ZOMATO HEADER
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


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "🏪 Total Restaurants",
        f"{total_restaurants:,}"
    )


with k2:

    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f} / 5"
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

st.caption(
    f"📍 {selected_location}   •   "
    f"⭐ Rating ≥ {min_rating:.1f}   •   "
    f"💰 Cost ≤ ₹{selected_max_cost:,}   •   "
    f"📊 {len(filtered_df):,} records"
)


# =========================================================
# CHART ROW 1
# =========================================================

chart1, chart2 = st.columns(2)


# =========================================================
# LOCATION COST
# =========================================================

with chart1:

    st.markdown(
        "#### 💰 Top Locations by Average Cost"
    )


    location_cost = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
    )


    fig1 = px.bar(
        location_cost,
        x="approx_cost",
        y="location",
        orientation="h",
        color="approx_cost",
        color_continuous_scale="Reds",
        template="plotly_dark",
        labels={
            "approx_cost": "Average Cost (₹)",
            "location": ""
        }
    )


    fig1.update_layout(
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=10,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14"
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

with chart2:

    st.markdown(
        "#### ⭐ Rating Distribution"
    )


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
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=10,
            b=5
        ),
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14"
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
# POPULAR RESTAURANTS
# =========================================================

with chart3:

    st.markdown(
        "#### 🔥 Most Popular Restaurants"
    )


    popular = (
        filtered_df
        .groupby("name")["votes"]
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .reset_index()
    )


    fig3 = px.bar(
        popular,
        x="votes",
        y="name",
        orientation="h",
        color="votes",
        color_continuous_scale="Oranges",
        template="plotly_dark",
        labels={
            "votes": "Votes",
            "name": ""
        }
    )


    fig3.update_layout(
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=10,
            b=5
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14"
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

with chart4:

    st.markdown(
        "#### 💰 Cost vs Customer Rating"
    )


    scatter_df = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()


    fig4 = px.scatter(
        scatter_df,
        x="approx_cost",
        y="rating",
        size="votes",
        color="rating",
        hover_name="name",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        labels={
            "approx_cost": "Cost (₹)",
            "rating": "Rating"
        }
    )


    fig4.update_layout(
        height=300,
        margin=dict(
            l=5,
            r=5,
            t=10,
            b=5
        ),
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14"
    )


    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Business Insights'
    '</div>',
    unsafe_allow_html=True
)


# Highest rated

best_restaurant = (
    filtered_df
    .sort_values(
        ["rating", "votes"],
        ascending=[False, False]
    )
    .iloc[0]
)


# Most voted

most_voted = (
    filtered_df
    .sort_values(
        "votes",
        ascending=False
    )
    .iloc[0]
)


# Costliest location

location_average = (
    filtered_df
    .groupby("location")["approx_cost"]
    .mean()
    .sort_values(ascending=False)
)


expensive_location = (
    location_average.index[0]
)

expensive_cost = (
    location_average.iloc[0]
)


i1, i2, i3 = st.columns(3)


with i1:

    st.success(
        f"⭐ **Highest Rated**  \n\n"
        f"**{best_restaurant['name']}**  \n"
        f"Rating: **{best_restaurant['rating']:.1f}/5**"
    )


with i2:

    st.warning(
        f"🔥 **Most Popular**  \n\n"
        f"**{most_voted['name']}**  \n"
        f"Votes: **{int(most_voted['votes']):,}**"
    )


with i3:

    st.info(
        f"💰 **Highest Cost Location**  \n\n"
        f"**{expensive_location}**  \n"
        f"Average Cost: **₹{expensive_cost:,.0f}**"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍽️ Zomato Restaurant Analytics  •  "
    "Built with Python | Pandas | Plotly | Streamlit"
)
