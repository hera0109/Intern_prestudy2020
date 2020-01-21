import parse as p
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations

def get_edges():
    edges = []
    for paper in p.paper_list:
        authors = paper.authors
        author_com = list(combinations(authors, 2))
        for author1, author2 in author_com:
            edges.append([author1.name, author2.name])

    return edges
