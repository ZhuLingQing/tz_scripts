import matplotlib.pyplot as plt
import numpy as np
import os, sys, getopt
import json
from enum import Enum

class CalPoint(Enum):
    btm = 0
    top = 1

class PlotCal:
    def __init__(self, json_path:str, save_path = None, matrix = None, dpi:int = 100, scatter_on:bool = False):
        with open(json_path, 'r', encoding='utf-8') as file:
            self.cal_json = json.load(file)
        if save_path is None:
            self.save_path = os.path.dirname(json_path)
        else:
            self.save_path = save_path
        self.matrix = matrix
        self.dpi = dpi
        self.scatter_on = scatter_on

    @staticmethod
    def __matrix_width(mat):
        w = mat[1:].lower().split('p')[0]
        return int(w)

    @staticmethod
    def __figure_size(width):
        if width == 8:
            return (18, 8)
        elif width == 32:
            return (18, 16)
        assert 0, f'invalid width {width}'

    @staticmethod
    def __subplot_size(width):
        if width == 8:
            return 240
        elif width == 32:
            return 440
        assert 0, f'invalid width {width}'

    @staticmethod
    def __wgt_lut_reverse(lut, top, btm):
        r = []
        for i in lut:
            if i[int(CalPoint.btm.value)]: # btm
                r.append(btm[i[int(CalPoint.btm.value)]])
            elif i[int(CalPoint.top.value)]: # top
                r.append(top[i[int(CalPoint.top.value)]])
            else:
                r.append(btm[i[int(CalPoint.btm.value)]])
        return r
        
    @staticmethod
    def __phase(js, width):
        plt.figure(figsize=PlotCal.__figure_size(width))
        mid = js[f'phase_middle']
        for tx in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + tx + 1)

            y = np.array(js[f'phase_top_{tx}'])
            x = np.linspace(0, len(y), len(y))
            plt.plot(x,y, label=f'top{tx}', color='blue')

            yd = np.array(js[f'phase_btm_{tx}'])
            x = np.linspace(0, len(yd), len(yd))
            plt.plot(x,yd, label=f'btm{tx}', color='red')

            if mid[tx][int(CalPoint.btm.value)] != 0:
                pot_x = mid[tx][int(CalPoint.btm.value)]
                pot_y = js[f'phase_btm_{tx}'][pot_x]
            else:
                pot_x = mid[tx][int(CalPoint.top.value)]
                pot_y = js[f'phase_top_{tx}'][pot_x]
            plt.scatter(pot_x, pot_y, color='green')

            # plt.legend(loc='lower right')
            plt.title(f'phase_tx{tx}')
            plt.tight_layout()

    @staticmethod
    def __modulator(js, width, scatter_on:bool = False):
        plt.figure(figsize=PlotCal.__figure_size(width))
        for tx in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + tx + 1)

            y = np.array(js[f'modulator_{tx}'])
            x = np.linspace(0, len(y), len(y))
            plt.plot(x,y, label=f'tx{tx}', color='blue')

            yd = np.array(js[f'modulator_denoised_{tx}'])
            x = np.linspace(0, len(yd), len(yd))
            plt.plot(x,yd, label=f'dtx{tx}', color='red')

            if scatter_on is True:
                lut = js[f'modulator_lut_{tx}']
                for pot in lut:
                    pot_x = pot
                    pot_y = js[f'modulator_denoised_{tx}'][pot_x]
                    plt.scatter(pot_x, pot_y, color='green')

            # plt.legend(loc='lower right')
            plt.title(f'modulator_tx{tx}')
            plt.tight_layout()

    @staticmethod
    def __mod_lut(js, width):
        plt.figure(figsize=(9,4))
        plt.subplot(120 + 1)
        for tx in range(0, width):
            yd = js[f'modulator_{tx}']

            lut = js[f'modulator_lut_{tx}']
            x = np.linspace(0, len(yd), len(lut))
            yl = []
            for i in lut:
                yl.append(yd[i])
            plt.plot(x,yl, label=f'tx{tx}')

        plt.legend(loc='lower right')
        plt.title(f'modulator_lut_raw')
        plt.tight_layout()

        plt.subplot(120 + 2)
        for tx in range(0, width):
            yd = js[f'modulator_denoised_{tx}']

            lut = js[f'modulator_lut_{tx}']
            x = np.linspace(0, len(yd), len(lut))
            yl = []
            for i in lut:
                yl.append(yd[i])
            plt.plot(x,yl, label=f'tx{tx}')

        plt.legend(loc='lower right')
        plt.title(f'modulator_lut_denoised')
        plt.tight_layout()

    @staticmethod
    def __weight(js, width, row = 0, scatter_on:bool = False):
        plt.figure(figsize=PlotCal.__figure_size(width))
        for col in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + col + 1)

            y = np.array(js[f'weight_top_f_row{row}_col{col}']) - np.array(js[f'weight_top_0_row{row}_col{col}'])
            x = np.linspace(0, len(y), len(y))
            plt.plot(x,y, label=f'top_r{row}c{col}', color='blue')

            yd = np.array(js[f'weight_top_denoised_row{row}_col{col}'])
            x = np.linspace(0, len(yd), len(yd))
            plt.plot(x,yd, label=f'dtop_r{row}c{col}', color='red')
            
            y = np.array(js[f'weight_btm_f_row{row}_col{col}']) - np.array(js[f'weight_btm_0_row{row}_col{col}'])
            x = np.linspace(0, len(y), len(y))
            plt.plot(x,y, label=f'btm_r{row}c{col}', color='blue')

            yd = np.array(js[f'weight_btm_denoised_row{row}_col{col}'])
            x = np.linspace(0, len(yd), len(yd))
            plt.plot(x,yd, label=f'dbtm_r{row}c{col}', color='red')

            if scatter_on is True:
                lut = js[f'weight_lut_row{row}_col{col}']
                for pot in lut:
                    if pot[int(CalPoint.btm.value)] != 0:
                        pot_x = pot[int(CalPoint.btm.value)]
                        pot_y = js[f'weight_btm_denoised_row{row}_col{col}'][pot_x]
                    else:
                        pot_x = pot[int(CalPoint.top.value)]
                        pot_y = js[f'weight_top_denoised_row{row}_col{col}'][pot_x]
                    plt.scatter(pot_x, pot_y, color='green')

            # plt.legend(loc='lower right')
            plt.title(f'weight_row{row}_col{col}')
            plt.tight_layout()

    @staticmethod
    def __wgt_lut(js, width, denoised:bool = True):
        plt.figure(figsize=PlotCal.__figure_size(width))
        for row in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + row + 1)
            for col in range(0, width):
                if denoised:
                    yt = js[f'weight_top_denoised_row{row}_col{col}']
                    yb = js[f'weight_btm_denoised_row{row}_col{col}']
                else:
                    yt = np.array(js[f'weight_top_f_row{row}_col{col}']) - np.array(js[f'weight_top_0_row{row}_col{col}'])
                    yb = np.array(js[f'weight_btm_f_row{row}_col{col}']) - np.array(js[f'weight_btm_0_row{row}_col{col}'])
                lut = js[f'weight_lut_row{row}_col{col}']
                r = PlotCal.__wgt_lut_reverse(lut, yt, yb)
                x = np.linspace(0, len(r), len(r))
                plt.plot(x,r, label=f'col{col}')

            plt.legend(loc='lower right')
            plt.title(f'weight_lut_row{row}')
            plt.tight_layout()

    @staticmethod
    def __wgt_lut_specified(js, width, row:int):
        plt.figure(figsize=PlotCal.__figure_size(width))
        for col in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + col + 1)
            lut = js[f'weight_lut_row{row}_col{col}']
            # print(f'r{row}c{col}:{lut}')

            yt = js[f'weight_top_denoised_row{row}_col{col}']
            yb = js[f'weight_btm_denoised_row{row}_col{col}']
            r = PlotCal.__wgt_lut_reverse(lut, yt, yb)
            x = np.linspace(0, len(r), len(r))
            plt.plot(x,r, label='denoised')
            
            yt = np.array(js[f'weight_top_f_row{row}_col{col}']) - np.array(js[f'weight_top_0_row{row}_col{col}'])
            yb = np.array(js[f'weight_btm_f_row{row}_col{col}']) - np.array(js[f'weight_btm_0_row{row}_col{col}'])
            r = PlotCal.__wgt_lut_reverse(lut, yt, yb)
            x = np.linspace(0, len(r), len(r))
            plt.plot(x,r, label='raw')

            plt.legend(loc='lower right')
            plt.title(f'weight_lut_row{row}_col{col}')
            plt.tight_layout()

    @staticmethod
    def __path_delay(js, width, scatter_on:bool = False):
        plt.figure(figsize=PlotCal.__figure_size(width))
        pot_rising = js[f'path_rising_point']
        pot_middle = js[f'path_middle_point']
        title_color = 'black'
        for index in range(0, width):
            plt.subplot(PlotCal.__subplot_size(width) + index + 1)

            y = np.array(js[f'path_delay_{index}'])
            x = np.linspace(0, len(y), len(y))
            plt.plot(x,y, label=f'path_delay_{index}', color='blue')

            if scatter_on is True:
                plt.scatter(x, y, color='green')
            else:
                plt.scatter(pot_rising[index], js[f'path_delay_{index}'][pot_rising[index]], color='green')
            if pot_middle[index]:
                plt.scatter(pot_middle[index], js[f'path_delay_{index}'][pot_middle[index]], color='red')
                title_color = 'red'

            # plt.legend(loc='lower right')
            plt.title(f'path_delay_{index}', color=title_color)
            plt.tight_layout()

    def __save(self, matrix, name):
        # name = sys._getframe().f_code.co_name
        save_file = self.save_path + f'/{matrix}_{name}.png'
        plt.savefig(save_file, dpi=self.dpi)
        print(f"save {matrix}:{name} to: " + save_file)
        plt.close()

    def __get_matrix(self):
        if self.matrix is None:
            mm = []
            for m in self.cal_json:
                mm.append(m)
        elif self.matrix.upper() in self.cal_json:
            mm = [self.matrix.upper()]
        else:
            assert 0, f'{self.matrix} not in json'
        return mm

    def phase(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__phase(js, width)
            self.__save(mat, sys._getframe().f_code.co_name)

    def modulator(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__modulator(js, width, scatter_on = self.scatter_on)
            self.__save(mat, sys._getframe().f_code.co_name)

    def mod_lut(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__mod_lut(js, width)
            self.__save(mat, sys._getframe().f_code.co_name)

    def weight(self, row = None):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            if row is None:
                for r in range(width):
                    self.__weight(js, width, row = r, scatter_on = self.scatter_on)
                    self.__save(mat, f'{sys._getframe().f_code.co_name}_row{r}')
            else:
                self.__weight(js, width, row)
                self.__save(mat, f'{sys._getframe().f_code.co_name}_row{row}')

    def wgt_lut_denoised(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__wgt_lut(js, width, denoised=True)
            self.__save(mat, sys._getframe().f_code.co_name)

    def wgt_lut_raw(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__wgt_lut(js, width, denoised=False)
            self.__save(mat, sys._getframe().f_code.co_name)

    def wgt_lut_specified(self, row):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__wgt_lut_specified(js, width, row = row)
            self.__save(mat, sys._getframe().f_code.co_name)

    def path_delay(self):
        for mat in self.__get_matrix():
            js = self.cal_json[mat]
            width = self.__matrix_width(mat)
            self.__path_delay(js, width, scatter_on = self.scatter_on)
            self.__save(mat, sys._getframe().f_code.co_name)

    def lut(self):
        self.mod_lut()
        self.wgt_lut_denoised()
        self.wgt_lut_raw()

    def all(self):
        self.phase()
        self.modulator()
        self.mod_lut()
        self.wgt_lut_denoised()
        self.wgt_lut_raw()
        self.weight()
        self.path_delay()

class MatrixArg:
    def __init__(self, argv):
        long_options = ["help", "path=", "matrix=", "scatter", "type=", "row=", "lut"]
        dict_options = self.__get_options(argv, long_options)
        for key, value in dict_options.items():
            setattr(self, key, value)
    def print_help(self):
        print(f'help    [h]: print help message')
        print(f'path=   [p]: specified json file')
        print(f'matrix= [m]: specified matrix (optional, default=all)')
        print(f'scatter [s]: turn on/off scatter (optional, default=off)')
        print(f'row=    [r]: specified weight row index (optional, default=all)')
        print(f'lut     [l]: only print lut (optional, default=false)')
        print(f'type=   [d]: specified curve type (optional, default=all)')
        print(f'supported curve type list: [phase, modulator, mod_lut, weight, wgt_lut_raw, wgt_lut_denoised, path_delay]')
    def print(self):
        print(vars(self))
    @staticmethod
    def __get_options(argv, long_options):
        short_options = ''
        dict_options = {}
        for l in long_options:
            short_options += l[0]
            if l[-1] == '=':
                short_options += ':'
                dict_options[l[:-1]] = None
            else:
                dict_options[l] = False
        args, dict_options['reserved'] = getopt.getopt(argv[1:], short_options, long_options)
        for arg, value in args:
            if arg[:2] == '--': # long_option
                if dict_options[arg[2:]] == False:  # without value
                    dict_options[arg[2:]] = True
                else:                               # within value
                    dict_options[arg[2:]] = value
            elif arg[:1] == '-': # short_option
                for l in long_options:
                    if arg[1] == l[0]: # match
                        if l[-1] == '=':            # within value
                            dict_options[l[:-1]] = value
                        else:                       # without value
                            dict_options[l] = True
            else:
                assert 0, f'unrecorgnized arg: {arg} = {value}'
        return dict_options

if __name__ == "__main__":
    arg = MatrixArg(sys.argv)
    if arg.help is True:
        arg.print_help()
        sys.exit(0)
    arg.print()
    d = PlotCal(json_path=arg.path, matrix=arg.matrix, dpi=150, scatter_on = False)
    if arg.lut == True:
        d.lut()
    elif arg.row is not None:
        d.wgt_lut_specified(row = arg.row)
    elif arg.type is None:
        d.all()
    else:
        type_func = getattr(d, arg.type)
        if type_func:
            type_func()
        else:
            print(f'{arg.type} not supported')
    