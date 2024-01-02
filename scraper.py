import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote

def download_pdfs(url, visited_urls=set(), downloaded_pdfs=set()):
    #check if the URL has already been visited to avoid infinite loops
    if url in visited_urls:
        return

    #adds current URL to the set of visited URLs
    visited_urls.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        #finds all links on current page
        links = soup.find_all('a', href=True)

        for link in links:
            absolute_url = urljoin(url, link['href'])

            #checks if the link points to a PDF file
            if absolute_url.lower().endswith('.pdf'):
                #checks if the PDF was already been downloaded
                if absolute_url in downloaded_pdfs:
                    continue

                print(f"Downloading PDF: {absolute_url}")

                #create the 'downloaded_pdfs' directory if it doesn't exist
                os.makedirs("downloaded_pdfs", exist_ok=True)

                #extract filename from URL and unquote it
                filename = unquote(os.path.basename(absolute_url))
                
                #save the PDF content to a file
                with open(f"downloaded_pdfs/{filename}", 'wb') as pdf_file:
                    pdf_file.write(requests.get(absolute_url).content)

                #add the downloaded PDF to the set
                downloaded_pdfs.add(absolute_url)

            else:
                #recursively visit other links on the page
                parsed_url = urlparse(absolute_url)
                if parsed_url.netloc == urlparse(url).netloc:
                    download_pdfs(absolute_url, visited_urls, downloaded_pdfs)

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")

if __name__ == "__main__":
    start_url = "https://WEBSITE.org/"
    download_pdfs(start_url)
