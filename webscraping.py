from bs4 import BeautifulSoup
import requests
import os
import time

# from requests_html import HTMLSession

import pandas as pd


def export_to_html(df):
    html: str = df.to_html(index=0, sparsify=0, render_links=1, escape=0, classes=['table', 'table-striped', 'table-dark'])
    css = """
        <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" 
            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <style>
            a, a:hover, a:visited{
                color: #fff;
            }
            .title {
                font-size:16px;
                font-weight:normal;
                color: black;
            }            
        </style>
        </head>
        """
    # a: link, a: visited
    # {
    #     text - decoration: none;
    # color:  # fff
    # }
    #
    # a: hover, a: active
    # {
    #     text - decoration: underline;
    # color:  # fff
    # }
    html = css + html

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)


def add_readable_html(link):
    print('get')
    source = requests.get(f'https://{link}').text
    soup = BeautifulSoup(source, 'lxml')
    print('got')
    if soup:
        return soup
    # TODO rendering purepc
    # else:
    #     session = HTMLSession()
    #     r = session.get(f'https://{link}')
    #     r.html.render()
    #     print(r.html)
    #     return r.html


def write_header_to_dict(dictionary, site_address):
    dictionary['Title'].append(f'<h2>{site_address}</h2>')
    dictionary['Desc'].append(f'<h2>{site_address}</h2>')


class Article:
    def __init__(self, path):
        print(f'Start: {path}')
        self.path = path
        self.items = {'Title': [], 'Desc': []}
        self.soup = add_readable_html(path)

        write_header_to_dict(self.items, self.path)

    def add_article(self, title, link, desc):
        link = f'https://{self.path}{link}'
        self.items['Title'].append(f'<a href={link} target="_blank" ><h5>{title}<h5></a>')
        self.items['Desc'].append(desc)

    def get_dataframe(self):
        return pd.DataFrame(self.items)


def newonce():
    site = Article('newonce.net')
    result = site.soup.find('div', class_='Feed_feedTiles__Syqo9')
    articles = result.find_all('div', class_='ArticleTile_tile__2EkYa')
    for article in articles:
        title = article.find('img')['alt']
        link = article.find('a')['href']
        desc = ''
        site.add_article(title, link, desc)

    return site.get_dataframe()


def gry_online():
    site = Article('gry-online.pl/newsroom/news/')

    articles = site.soup.find_all('div', class_='box')

    for article in articles:
        title = article.find('h5').text
        link = article.find('a')['href']
        desc = article.find('p', class_='').text
        site.add_article(title, link, desc)

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
        path = 'donald.pl/news'
        site = Article(path)

        # for big first
        articles = site.soup.find('div', class_='sc-1ucdnva-0')
        title = articles.find('h3').text
        link = articles.find('a')['href']
        desc = ''
        site.add_article(title, link, desc)

        # for the rest
        articles = site.soup.find_all('div', class_='sc-1uxgugq-5')
        for article in articles:
            title = article.find('a').text
            link = article.find('a')['href']
            desc = ''
            site.add_article(title, link, desc)

        return site.get_dataframe()

    def main_site():
        site = Article('donald.pl')
        articles = site.soup.find_all('div', class_='sc-1sp7ghq-0')

        for article in articles:
            title = article.find('div', class_='hys1q5-0').text
            link = article.find('a')['href']
            desc = article.find('div', 'sc-1sp7ghq-7').text
            site.add_article(title, link, desc)

        return site.get_dataframe()

    all_sites = pd.concat((news(), main_site()))

    return all_sites


if __name__ == '__main__':
    articles_tuple = (
        newonce(),
        gry_online(),
        # purepc(),
        donald(),
    )
    all_articles = pd.concat(articles_tuple)
    export_to_html(all_articles)

    os.system(".\\index.html")
    time.sleep(5)
    os.remove(".\\index.html")
