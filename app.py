import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Zomato Analytics", layout="wide")

# ------------------ CUSTOM DARK CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.metric-card {
    background: linear-gradient(145deg, #1c1f26, #111);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.05);
}
h1, h2, h3 {
    color: #ffffff;
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

# ------------------ TITLE ------------------
st.title("🍽️ Zomato Analytics Dashboard")

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("🔎 Filter Panel")

location = st.sidebar.selectbox("Select Location", df['location'].dropna().unique())
restaurant = st.sidebar.selectbox("Select Restaurant", df['name'].dropna().unique())

filtered_df = df[df['location'] == location]

# ------------------ KPIs ------------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card">
<h3>⭐ Rating</h3>
<h2>{round(filtered_df['rating'].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<h3>🗳️ Total Votes</h3>
<h2>{int(filtered_df['votes'].sum())}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
<h3>💰 Avg Cost</h3>
<h2>{int(filtered_df['approx_cost'].mean())}</h2>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card">
<h3>🏪 Restaurants</h3>
<h2>{filtered_df.shape[0]}</h2>
</div>
""", unsafe_allow_html=True)

# ------------------ EXTRA KPIs ------------------
col5, col6 = st.columns(2)

col5.markdown(f"""
<div class="metric-card">
<h3>📍 Avg Location Cost</h3>
<h2>{int(filtered_df['approx_cost'].mean())}</h2>
</div>
""", unsafe_allow_html=True)

col6.markdown(f"""
<div class="metric-card">
<h3>📊 Avg Location Rating</h3>
<h2>{round(filtered_df['rating'].mean(),2)}</h2>
</div>
""", unsafe_allow_html=True)

# ------------------ CHART 1 (LOCATION COST) ------------------
st.subheader("📍 Expensive Locations")

loc_cost = df.groupby('location')['approx_cost'].mean().sort_values(ascending=False).head(10)

fig1 = px.bar(
    x=loc_cost.index,
    y=loc_cost.values,
    labels={'x':'Location', 'y':'Avg Cost'},
    template='plotly_dark'
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------ CHART 2 (RESTAURANT COST) ------------------
st.subheader("🏨 Restaurant Cost Analysis")

rest_cost = df.groupby('name')['approx_cost'].mean().sort_values(ascending=False).head(10)

fig2 = px.bar(
    x=rest_cost.index,
    y=rest_cost.values,
    labels={'x':'Restaurant', 'y':'Avg Cost'},
    template='plotly_dark'
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------ TABLE ------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df.head(20))

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Made with ❤️ by Atharv")
