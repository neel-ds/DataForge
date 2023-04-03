# Importing necessary libraries
from bs4 import BeautifulSoup # For parsing HTML
from pandas_profiling import ProfileReport # For creating pandas profiling report

# Function to filter HTML content from pandas profiling report and replace with new content
def filterHTML(df):
    """
    Filters the HTML content of pandas profiling report and replaces it with new content
    
    Parameters:
        - df : input dataframe for which pandas profiling report is to be generated
        
    Returns:
        - None
    """
    profile = ProfileReport(df, title="Pandas Profiling Report") # Generating pandas profiling report for input dataframe
    html = profile.to_html() # Converting pandas profiling report into HTML format

    soup = BeautifulSoup(html, 'html.parser') # Parse the HTML using BeautifulSoup library

    # Find the element you want to replace with class
    element_to_replace = soup.find('a', {'class': 'navbar-brand anchor'})

    # Replace the element's content with new content
    new_content = 'DataForge EDA Report'
    element_to_replace.string.replace_with(new_content)

    # Find the element you want to replace with class
    element_to_replace = soup.find('p', {'class': 'text-muted text-center'})
    element_to_replace.extract() # Remove the element from the HTML content

    # Save the modified HTML content in a templates folder as report.html file
    with open('templates/report.html', 'w') as f:
        f.write(str(soup))