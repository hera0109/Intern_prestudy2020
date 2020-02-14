import parse as p
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations
import collections

class ResearchGroup:
    def __init__(self, ID):
        self.ID = ID
        self.authors = []
        self.co_groups = []
        self.papers = []
        self.co_worked = 0

    def add_authors(self, name):
        if (name not in self.authors):
            self.authors.append(name)

    def find_co_group(self, group):
        co_id = group.ID
        i = 0
        for co in self.co_groups:
            if (co_id == co[0]):
                return i
        return -1

    def add_co_group(self, group):
        co_id = self.find_co_group(group)

        if (co_id < 0):
            self.co_groups.append([group.ID, 1])
        else:
            self.co_groups[co_id][1] += 1
        self.co_worked += 1

    def add_paper(self, paper):
        flag = True
        for p in self.papers:
            if (p.title == paper.title):
                flag = False
        if (flag):
            self.papers.append(paper)

    def add_all_paper(self, author_list):
        for name in self.authors:
            author = author_list[p.find_author(name, author_list)]
            for paper in author.papers:
                self.add_paper(paper)


def get_edges(author_list, paper_list):
    edges = []
    alone_author = []
    for paper in paper_list:
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


def get_edges_from_values(G, values, counts, author_list, paper_list, num):
    ctr = collections.Counter(values)
    top_RG = ctr.most_common(num)
    top_values = []

    for i, count in top_RG:
        top_values.append(i)
    r_authors = []
    r_counts = []
    r_values = []
    i = 0
    for node in G:
        if (values[i] in top_values):
            r_authors.append(node)
            r_counts.append(counts[i])
            r_values.append(values[i])
        i += 1
    print(len(r_authors))

    total_edges, total_alone = get_edges(author_list, paper_list)
    r_edges = []
    r_alone = []
    for e in total_edges:
        if ((e[0] in r_authors) and (e[1] in r_authors)):
            r_edges.append(e)
        elif ((e[0] not in r_authors) and (e[1] in r_authors)):
            r_alone.append(e[1])
        elif ((e[0] in r_authors) and (e[1] not in r_authors)):
            r_alone.append(e[0])
    for a in total_alone:
        if (a in r_authors):
            r_alone.append(a)

    G_r = nx.MultiGraph()
    G_r.add_edges_from(r_edges)
    G_r.add_nodes_from(r_alone)

    # Adding number of papers attribute
    for i in range(len(r_authors)):
        G_r.nodes[r_authors[i]]['papers'] = r_counts[i]
    return G_r, r_values

def get_edges_from_topN(G, values, counts, author_list, paper_list, N):
    top_values = sorted(values, reverse=True)[:N]

    r_authors = []
    r_counts = []
    r_values = []
    i = 0
    for node in G:
        if (values[i] in top_values):
            r_authors.append(node)
            r_counts.append(counts[i])
            r_values.append(values[i])
        i += 1

    total_edges, total_alone = get_edges(author_list, paper_list)
    r_edges = []
    r_alone = []
    for e in total_edges:
        if ((e[0] in r_authors) and (e[1] in r_authors)):
            r_edges.append(e)
        elif ((e[0] not in r_authors) and (e[1] in r_authors)):
            r_alone.append(e[1])
        elif ((e[0] in r_authors) and (e[1] not in r_authors)):
            r_alone.append(e[0])
    for a in total_alone:
        if (a in r_authors):
            r_alone.append(a)

    G_r = nx.MultiGraph()
    G_r.add_edges_from(r_edges)
    G_r.add_nodes_from(r_alone)

    # Adding number of papers attribute
    for i in range(len(r_authors)):
        G_r.nodes[r_authors[i]]['papers'] = r_counts[i]
    return G_r, r_values



def co_worker_counts(author_list):
    author_name = []
    co_worker_count = []
    for author in author_list:
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


def find_other_group(G, values, author_list):
    other_group = []
    author_group = {}
    i = 0
    for name in G.nodes():
         author_group[name] = values[i]
         i += 1
    for name in G.nodes():
        n = p.find_author(name, author_list)
        temp = set()
        if (n >= 0):
            author = author_list[n]
            for co in author.co_workers:
                if (author_group[name] != author_group[co.name]):
                    temp.add(author_group[co.name])
        other_group.append((name, len(temp)))
    return sorted(other_group, key = lambda x: x[1], reverse = True)


def make_colormap(G, sorted_authors, author_list, num):
    colormap = []
    top_authors = sorted_authors[:num]
    for node in G:
        author_id = p.find_author(node, author_list)
        if (author_id >= 0 and (node in top_authors)):
            colormap.append('blue')
        else:
            colormap.append('ivory')
    return colormap

def find_group(ID, groups):
    i = 0
    for group in groups:
        if(ID == group.ID):
            return i
        i += 1
    return -1

def get_group_edges(total_groups):
    edges = []
    alone = []
    for group in total_groups:
        co_groups = group.co_groups
        groups = []
        groups.append(group.ID)
        for g in co_groups:
            temp = [[group.ID, g[0]] for i in range(g[1])]
            edges += temp
        if (len(co_groups) < 1):
            alone.append(group.ID)
    return edges, alone

def make_research_groups(G, values):
    total_groups = []
    i = 0
    for node in G:
        ID = values[i]
        index = find_group(ID, total_groups)

        G.nodes[node]['group'] = ID

        if(index < 0):
            group = ResearchGroup(ID)
            group.add_authors(node)
            total_groups.append(group)
        else:
            group = total_groups[index]
            group.add_authors(node)
        i += 1

    for node in G:
        neighbors = [n for n in G.neighbors(node)]
        group_id = G.nodes[node]['group']
        group = total_groups[find_group(group_id, total_groups)]

        for nei in neighbors:
            group_id_ = G.nodes[nei]['group']
            if (group_id != group_id_):
                nei_group = total_groups[find_group(group_id_, total_groups)]
                group.add_co_group(nei_group)

    edges, alone = get_group_edges(total_groups)
    G = nx.MultiGraph()
    G.add_edges_from(edges)
    G.add_nodes_from(alone)

    return total_groups, G

def get_top_group(G, groups, num):
    r_groups = sorted(groups, key=lambda x: x.co_worked, reverse=True)[:num]
    r_counts = [group.co_worked for group in r_groups]
    r_ids = [group.ID for group in r_groups]
    r_edges = []
    r_alone = []
    
    for group in r_groups:
        co_groups = []
        group_ID = group.ID
        flag = True
        for co_g in group.co_groups:
            co_ID = co_g[0]
            if(co_ID in r_ids):
                if (co_ID > group_ID):
                    r_edges.append([group_ID, co_ID])
                else:
                    r_edges.append([co_ID, group_ID])
                flag = False
        if (flag):
            r_alone.append(group_ID)
        
    G_r = nx.MultiGraph()
    G_r.add_edges_from(r_edges)
    G_r.add_nodes_from(r_alone)

    # Adding number of papers attribute
    for i in range(len(r_groups)):
        G_r.nodes[r_groups[i].ID]['authors'] = r_counts[i]
    return G_r, r_groups


