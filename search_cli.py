from search_engine import search_guide

def main():
    print("🔍 DVT Guide Search CLI")
    print("Type your query below (type 'exit' to quit):")
    while True:
        query = input("> ")
        if query.strip().lower() in ('exit', 'quit'):
            break
        results = search_guide(query)
        if not results:
            print("No results found.")
        for score, title, url, content in results:
            print(f"[{score:.2f}] {title} → {url}")
            print(content.strip().split('\n')[0][:200] + "...")
            print("-" * 80)

if __name__ == "__main__":
    main()
