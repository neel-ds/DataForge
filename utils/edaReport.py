from pandas_profiling import ProfileReport

def edaReport(df):
    profile = ProfileReport(df, title="Pandas Profiling Report")
    profile.to_file("./templates/report.html")