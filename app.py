import streamlit as st
import pandas as pd
from utils.data_cleaner import clean_data, detect_outliers, remove_outliers
from utils.data_profile import generate_profile

st.set_page_config(page_title="CSV Data Cleaner", layout="wide")
st.title("🧹 CSV Data Cleaner (Open Source)")
st.write("Clean, analyze, and download your dataset easily!")

uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    tab1, tab2, tab3 = st.tabs(["🧼 Clean Data", "📈 Outlier Detection", "🧠 Profiling Report"])

    # ---------- TAB 1: CLEAN DATA ----------
    with tab1:
        st.subheader("Dataset Overview")
        st.dataframe(df.head())
        st.info(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

        remove_duplicates = st.checkbox("Remove Duplicates", True)
        handle_missing = st.selectbox(
            "Handle Missing Values",
            ["Do Nothing", "Drop Rows", "Fill with Mean", "Fill with Median", "Fill with 0"]
        )

        if st.button("Clean Data"):
            clean_df = clean_data(df, remove_duplicates, handle_missing)
            st.success("✅ Data cleaned successfully!")
            st.dataframe(clean_df.head())

            st.download_button(
                label="📥 Download Cleaned CSV",
                data=clean_df.to_csv(index=False).encode("utf-8"),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="📊 Download as Excel",
                data=clean_df.to_excel(index=False, engine='openpyxl'),
                file_name="cleaned_data.xlsx"
            )

    # ---------- TAB 2: OUTLIER DETECTION ----------
    with tab2:
        st.subheader("Detect Outliers (IQR Method)")
        outlier_summary = detect_outliers(df)
        st.write("Outlier counts per numeric column:")
        st.json(outlier_summary)

        if st.button("Remove Outliers"):
            cleaned = remove_outliers(df)
            st.success("✅ Outliers removed successfully!")
            st.dataframe(cleaned.head())
            st.download_button(
                "📥 Download Without Outliers",
                cleaned.to_csv(index=False).encode("utf-8"),
                "no_outliers.csv",
                "text/csv"
            )

    # ---------- TAB 3: DATA PROFILING ----------
    with tab3:
        st.subheader("Automated Data Profiling Report")
        if st.button("Generate Profiling Report"):
            report_path = generate_profile(df)
            st.success("📊 Profiling report generated successfully!")
            st.markdown(f"[Click here to view report]({report_path})", unsafe_allow_html=True)