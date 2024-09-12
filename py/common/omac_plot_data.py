import matplotlib.pyplot as plt
import numpy as np
# 导入目标文件
import os
from mpl_toolkits.mplot3d import Axes3D
import shutil
import sys
import importlib

def plot_3d_matrix(matrix, matrix_name="Matrix", save_path=None):
    """
    绘制二维矩阵数据的三维图形，并可选地保存为图片。

    参数:
        matrix (list of list of int): 二维矩阵数据，每行包含两个整数。
        matrix_name (str, optional): 矩阵的名字，将用作图形的标题。默认值为 "Matrix"。
        save_path (str, optional): 如果提供了保存路径，将图形保存为该路径的图片文件。
    """
    # 将数据转换为numpy数组
    data = np.array(matrix)

    # 分别提取X, Y, Z轴的数据
    x = np.arange(data.shape[0])  # 索引作为X轴
    y = data[:, 0]  # 第一列作为Y轴
    z = data[:, 1]  # 第二列作为Z轴

    # 创建三维图形
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制三维散点图
    ax.scatter(x, y, z, c='r', marker='')

    # 使用矩阵名作为标题
    ax.set_title(f'3D Visualization of {matrix_name}')
    ax.set_xlabel('Index')
    ax.set_ylabel('Column 0')
    ax.set_zlabel('Column 1')

    if save_path:
        plt.savefig(save_path)
    plt.close()

def show_2_dim_data(matrix, matrix_name="Matrix", save_path=None):
        # 将数据转换为numpy数组
    data = np.array(matrix)

    # 分别提取第一列和第二列的数据
    x = data[:, 0]
    y = data[:, 1]

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 绘制两个序列的折线图
    plt.plot(x, label='Column 0')
    plt.plot(y, label='Column 1')

    # 添加标题和标签
    plt.title(f' {matrix_name}')
    plt.xlabel('Index')
    plt.ylabel('Values')

    # 显示图例
    plt.legend()

    if save_path:
        plt.savefig(save_path)
    plt.close()



def are_strings_similar_with_btm_top(str1, str2):
    if len(str1) != len(str2):
        #print('length different')
        return False
    
    diff_count = 0
    i = 0
    while i < len(str1):
        if str1[i] != str2[i]:
            if (str1[i:i+3] == 'btm' and str2[i:i+3] == 'top') or (str1[i:i+3] == 'top' and str2[i:i+3] == 'btm'):
                i += 3
            else:
                print(f'{str1[i:i+3]} is different {str2[i:i+3]}')
                return False
        else:
            i += 1
    
    return True

def get_list_names_from_module(module):
    list_names = []
    attributes = dir(module)
    
    for attr in attributes:
        if not attr.startswith("__") and isinstance(getattr(module, attr), list):
            list_names.append(attr)
    
    return list_names

def plot_and_save_lists_from_module(module, output_dir):
    # 如果输出目录不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取模块中的所有属性
    attributes = dir(module)
    
    for attr in attributes:
        # 排除内置属性和非列表类型
        if not attr.startswith("__") and isinstance(getattr(module, attr), list):
            data = getattr(module, attr)
            if((np.array(data)).ndim==1):
                if all(isinstance(i, (int, float)) for i in data):
                    # 创建图表
                    if(len(data)==0):
                        continue
                    plt.figure()
                    plt.plot(data, marker='o')
                    plt.title(attr)
                    plt.xlabel('Index')
                    plt.ylabel('Value')
                    plt.grid(True)
                    folder_name=attr.split('_')
                    dir_path = os.path.join(output_dir,f'{folder_name[0]}')
                    os.makedirs(dir_path,exist_ok=True)
                    # 生成文件名并保存
                    file_path = os.path.join(dir_path, f"{attr}.png")
                    if os.path.exists(file_path):
                            plt.close()
                            continue
                    plt.savefig(file_path)
                    plt.close()  # 关闭图表以释放内存
            else:
                folder_name=attr.split('_')
                dir_path = os.path.join(output_dir,f'{folder_name[0]}')
                os.makedirs(dir_path,exist_ok=True)
                file_path =os.path.join(dir_path, f"{attr}.png")
                if os.path.exists(file_path):
                    continue
                show_2_dim_data(data,attr,file_path)
                #plot_3d_matrix(data,attr,file_path)

def remove_subdirectories(parent_dir):
    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)


def subtract_and_plot_similar_lists(module):
    list_names = get_list_names_from_module(module)
    for i in range(len(list_names)):
        for j in range(i + 1, len(list_names)):
            if(np.array(list_names[i]).ndim==1) and (np.array(list_names[j]).ndim==1):
                if are_strings_similar_with_btm_top(list_names[i], list_names[j]):
                    list1 = getattr(module, list_names[i])
                    list2 = getattr(module, list_names[j])
                    if (len(list1)==0) | (len(list2)==0) :
                        continue
                    if len(list1) == len(list2):
                        result = [a - b for a, b in zip(list1, list2)]
                        #print(f"Result of {list_names[i]} - {list_names[j]}: {result}")
                        
                        # 绘图
                        plt.figure()
                        plt.plot(result, marker='')
                        plt.title(f"{list_names[i]} - {list_names[j]}")
                        plt.xlabel('Index')
                        plt.ylabel('Difference')
                        plt.grid(True)
                        
                        # 保存图像
                        filename = f"{list_names[i]}_minus_{list_names[j]}.png"
                        mode_dir={list_names[i]}.split('_')
                        filename = os.path.join('logs',f'{mode_dir[0]}',filename)
                        if os.path.exists(filename):
                            plt.close()
                            continue
                        plt.savefig(filename)
                        plt.close()  # 关闭图表以释放内存
                else:
                    print(f"Length mismatch between {list_names[i]} and {list_names[j]}")
def draw_flow(module_path):
    current_folder = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(current_folder)

    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    if os.path.isdir(parent_folder):
        sys.path.append(parent_folder)
    else:
        print(f"目录不存在: {parent_folder}")
    module = importlib.import_module(module_path)
    remove_subdirectories('../logs')
    plot_and_save_lists_from_module(module,'../logs')
    subtract_and_plot_similar_lists(module)
    

if __name__ == "__main__":
    current_folder = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(current_folder)

    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    if os.path.isdir(parent_folder):
        sys.path.append(parent_folder)
    else:
        print(f"目录不存在: {parent_folder}")
    import X8P00_20240826_204140 as poltdata
    # 使用方法
    remove_subdirectories('../logs')
    plot_and_save_lists_from_module(poltdata,'../logs')
    subtract_and_plot_similar_lists(poltdata)



