import json
import pandas as pd

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
        self.group = -1

    def add_paper(self, paper):
        self.papers.append(paper)
        self.co_workers += paper.authors

    def paper_count(self):
        return len(self.papers)


def find_author(name, author_list):
    if len(author_list) <= 0:
        return -1
    for author in author_list:
        if (name == author.name):
            return author.ID

    return -1

def find_paper(title, paper_list):
    if len(paper_list) <= 0:
        return -1
    i = 0
    for paper in paper_list:
        if (title == paper.title):
            return i
        i += 1
    return -1

def paper_exists(title, paper_list):
    if len(paper_list) <= 0:
        False
    for paper in paper_list:
        if (title == paper.title):
            return True
    return False

def print_authors(author_list):
    for a in author_list:
        temp1 = []
        temp2 = []
        for paper in a.papers:
            temp1.append(paper.title)
        for co in a.co_workers:
            temp2.append(co.name)
        print (a.name, a.ID, temp1, temp2)

def parse_json(file_list):
    author_list = []
    paper_list = []

    for filename in file_list:
        with open(filename) as json_file:
            data = json.load(json_file)

        if 'icml' in filename:
            flag = True
        else:
            flag = False

        for key, paper_dict in data.items():
            ID = key

            if (paper_exists(paper_dict['title'], paper_list)):
                print(paper_dict['title'])
                continue
            if flag:
                author_names = paper_dict['authors']
            else:
                temp = paper_dict['authors']
                author_names = []
                for i in temp:
                    author_names.append(i[0])

            paper = Paper(ID, paper_dict['title'], paper_dict['year'],
                    paper_dict['abstract'])
            paper_list.append(paper)
            authors = []

            for name in author_names:
                i = find_author(name, author_list)
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
    print('Read {} files, {} papers and {} authors'.format(
        len(file_list), len(paper_list), len(author_list)))

    return author_list, paper_list
        # print_authors()

def get_paper_count(author_list):
    author_name = []
    author_paper = []
    for author in author_list:
        author_name.append(author.name)
        author_paper.append(author.paper_count())

    ret1 = [author_name, author_paper]
    ret2 = [[x for _,x in sorted(zip(author_paper,author_name), reverse = True)],
            sorted(author_paper, reverse = True)]

    return ret1, ret2

def save_authors_csv(filename, G, values):
    names = []
    paper_nums = []
    group_id = []
    i = 0
    for name in G:
        names.append(name)
        paper_nums.append(G.nodes[name]['papers'])
        group_id.append(values[i])
        i += 1
    data = {'Name': names,
            '# of Papers': paper_nums,
            'Group id': group_id}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename)
