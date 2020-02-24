import numpy as np
import networkx as nx
import parse as p

from itertools import combinations
from torch.utils.data import Dataset, TensorDataset, DataLoader, RandomSampler, SequentialSampler
from pytorch_transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from keras.preprocessing.sequence import pad_sequences
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from node2vec import Node2Vec
import chart_studio.plotly as py
import plotly.graph_objs as go
from numpy.linalg import norm
import numpy as np
import pandas as pd
import collections


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


def tokenize_data(data):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    ids = []
    for d in data:
        encoded = tokenizer.encode(d, add_special_tokens=True)
        ids.append(encoded)
    
    print('Max sentence length: ', max([len(sen) for sen in ids]))
    ids = pad_sequences(ids, maxlen=512, dtype="long", 
                        value=0, truncating="post", padding="post") 

    attention_masks = []
    n = 0
    for i in ids:
        temp = [float(t>0) for t in i]
        attention_masks.append(temp)
        n += 1
    print('number:'+str(n))
    return ids, attention_masks


def cos_sim(a, b):
       return np.dot(a, b)/(norm(a)*norm(b))


def get_cos_sim(vec):
    total_num = len(vec)
    index_com = list(combinations([n for n in range(total_num)], 2))
    sim_list = [[0 for i in range(total_num)] for i in range(total_num)]
    for i1, i2 in index_com:
        v1 = vec[i1]
        v2 = vec[i2]
        sim = cos_sim(v1, v2)
        sim_list[i1][i2] = sim
        sim_list[i2][i1] = sim
    return sim_list


def top_cos_sim(vec, num, M):
    vec1 = np.array(vec)
    vec1 = vec1/np.sqrt(np.sum(np.square(np.array(vec1)), axis=1))[:,None]
    sim_matrix = np.matmul(vec1, vec1.T)
    sim_matrix -= np.eye(len(vec1))
    sim_shape = sim_matrix.shape

    sim_vec = sorted([ [i,j,sim_matrix[i][j]] for i in range(sim_shape[0]) for j in range(i,sim_shape[1])],
            key=lambda x: x[2], reverse=True)[:num]

    return sim_vec



def make_paper_edges(paper_list, sim_list):
    total_num = len(paper_list)
    edge_list = []

    for i,j,vec in sim_list:
        title = paper_list[i].title
        nei_title = paper_list[j].title
        edge = [title, nei_title, vec]
        edge_list.append(edge)
    return edge_list


def make_paper_graph(paper_list, sim_list):
    edges = make_paper_edges(paper_list, sim_list)

    G = nx.Graph()
    for e in edges:
        G.add_edge(e[0], e[1], weight=e[2])
    return G

def make_iplot_fig(G, sp, values, color, node_size, edge_color, size):
    background_color = '#ffffff'
    if(edge_color == None):
        edge_color = background_color
    labels = []
    X = []
    Y = []
    i = 0
    for p in sp:
        labels.append('['+str(values[i])+'] '+p)
        X.append(sp[p][0])
        Y.append(sp[p][1])
        i += 1
    
    
        
    trace_nodes = dict(type='scatter',
                     x=X,
                     y=Y,
                     mode='markers',
                     marker=dict(size=node_size, color=values,
                                 colorscale=color),
                     text=labels,
                     hoverinfo='text')
    Xe = []
    Ye = []
    for e in G.edges():
        Xe.extend([sp[e[0]][0], sp[e[1]][0], None])
        Ye.extend([sp[e[0]][1], sp[e[1]][1], None])

    trace_edges = dict(type='scatter',
                     mode='lines',
                     x=Xe,
                     y=Ye,
                     line=dict(width=0.2, color='rgb(25,25,25)'),
                     hoverinfo='none'
                    )

    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

    layout = dict(title = 'My Graph',
                font = dict(family='Balto'),
                width=size[0],
                height=size[1],
                autosize=False,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(
                l=40,
                r=40,
                b=85,
                t=100,
                pad=0,

        ),
        hovermode='closest',
        plot_bgcolor= background_color #set background color
        )
    fig = dict(data=[trace_edges, trace_nodes], layout=layout)
    return fig


def node2vec_kmeans(G, K):
    node2vec = Node2Vec(graph=G,
                        dimensions=20,
                        walk_length=10,
                        p = 1,
                        q = 0.0001,
                        weight_key='weight',
                        num_walks=2000,
                        workers=1,
                       )

    for i, each_walk in enumerate(node2vec.walks):
        print(f"{i:0>2d}, {each_walk}")
        if i>1:
            break
    model = node2vec.fit(window=10)
    kmeans = KMeans(n_clusters=K, random_state=0).fit(model.wv.vectors)
    for n, label in zip(model.wv.index2entity, kmeans.labels_):
        G.nodes[n]['node2vec'] = label
    values_nv = [n[1]['node2vec'] for n in G.nodes(data=True)]
    return values_nv


def save_paper_csv(filename, G, paper_list, values_lou, values_nv):
    titles = []
    abstracts = []
    lou_id = []
    nv_id = []
    i = 0
    for node in G:
        index = p.find_paper(node, paper_list)
        paper = paper_list[index]
        titles.append(paper.title)
        abstracts.append(paper.abstract)
        lou_id.append(values_lou[i])
        nv_id.append(values_nv[i])
        i += 1
    data = {'Title': titles,
            'id(louvain)': lou_id,
            'id(node2vec)': nv_id,
            'abstract': abstracts}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename)
    
def save_topN_paper_csv(filename, G, paper_list, values_lou, num):
    ctr = collections.Counter(values_lou)
    top_RG = ctr.most_common(num)
    top_values = []

    for i, count in top_RG:
        top_values.append(i)
        
    print(top_RG)

    titles = []
    abstracts = []
    size = []
    lou_id = []
    i = 0
    for node in G:
        value = values_lou[i]
        if (value in top_values):
            index = p.find_paper(node, paper_list)
            paper = paper_list[index]
            titles.append(paper.title)
            abstracts.append(paper.abstract)
            lou_id.append(value)
            size.append(ctr[value])
        i += 1
    data = {'Title': titles,
            'id(louvain)': lou_id,
            'group size': size,
            'abstract': abstracts}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename)
