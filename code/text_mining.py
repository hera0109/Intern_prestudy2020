import parse as p
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations

def get_abstracts(paper_list):
    abstract_list = []
    for paper in paper_list:
        abstract_list.append(paper.abstract)
    return abstract_list

def get_title_abstracts(paper_list):
    abstract_list = []
    for paper in paper_list:
        abstract_list.append(paper.title +'\n' + paper.abstract)
    return abstract_list




