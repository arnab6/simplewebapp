from fastapi import FastAPI, Query, Body
from typing import Optional, Dict
import requests
from lxml import html

app = FastAPI()

# Preloaded URLs for the original /scrape API
urls_with_names = [
    ('DL',
     'https://mettl.com/analytics/share-report?key=I4X4nHy4ryO9YaD%2B%2BU%2BpeQ%3D%3D'
     ),
    ('NLP',
     'https://mettl.com/analytics/share-report?key=EUND5FZzQ1DxnqUGIc8jLw%3D%3D'
     ),
    ('DRL',
     'https://mettl.com/analytics/share-report?key=gSZNDDOqJLiBQ8L%2FsHkqpA%3D%3D'
     ),
    ('IR',
     'https://mettl.com/analytics/share-report?key=6hTwAmY5Mrk59NR4AMEDlg%3D%3D'
     )
]

def fetch_page_content(url):
    """Fetches page content using GET request."""
    response = requests.get(url)
    response.raise_for_status()
    return html.fromstring(response.content)

def extract_text(tree, xpath):
    """Extracts text from the provided tree using given XPath."""
    elements = tree.xpath(xpath)
    return elements[0].strip() if elements else None

# Original FastAPI route to scrape the preloaded URLs
@app.get("/scrape")
def scrape_urls():
    results = []
    
    for name, url in urls_with_names:
        try:
            tree = fetch_page_content(url)

            # Define XPaths for required elements
            percentile_xpath = '/html/body/main/div[1]/div[2]/div/div[4]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/span[1]/text()'
            marks_xpath = '/html/body/main/div[1]/div[2]/div/div[4]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span/text()'

            percent = extract_text(tree, percentile_xpath) or 'Percentile information not found'
            marks = extract_text(tree, marks_xpath) or 'Marks information not found'

            results.append({
                "name": name,
                "percentile": percent,
                "marks": marks
            })
        except requests.RequestException as e:
            results.append({
                "name": name,
                "error": f"Failed to retrieve the webpage. Error: {e}"
            })
    
    return results

# New dynamic FastAPI route to scrape URLs provided via JSON
@app.post("/scrape_v1")
def scrape_v1(data: Dict[str, str] = Body(...)):
    results = []
    
    for subject, url in data.items():
        try:
            tree = fetch_page_content(url)

            # Define XPaths for required elements
            percentile_xpath = '/html/body/main/div[1]/div[2]/div/div[4]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/span[1]/text()'
            marks_xpath = '/html/body/main/div[1]/div[2]/div/div[4]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span/text()'

            percent = extract_text(tree, percentile_xpath) or 'Percentile information not found'
            marks = extract_text(tree, marks_xpath) or 'Marks information not found'

            results.append({
                "subject": subject,
                "percentile": percent,
                "marks": marks
            })
        except requests.RequestException as e:
            results.append({
                "subject": subject,
                "error": f"Failed to retrieve the webpage. Error: {e}"
            })
    
    return results

# Original FastAPI route
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
