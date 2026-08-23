import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Zomato Analytics",
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

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #151922;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #191e27;
        border: 1px solid #2d3440;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #aeb6c2;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Headers */
    h1 {
        color: #e23744 !important;
    }

    h2, h3 {
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
    }

    /* Divider */
    hr {
        border-color: #303640;
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

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        st.error(
            "❌ CSV mein required columns missing hain:"
        )
        st.write(missing)

        st.info(
            "Available columns:"
        )
        st.write(list(df.columns))

        st.stop()

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    df["name"] = (
        df["name"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    df["location"] = (
        df["location"]
        .astype(str)
        .str.strip()
    )

    # -----------------------------------------------------
    # COST
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
    # VOTES
    # -----------------------------------------------------

    df["votes"] = pd.to_numeric(
        df["votes"],
        errors="coerce"
    )

    df["votes"] = df["votes"].fillna(0)

    # -----------------------------------------------------
    # RATING
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # REMOVE INVALID DATA
    # -----------------------------------------------------

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
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use filters to explore restaurant data."
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
    "📍 Location",
    ["All Locations"] + locations
)


# ---------------------------------------------------------
# RATING
# ---------------------------------------------------------

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)


# ---------------------------------------------------------
# COST
# ---------------------------------------------------------

max_cost_data = int(
    df["approx_cost"].max()
)

selected_max_cost = st.sidebar.slider(
    "💰 Maximum Cost",
    min_value=0,
    max_value=max_cost_data,
    value=max_cost_data,
    step=100
)


# ---------------------------------------------------------
# OPTIONAL ONLINE ORDER FILTER
# ---------------------------------------------------------

if "online_order" in df.columns:

    online_options = sorted(
        df["online_order"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_online_order = st.sidebar.selectbox(
        "🛵 Online Order",
        ["All"] + online_options
    )

else:

    selected_online_order = "All"


# ---------------------------------------------------------
# OPTIONAL BOOK TABLE FILTER
# ---------------------------------------------------------

if "book_table" in df.columns:

    table_options = sorted(
        df["book_table"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_book_table = st.sidebar.selectbox(
        "🍽️ Table Booking",
        ["All"] + table_options
    )

else:

    selected_book_table = "All"


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
    and selected_online_order != "All"
):

    filtered_df = filtered_df[
        filtered_df["online_order"]
        .astype(str)
        == selected_online_order
    ]


# Table booking

if (
    "book_table" in filtered_df.columns
    and selected_book_table != "All"
):

    filtered_df = filtered_df[
        filtered_df["book_table"]
        .astype(str)
        == selected_book_table
    ]


# =========================================================
# HEADER
# =========================================================

st.title("🍽️ Zomato Restaurant Analytics")

st.caption(
    "Interactive analysis of restaurant ratings, pricing, "
    "popularity and customer behaviour"
)

st.divider()


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ Current filters ke according koi restaurant data nahi mila."
    )

    st.info(
        "Please Rating, Cost ya Location filter ko change karein."
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
# KPI ROW
# =========================================================

st.subheader("📊 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)


with k1:
    st.metric(
        label="🏪 Restaurants",
        value=f"{total_restaurants:,}"
    )


with k2:
    st.metric(
        label="⭐ Average Rating",
        value=f"{average_rating:.2f} / 5"
    )


with k3:
    st.metric(
        label="🗳️ Total Votes",
        value=f"{int(total_votes):,}"
    )


with k4:
    st.metric(
        label="💰 Average Cost",
        value=f"₹{average_cost:,.0f}"
    )


st.write("")


# =========================================================
# FILTER STATUS
# =========================================================

st.info(
    f"📍 **Location:** {selected_location}  |  "
    f"⭐ **Rating:** {min_rating}+  |  "
    f"💰 **Max Cost:** ₹{selected_max_cost:,}  |  "
    f"📊 **Records:** {len(filtered_df):,}"
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📈 Overview",
        "🏆 Restaurant Analysis",
        "📋 Data Explorer"
    ]
)


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.subheader("📈 Business Overview")

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # LOCATION COST
    # -----------------------------------------------------

    with col1:

        location_cost = (
            filtered_df
            .groupby("location")["approx_cost"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
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
            title="💰 Top 10 Locations by Average Cost",
            labels={
                "approx_cost": "Average Cost (₹)",
                "location": "Location"
            }
        )

        fig1.update_layout(
            height=450,
            coloraxis_showscale=False,
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # -----------------------------------------------------
    # RATING DISTRIBUTION
    # -----------------------------------------------------

    with col2:

        fig2 = px.histogram(
            filtered_df,
            x="rating",
            nbins=15,
            color_discrete_sequence=["#e23744"],
            template="plotly_dark",
            title="⭐ Restaurant Rating Distribution",
            labels={
                "rating": "Rating"
            }
        )

        fig2.update_layout(
            height=450,
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # -----------------------------------------------------
    # COST VS RATING
    # -----------------------------------------------------

    st.subheader("💰 Price vs Customer Rating")

    scatter_data = filtered_df[
        [
            "name",
            "approx_cost",
            "rating",
            "votes"
        ]
    ].copy()

    fig3 = px.scatter(
        scatter_data,
        x="approx_cost",
        y="rating",
        size="votes",
        color="rating",
        hover_name="name",
        color_continuous_scale="RdYlGn",
        template="plotly_dark",
        title="Relationship Between Restaurant Cost and Rating",
        labels={
            "approx_cost": "Approx Cost (₹)",
            "rating": "Rating",
            "votes": "Votes"
        }
    )

    fig3.update_layout(
        height=500,
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# =========================================================
# TAB 2 - RESTAURANT ANALYSIS
# =========================================================

with tab2:

    st.subheader("🏆 Restaurant Performance")

    col3, col4 = st.columns(2)

    # -----------------------------------------------------
    # POPULAR RESTAURANTS
    # -----------------------------------------------------

    with col3:

        popular = (
            filtered_df
            .groupby("name")["votes"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig4 = px.bar(
            popular,
            x="votes",
            y="name",
            orientation="h",
            color="votes",
            color_continuous_scale="Oranges",
            template="plotly_dark",
            title="🔥 Top 10 Restaurants by Votes",
            labels={
                "votes": "Total Votes",
                "name": "Restaurant"
            }
        )

        fig4.update_layout(
            height=500,
            coloraxis_showscale=False,
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    # -----------------------------------------------------
    # TOP RATED
    # -----------------------------------------------------

    with col4:

        top_rated_chart = (
            filtered_df
            .groupby("name")
            .agg(
                rating=("rating", "mean"),
                votes=("votes", "sum")
            )
            .sort_values(
                ["rating", "votes"],
                ascending=[False, False]
            )
            .head(10)
            .reset_index()
        )

        fig5 = px.bar(
            top_rated_chart,
            x="rating",
            y="name",
            orientation="h",
            color="rating",
            color_continuous_scale="RdYlGn",
            template="plotly_dark",
            title="⭐ Top 10 Highest Rated Restaurants",
            labels={
                "rating": "Average Rating",
                "name": "Restaurant"
            }
        )

        fig5.update_layout(
            height=500,
            coloraxis_showscale=False,
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            xaxis=dict(
                range=[0, 5]
            )
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    # -----------------------------------------------------
    # BUSINESS INSIGHTS
    # -----------------------------------------------------

    st.subheader("💡 Business Insights")

    best_rating_row = (
        filtered_df
        .sort_values(
            ["rating", "votes"],
            ascending=[False, False]
        )
        .iloc[0]
    )

    most_voted_row = (
        filtered_df
        .sort_values(
            "votes",
            ascending=False
        )
        .iloc[0]
    )

    expensive_location = (
        filtered_df
        .groupby("location")["approx_cost"]
        .mean()
        .sort_values(ascending=False)
    )

    if len(expensive_location) > 0:
        expensive_location_name = expensive_location.index[0]
        expensive_location_cost = expensive_location.iloc[0]
    else:
        expensive_location_name = "N/A"
        expensive_location_cost = 0

    insight1, insight2, insight3 = st.columns(3)

    with insight1:

        st.success(
            f"⭐ **Highest Rated**\n\n"
            f"{best_rating_row['name']}\n\n"
            f"Rating: **{best_rating_row['rating']:.1f}/5**"
        )

    with insight2:

        st.warning(
            f"🔥 **Most Voted Restaurant**\n\n"
            f"{most_voted_row['name']}\n\n"
            f"Votes: **{int(most_voted_row['votes']):,}**"
        )

    with insight3:

        st.info(
            f"💰 **Costliest Location**\n\n"
            f"{expensive_location_name}\n\n"
            f"Avg Cost: **₹{expensive_location_cost:,.0f}**"
        )


# =========================================================
# TAB 3 - DATA EXPLORER
# =========================================================

with tab3:

    st.subheader("📋 Restaurant Data Explorer")

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = st.text_input(
        "🔍 Search Restaurant",
        placeholder="Example: AB's, Cafe, Empire..."
    )

    display_df = filtered_df.copy()

    if search:

        display_df = display_df[
            display_df["name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    sort_option = st.selectbox(
        "Sort Data By",
        [
            "Rating - High to Low",
            "Votes - High to Low",
            "Cost - High to Low",
            "Cost - Low to High"
        ]
    )

    if sort_option == "Rating - High to Low":

        display_df = display_df.sort_values(
            "rating",
            ascending=False
        )

    elif sort_option == "Votes - High to Low":

        display_df = display_df.sort_values(
            "votes",
            ascending=False
        )

    elif sort_option == "Cost - High to Low":

        display_df = display_df.sort_values(
            "approx_cost",
            ascending=False
        )

    else:

        display_df = display_df.sort_values(
            "approx_cost",
            ascending=True
        )

    # -----------------------------------------------------
    # DISPLAY COLUMNS
    # -----------------------------------------------------

    table_columns = [
        "name",
        "location",
        "rating",
        "votes",
        "approx_cost"
    ]

    table_columns = [
        col
        for col in table_columns
        if col in display_df.columns
    ]

    final_table = display_df[table_columns].copy()

    final_table = final_table.rename(
        columns={
            "name": "Restaurant",
            "location": "Location",
            "rating": "Rating",
            "votes": "Votes",
            "approx_cost": "Approx Cost (₹)"
        }
    )

    st.write(
        f"Showing **{len(final_table):,}** restaurants"
    )

    st.dataframe(
        final_table.head(100),
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    csv_data = final_table.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="zomato_filtered_data.csv",
        mime="text/csv"
    )


# =========================================================
# DATASET INFORMATION
# =========================================================

st.divider()

st.subheader("📁 Dataset Information")

d1, d2, d3, d4 = st.columns(4)

with d1:

    st.metric(
        "Total Dataset Rows",
        f"{len(df):,}"
    )

with d2:

    st.metric(
        "Unique Restaurants",
        f"{df['name'].nunique():,}"
    )

with d3:

    st.metric(
        "Unique Locations",
        f"{df['location'].nunique():,}"
    )

with d4:

    st.metric(
        "Overall Avg Rating",
        f"{df['rating'].mean():.2f}"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍽️ Zomato Restaurant Analytics | "
    "Built with Python • Pandas • Plotly • Streamlit"
)

st.caption(
    "Made with ❤️ by Atharv"
)
