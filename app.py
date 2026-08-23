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

    /* =====================================================
       MAIN PAGE
       ===================================================== */

    .stApp {
        background-color: #0b0f14;
    }

    .block-container {
        max-width: 1800px;
        padding-top: 1.0rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 1rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #151a21;
        border-right: 1px solid #303640;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }

    section[data-testid="stSidebar"] h2 {
        color: #e23744 !important;
        font-size: 25px !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
    }

    section[data-testid="stSidebar"] p {
        font-size: 14px !important;
        color: #aeb7c3 !important;
    }

    /* Sidebar labels */
    section[data-testid="stSidebar"] label {
        color: #f1f3f5 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }

    /* Select box */
    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background-color: #0e1218 !important;
        border: 1px solid #3b424d !important;
        border-radius: 10px !important;
        min-height: 45px !important;
    }

    /* Slider */
    section[data-testid="stSidebar"] .stSlider {
        padding-top: 6px;
        padding-bottom: 12px;
    }

    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
        margin-top: 5px;
    }


    /* =====================================================
       ZOMATO HEADER
       ===================================================== */

    .zomato-title {
        text-align: center;
        color: #e23744;
        font-size: 54px;
        line-height: 1.1;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-top: 4px;
        margin-bottom: 5px;
    }

    .zomato-subtitle {
        text-align: center;
        color: #aeb7c3;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 14px;
    }


    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 10px;
    }


    /* =====================================================
       KPI CARDS
       ===================================================== */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #1c222c,
            #151a21
        );

        border: 1px solid #353d49;

        border-radius: 16px;

        padding: 20px 22px;

        min-height: 115px;

        box-shadow:
            0 7px 20px rgba(0, 0, 0, 0.28);
    }

    [data-testid="stMetricLabel"] {
        color: #aeb7c3 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 31px !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       PLOTLY / CHART AREA
       ===================================================== */

    div[data-testid="stPlotlyChart"] {
        background-color: #11161d;
        border: 1px solid #2d343e;
        border-radius: 14px;
        padding: 6px;
        margin-bottom: 12px;
    }


    /* =====================================================
       INSIGHT CARDS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 13px !important;
        min-height: 95px;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: #303640 !important;
        margin-top: 10px !important;
        margin-bottom: 12px !important;
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
        st.error("❌ Required columns missing hain:")
        st.write(missing_columns)
        st.write("Available columns:", list(df.columns))
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

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "name",
            "location",
            "rating",
            "approx_cost"
        ]
    )

    # Valid ratings
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
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🔎 Dashboard Filters")

st.sidebar.caption(
    "Use filters to explore restaurant performance."
)

st.sidebar.divider()


# ---------------------------------------------------------
# LOCATION
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
# MINIMUM RATING
# ---------------------------------------------------------

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# ---------------------------------------------------------
# MAXIMUM COST
# ---------------------------------------------------------

max_cost = int(
    df["approx_cost"].max()
)

selected_max_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=max_cost,
    value=max_cost,
    step=100
)


# ---------------------------------------------------------
# ONLINE ORDER
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TABLE BOOKING
# ---------------------------------------------------------

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
    filtered_df["approx_cost"] <= selected_max_cost
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
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Current filters ke according koi restaurant data nahi mila."
    )

    st.info(
        "Please filters ko thoda relax karke dobara try karein."
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

average_rating = filtered_df["rating"].mean()

total_votes = filtered_df["votes"].sum()

average_cost = filtered_df["approx_cost"].mean()


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Key Performance Indicators'
    '</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(
    [1, 1, 1, 1],
    gap="large"
)


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


st.caption(
    f"📍 {selected_location}   •   "
    f"⭐ Rating ≥ {min_rating:.1f}   •   "
    f"💰 Cost ≤ ₹{selected_max_cost:,}   •   "
    f"📊 {len(filtered_df):,} records"
)


# =========================================================
# CHART SECTION
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

chart1, chart2 = st.columns(
    [1, 1],
    gap="large"
)


# ---------------------------------------------------------
# LOCATION COST
# ---------------------------------------------------------

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
        color_continuous_scale=[
            "#7f1d1d",
            "#e23744",
            "#ff6b6b"
        ],
        template="plotly_dark",
        labels={
            "approx_cost": "Average Cost (₹)",
            "location": ""
        }
    )

    fig1.update_layout(
        height=390,
        margin=dict(
            l=15,
            r=15,
            t=20,
            b=15
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            color="#ffffff"
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ---------------------------------------------------------
# RATING DISTRIBUTION
# ---------------------------------------------------------

with chart2:

    fig2 = px.histogram(
        filtered_df,
        x="rating",
        nbins=15,
        color_discrete_sequence=[
            "#e23744"
        ],
        template="plotly_dark",
        labels={
            "rating": "Rating"
        }
    )

    fig2.update_layout(
        height=390,
        margin=dict(
            l=15,
            r=15,
            t=20,
            b=15
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            color="#ffffff"
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

chart3, chart4 = st.columns(
    [1, 1],
    gap="large"
)


# ---------------------------------------------------------
# POPULAR RESTAURANTS
# ---------------------------------------------------------

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
        color_continuous_scale=[
            "#78350f",
            "#f97316",
            "#fb923c"
        ],
        template="plotly_dark",
        labels={
            "votes": "Total Votes",
            "name": ""
        }
    )

    fig3.update_layout(
        height=390,
        margin=dict(
            l=15,
            r=15,
            t=20,
            b=15
        ),
        coloraxis_showscale=False,
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            color="#ffffff"
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# ---------------------------------------------------------
# COST VS RATING
# ---------------------------------------------------------

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
        color_continuous_scale=[
            "#ef4444",
            "#facc15",
            "#22c55e"
        ],
        template="plotly_dark",
        labels={
            "approx_cost": "Approx Cost (₹)",
            "rating": "Rating"
        }
    )

    fig4.update_layout(
        height=390,
        margin=dict(
            l=15,
            r=15,
            t=20,
            b=15
        ),
        plot_bgcolor="#11161d",
        paper_bgcolor="#11161d",
        font=dict(
            color="#ffffff"
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


# Most popular

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


expensive_location = location_average.index[0]

expensive_cost = location_average.iloc[0]


i1, i2, i3 = st.columns(
    [1, 1, 1],
    gap="large"
)


with i1:

    st.success(
        f"⭐ **Highest Rated Restaurant**\n\n"
        f"**{best_restaurant['name']}**\n\n"
        f"Rating: **{best_restaurant['rating']:.1f}/5**"
    )


with i2:

    st.warning(
        f"🔥 **Most Popular Restaurant**\n\n"
        f"**{most_voted['name']}**\n\n"
        f"Votes: **{int(most_voted['votes']):,}**"
    )


with i3:

    st.info(
        f"💰 **Highest Cost Location**\n\n"
        f"**{expensive_location}**\n\n"
        f"Average Cost: **₹{expensive_cost:,.0f}**"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍽️ Zomato Restaurant Analytics Dashboard  •  "
    "Python | Pandas | Plotly | Streamlit"
)
