import requests
import eventlet
from bs4 import BeautifulSoup
from urllib.parse import urlparse

#TODO make it work for telegraph and time

class Scraper:
    @staticmethod
    def scrap_data(url):
        # print("Scraping:", url)
        site_name = Scraper._extract_site_name(url)

        source = requests.get(url, timeout=20)
        # if not source:
        #     f = open('../prepared_data/scrapproof.txt', 'a')
        #     f.write("timed out: " + url + '\n')
        #     print('timed out', url)
        #     raise ConnectionError

        # print(source) # uncomment to check why site is not available
        soup = BeautifulSoup(source.text, 'html.parser')
        # print("got html for", url)
        article_container = Scraper._extract_article_container(soup, url)
        title = ''  # TODO
        # title = Scraper._extract_title(article_container, url)
        article_paragraphs = Scraper._extract_article(article_container, url)

        # print('Scrapped', url)
        return site_name, title, article_paragraphs

    @staticmethod
    def _extract_site_name(url):
        parsed = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed)
        return domain

    @staticmethod
    def _extract_article_container(soup, url):
        if soup.find('div', {'class': 'post'}):
            return soup.find('div', {'class': 'post'})

        if soup.find('div', {'class': 'article-container'}):
            return soup.find('div', {'class': 'article-container'})

        if soup.find('div', {'class': 'article-text'}):
            return soup.find('div', {'class': 'article-text'})

        if soup.find('article', {'class': 'a-main'}):
            return soup.find('article', {'class': 'a-main'})

        if soup.find('div', {'class': 'js-article-inner'}):
            return soup.find('div', {'class': 'js-article-inner'})

        if soup.article:
            return soup.article

        if soup.find('div', {'class': 'story-body'}):
            return soup.find('div', {'class': 'story-body'})

        if soup.find('div', {'id': 'content-start'}):
            return soup.find('div', {'id': 'content-start'})

        if soup.find('div', {'class': 'entry-content'}):
            return soup.find('div', {'class': 'entry-content'})

        if soup.find('div', {'class': 'td-post-content'}):
            return soup.find('div', {'class': 'td-post-content'})

        if soup.find('div', {'class': 'theiaPostSlider_slides'}):
            return soup.find('div', {'class': 'theiaPostSlider_slides'})

        f = open('../prepared_data/scrapproof.txt', 'a')
        f.write("article container: " + url + '\n')
        print("article container error")
        raise ConnectionError

    @staticmethod
    def _extract_title(article, url):
        if article.h1:
            return article.h1.getText()

        if article.h2:
            return article.h2.getText()

        if article.header:
            return article.header.getText()

        f = open('../prepared_data/scrapproof.txt', 'a')
        f.write("title: " + url + '\n')
        print('title error')
        raise ConnectionError

    @staticmethod
    def _extract_article(article, url):
        if article:
            return list(p.get_text().lower() for p in (article.findAll('p') + article.findAll('span')))
        else:
            f = open('../prepared_data/scrapproof.txt', 'a')
            f.write("paragraphs: " + url + '\n')
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
