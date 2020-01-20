import requests
from bs4 import BeautifulSoup
import json
'''
req = requests.get("http://proceedings.mlr.press/v97/")

html = req.text

soup = BeautifulSoup(html, 'html.parser')

my_contents = soup.select(
        '#content > div.wrapper > div.paper > p.links >a:nth-child(1)'
        )

for link in my_contents:
    href = link.attrs['href']
    text = link.string
    print(text, ">", href)
    req_t = requests.get(href)
    html_t = req_t.text
    soup_t = BeautifulSoup(html_t, 'html.parser')
    my_abstract = soup_t.select('#abstract')
    print(my_abstract[0].text)
    #for abstract in my_abstract:
    #    print(abstract.text)

for title in my_contents:
    print(title.text)
'''


class WebPage:
    def __init__(self, link):
        self.req = requests.get(link)
        self.html = self.req.text
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def page_contents(self, selector):
        self.contents_selector = selector

    def get_titles(self, selector):
        self.titles = self.soup.select(self.contents_selector + '>' + selector)
        for title in self.titles:
            print(title.text)

    def ICML_crawling(self, selector):
        self.paper_dict = {}

        index = 1
        mainpage = self.soup.select(selector)
        for link in mainpage:
            href = link.attrs['href']
            # print(link.string, '>', href)

            temp_req = requests.get(href)
            temp_html = temp_req.text
            temp_soup = BeautifulSoup(temp_html, 'html.parser')
            content = temp_soup.select('#content > div.wrapper > article.post-content')[0]

            title = content.find('h1').text
            authors = self.author_parsing(content.find('div', {'id':'authors'}).text)
            info_year = self.info_parsing(content.find('div', {'id':'info'}).text)
            info = info_year[0]
            year = info_year[1]
            abstract = content.find('div', {'id':'abstract'}).text

            paper = {'title':title, 'authors':authors, 'info':info, 'year':year, 'abstract':abstract}
            self.paper_dict[str(index)] = paper
            print(index, title)
            index += 1

    def author_parsing(self, authors):
        author_list = authors.split(',')
        for i in range(len(author_list)):
            author_list[i] = author_list[i].strip('; \n').strip()
        return author_list

    def info_parsing(self, info):
        info_list = info.split(', ')
        ret = [info_list[1], info_list[2].strip('. \n')]
        return ret

    def save_json(self, filename):
        print('save_json')
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump(self.paper_dict, fp, indent='\t')


'''
{
    "n": {
        "title": "",
        "authors": "",
        "info": "",
        "year":"",
        "abstract": ""
    }
}
'''

ICML97 = WebPage('http://proceedings.mlr.press/v97/')
ICML97.ICML_crawling('#content > div.wrapper > div.paper > p.links > a:nth-child(1)')
# ICML97.get_titles('p.title')
ICML97.save_json('../data/icml2019.json')

ICML80 = WebPage('http://proceedings.mlr.press/v80/')
ICML80.ICML_crawling('#content > div.wrapper > div.paper > p.links > a:nth-child(1)')
# ICML97.get_titles('p.title')
ICML80.save_json('../data/icml2018.json')

ICML70 = WebPage('http://proceedings.mlr.press/v70/')
ICML70.ICML_crawling('#content > div.wrapper > div.paper > p.links > a:nth-child(1)')
# ICML97.get_titles('p.title')
ICML70.save_json('../data/icml2017.json')






