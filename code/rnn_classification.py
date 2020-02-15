import numpy as np
import torch
import pandas as pd

def read_json_file(filename):
    df = pd.read_json(filename)
    return df

def parse_imdb_data(df):
    raw_text = df.text_a.values
    raw_label = df.label.values




