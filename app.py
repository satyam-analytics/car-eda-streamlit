import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page Config ----------------
st.set_page_config(page_title="Cars EDA Dashboard", layout="wide")

# ---------------- SAFE DESIGN CSS ----------------
st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #f0f2f6;
    padding: 16px;
    border-radius: 12px;
    border-left: 6px solid #6c63ff;
}

.custom-card {
    padding: 22px;
    border-radius: 14px;
    border: 2px solid #6c63ff;
    background-color: #ffffff;
    margin-bottom: 18px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.custom-insight {
    padding: 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    return pd.read_csv("Cars.csv")

df = load_data()
clean_df = df.dropna()

# ---------------- Sidebar ----------------
st.sidebar.title("🚗 Cars EDA Project")
page = st.sidebar.radio(
    "Navigation",
    ["Introduction", "Car Data Analysis", "Conclusion"]
)

# ================= INTRODUCTION =================
if page == "Introduction":
    st.title("🚗 Used Cars Data Analysis Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Cars", df.shape[0])
    c2.metric("Average Price", round(df["Price"].mean(), 2))
    c3.metric("Fuel Types", df["Fuel_Type"].nunique())

    st.markdown("""
    <div class="custom-card">
    <b>Dataset Overview</b><br>
    This dashboard performs exploratory data analysis on used car data to
    understand pricing trends, fuel preferences, ownership impact and usage patterns.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Show Raw Data"):
            st.subheader("Raw Dataset")
            st.dataframe(df)

    with col2:
        if st.button("🧹 Show Clean Data"):
            st.subheader("Cleaned Dataset (Missing Values Removed)")
            st.dataframe(clean_df)

# ================= ANALYSIS =================
elif page == "Car Data Analysis":
    st.title("📊 Exploratory Data Analysis")

    tab1, tab2, tab3 = st.tabs(
        ["📊 Univariate Analysis", "📈 Bivariate Analysis", "📉 Multivariate Analysis"]
    )

    # ---------- Univariate ----------
    with tab1:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df["Price"], kde=True, ax=ax)
        st.pyplot(fig)

        st.subheader("Fuel Type Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x="Fuel_Type", data=df, ax=ax)
        st.pyplot(fig)

    # ---------- Bivariate ----------
    with tab2:
        st.subheader("Price vs Fuel Type")
        fig, ax = plt.subplots()
        sns.boxplot(x="Fuel_Type", y="Price", data=df, ax=ax)
        st.pyplot(fig)

        st.subheader("Price vs Transmission")
        fig, ax = plt.subplots()
        sns.barplot(x="Transmission", y="Price", data=df, ax=ax)
        st.pyplot(fig)

    # ---------- Multivariate ----------
    with tab3:
        st.subheader("Fuel Type & Transmission vs Price")
        fig, ax = plt.subplots()
        sns.barplot(
            x="Fuel_Type",
            y="Price",
            hue="Transmission",
            data=df,
            ax=ax
        )
        st.pyplot(fig)

# ================= CONCLUSION =================
else:
    st.title("✅ Conclusion & Business Insights")

    st.markdown(
        """
        <div class="custom-card">
            <b>Summary</b><br>
            This analysis identifies the key factors influencing used car prices
            and provides actionable insights for data-driven business decisions.
        </div>

        <div class="custom-insight">
            <b>1. Pricing Strategy:</b><br>
            Diesel and automatic cars consistently achieve higher resale prices.
            Stocking these variants can significantly improve margins.
        </div>

        <div class="custom-insight">
            <b>2. Ownership Impact:</b><br>
            First-owner vehicles command a strong price premium.
            Clearly displaying ownership history builds buyer trust.
        </div>

        <div class="custom-insight">
            <b>3. Usage Pattern:</b><br>
            Lower mileage vehicles retain higher value and sell faster,
            making them ideal for premium listings.
        </div>

        <div class="custom-insight">
            <b>4. Market Demand:</b><br>
            Manual transmission cars dominate overall volume,
            indicating strong demand in budget-conscious segments.
        </div>

        <div class="custom-insight">
            <b>5. Portfolio Optimization:</b><br>
            A balanced mix of fuel types and transmission options
            helps reduce pricing risk and attract a wider customer base.
        </div>
        """,
        unsafe_allow_html=True
    )
