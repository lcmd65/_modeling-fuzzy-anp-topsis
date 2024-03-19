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

def cal_arr(arr1, arr2, operator):
    """_summary_

    Args:
        arr1 (_type_): _description_
        arr2 (_type_): _description_
        operator (_type_): _description_

    Returns:
        _type_: _description_
    """
    arr= []
    if (operator == "+"):
        for index in range(len(arr1)):
            arr.append(arr1[index] + arr2[index])
    elif operator == "-":
        for index in range(len(arr1)):
            arr.append(arr1[index] - arr2[index])
    elif operator == "/":
        for index in range(len(arr1)):
            arr.append(arr1[index]/ arr2[index])
    elif operator =="*":
        for index in range(len(arr1)):
            arr.append(arr1[index] * arr2[index])
            
    return arr
        


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
        data = pd.read_csv(file, delimiter='\t', header=None)
    file.close()
    return data

def element_factor_mattrix(filename):
    row = []
    matrix = read_matrix(filename)
    for index, item in matrix.iterrows():
        val = [0, 0, 0]
        for value in item:
            val = cal_arr( val, TFN_matrix.get(value), "+")
        val = cal_arr(val, [3,3,3], "/")
        row.append(val)
    return row

def max_(row):
    max= -1
    for item in row:
        for element in item:
            if element > max:
                max = element
    return max
    


def factor_matrix():
    """_summary_
    Overrall mattrix of factor
    """
    
    df_standard = draw_df()
    for row in range(df_standard.shape[0]):
        max_value = max_(df_standard.iloc[row])  # Finding the maximum value in each row
        for col in range(df_standard.shape[1]):
            for index in range (3):
                df_standard.iloc[row, col][index] = df_standard.iloc[row, col][index] / max_value  # Normalizing each value by dividing by the maximum value
    df_standard.to_csv('output/df_standard.csv', index=False)
    
    df_standard_weight = df_standard
    for row, value in zip(range(df_standard.shape[0]), weight_matrix.values()):
        for col in range(df_standard.shape[1]):
            for index in range(3):
                df_standard.iloc[row, col][index] = df_standard.iloc[row,
                                                                     col][index]*value
    df_standard_weight.to_csv('output/df_standard_weight.csv', index=False)
    
    s_max = S_max(df_standard_weight)
    pd.DataFrame(s_max).to_csv('output/S+.csv', index=False)
    
    s_min = S_min(df_standard_weight)
    pd.DataFrame(s_min).to_csv('output/S-.csv', index=False)
    
    df_s_max = df_standard_weight.copy()
    df_s_min = df_standard_weight.copy()
    print(df_standard_weight)
    fpis = FPIS(df_s_max, s_max)
    fpis.to_csv('output/fpis.csv', index=False)
    
    fnis = FNIS(df_s_min, s_min)
    fnis.to_csv('output/fnis.csv', index=False)
    
    d1 = []
    d2 = []
    for columns in fpis:
        d1.append(sum(fpis[columns]))
    for columns in fnis.columns:
        d2.append(sum(fnis[columns]))
    pd.DataFrame(d1).to_csv('output/d+.csv', index=False)
    pd.DataFrame(d2).to_csv('output/d-.csv', index=False)
    
    df_result = pd.DataFrame(columns = ["supliers", "CCi", "Rank"])
    data_to_concat = []
    for index in range(6):
        data_to_concat.append(["".join(["S", str(index)]), d2[index] / (d1[index] + d2[index]), None])

    # Concatenate DataFrames
    df_result = pd.concat([df_result, pd.DataFrame(data_to_concat, columns=["supliers", "CCi", "Rank"])], ignore_index=True)

    # Calculate ranks
    df_result["Rank"] = df_result["CCi"].rank(method='min', ascending=False)
    print(df_result)
    df_result.to_csv('output/suplier_rank.csv', index=False)

    

def S_max(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    S =[]
    for row, value in zip(range(df.shape[0]), weight_matrix.values()):
        max = -1
        for col in range(df.shape[1]):
            if df.iloc[row, col][2] > max:
                    max = df.iloc[row, col][2]
        S.append([max, max, max])
    return S


def S_min(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    S = []
    for row, value in zip(range(df.shape[0]), weight_matrix.values()):
        min = 1
        for col in range(df.shape[1]):
            if df.iloc[row, col][0] < min:
                min = df.iloc[row, col][0]
        S.append([min,min,min])
    return S
        

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
    

def distances_(triangle1, triangle2):
    """_summary_

    Args:
        triangle1 (Triangle)
        triangle2 (Triangle): 

    Returns:
        distance
    """
    return math.sqrt(1/3 *
                     ((triangle1[0] - triangle2[0])**2 +
                         (triangle1[1] - triangle2[1])**2 +
                         (triangle1[2] - triangle2[2])**2))
    

def FPIS(df, s):
    """ d+ matrix 

    Args:
        df (_type_): _description_
        s (_type_): _description_
    """
    for row in (range(df.shape[0])):
        for col in range(df.shape[1]):
            #df.iloc[row, col] = distances_(df.iloc[row, col], s[row])
            val = distances_(df.iloc[row, col], s[row])
            df.iloc[row, col] = val
    return df

def FNIS(df,s):
    """ d- matrix 

    Args:
        df (_type_): _description_
        s (_type_): _description_
    """
    for row in (range(df.shape[0])):
        for col in range(df.shape[1]):
            val = distances_(df.iloc[row, col], s[row])
            df.iloc[row, col] = val
    return df
    
def model(): 
    pass

def draw_df():
    dataframe = []
    dataframe.append(element_factor_mattrix("dataset/cost/c1.txt"))
    dataframe.append(element_factor_mattrix("dataset/cost/c2.txt"))
    dataframe.append(element_factor_mattrix("dataset/cost/c3.txt"))
    dataframe.append(element_factor_mattrix("dataset/quality/q1.txt"))
    dataframe.append(element_factor_mattrix("dataset/quality/q2.txt"))
    dataframe.append(element_factor_mattrix("dataset/prestige/p1.txt"))
    dataframe.append(element_factor_mattrix("dataset/prestige/p2.txt"))
    dataframe.append(element_factor_mattrix("dataset/prestige/p3.txt"))
    dataframe.append(element_factor_mattrix("dataset/prestige/p4.txt"))
    dataframe.append(element_factor_mattrix("dataset/factory/f1.txt"))
    dataframe.append(element_factor_mattrix("dataset/factory/f2.txt"))
    dataframe.append(element_factor_mattrix("dataset/factory/f3.txt"))
    dataframe.append(element_factor_mattrix("dataset/factory/f4.txt"))
    dataframe.append(element_factor_mattrix("dataset/level/l1.txt"))
    dataframe.append(element_factor_mattrix("dataset/level/l2.txt"))
    dataframe.append(element_factor_mattrix("dataset/env/e1.txt"))
    dataframe.append(element_factor_mattrix("dataset/env/e2.txt"))

    df = pd.DataFrame(dataframe, columns=[
                      "S1", "S2", "S3", "S4", "S5", "S6"])
    return df