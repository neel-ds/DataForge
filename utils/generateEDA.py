from bs4 import BeautifulSoup
from pandas_profiling import ProfileReport

def filterHTML(df):
    profile = ProfileReport(df, title="Pandas Profiling Report")
    html = profile.to_html()

    soup = BeautifulSoup(html, 'html.parser')
    # Find the element you want to replace with class
    element_to_replace = soup.find('a', {'class': 'navbar-brand anchor'})

    # Replace the element's content with new content
    new_content = 'DataForge EDA Report'
    element_to_replace.string.replace_with(new_content)


    element_to_replace = soup.find('p', {'class': 'text-muted text-center'})
    element_to_replace.extract()

    # Save the new HTML in a templates folder with report.html
    with open('templates/report.html', 'w') as f:
        f.write(str(soup))
