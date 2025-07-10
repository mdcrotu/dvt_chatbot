import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
import argparse

# Constants
BASE_URL = "https://eda.amiq.com/documentation/eclipse/sv/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_FILE = os.path.join(SCRIPT_DIR, "..", "dvt_guide_seeds.txt")
OUTPUT_FILE = "dvt_chatbot/data/guide.json"
DELAY = 0.5  # polite crawling delay in seconds

# Initialize embedder
embedder = SentenceTransformer("all-MiniLM-L6-v2")

visited = set()
guide_data = []

def is_valid_url(url):
    return url.startswith(BASE_URL) and url.endswith(".html")

def clean_text(soup):
    # Remove navigation, footer, headers
    for tag in soup(['nav', 'header', 'footer', 'script', 'style']):
        tag.decompose()

    # Remove TOC/sidebar/menu links and repetitive junk
    for div in soup.find_all("div", class_=["navheader", "navfooter", "toc-header"]):
        div.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else url
        content = clean_text(soup)
        embedding = embedder.encode(content).tolist()

        guide_data.append({
            "title": title,
            "url": url,
            "content": content,
            "embedding": embedding
        })
        print(f"✅ Scraped: {url}")

        # Discover and follow internal links
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if is_valid_url(link) and link not in visited:
                visited.add(link)
                time.sleep(DELAY)
                scrape_page(link)

    except Exception as e:
        print(f"⚠️ Failed to scrape {url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scrape DVT SystemVerilog Guide")
    parser.add_argument("--max", type=int, default=None, help="Maximum number of pages to scrape")
    args = parser.parse_args()

    scraped_urls = set()

    # Load existing data if present
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                guide_data.extend(existing_data)
                for entry in existing_data:
                    url = entry.get("url")
                    if url:
                        scraped_urls.add(url)
                        visited.add(url)
                print(f"🔄 Resuming from {len(existing_data)} previously scraped entries.")
            except json.JSONDecodeError:
                print("⚠️ Warning: Could not decode existing output file. Starting fresh.")
    else:
        print("🆕 Starting fresh scrape.")

    if not os.path.exists(SEED_FILE):
        print(f"❌ Seed file '{SEED_FILE}' not found.")
        return

    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    count = len(guide_data)

    for seed in seeds:
        print(f"args.max {args.max}")
        print(f"count {count}")
        if args.max is not None and count >= args.max:
            print(f"🛑 Reached max limit of {args.max} pages.")
            break
        if not is_valid_url(seed):
            print(f"⚠️ Invalid URL skipped: {seed}")
            continue
        if seed in scraped_urls:
            print(f"⏭️  Already scraped: {seed}")
            continue

        visited.add(seed)
        before = len(guide_data)
        scrape_page(seed)
        count += len(guide_data) - before

        if args.max is not None and count >= args.max:
            print(f"🛑 Reached max limit of {args.max} pages.")
            break

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(guide_data, f, indent=2)

    print(f"\n✅ Done! Total scraped entries: {len(guide_data)}")


if __name__ == "__main__":
    main()
