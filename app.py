import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Zomato Dashboard", layout="wide")

# ------------------ DARK THEME ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.metric-card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Zomato_Data.csv")
    df['approx_cost'] = df['approx_cost'].replace('[,]', '', regex=True).astype(int)
    
    df['rating'] = df['rate'].astype(str).str.split('/').str[0]
    df = df[df['rating'] != 'NEW']
    df['rating'] = df['rating'].astype(float)

    return df

df = load_data()

# ------------------ SIDEBAR ------------------
st.sidebar.header("🔎 Filters")
location = st.sidebar.selectbox("Location", df['location'].dropna().unique())

filtered_df = df[df['location'] == location]

# ------------------ TITLE ------------------
st.title("🍽️ Zomato Dashboard")

# ------------------ KPI ROW ------------------
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='metric-card'><h4>⭐ Rating</h4><h2>{round(filtered_df['rating'].mean(),2)}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><h4>🗳 Votes</h4><h2>{int(filtered_df['votes'].sum())}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><h4>💰 Avg Cost</h4><h2>{int(filtered_df['approx_cost'].mean())}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><h4>🏪 Restaurants</h4><h2>{filtered_df.shape[0]}</h2></div>", unsafe_allow_html=True)

# ------------------ CHARTS SIDE BY SIDE ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location Cost")
    loc_cost = df.groupby('location')['approx_cost'].mean().sort_values(ascending=False).head(10)
    fig1 = px.bar(x=loc_cost.index, y=loc_cost.values, template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏨 Restaurant Cost")
    rest_cost = df.groupby('name')['approx_cost'].mean().sort_values(ascending=False).head(10)
    fig2 = px.bar(x=rest_cost.index, y=rest_cost.values, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# ------------------ AVG LOCATION CARDS (BELOW GRAPHS) ------------------
c5, c6 = st.columns(2)

c5.markdown(f"<div class='metric-card'><h4>📍 Avg Location Cost</h4><h2>{int(filtered_df['approx_cost'].mean())}</h2></div>", unsafe_allow_html=True)
c6.markdown(f"<div class='metric-card'><h4>📊 Avg Location Rating</h4><h2>{round(filtered_df['rating'].mean(),2)}</h2></div>", unsafe_allow_html=True)

# ------------------ TABLE ------------------
st.subheader("📋 Data")
st.dataframe(filtered_df.head(20))

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Made with ❤️ by Atharv")
