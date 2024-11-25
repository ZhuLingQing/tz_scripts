import matplotlib.pyplot as plt
import numpy as np
import os, sys, getopt
import csv
from enum import Enum
import pandas as pd
import csv

class plot_vt:
    def __init__(self, path):
        self.__path = path
        self.dpi = 150
        self.__get_basic_data(path)
        self.__get_ic_num()
        
    def __get_basic_data(self, path:str):
        self.__list_data = []
        self.__title = None
        with open(path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if self.__title is None: self.__title = row
                else: self.__list_data.append(row)
        self.__title = self.remove_spaces_from_list(self.__title)

    @staticmethod
    def remove_spaces_from_list(lst):
        if isinstance(lst, list):
            return [plot_vt.remove_spaces_from_list(item) for item in lst]
        elif isinstance(lst, str):
            return lst.replace(" ", "")
        else:
            return lst
            
    def __get_ic_num(self):
        for i in range(1,99999):
            found = False
            for col in self.__title:
                if f'IC{i}' in col:
                    found = True
                    break
            if found is False:
                self.__ic_num = i - 1
                break
                
    def print(self):
        print(f'{self.__ic_num} ICs')
        print(f'keywords: {self.__keyword_list}')
        # print(self.__dict_data)
        l_dict = []
        for kw in self.__dict_data:
            l_dict.append(len(self.__dict_data[kw]))
        print(l_dict)
    
    def parse(self, keyword:str):
        self.__keyword_list = []
        self.__keyword_index = self.__title.index(keyword)
        for row in self.__list_data:
            if row[self.__keyword_index] not in self.__keyword_list:
                self.__keyword_list.append(row[self.__keyword_index])
        self.__dict_data = {}
        for kw in self.__keyword_list:
            self.__dict_data[kw] = []
        for row in self.__list_data:
            kw = row[self.__keyword_index]
            self.__dict_data[kw].append([float(item) for item in row])
            
    def get_curve(self, l_data:list, index:int):
        curve = []
        for l in l_data:
            curve.append(l[index])
        return curve
    
    @staticmethod
    def transpose_2d_list(lst):
        return [list(row) for row in zip(*lst)]
            
    def plot_sub(self, kw:str, x:str, y_list:list):
        to_draw = sorted(self.__dict_data[kw], key=lambda _x: _x[self.__title.index(x)])
        trans_draw = self.transpose_2d_list(to_draw)
        x_curve = trans_draw[self.__title.index(x)]
        for y in y_list:
            y_curve = trans_draw[self.__title.index(y)]
            ref = trans_draw[self.__title.index('Tref1')]
            diff_y = [a - b for a, b in zip(y_curve, ref)]
            plt.plot(x_curve, diff_y, label=y)
            # plt.xlabel(x)
            plt.ylabel(y)
        plt.locator_params(axis='x', nbins=len(x_curve))
        plt.legend(loc='upper center')
        plt.title(x)
        
    def plot_one(self, keyword:str, path:str):
        plt.figure(figsize=(18, 16))
        for i in range(self.__ic_num):
            plt.subplot(4, 4, i + 1)
            yl = [f'Tdm_IC{i + 1}', f'Tdg_IC{i + 1}', f'Tcm_IC{i + 1}', f'Tcg_IC{i + 1}']
            self.plot_sub(kw=keyword, x='Temperature', y_list=yl)
        plt.suptitle(keyword)
        # plt.show()
        if path is None: plt.show()
        else: 
            path_name = f'{path}\\{keyword}.png'
            plt.savefig(path_name, dpi=self.dpi)
            print(f"save to: {path_name}")

    def plot(self, path = None):
        for kw in self.__dict_data:
            self.plot_one(kw, path)
            
            
def get_path(path:str):
    if path[1] == ':':
        return path
    else:
        return os.path.realpath(os.getcwd()) + '\\' + path

two_dimensional_list = []
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("arg1: input csv")
        print("arg2: output image path")
        sys.exit(1)
    ipath = get_path(sys.argv[1])
    opath = None
    if len(sys.argv) >= 3:
        opath = get_path(sys.argv[2])
        if not os.path.exists(opath):
            print(f'{opath} not exist.')
            sys.exit(1)
        if os.path.isfile(opath):
            print(f'{opath} is a file, it should be a path.')
            sys.exit(1)
    pl = plot_vt(ipath)
    pl.parse(keyword='Voltage')
    pl.plot(opath)
    print('done')