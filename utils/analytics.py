# from pandas_profiling import ProfileReport
import pandas as pd
from generateEDA import filterHTML

def show():
    df = pd.read_csv('data/melb_data.csv')
    print(df)
    filterHTML(df)
    # profile = ProfileReport(df, title="Pandas Profiling Report")
    # html = profile.to_html()
    # with open('templates/report.html', 'w') as f:
    #     f.write(str(html))
show()