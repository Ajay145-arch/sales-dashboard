import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
df = pd.read_csv("sales_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.title("📊 Sales Dashboard")
st.write("Interactive analysis of sales, profit and product performance")

# Sidebar filters
st.sidebar.header("🔎 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# KPI calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
col3.metric("📦 Items Sold", f"{total_quantity:,}")

st.divider()

# Monthly Sales
st.subheader("📈 Monthly Sales")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Date"].dt.strftime("%Y-%m"))["Sales"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 4))
monthly_sales.plot(kind="line", marker="o", ax=ax)

ax.set_xlabel("Month")
ax.set_ylabel("Sales (₹)")
ax.set_title("Monthly Sales Trend")

st.pyplot(fig)

# Two columns
col1, col2 = st.columns(2)

# Product Sales
with col1:
    st.subheader("🏆 Sales by Product")

    product_sales = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    product_sales.plot(kind="bar", ax=ax)

    ax.set_xlabel("Product")
    ax.set_ylabel("Sales (₹)")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)

# Regional Sales
with col2:
    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    region_sales.plot(kind="bar", ax=ax)

    ax.set_xlabel("Region")
    ax.set_ylabel("Sales (₹)")

    st.pyplot(fig)

# Data table
st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)