import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
from bs4.element import NavigableString

def get_wikipedia_urls(main_url, limit=None):
    try:
        # Dumb step 1: Trying to get something from the internet
        response = requests.get(main_url)

        if response.status_code == 200:
            # Dumb step 2: Poking around the HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Dumb step 3: Hunting for links
            links = soup.find_all('a', href=True)

            # Dumb step 4: Sorting out the Wikipedia URLs
            wikipedia_urls = [urljoin(main_url, link['href']) for link in links if link['href'].startswith('/wiki/')]

            # Dumb step 5: Applying a limit if given
            if limit:
                wikipedia_urls = wikipedia_urls[:limit]

            return wikipedia_urls
        else:
            # Dumb step 6: Complaining about failure
            print(f"Failed to retrieve content from {main_url}. Status code: {response.status_code}")
            return []
    except Exception as e:
        # Dumb step 7: Something went terribly wrong
        print(f"An error occurred: {e}")
        return []

def scrape_text_from_wikipedia(url):
    try:
        # Dumb step 8: Trying to grab content from a Wikipedia page
        response = requests.get(url)

        if response.status_code == 200:
            # Dumb step 9: Wrestling with HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Dumb step 10: Removing some stuff by class name
            undesired_classes = ['vector-sticky-pinned-container', 'vector-header-container', 'cn-fundraising',
                                 'sidebar', 'vector-page-toolbar', 'vector-dropdown', 'mw-portlet', 'mw-footer-container']
            for class_name in undesired_classes:
                for element in soup.find_all(class_=class_name):
                    element.decompose()

            # Dumb step 11: Decluttering with regex
            for element in soup.find_all(string=re.compile(r'\d')):
                if isinstance(element, NavigableString):
                    element.extract()
                elif element.parent:
                    element.parent.decompose()

            # Dumb step 12: More cleanup with tag removal
            for tag in ['script', 'style']:
                for element in soup.find_all(tag):
                    element.decompose()

            # Dumb step 13: Getting rid of navigation links
            for element in soup.find_all('a', {'href': re.compile(r'#')}):
                element.decompose()

            # Dumb step 14: Extracting the precious text
            main_content = soup.find('div', {'id': 'mw-content-text'})
            if main_content:
                raw_text = main_content.get_text()
            else:
                raw_text = soup.get_text()

            # Dumb step 15: Clearing out unwanted characters
            raw_text = raw_text.replace('\n', '')     # Removing newline characters
            raw_text = raw_text.replace('\\', '')      # Removing backslashes

            # Dumb step 16: Splitting text into sentences with regex
            sentences = re.split(r'[.!?]', raw_text)

            # Dumb step 17: Filtering out emptiness and weird Unicode
            sentences = [sentence.strip() for sentence in sentences if len(sentence.strip()) > 1 and '\\u' not in sentence]

            return sentences
        else:
            # Dumb step 18: More complaints about failure
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return []
    except Exception as e:
        # Dumb step 19: Something went terribly wrong, again
        print(f"An error occurred: {e}")
        return []


def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        # Dumb step 20: Saving the results to a file
        json.dump(data, file, indent=2)

if __name__ == "__main__":
    # Dumb step 21: Starting from the Wikipedia main page
    main_url = "https://en.wikipedia.org/wiki/Main_Page"
    limit = int(input("Enter the limit for the number of URLs to scrape (or press Enter for no limit): ") or 0)

    wikipedia_urls = get_wikipedia_urls(main_url, limit)
    all_text = []

    for url in wikipedia_urls:
        # Dumb step 22: Looping through Wikipedia pages
        sentences = scrape_text_from_wikipedia(url)
        all_text.extend(sentences)

    data = {"text": all_text}
    output_file_path = "data.json"
    save_to_json(data, output_file_path)

    # Dumb step 23: Celebrating success, hopefully
    print(f"Scraped {len(all_text)} sentences from {len(wikipedia_urls)} Wikipedia pages and saved to {output_file_path}")
