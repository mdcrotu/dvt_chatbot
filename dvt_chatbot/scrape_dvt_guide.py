import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
from uuid import uuid4
import argparse
import os

BASE_URL = "https://eda.amiq.com/documentation/eclipse/sv/index.html"
DOMAIN = "eda.amiq.com"
OUTPUT_FILE = "data/dvt_guide_data.json"

visited = set()
collected = []

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

def extract_links(soup, base_url):
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        if DOMAIN in urlparse(full_url).netloc and full_url.endswith(".html"):
            links.add(full_url)
    return links

def extract_title(soup):
    if soup.title:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    return h1.text.strip() if h1 else "Untitled Section"

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = extract_title(soup)
        content = clean_text(response.text)
        tokens = len(content.split())

        entry = {
            "id": str(uuid4()),
            "title": title,
            "url": url,
            "content": content,
            "section_path": [],  # reserved for future use
            "tokens": tokens,
            "source": "scraped"
        }
        return soup, entry
    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None, None

def crawl(start_url, max_pages=200):
    queue = [start_url]
    count = 0
    while queue and count < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        print(f"[{count+1}] 🧭 Crawling: {url}")
        soup, entry = scrape_page(url)
        visited.add(url)
        if entry:
            collected.append(entry)
            new_links = extract_links(soup, url)
            queue.extend(new_links - visited)
            count += 1
            time.sleep(0.5)  # Be nice to the server

    print(f"\n✅ Finished scraping {len(collected)} pages.")
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=2)
    print(f"📄 Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape the DVT IDE User Guide")
    parser.add_argument("--max", type=int, default=200, help="Maximum number of pages to scrape")
    args = parser.parse_args()
    crawl(BASE_URL, max_pages=args.max)
