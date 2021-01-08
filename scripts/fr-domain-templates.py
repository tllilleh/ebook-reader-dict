import requests
from bs4 import BeautifulSoup


ROOT = "https://fr.wiktionary.org"
START_URL = (
    "https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Mod%C3%A8les_de_th%C3%A9matique"
)
NEXTPAGE_TEXT = "page suivante"


def get_soup(url):
    req = requests.get(url)
    page = req.content
    return BeautifulSoup(page, features="html.parser")


def process_category_page(url, results):
    soup = get_soup(url)

    nextpage = ""
    nextpage_div = soup.find(id="mw-pages")
    last_link = nextpage_div.find_all("a")[-1]
    if NEXTPAGE_TEXT == last_link.text:
        nextpage = ROOT + last_link.get("href")

    content_div = soup.find("div", "mw-category-generated")
    lis = content_div.find_all("li")
    for li in lis:
        template_url = ROOT + li.find("a").get("href")
        template_name = li.text.split(":")[1]
        template_soup = get_soup(template_url)
        parser_output = template_soup.find("span", {"class": ["term", "texte"]})
        rendering = parser_output.text
        if template_name and rendering:
            results[template_name] = rendering.strip("()")
    return nextpage


next_page_url = START_URL
results = {}

while next_page_url:
    next_page_url = process_category_page(next_page_url, results)

print("domain_templates = {")
for t, r in results.items():
    print(f'    "{t}": "{r}",')
print(f"}}  # {len(results):,}")