import parse as p
import author_network as an
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt

p.parse_json('../data/icml2019.json')


an.get_edges()

# print(an.co_worker_counts())

