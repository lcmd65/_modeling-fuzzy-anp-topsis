import pandas as pd
import numpy as np
import math

""" TFN Matrix """
TFN_matrix = {
    'EB': [0, 0, 1],
    'B': [0, 1, 3],
    'AB': [1, 3, 5],
    'A': [3, 5, 7],
    'AS': [5, 7, 9],
    'S': [7, 9, 10],
    'ES': [9, 9, 10]
}


""" weight matrix"""
weight_matrix ={
    'A1':	0.04234,
    'A2':   0.08788,
    'A3':	0.07264,
    'A4':	0.09554,
    'A5':	0.04195,
    'B1':	0.07762,
    'B2':	0.04414,
    'B3':	0.05652,
    'B4':	0.03093,
    'C1':	0.08674,
    'C2':	0.03854,
    'C3':	0.03001,
    'C4':	0.05033,
    'D1':	0.03803,
    'D2':	0.03326,
    'D3':	0.09163,
    'D4':	0.08191
}


class Triagle():
    def __init__(self, l, m, u):
        self.l = l
        self.m = m
        self.u = u
        
        
def read_matrix(filename):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(filename, "r") as file:
        data = pd.read_csv(file, delimiter="\t")
    file.close()
    return data

def element_factor_mattrix(filename):
    row = []
    matrix = read_matrix(filename)
    for index, item in matrix.iterrows():
        val = [0, 0, 0]
        for value in item:
            val += TFN_matrix.get(value)
        for val_ in val:
            val_ = val_/3
        row.append(val)
    return row
        


def factor_matrix():
    """_summary_
    Overrall mattrix of factor
    """
    dataframe = pd.DataFrame(columns = ["S1", "S2", "S3", "S4", "S5", "S6"])
    dataframe = pd.concat([dataframe, pd.DataFrame(element_factor_mattrix("dataset/cost/c1.txt"))], ignore_index=True)
    print(dataframe)

def distances(triangle1, triangle2):
    """_summary_

    Args:
        triangle1 (Triangle)
        triangle2 (Triangle): 

    Returns:
        distance
    """
    return math.sqrt(1/3*
                        ((triangle1.l - triangle2.l)**2 + 
                         (triangle1.m - triangle2.m)**2 + 
                         (triangle1.u - triangle2.u)**2))
    
    
def model():
    
    pass