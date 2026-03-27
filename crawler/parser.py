from bs4 import BeautifulSoup


def parse_html(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string if soup.title else "No title"

    content = soup.get_text(separator=" ", strip=True)

    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])

    return {
        "url": url,
        "title": title,
        "content": content,
        "links": links
    }