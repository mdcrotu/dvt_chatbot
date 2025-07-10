import requests
import json
import time
import argparse
from urllib.parse import urljoin, urlparse
from uuid import uuid4
from bs4 import BeautifulSoup

BASE_URL = "https://eda.amiq.com/documentation/eclipse/sv/index.html"
visited = set()
collected = []

def extract_links(soup, base_url):
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#"):
            continue
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.append(full_url)
    return list(set(links))

def clean_text(soup):
    for tag in soup(["script", "style", "header", "nav", "aside", "footer", "form"]):
        tag.decompose()

    main = soup.find("main") or soup.find("div", class_="content") or soup
    h1 = main.find("h1")
    section = h1.get_text(strip=True) if h1 else ""

    text = main.get_text(separator=" ", strip=True)
    import re
    text = re.sub(r"\s+", " ", text)
    words = text.split()
    if len(words) > 300:
        text = " ".join(words[:300]) + "…"

    return section, text

def extract_title(soup):
    title_tag = soup.find("title")
    return title_tag.get_text(strip=True) if title_tag else "Untitled"

def scrape_page(url):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = extract_title(soup)
        section, content = clean_text(soup)
        tokens = len(content.split())
        collected.append({
            "id": str(uuid4()),
            "title": title,
            "url": url,
            "section": section,
            "content": content,
            "section_path": [],
            "tokens": tokens,
            "source": "scraped"
        })
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def scrape_site(start_url, max_pages=100, delay=0.5):
    to_visit = [start_url]
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        print(f"Scraping: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            scrape_page(url)
            links = extract_links(soup, url)
            for link in links:
                if link not in visited and len(visited) < max_pages:
                    to_visit.append(link)
            time.sleep(delay)
        except Exception as e:
            print(f"Error visiting {url}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dvt_guide_data.json")
    parser.add_argument("--start_url", default=BASE_URL)
    parser.add_argument("--max_pages", type=int, default=100)
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    scrape_site(args.start_url, args.max_pages, args.delay)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)
    print(f"\nScraped {len(collected)} pages into {args.output}")

if __name__ == "__main__":
    main()
