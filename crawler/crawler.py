import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin

from crawler.parser import parse_html
from crawler.scheduler import URLScheduler
from database.db import Database


# -------------------------------
# NORMALIZE URL
# -------------------------------
def normalize_url(url):
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")


# -------------------------------
# DOMAIN CHECK
# -------------------------------
def is_same_domain(url, base_domain):
    return urlparse(url).netloc == base_domain


# -------------------------------
# FILTER URL
# -------------------------------
def is_valid_url(url, base_domain):
    if not url:
        return False

    if not url.startswith("http"):
        return False

    blocked_keywords = ["logout", "login", "signup", "register"]

    for keyword in blocked_keywords:
        if keyword in url.lower():
            return False

    if not is_same_domain(url, base_domain):
        return False

    return True


# -------------------------------
# FETCH FUNCTION
# -------------------------------
async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except:
        return None


# -------------------------------
# WORKER FUNCTION
# -------------------------------
async def worker(session, scheduler, base_domain, db):
    url = scheduler.get_url()

    if not url:
        return

    print(f"\nCrawling: {url}")

    html = await fetch(session, url)

    if not html:
        return

    data = parse_html(html, url)

    print("Title:", data["title"])

    # ✅ Debug print
    print(f"Saving: {data['url']}")

    # ✅ Save to DB
    db.insert_page(
        url=data["url"],
        title=data["title"],
        content=data["content"]
    )

    # ✅ Process links
    for link in data["links"]:
        absolute_url = urljoin(url, link)
        normalized = normalize_url(absolute_url)

        if is_valid_url(normalized, base_domain):
            scheduler.add_url(normalized)


# -------------------------------
# MAIN CRAWLER
# -------------------------------
async def crawl():
    scheduler = URLScheduler()
    db = Database()  # ✅ initialize DB

    seed_url = "https://quotes.toscrape.com"
    base_domain = "quotes.toscrape.com"

    scheduler.add_url(seed_url)

    async with aiohttp.ClientSession() as session:

        max_pages = 20
        concurrency = 5

        count = 0

        while scheduler.has_urls() and count < max_pages:

            tasks = []

            for _ in range(concurrency):
                if not scheduler.has_urls():
                    break

                tasks.append(worker(session, scheduler, base_domain, db))
                count += 1

            await asyncio.gather(*tasks)

    db.close()  # ✅ close DB connection


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    asyncio.run(crawl())