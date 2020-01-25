import parse as p
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations

def get_abstracts():
    abstract_list = []
    for paper in p.paper_list:
        abstract_list.append(paper.abstract)
    return abstract_list




