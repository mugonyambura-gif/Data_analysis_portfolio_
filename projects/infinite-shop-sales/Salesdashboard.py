
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# PAGE SETTINGS
# ==========================================================

st.set_page_config(
    page_title="Shop Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Retail_Superstore_Analysis_Dataset.csv")

    # Convert Order Date to date format
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    # Remove rows where date is invalid
    df = df.dropna(subset=["Order Date"])

    return df


df = load_data()


# ==========================================================
# DATE COLUMNS
# ==========================================================

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%b")


# ==========================================================
# DASHBOARD TITLE
# ==========================================================

st.title("📊 Shop Sales Dashboard")

st.write(
    "Interactive analysis of sales, profit, orders, "
    "customers and product performance."
)

st.divider()


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("🔎 Filters")


# REGION FILTER
regions = sorted(
    df["Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)


# CATEGORY FILTER
categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)


# SEGMENT FILTER
segments = sorted(
    df["Segment"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "Segment",
    segments,
    default=segments
)


# YEAR FILTER
years = sorted(
    df["Year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "Year",
    years,
    default=years
)


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Segment"].isin(selected_segments)) &
    (df["Year"].isin(selected_years))
]


# ==========================================================
# CHECK FILTER RESULT
# ==========================================================

if filtered_df.empty:

    st.warning(
        "No data is available for the selected filters."
    )

    st.stop()


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()


# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📌 Key Performance Indicators")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Sales",
        f"{total_sales:,.2f}"
    )


with col2:

    st.metric(
        "Total Profit",
        f"{total_profit:,.2f}"
    )


with col3:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )


st.divider()


# ==========================================================
# SALES BY CATEGORY
# ==========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    category_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")
    ax.set_title("Sales by Category")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# SALES BY REGION
# ==========================================================

with col2:

    st.subheader("Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    region_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Sales")
    ax.set_title("Sales by Region")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# MONTHLY SALES TREND
# ==========================================================

st.divider()

st.subheader("📈 Monthly Sales Trend")


monthly_sales = (
    filtered_df
    .groupby(["Year", "Month"])["Sales"]
    .sum()
    .reset_index()
)


monthly_sales["Date"] = pd.to_datetime(
    monthly_sales["Year"].astype(str)
    + "-"
    + monthly_sales["Month"].astype(str)
    + "-01"
)


monthly_sales = monthly_sales.sort_values("Date")


fig, ax = plt.subplots(figsize=(14, 5))


ax.plot(
    monthly_sales["Date"],
    monthly_sales["Sales"],
    marker="o"
)


ax.set_xlabel("Month")
ax.set_ylabel("Sales")
ax.set_title("Monthly Sales Trend")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close(fig)


# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏆 Top 10 Products by Sales")


    top_products = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )


    fig, ax = plt.subplots(figsize=(9, 6))


    top_products.plot(
        kind="barh",
        ax=ax
    )


    ax.set_xlabel("Sales")
    ax.set_ylabel("Product")
    ax.set_title("Top 10 Products")


    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# SALES BY SEGMENT
# ==========================================================

with col2:

    st.subheader("Sales by Segment")


    segment_sales = (
        filtered_df
        .groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


    fig, ax = plt.subplots(figsize=(8, 6))


    segment_sales.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )


    ax.set_ylabel("")

    ax.set_title(
        "Sales Distribution by Segment"
    )


    st.pyplot(fig)

    plt.close(fig)


# ==========================================================
# PROFIT BY CATEGORY
# ==========================================================

st.divider()

st.subheader("💰 Profit by Category")


category_profit = (
    filtered_df
    .groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)


fig, ax = plt.subplots(figsize=(10, 5))


category_profit.plot(
    kind="bar",
    ax=ax
)


ax.set_xlabel("Category")
ax.set_ylabel("Profit")
ax.set_title("Profit by Category")


plt.xticks(rotation=0)

st.pyplot(fig)

plt.close(fig)


# ==========================================================
# FILTERED DATA TABLE
# ==========================================================

st.divider()

st.subheader("📋 Filtered Data")


st.dataframe(
    filtered_df,
    use_container_width=True
)


# ==========================================================
# DOWNLOAD BUTTON
# ==========================================================

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_shop_sales.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Shop Sales Dashboard | "
    "Built with Python, Pandas, Matplotlib and Streamlit"
)
