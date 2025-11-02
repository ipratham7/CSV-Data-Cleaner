# DataScrub

**DataScrub** — CSV Data Cleaner (Open-source Streamlit app)

An easy-to-use Streamlit app to clean, profile, and export datasets.
Includes:
- Remove duplicates, handle missing values, detect & remove outliers (IQR)
- Generate automated data profiling report (ydata-profiling)
- Supports CSV and Excel formats
- Simple UI with tabs for cleaning, outlier detection, and profiling

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```
DataScrub/
├── app.py
├── requirements.txt
├── utils/
│   ├── data_cleaner.py
│   └── data_profile.py
├── sample_data/sample_sales_messy.csv
└── README.md
```

## Footer
Made with ❤️ by Pratham Kataria

## License
MIT
