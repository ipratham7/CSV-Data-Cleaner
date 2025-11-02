import pandas as pd
import numpy as np

def clean_data(df, remove_duplicates=True, handle_missing='Do Nothing'):
    clean_df = df.copy()

    # Remove duplicates
    if remove_duplicates:
        clean_df = clean_df.drop_duplicates()

    # Handle missing values
    if handle_missing == 'Drop Rows':
        clean_df = clean_df.dropna()
    elif handle_missing == 'Fill with Mean':
        clean_df = clean_df.fillna(clean_df.mean(numeric_only=True))
    elif handle_missing == 'Fill with Median':
        clean_df = clean_df.fillna(clean_df.median(numeric_only=True))
    elif handle_missing == 'Fill with 0':
        clean_df = clean_df.fillna(0)

    return clean_df


def detect_outliers(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    outlier_summary = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_summary[col] = int(len(outliers))

    return outlier_summary


def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=np.number).columns
    filtered = df.copy()
    for col in numeric_cols:
        Q1 = filtered[col].quantile(0.25)
        Q3 = filtered[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        filtered = filtered[(filtered[col] >= lower) & (filtered[col] <= upper)]
    return filtered
