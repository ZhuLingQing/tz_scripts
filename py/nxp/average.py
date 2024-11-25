import matplotlib.pyplot as plt
import numpy as np
import os, sys, getopt
import csv
from enum import Enum
import pandas as pd
import csv

class AveragedList:
    def __init__(self, keywords:list):
        self.__keywords = keywords
    
    @staticmethod
    def delNone(l_in):
        return l_in
    
    def del1stLast(l_data):
        return l_data[1:-1] # remove Time and last ','

    @staticmethod
    def CsvToList(path:str, delFunc=None):
        try:
            csvfile = open(path, newline='')
        except:
            assert 0, f'fail to open {path}'
        csv_reader = csv.reader(csvfile)
        l_data = []
        for data in csv_reader:
            l_data.append(delFunc(data))
        return l_data
    
    @staticmethod
    def ListToCsv(path:str, data:list):
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in data:
                csvwriter.writerow(row)
    
    def Dump(self, data:list):
        print(self.__keywords)
        for d in data:
            print(d)

    def __same_key(self, last, data, key_idx_list):
        for k in key_idx_list:
            if last[k] != data[k]: return False
        return True
    
    def __make_average(self, sum_data):
        num_cols = len(sum_data[0])
        num_rows = len(sum_data)
        assert num_cols, 'no data for average'
        # print(f'{num_cols} cols, {num_rows} rows')
        if num_cols == 1: return [float(item) for item in sum_data]
        float_matrix = [[float(item) for item in sublist] for sublist in sum_data]
        column_averages = [0] * num_cols
        for col in range(num_cols):
            sum = 0
            for row in range(num_rows):
                sum += float_matrix[row][col]
            column_averages[col] = sum / num_rows
        return column_averages
    
    def MakeAverage(self, l_data:list):
        title = l_data[0]
        key_idx_list = []
        for k in self.__keywords:
            key_idx_list.append(title.index(k))
        averaged_data = [title]
        last_data = l_data[1]
        sum_data = [last_data]
        for data in l_data[2:]:
            if self.__same_key(last_data, data, key_idx_list):
                sum_data.append(data)
            else:
                averaged_data.append(self.__make_average(sum_data))
                last_data = data
                sum_data = [last_data]
        averaged_data.append(self.__make_average(sum_data))
        return averaged_data
    
def GetRealPath(argv):
    if argv[1] == ':':
        return sys.argv
    else:
        return os.path.realpath(os.getcwd()) + '\\' + argv


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("arg1: csv in path")
        print("arg2: csv out path")
    l_data = AveragedList.CsvToList(GetRealPath(sys.argv[1]), delFunc=AveragedList.del1stLast)
    al = AveragedList(['Voltage', 'Temperature'])
    data = al.MakeAverage(l_data)
    if len(sys.argv) > 2:
        path = GetRealPath(sys.argv[2])
        AveragedList.ListToCsv(path, data)
        print(f'save to {path}')
    else:
        al.Dump(data)