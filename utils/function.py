import pandas as pd
import numpy as np


def read_matrix(filename):
    with open(filename, "r") as file:
        data = pd.read_csv(file, delimiter="\t")
    file.close()
    return data

def weight_get():
    with open("dataset/matrix_score.txt", "r") as file:
        pass


def model():
    pass