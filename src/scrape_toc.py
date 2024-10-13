import requests
from bs4 import BeautifulSoup
import openpyxl
import time

from datetime import datetime

# Function to save scraped content to Excel
def save_to_excel(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Create a timestamp
    filename = f'theory_of_change_content_{timestamp}.xlsx'  # Append timestamp to filename
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Theory of Change Content"
    sheet.append(["Link", "Content"])  # Header

    for link, text in data:
        sheet.append([link, text])

    workbook.save(filename)
    print(f"Results saved to {filename}")


# Function to search for a term and return the results
def search(query, num_pages=50):
    search_url = "https://www.bing.com/search?q=" + query
    links = []

    for page in range(num_pages):
        # Update the URL for pagination (Bing uses the 'first' parameter for pagination)
        paginated_url = f"{search_url}&first={page * 10 + 1}"  # Bing shows 10 results per page
        print(f"Searching on page {page + 1}: {paginated_url}")

        response = requests.get(paginated_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all search result links
        for item in soup.find_all('li', class_='b_algo'):
            link = item.find('a')['href']
            links.append(link)

        time.sleep(2)  # Respectful delay to avoid hitting the server too hard

    return links

# Function to scrape the content from each link
def scrape_content(links):
    content = []
    for link in links:
        print(f"Scraping content from {link}...")
        try:
            response = requests.get(link)
            page_content = BeautifulSoup(response.text, "html.parser")

            # Extract text from the body of the page
            paragraphs = page_content.find_all('p')
            page_text = "\n".join([para.get_text() for para in paragraphs])
            content.append((link, page_text))
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")

        time.sleep(2)  # Respectful delay between requests

    return content

# Function to save scraped content to Excel
def save_to_excel(data, filename='theory_of_change_content.xlsx'):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Theory of Change Content"
    sheet.append(["Link", "Content"])  # Header

    for link, text in data:
        sheet.append([link, text])

    workbook.save(filename)
    print(f"Results saved to {filename}")

# Main execution
if __name__ == "__main__":
    query = "Theory of Change"
    print(f"Searching for '{query}'...")

    # Search and get links
    links = search(query, num_pages=50)
    print(f"Found {len(links)} links.")

    # Scrape content from the found links
    content = scrape_content(links)

    # Save results to Excel
    save_to_excel(content)
