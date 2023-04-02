from pandas_profiling import ProfileReport

def show(df):
    profile = ProfileReport(df, title="Pandas Profiling Report")
    html = profile.to_html()
    with open('templates/report.html', 'w') as f:
        f.write(str(html))