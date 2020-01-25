import parse as p
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations

def get_edges():
    edges = []
    alone_author = []
    for paper in p.paper_list:
        authors = paper.authors
        author_com = list(combinations(authors, 2))
        for author1, author2 in author_com:
            if (author1.name < author2.name):
                edges.append([author1.name, author2.name])
            else:
                edges.append([author2.name, author1.name])
        if len(authors) == 1:
            author = authors[0].name
            alone_author.append(author)

    return [edges, alone_author]

def co_worker_counts():
    author_name = []
    co_worker_count = []
    for author in p.author_list:
        co_worker = author.co_workers
        temp = []
        for co in co_worker:
            temp.append(co)
        co_count = len(set(temp))
        author_name.append(author.name)
        co_worker_count.append(co_count)
    return [[x for _, x in sorted(zip(co_worker_count, author_name),
        reverse = True)], sorted(co_worker_count, reverse = True)]
    # return sorted(co_worker_count, key = lambda x: x[1], reverse = True)

def find_other_group(G, values):
    other_group = []
    author_group = {}
    i = 0
    for name in G.nodes():
         author_group[name] = values[i]
         i += 1
    for name in G.nodes():
        n = p.find_author(name)
        temp = set()
        if (n >= 0):
            author = p.author_list[n]
            for co in author.co_workers:
                if (author_group[name] != author_group[co.name]):
                    temp.add(author_group[co.name])
        other_group.append((name, len(temp)))
    return sorted(other_group, key = lambda x: x[1], reverse = True)
