import matplotlib.pyplot as plt
import numpy as np
import os, sys, getopt
import csv
from enum import Enum
import pandas as pd
import csv

class csv_average:
    def __init__(self, path, keywords:list):
        self.__path = path
        self.__keywords = keywords
        self.__parse()

    def __same_key(self, last, data):
        for k in self.__key_index:
            if last[k] != data[k]: return False
        return True
    
    def __column_filter(self, l_data):
        return l_data[1:-1] # remove Time and last ','
    
    def __make_average(self, sum_data):
        num_cols = len(sum_data[0])
        num_rows = len(sum_data)
        assert num_cols, 'no data for average'
        print(f'{num_cols} cols, {num_rows} rows')
        if num_cols == 1: return [float(item) for item in sum_data]
        float_matrix = [[float(item) for item in sublist] for sublist in sum_data]
        column_averages = [0] * num_cols
        for col in range(num_cols):
            sum = 0
            for row in range(num_rows):
                sum += float_matrix[row][col]
            column_averages[col] = sum
        return column_averages
    
    def __parse(self):
        try:
            csvfile = open(path, newline='')
        except:
            assert 0, f'fail to open {path}'
        csv_reader = csv.reader(csvfile)
        self.__title = self.__column_filter(next(csv_reader))
        self.__key_index = []
        for k in self.__keywords:
            self.__key_index.append(self.__title.index(k))
        self.__averaged_data = []
        last_data = None
        for data in csv_reader:
            f_data = self.__column_filter(data)
            if last_data is None:
                last_data = f_data
                sum_data = [f_data]
            else:
                if self.__same_key(last_data, f_data):
                    sum_data.append(f_data)
                else:
                    self.__averaged_data.append(self.__make_average(sum_data))
                    last_data = f_data
                    sum_data = [f_data]
            self.__averaged_data.append(self.__make_average(sum_data))
    def dump(self):
        print(self.__title)
        # print(self.__key_index)
        print(self.__averaged_data)

two_dimensional_list = []
if __name__ == "__main__":
    if sys.argv[1][1] == ':':
        path = sys.argv[1]
    else:
        path = os.path.realpath(os.getcwd()) + '\\' + sys.argv[1]
    pl = csv_average(path, ['Temperature', 'Voltage'])
    pl.dump()