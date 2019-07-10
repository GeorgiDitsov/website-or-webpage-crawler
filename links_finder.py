import re
import requests
from bs4 import BeautifulSoup


class LinksFinder:

    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url

    # Function sends request to the page_url of the base_url website, it takes the source code of the web page
    # With BeautifulSoup library we are pulling the <a> tags which are the links from the page_url
    def get_links(self):
        source_code = requests.get(self.page_url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        links = set()
        for l in soup.findAll('a', attrs={'href': re.compile(self.base_url)}):  # Spider takes only links from the
                                                                                # base_url webite

            links.add(l.get('href'))  # adds all links which are found by the spider, to set()
        return links
