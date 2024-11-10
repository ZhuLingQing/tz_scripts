import matplotlib.pyplot as plt
import numpy as np
import os, sys, getopt
import csv
from enum import Enum
import pandas as pd
import csv

class plot_zm:
    def __init__(self, path):
        self.__path = path
        self.__parse()
    
    def __parse(self):
        self.__list_data = []
        self.__list_frequency = []
        with open(path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                self.__list_data.append(row)
        self.__frequency_index = self.__list_data[0].index('Frequency')
        for row in self.__list_data[1:]:
            self.__list_frequency.append(row[self.__frequency_index])
        self.__record_num = len(self.__list_frequency)
        self.__list_real = []
        self.__list_imag = []
        self.__ic_num = 0
        while True:
            try:
                real_index = self.__list_data[0].index(f'Zreal_IC{self.__ic_num + 1}')
                imag_index = self.__list_data[0].index(f'Zimag_IC{self.__ic_num + 1}')
                list_real = []
                list_imag = []
                for i in range(self.__record_num):
                    list_real.append(float(self.__list_data[i + 1][real_index]))
                    list_imag.append(float(self.__list_data[i + 1][imag_index]))
                self.__list_real.append(list_real)
                self.__list_imag.append(list_imag)
                self.__ic_num += 1
            except:
                print(f'not found at {self.__ic_num}')
                break
            
    def __plot_imag(self):
        for index in range(self.__ic_num):
            y = self.__list_imag[index]
            x = self.__list_real[index]
            plt.plot(x,y, label=f'IC{index+1}')
            plt.xlabel('imag')
            plt.ylabel('real')
        plt.legend(loc='lower right')
        plt.title(f'real:imag')
        
    def __plot_freq(self):
        for index in range(self.__ic_num):
            x = self.__list_frequency
            y = self.__list_real[index]
            plt.plot(x,y, label=f'IC{index+1}')
            plt.xlabel('frequency')
            plt.ylabel('real')
        plt.legend(loc='lower left')
        plt.title(f'freq:imag')

    def plot_by_imag(self, path = None):
        plt.figure(figsize=(10, 8))
        plt.subplot(110 + 1)
        self.__plot_imag()
        plt.show()

    def plot_by_frequency(self, path = None):
        plt.figure(figsize=(10, 8))
        plt.subplot(110 + 1)
        self.__plot_freq()
        plt.show()

    def plot(self, path = None):
        plt.figure(figsize=(18, 8))
        plt.subplot(120 + 1)
        self.__plot_imag()
        plt.subplot(120 + 2)
        self.__plot_freq()
        plt.show()

two_dimensional_list = []
if __name__ == "__main__":
    path = os.path.realpath(os.getcwd()) + '\\' + sys.argv[1]
    pl = plot_zm(path)
    # pl.plot_by_imag()
    # pl.plot_by_frequency()
    pl.plot()
    print('done')