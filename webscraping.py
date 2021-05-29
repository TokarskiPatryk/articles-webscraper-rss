from bs4 import BeautifulSoup
import requests
import os
import json

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

    path = "articles/"
    if not os.path.exists(path):
        os.makedirs(path)
    # TODO add datetime and changing filename
    path += 'index.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def exporting_to_json(list_of_articles, filename):
    path = "articles/"
    if not os.path.exists(path):
        os.makedirs(path)
    # TODO add datetime and changing filename
    path += filename

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(list_of_articles, f, ensure_ascii=False, indent=2)


def add_readable_html(link):
    source = requests.get(f'https://{link}').text
    soup = BeautifulSoup(source, 'lxml')
    return soup


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
        # self.articles = []

        write_header_to_dict(self.items, self.path)

    def add_article(self, title, link, desc=''):
        self.items['Title'].append(title)
        self.items['Link'].append(link)
        self.items['Desc'].append(desc)

    def get_dataframe(self):
        return pd.DataFrame(self.items)

    # TODO add loop for articles
    # def loop(self, title, link, desc):
    #     for article in self.articles:
    #         article_desc = desc()
    #         article_link = link()
    #         article_title = title()
    #
    #         self.add_article(article_title, article_link)


def newonce():
    site = Article('newonce.net')
    result = site.soup.find('div', class_='Feed_feedTiles__Syqo9')
    articles = result.find_all('div', class_='ArticleTile_tile__2EkYa')

    for article in articles:
        article_link = article.find('a')['href']
        article_link = f'https://www.{site.path}{article_link}'
        article_title = article.find('img')['alt']

        site.add_article(article_title, article_link)

    return site.get_dataframe()


@property
def gry_online():
    site = Article('gry-online.pl/newsroom/news/')

    articles = site.soup.find_all('div', class_='box')

    for article in articles:
        article_link = article.find('a')['href']
        article_link = f'https://www.{site.path}{article_link}'
        article_title = article.find('h5').text
        article_desc = article.find_all('p')[1].text

        site.add_article(article_title, article_link, article_desc)

    return site.get_dataframe()


if __name__ == '__main__':
    articles_tuple = (
        newonce(),
        gry_online(),
    )
    all_articles = pd.concat(articles_tuple)
    export_to_html(all_articles)

    os.system(".\\articles\\index.html")
