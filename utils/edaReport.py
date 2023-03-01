from pandas_profiling import ProfileReport

def edaReport(df):
    profile = ProfileReport(df, title="Pandas Profiling Report")
    # return html file 
    return profile.to_html()