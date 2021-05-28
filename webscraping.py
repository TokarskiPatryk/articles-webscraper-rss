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


def newonce():
    items = {'Title': [], 'Desc':[], 'Link': []}
    path = 'newonce.net'
    soup = add_readable_html(path)

    result = soup.find('div', class_='Feed_feedTiles__Syqo9')
    articles = result.find_all('div', class_='ArticleTile_tile__2EkYa')

    write_header_to_dict(items, path)

    for article in articles:
        article_link = article.find('a')['href']
        article_link = f'https://www.{path}{article_link}'
        article_title = article.find('img')['alt']

        items['Title'].append(article_title)
        items['Link'].append(article_link)
        items['Desc'].append('')
    return pd.DataFrame(items)


def gry_online():
    items = {'Title': [], 'Desc': [], 'Link': []}
    path = 'gry-online.pl/newsroom/news/'
    soup = add_readable_html(path)

    articles = soup.find_all('div', class_='box')

    write_header_to_dict(items, path)

    for article in articles:
        article_link = article.find('a')['href']
        article_link = f'https://www.{path}{article_link}'
        article_title = article.find('h5').text
        article_desc = article.find_all('p')[1].text

        items['Title'].append(article_title)
        items['Link'].append(article_link)
        items['Desc'].append(article_desc)

    return pd.DataFrame(items)


con = (
    newonce(),
    gry_online()
)
result = pd.concat(con)

export_to_html(result)

os.system(".\\articles\\index.html")


