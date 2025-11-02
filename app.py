import streamlit as st
import pandas as pd
from io import BytesIO
from utils.data_cleaner import clean_data, detect_outliers, remove_outliers
from utils.data_profile import generate_profile
import os

st.set_page_config(page_title='DataScrub - CSV Data Cleaner', layout='wide')
st.title('🧹 DataScrub — CSV Data Cleaner')
st.write('Clean, analyze, and download your dataset easily!')

uploaded_file = st.file_uploader('📤 Upload CSV or Excel file', type=['csv', 'xlsx'])

def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f'Failed to read file: {e}')
        st.stop()

    tab1, tab2, tab3 = st.tabs(['🧼 Clean Data', '📈 Outlier Detection', '🧠 Profiling Report'])

    with tab1:
        st.subheader('Dataset Overview')
        st.dataframe(df.head())
        st.info(f'Rows: {df.shape[0]} | Columns: {df.shape[1]}')

        remove_duplicates = st.checkbox('Remove Duplicates', True)
        handle_missing = st.selectbox(
            'Handle Missing Values',
            ['Do Nothing', 'Drop Rows', 'Fill with Mean', 'Fill with Median', 'Fill with 0']
        )

        if st.button('Clean Data'):
            clean_df = clean_data(df, remove_duplicates, handle_missing)
            st.success('✅ Data cleaned successfully!')
            st.dataframe(clean_df.head())

            csv_bytes = clean_df.to_csv(index=False).encode('utf-8')
            st.download_button('📥 Download Cleaned CSV', data=csv_bytes, file_name='cleaned_data.csv', mime='text/csv')

            excel_bytes = to_excel_bytes(clean_df)
            st.download_button('📊 Download as Excel', data=excel_bytes, file_name='cleaned_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    with tab2:
        st.subheader('Detect Outliers (IQR Method)')
        outlier_summary = detect_outliers(df)
        st.write('Outlier counts per numeric column:')
        st.json(outlier_summary)

        if st.button('Remove Outliers'):
            cleaned = remove_outliers(df)
            st.success('✅ Outliers removed successfully!')
            st.dataframe(cleaned.head())
            csv_bytes = cleaned.to_csv(index=False).encode('utf-8')
            st.download_button('📥 Download Without Outliers', data=csv_bytes, file_name='no_outliers.csv', mime='text/csv')

    with tab3:
        st.subheader('Automated Data Profiling Report')
        if st.button('Generate Profiling Report'):
            out_path = 'profile_report.html'
            try:
                generate_profile(df, output_path=out_path)
                st.success('📊 Profiling report generated successfully!')
                with open(out_path, 'rb') as f:
                    html_bytes = f.read()
                st.download_button('📥 Download Profiling Report (HTML)', data=html_bytes, file_name='profile_report.html', mime='text/html')
                # Show small preview
                st.markdown('**Preview (first 2000 chars):**')
                st.code(open(out_path, 'r', encoding="utf-8").read()[:2000])
            except Exception as e:
                st.error(f'Failed to generate profile: {e}')


# Footer
st.markdown('---')
st.markdown('Made with ❤️ by Pratham Kataria')
