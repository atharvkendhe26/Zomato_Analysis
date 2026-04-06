import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Zomato Dashboard", layout="wide")

# Custom Dark Theme Styling
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .metric-card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Data.csv")
    df['approx_cost'] = df['approx_cost'].replace('[,]', '', regex=True).astype('int64')
    return df

df = load_data()

# Title
st.title("🍽️ Zomato Data Analysis Dashboard")

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("⭐ Avg Rating", round(df['rate'].astype(str).str.split('/').str[0].astype(float).mean(),2))
col2.metric("🗳️ Total Votes", int(df['votes'].sum()))
col3.metric("💰 Avg Cost", int(df['approx_cost'].mean()))
col4.metric("🏪 Total Restaurants", df.shape[0])

# Location-wise Analysis
st.subheader("📍 Location-wise Avg Cost")
loc_cost = df.groupby('location')['approx_cost'].mean().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots()
sns.barplot(x=loc_cost.values, y=loc_cost.index, ax=ax1)
ax1.set_title("Top Locations by Avg Cost")
st.pyplot(fig1)

# Location-wise Rating
st.subheader("📊 Location-wise Avg Rating")
df['rating'] = df['rate'].astype(str).str.split('/').str[0]
df = df[df['rating'] != 'NEW']
df['rating'] = df['rating'].astype(float)

loc_rating = df.groupby('location')['rating'].mean().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=loc_rating.values, y=loc_rating.index, ax=ax2)
ax2.set_title("Top Locations by Rating")
st.pyplot(fig2)

# Restaurant-wise Cost
st.subheader("🏨 Restaurant-wise Avg Cost")
rest_cost = df.groupby('name')['approx_cost'].mean().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
sns.barplot(x=rest_cost.values, y=rest_cost.index, ax=ax3)
ax3.set_title("Top Restaurants by Cost")
st.pyplot(fig3)

# Filters
st.sidebar.header("🔍 Filters")
selected_location = st.sidebar.selectbox("Select Location", df['location'].dropna().unique())

filtered_df = df[df['location'] == selected_location]

st.subheader(f"📌 Data for {selected_location}")
st.dataframe(filtered_df.head(50))

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

