from bs4 import BeautifulSoup
import requests
import os
import json
from time import sleep
from requests_html import HTMLSession

import pandas as pd


def export_to_html(df):
    html: str = df.to_html(index=0, sparsify=0, render_links=1, escape=0)
    css = """
        <head>
        <style>
            .site {
                font-size:20px;
                font-weight:bold;
        
            }
            table {
            
            }
        
        </style>
        </head>
        """

    html = css + html

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)


def exporting_to_json(list_of_articles, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(list_of_articles, f, ensure_ascii=False, indent=2)


def add_readable_html(link):
    source = requests.get(f'https://{link}').text
    soup = BeautifulSoup(source, 'lxml')
    print('got link')
    if soup:
        return soup
    # TODO rendering purepc
    # else:
    #     session = HTMLSession()
    #     r = session.get(f'https://{link}')
    #     r.html.render()
    #     print(r.html)
    #     return r.html


def write_header_to_dict(dictionary, site_adress):
    dictionary['Title'].append(f'<span class="site">{site_adress}</span>')
    dictionary['Desc'].append(f'<span class="site">{site_adress}</span>')
    dictionary['Link'].append(f'<span class="site">{site_adress}</span>')


def write_article(class_, article_title, article_desc, article_link):
    class_.items['Title'].append(article_title)
    class_.items['Link'].append(article_link)
    class_.items['Desc'].append(article_desc)


class Article:

    def __init__(self, path):
        self.path = path
        self.items = {'Title': [], 'Desc': [], 'Link': []}
        self.soup = add_readable_html(path)

        write_header_to_dict(self.items, self.path)

    def add_article(self, title, link, desc):
        self.items['Title'].append(title)
        self.items['Link'].append(link)
        self.items['Desc'].append(desc)

    def get_dataframe(self):
        return pd.DataFrame(self.items)


class Finder:
    def __init__(self, article, site):
        self.find = article.find
        self.find_all = article.find_all
        self.site = site

    def link(self, a, href):
        link = self.find(a)[href]
        return f'https://www.{self.site}{link}'

    def title(self, box):
        return self.find(box)

    def desc(self, div, class_):
        return self.find(div, class_)


def newonce():
    path = 'newonce.net'
    site = Article(path)
    result = site.soup.find('div', class_='Feed_feedTiles__Syqo9')
    articles = result.find_all('div', class_='ArticleTile_tile__2EkYa')

    for article in articles:
        find = Finder(article, path)
        site.add_article(find.title('img')['alt'], find.link('a', 'href'), '')

    return site.get_dataframe()


def gry_online():
    path = 'gry-online.pl/newsroom/news/'
    site = Article(path)

    articles = site.soup.find_all('div', class_='box')

    for article in articles:
        find = Finder(article, path)
        site.add_article(find.title('h5').text, find.link('a', 'href'), find.desc('p', class_='').text)

    return site.get_dataframe()


def purepc():
    site = Article('purepc.pl')
    result = site.soup.find('div', class_='container')
    articles = result.find_all('div', class_='ln_item')

    for article in articles:
        article_title = article.find_all('a')[1]['title']
        article_link = article.find_all('a')[1]['link']
        article_desc = article.find('p').text

        site.add_article(article_title, article_link, article_desc)

    return site.get_dataframe()


def donald():
    def news():
        site = Article('donald.pl/news')

        article_main = site.soup.find('div', class_='sc-1ucdnva-0')
        articles = site.soup.find_all('div', class_='sc-1uxgugq-5')

        main_link = article_main.find('a')['href']
        main_link = f'https://www.{site.path}{main_link}'
        main_title = article_main.find('h3').text
        main_desc = ''
        site.add_article(main_title, main_link, main_desc)

        for article in articles:
            article_link = article.find('a')['href']
            article_link = f'https://www.{site.path}{article_link}'
            article_title = article.find('a').text
            article_desc = ''

            site.add_article(article_title, article_link, article_desc)

        return site.get_dataframe()

    def main_site():
        site = Article('donald.pl')
        articles = site.soup.find_all('div', class_='sc-1sp7ghq-0')

        for article in articles:
            article_link = article.find('a')['href']
            article_link = f'https://www.{site.path}{article_link}'
            article_title = article.find('div', class_='hys1q5-0').text
            article_desc = article.find('div', class_='sc-1sp7ghq-7').text
            site.add_article(article_title, article_link, article_desc)

        return site.get_dataframe()

    all_sites = pd.concat((news(), main_site()))

    return all_sites


if __name__ == '__main__':
    # articles_tuple = (
    #     newonce(),
    #     gry_online(),
    #     # purepc(),
    #     donald(),
    # )
    # all_articles = pd.concat(articles_tuple)
    export_to_html(gry_online())

    os.system(".\\index.html")
    sleep(1)
    os.remove(".\\index.html")
