import json
author_list = []
paper_list = []

class Paper:
    def __init__(self, ID, title, year, abstract):
        self.ID = ID
        self.title = title
        self.authors = []
        self.year = year
        self.abstract = abstract

    def add_authors(self, authors):
        self.authors = authors


class Author:
    def __init__(self, ID, name):
        self.name = name
        self.ID = ID
        self.papers = []
        self.co_workers = []

    def add_paper(self, paper):
        self.papers.append(paper)
        self.co_workers += paper.authors

    def paper_count(self):
        return len(self.papers)

def find_author(name):
    if len(author_list):
        return -1
    for auhtor in author_list:
        if (name == author.name):
            return author.ID-1

    return -1


def print_authors():
    for a in author_list:
        temp1 = []
        temp2 = []
        for paper in a.papers:
            temp1.append(paper.title)
        for co in a.co_workers:
            temp2.append(co.name)
        print (a.name, a.ID, temp1, temp2)

def parse_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)

    for key, paper_dict in data.items():
        ID = key
        author_names = paper_dict['authors']

        paper = Paper(ID, paper_dict['title'], paper_dict['year'],
                paper_dict['abstract'])
        paper_list.append(paper)
        authors = []

        for name in author_names:
            i = find_author(name)
            if (i < 0):
                a_id = len(author_list)
                author = Author(a_id, name)
                author_list.append(author)
            else:
                author = author_list[i]
            authors.append(author)

        paper.add_authors(authors)
        for author in authors:
            author.add_paper(paper)
    # print_authors()




