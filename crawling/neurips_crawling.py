import requests
from bs4 import BeautifulSoup
import json

class WebPage:
    def __init__(self, link, year):
        self.req = requests.get(link)
        self.html = self.req.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.year = year

    def page_contents(self, selector):
        self.contents_selector = selector

    def get_titles(self, selector):
        self.titles = self.soup.select(selector)
        for title in self.titles:
            print(title.text)

    def NIPS_crawling(self, selector):
        self.paper_dict = {}

        index = 1
        mainpage = self.soup.select(selector)
        for link in mainpage:
            href = 'https://papers.nips.cc' + link.attrs['href']

            temp_req = requests.get(href)
            temp_html = temp_req.text
            temp_soup = BeautifulSoup(temp_html, 'html.parser')
            content = temp_soup.select('body > div.main-container > div')[0]

            title = content.find('h2', {'class':'subtitle'}).text
            authors = list(map(lambda i: [i.find('a').text, i.find('a').attrs['href']], content.find_all('li', {'class':'author'})))
            abstract = content.find('p', {'class':'abstract'}).text
            info = content.find('p').find('a').text
            year = self.year

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
        print('save_json', filename)
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

NIPS19  = WebPage('https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019', '2019')
NIPS19.NIPS_crawling('body > div.main-container > div > ul > li > a:nth-child(1)')
NIPS19.save_json('../data/nips2019.json')

NIPS18  = WebPage('https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2018', '2018')
NIPS18.NIPS_crawling('body > div.main-container > div > ul > li > a:nth-child(1)')
NIPS18.save_json('../data/nips2018.json')

NIPS17  = WebPage('https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2017', '2017')
NIPS17.NIPS_crawling('body > div.main-container > div > ul > li > a:nth-child(1)')
NIPS17.save_json('../data/nips2017.json')


