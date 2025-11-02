from ydata_profiling import ProfileReport

def generate_profile(df, output_path='profile_report.html'):
    profile = ProfileReport(df, title='Data Profiling Report', explorative=True)
    profile.to_file(output_path)
    return output_path
