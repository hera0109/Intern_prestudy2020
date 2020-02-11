import parse as p
import author_network as an
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations
import collections
from sklearn.linear_model import LinearRegression

def get_author_vector(re_authors, re_papers, years):
    years.sort()
    year_paper = []
    author_vec = []
    b_year = int(years[0])

    for year in years:
        year_paper.append([year, 0])

    for paper in re_papers:
        index = int(paper.year) - b_year
        year_paper[index][1] += 1

    for i in range(len(re_authors)):
        author_vec.append([0 for year in years])
        author = re_authors[i]
        author_papers = author.papers
        for p in author_papers:
            index = int(p.year) - b_year
            author_vec[i][index] += 1/year_paper[index][1]

    print(year_paper)
    return author_vec

def get_author_regression(re_authors, re_papers, years, target):
    author_vec = get_author_vector(re_authors, re_papers, years)
    predictions = []

    for vec in author_vec:
        line = LinearRegression()
        line.fit(np.array(years).reshape(-1,1)
                , np.array(vec))
        predict = line.predict([[target]])
        predictions.append(predict[0])

    total_vec =  [author_vec[i]+[predictions[i]]
                for i in range(len(author_vec))]
    author_name = [author.name for author in re_authors]

    return [[x for _,x in sorted(zip(total_vec, author_name)
        , key=lambda y: y[0][len(years)], reverse=True)],
        sorted(total_vec, key=lambda x: x[len(years)], reverse=True)]

def get_group_vector(re_groups, re_papers, years):
    years.sort()
    year_paper = []
    group_vec = []
    b_year = int(years[0])

    for year in years:
        year_paper.append([year, 0])

    for paper in re_papers:
        index = int(paper.year) - b_year
        year_paper[index][1] += 1

    for i in range(len(re_groups)):
        group_vec.append([0 for year in years])
        group = re_groups[i]
        group_papers = group.papers
        for p in group_papers:
            index = int(p.year) - b_year
            group_vec[i][index] += 1/year_paper[index][1]

    return group_vec

def get_group_regression(re_groups, re_papers, years, target):
    group_vec = get_group_vector(re_groups, re_papers, years)
    predictions = []

    for vec in group_vec:
        line = LinearRegression()
        line.fit(np.array(years).reshape(-1,1)
                , np.array(vec))
        predict = line.predict([[target]])
        predictions.append(predict[0])

    total_vec =  [group_vec[i]+[predictions[i]]
                for i in range(len(group_vec))]
    group_id = [group.ID for group in re_groups]

    return [[x for _,x in sorted(zip(total_vec, group_id)
        , key=lambda y: y[0][len(years)], reverse=True)],
        sorted(total_vec, key=lambda x: x[len(years)], reverse=True)]

