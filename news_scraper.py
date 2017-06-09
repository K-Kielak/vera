import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Scraper:
    @staticmethod
    def scrap_data(url):
        print("Scraping:", url)
        site_name = Scraper._extract_site_name(url)
        source = requests.get(url).text
        # print(source) # uncomment to check why site is not available
        soup = BeautifulSoup(source, 'html.parser')
        article_container = Scraper._extract_article_container(soup)
        title = Scraper._extract_title(article_container)
        article_paragraphs = Scraper._extract_article(article_container)

        return site_name, title, article_paragraphs

    @staticmethod
    def _extract_site_name(url):
        parsed = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed)
        return domain

    @staticmethod
    def _extract_article_container(soup):
        if soup.find('div', {'class': 'post'}):
            return soup.find('div', {'class': 'post'})

        if soup.find('div', {'class': 'article-container'}):
            return soup.find('div', {'class': 'article-container'})

        if soup.find('div', {'class': 'article-text'}):
            return soup.find('div', {'class': 'article-text'})

        if soup.find('article', {'class': 'a-main'}):
            return soup.find('article', {'class': 'a-main'})

        if soup.article:
            return soup.article

        if soup.find('div', {'class': 'story-body'}):
            return soup.find('div', {'class': 'story-body'})

        raise ConnectionError

    @staticmethod
    def _extract_title(article):
        if article.h1:
            return article.h1.getText()

        if article.h2:
            return article.h2.getText()

        if article.header:
            return article.header.getText()

        print('title error')
        raise ConnectionError

    @staticmethod
    def _extract_article(article):
        if article:
            return list(p.get_text().lower() for p in (article.findAll('p') + article.findAll('span')))
        else:
            raise ConnectionError

# # TESTS
#
# urls = [
#     'http://edition.cnn.com/2017/06/04/europe/london-terror-attack-new/index.html'
# ]
#
# for url in urls:
#     try:
#         s, t, a = Scraper.scrap_data(url)
#         print(s)
#         print(t)
#         print(a)
#     except ConnectionError:
#         print(url, 'is not available')
