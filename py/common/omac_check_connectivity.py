import warnings
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import importlib
import os
import logs.X8P00_20240822_151311


def tile_list(path):
    if os.path.isdir(path):
        file_list = os.listdir(path)
        file_names = []
        for ii in range(len(file_list)):
            if ".py" in file_list[ii]:
                file_names.append(os.path.basename(file_list[ii]).split('.py')[0])
        return file_names


def data_check(data, ifplot=0):
    x = np.linspace(1, len(data), len(data))
    p = np.polyfit(x, data, 7)
    result = np.polyval(p, x)
    dynamic_range = np.max(result) - np.min(result)
    noise = np.std(np.array(result) - data)
    # mean_value = np.mean(result)
    if ifplot:
        plt.plot(x, data)
        plt.plot(x, result)

    if dynamic_range > noise * 10:
        return True
    else:
        return False


def connectivity_check(sip_name, tile_name, ifplot=1):
    data = importlib.import_module(sip_name + "." + tile_name)
    print(f'{sip_name + "." + tile_name}',data)
    if "X8" in tile_name:
        size = 8
    elif "X32" in tile_name:
        size = 32
    else:
        warnings.warn("wrong tile name, please check~")
        return False

    Headers = ["", "tx_pha_top", "tx_pha_btm", "tx_mod"]
    for ii in range(size):
        Headers.append("wgt_top_row" + str(ii))
        Headers.append("wgt_btm_row" + str(ii))
    connect_status = np.zeros([size + 1, 3 + size * 2 + 1],dtype=object)
    connect_status[0, :] = Headers
    ## tx part
    for ii in range(size):
        connect_status[ii+1,0] = "col"+str(ii)
        # pha_top
        tx_pha_top_ii = eval("data.pha_top_" + str(ii))
        if data_check(tx_pha_top_ii, ifplot):
            connect_status[ii+1, 1] = 1
        else:
            connect_status[ii+1, 1] = 0
        # pha_bot
        tx_pha_btm_ii = eval("data.pha_btm_" + str(ii))
        if data_check(tx_pha_btm_ii, ifplot):
            connect_status[ii+1, 2] = 1
        else:
            connect_status[ii+1, 2] = 0

        # mod
        tx_mod_ii = eval("data.mod_" + str(ii))
        if data_check(tx_mod_ii, ifplot):
            connect_status[ii+1, 3] = 1
        else:
            connect_status[ii+1, 3] = 0
    #weight part
    print(size)
    for ii in range(size):  # row index, same RX
        for jj in range(size):  # col index, same tx channel

            mod_top_ff_rowii_coljj = eval("data.mod_top_ff_row" + str(ii) + "_col" + str(jj))
            if(mod_top_ff_rowii_coljj == []):
                break
            #print(mod_top_ff_rowii_coljj)
            mod_top_00_rowii_coljj = eval("data.mod_top_00_row" + str(ii) + "_col" + str(jj))
            #print(mod_top_00_rowii_coljj)
            mod_top_rowii_coljj = np.array(mod_top_ff_rowii_coljj) - mod_top_00_rowii_coljj
            #print(mod_top_rowii_coljj)
            if data_check(mod_top_rowii_coljj, ifplot):
                connect_status[jj+1, 3 + 2 * ii+1] = 1
            else:
                connect_status[jj+1, 3 + 2 * ii+1] = 0

            mod_btm_ff_rowii_coljj = eval("data.mod_btm_ff_row" + str(ii) + "_col" + str(jj))
            mod_btm_00_rowii_coljj = eval("data.mod_btm_00_row" + str(ii) + "_col" + str(jj))
            mod_btm_rowii_coljj = np.array(mod_btm_ff_rowii_coljj) - mod_btm_00_rowii_coljj
            if data_check(mod_btm_rowii_coljj, ifplot):
                connect_status[jj+1, 3 + 2 * ii + 2] = 1
            else:
                connect_status[jj+1, 3 + 2 * ii + 2] = 0

    return connect_status


SiP_name = "logs"
file_path = "./" + SiP_name + "/"
tiles = tile_list(file_path)
wb = openpyxl.Workbook("info")
for tile in tiles:
    status = connectivity_check(SiP_name, tile, ifplot=1)
    if status is not False:
        sheet1 = wb.create_sheet(tile)
        for element in status:
            sheet1.append(element.tolist())
wb.save(SiP_name + ".xls")
wb.close()
plt.show()
