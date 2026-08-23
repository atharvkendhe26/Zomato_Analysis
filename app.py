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
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main app */
    .stApp {
        background-color: #0b0f14;
    }

    /* Reduce top spacing */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 0.5rem;
        max-width: 1500px;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #e23744;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }

    .sub-title {
        font-size: 16px;
        color: #9da6b2;
        text-align: center;
        margin-top: 3px;
        margin-bottom: 12px;
    }

    /* Section headings */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
        margin-bottom: 7px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            #1b212b,
            #141920
        );

        border: 1px solid #303743;
        border-radius: 14px;

        padding: 13px 18px;

        min-height: 88px;

        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #aeb7c4 !important;
        font-size: 14px !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 25px !important;
        font-weight: 700 !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #171c24;
        border: 1px solid #343b47;
        border-radius: 9px;
    }

    /* Slider labels */
    .stSlider label {
        color: #e7ebf0 !important;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border-color: #303640;
        margin: 8px 0;
    }

    /* Info */
    .stAlert {
        padding: 8px 14px;
        margin-bottom: 8px;
    }

    /* Hide Streamlit footer */
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
        col for col in required
        if col not in df.columns
    ]

    if missing:
        st.error(
            "❌ Required columns missing hain:"
        )
        st.write(missing)
        st.write("Available columns:", list(df.columns))
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
        .str.strip()
    )

    df["approx_cost"] = pd.to_numeric(
        df["approx_cost"],
        errors="coerce"
    )

    # Votes cleaning
    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["votes"] = df["votes"].fillna(0)

    # Rating cleaning
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


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🍽️ ZOMATO RESTAURANT ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Interactive Restaurant Analysis • Ratings • Pricing • Popularity'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# FILTER SECTION
# =========================================================

st.markdown(
    '<div class="section-header">🔎 Dashboard Filters</div>',
    unsafe_allow_html=True
)

filter1, filter2, filter3, filter4, filter5 = st.columns(
    [1.5, 1.2, 1.4, 1.2, 1.2]
)


# ---------------------------------------------------------
# Location
# ---------------------------------------------------------

locations = sorted(
    df["location"]
    .dropna()
    .unique()
    .tolist()
)

with filter1:

    selected_location = st.selectbox(
        "📍 Location",
        ["All Locations"] + locations
    )


# ---------------------------------------------------------
# Minimum Rating
# ---------------------------------------------------------

with filter2:

    min_rating = st.slider(
        "⭐ Minimum Rating",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.1
    )


# ---------------------------------------------------------
# Maximum Cost
# ---------------------------------------------------------

max_cost = int(
    df["approx_cost"].max()
)

with filter3:

    selected_max_cost = st.slider(
        "💰 Maximum Cost",
        min_value=0,
        max_value=max_cost,
        value=max_cost,
        step=100
    )


# ---------------------------------------------------------
# Online Order
# ---------------------------------------------------------

with filter4:

    if "online_order" in df.columns:

        online_values = sorted(
            df["online_order"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_online = st.selectbox(
            "🛵 Online Order",
            ["All"] + online_values
        )

    else:

        selected_online = "All"

        st.selectbox(
            "🛵 Online Order",
            ["All"],
            disabled=True
        )


# ---------------------------------------------------------
# Table Booking
# ---------------------------------------------------------

with filter5:

    if "book_table" in df.columns:

        table_values = sorted(
            df["book_table"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_table = st.selectbox(
            "🍽️ Table Booking",
            ["All"] + table_values
        )

    else:

        selected_table = "All"

        st.selectbox(
            "🍽️ Table Booking",
            ["All"],
            disabled=True
        )


# =========================================================
# FILTER DATA
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
        "⚠️ Current filters ke according koi data nahi mila."
    )

    st.stop()


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-header">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

total_restaurants = len(filtered_df)

average_rating = filtered_df["rating"].mean()

total_votes = filtered_df["votes"].sum()

average_cost = filtered_df["approx_cost"].mean()


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
# CHART SECTION
# =========================================================

st.markdown(
    '<div class="section-header">📈 Restaurant Insights</div>',
    unsafe_allow_html=True
)


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
        title="💰 Top Locations by Average Cost"
    )

    fig1.update_layout(
        height=285,
        margin=dict(
            l=10,
            r=10,
            t=45,
            b=10
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        font=dict(
            color="white"
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
# CHART 2 - RATING DISTRIBUTION
# =========================================================

with chart2:

    fig2 = px.histogram(
        filtered_df,
        x="rating",
        nbins=12,
        color_discrete_sequence=["#e23744"],
        template="plotly_dark",
        title="⭐ Rating Distribution"
    )

    fig2.update_layout(
        height=285,
        margin=dict(
            l=10,
            r=10,
            t=45,
            b=10
        ),
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        font=dict(
            color="white"
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# SECOND CHART ROW
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
        title="🔥 Most Popular Restaurants"
    )

    fig3.update_layout(
        height=285,
        margin=dict(
            l=10,
            r=10,
            t=45,
            b=10
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        font=dict(
            color="white"
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
# CHART 4 - COST VS RATING
# =========================================================

with chart4:

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
        title="💰 Cost vs Rating"
    )

    fig4.update_layout(
        height=285,
        margin=dict(
            l=10,
            r=10,
            t=45,
            b=10
        ),
        plot_bgcolor="#0b0f14",
        paper_bgcolor="#0b0f14",
        font=dict(
            color="white"
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
# QUICK BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-header">💡 Quick Business Insights</div>',
    unsafe_allow_html=True
)


best_restaurant = (
    filtered_df
    .sort_values(
        ["rating", "votes"],
        ascending=[False, False]
    )
    .iloc[0]
)

most_voted = (
    filtered_df
    .sort_values(
        "votes",
        ascending=False
    )
    .iloc[0]
)

best_location_data = (
    filtered_df
    .groupby("location")["approx_cost"]
    .mean()
    .sort_values(ascending=False)
)

if len(best_location_data) > 0:

    expensive_location = best_location_data.index[0]

    expensive_location_cost = best_location_data.iloc[0]

else:

    expensive_location = "N/A"

    expensive_location_cost = 0


i1, i2, i3 = st.columns(3)


with i1:

    st.success(
        f"⭐ **Highest Rated**  \n"
        f"{best_restaurant['name']}  \n"
        f"Rating: **{best_restaurant['rating']:.1f}/5**"
    )


with i2:

    st.warning(
        f"🔥 **Most Popular**  \n"
        f"{most_voted['name']}  \n"
        f"Votes: **{int(most_voted['votes']):,}**"
    )


with i3:

    st.info(
        f"💰 **Highest Cost Location**  \n"
        f"{expensive_location}  \n"
        f"Average: **₹{expensive_location_cost:,.0f}**"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍽️ Zomato Restaurant Analytics Dashboard  •  "
    "Python | Pandas | Plotly | Streamlit"
)
