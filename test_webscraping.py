import unittest, webscraping


class AccessTesting(unittest.TestCase):
    def test_access_to_newonce(self):
        site = webscraping.Article('newonce.net')
        self.assertNotEqual(site.soup.text, '')

    def test_access_to_gry_online(self):
        site = webscraping.Article('gry-online.pl/newsroom/news/')
        self.assertNotEqual(site.soup.text, '')

    def test_access_to_purepc(self):
        site = webscraping.Article('purepc.pl/rss_all.xml')
        self.assertNotEqual(site.soup.text, '')

    def test_access_to_donald(self):
        site = webscraping.Article('donald.pl/news')
        self.assertNotEqual(site.soup.text, '')


if __name__ == '__main__':
    unittest.main()
