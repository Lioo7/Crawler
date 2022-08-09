from html.parser import HTMLParser
from urllib import parse


# This class give us all the links from the HTML

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    # if it already a full url, then is going to keep it
                    # but if the value is relative url, in this case, it concatenates the base url
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message: str) -> None:
        pass
