from bs4 import BeautifulSoup
import requests
import os
import time
import pandas as pd
print('imported libraries')


def export_to_html_file(df):
    html: str = df.to_html(index=0, sparsify=0, render_links=1, escape=0,
                           classes=['table', 'table-striped', 'table-dark'])
    css = """
        <head>
        <title>Shorter</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" 
            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <style>
            a, a:hover, a:visited{
                color: #fff;
            }   
            h2 {
                font-weight:bold;
            }       
        </style>
        </head>
        """
    html = css + html

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)


def add_readable_html(link, features):
    source = requests.get(f'https://{link}').content
    soup = BeautifulSoup(source, features=features)
    return soup


def write_header_to_dict(dictionary, site_address):
    dictionary['Title'].append(f'<h2><a href=https://{site_address} >{site_address}<a></h2>')
    dictionary['Desc'].append(f'<h2><a href=https://{site_address} >{site_address}<a></h2>')


class Article:
    def __init__(self, path,  extension='', features='lxml'):
        print(f'Start: {path}')
        self.path = path
        self.extension = extension
        self.img = ''
        self.items = {'Title': [], 'Desc': []}
        self.soup = add_readable_html(path+extension, features)

        write_header_to_dict(self.items, path)

    def add_article(self, title, link, desc, img='', extension_for_article=''):
        if extension_for_article:
            link = f'https://{self.path}{self.extension}{link}'
        else:
            link = f'https://{self.path}{extension_for_article}{link}'
        if img:
            self.img = f'<br><br><img src={img} height=200px>'
        self.items['Title'].append(f'<a target="_blank" href={link} > <h4>{title} {self.img}<h4></a>')
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
        img = article.find('img')['src']

        site.add_article(title, link, desc, img)

    return site.get_dataframe()


def gry_online():
    site = Article('gry-online.pl', '/newsroom/news/')

    articles = site.soup.find_all('div', class_='box')

    for article in articles:
        title = article.find('h5').text
        link = article.find('a')['href']
        desc = article.find('p', class_='').text

        site.add_article(title, link, desc)

    return site.get_dataframe()


def donald():
    def news():
        site = Article('donald.pl', '/news')

        articles = site.soup.find_all('div', class_='sc-1uxgugq-5')
        for article in articles:
            title = article.find('a').text
            link = article.find('a')['href']
            desc = ''
            site.add_article(title, link, desc)

        return site.get_dataframe()

    def main_site():
        site = Article('donald.pl')

        # top 1
        top_articles = site.soup.find('div', class_='sc-23vgyc-1 bFvgnQ')

        article = top_articles.find('div', 'sc-23vgyc-3 fDSkTO')

        title = article.find('h2').text
        link = article.find('a')['href']
        desc = ''
        img = article.find('img')['data-src']

        site.add_article(title, link, desc, img)

        # 2 on the side
        articles = top_articles.find('div', class_='sc-23vgyc-4 ihtiRV')
        articles = articles.find_all('li', class_='sc-1uxgugq-0 hiiSmU')
        for article in articles:
            title = article.find('h3').text
            link = article.find('a')['href']
            desc = ''
            img = article.find('img')['data-src']

            site.add_article(title, link, desc, img)

        # rest
        articles = site.soup.find_all('div', class_='sc-1sp7ghq-0')
        for article in articles:
            title = article.find('div', class_='hys1q5-0').text
            link = article.find('a')['href']
            desc = article.find('div', 'sc-1sp7ghq-7').text
            img = article.find('img')['data-src']

            site.add_article(title, link, desc, img)

        return site.get_dataframe()

    all_sites = pd.concat((news(), main_site()))

    return all_sites


def purepc():
    site = Article('purepc.pl', '/rss_all.xml', 'html.parser')
    title = [x.get_text() for x in site.soup.find_all('title')]
    title = title[2:]

    link = [x.get_text() for x in site.soup.find_all('link')]
    link = link[2:]

    desc = [x.get_text() for x in site.soup.find_all('description')]
    desc = desc[1:]

    img = site.soup.find_all('enclosure')
    img = map(lambda n: n['url'], img)
    img2 = list(img)

    for index in range(len(title)):
        site.add_article(title[index], link[index], desc[index], img2[index])

    return site.get_dataframe()


def xkcd():
    site = Article('xkcd.com', '/rss.xml', 'html.parser')
    result = site.soup.find('item')
    title = result.find('title').text
    link = result.find('link').text
    img = result.find('description').text
    site.add_article(title, link, img)

    return site.get_dataframe()


if __name__ == '__main__':
    articles_tuple = (
        xkcd(),
        newonce(),
        purepc(),
        donald(),
        gry_online(),
    )
    all_articles = pd.concat(articles_tuple)
    export_to_html_file(all_articles)

    os.system(".\\index.html")
    time.sleep(5)
    os.remove(".\\index.html")


# for tests only

# if __name__ == '__main__':
#     export_to_html_file(xkcd())
#
#     os.system(".\\index.html")
#     time.sleep(5)
#     os.remove(".\\index.html")
