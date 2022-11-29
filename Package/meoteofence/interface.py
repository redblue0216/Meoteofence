# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个meoteofence对外接口封装类，主要功能对外提供封装好接口。
"""
模块介绍
-------

这是一个meoteofence对外接口封装类，主要功能对外提供封装好接口。

设计模式：

    （1）  无 

关键点：    

    （1）接口封装

主要功能：            

    （1）对外提供封装接口                          

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import pluggy
from meoteofence.hook_specs import PretreatmentSpec
from meoteofence.hook_impl import PretreatmentPlugin
from meoteofence import HOOK_NAMESPACE
from meoteofence import hdf5_read_ndarray
import time
import os
from multiprocessing import Pool
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d



####### 对外接口封装类 ######################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）接口封装                                                        ###
### 主要功能：                                                           ###
### （1）对外提供封装接口                                                  ###
############################################################################



####### 整理的二级API ###########################################################################################
###############################################################################################################



### 整理一个二级API
def secondary_api_meoteo_pretreatment(file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size):
    '''
    方法功能：

        定义一个气象预处理的二级API

    参数：
        file_path (str): 预处理数据目标文件夹
        hdf5_store_path_pre (str): hdf5存储路径前缀
        station_location (tuple): 场站坐标元组
        variable_name_list (list): 气象物理量列表
        resolution_ratio (float): 分辨率
        grid_size (int): 网格大小

    返回：
        result (str): 运行结果信息
    '''

    ### 创建hook插件管理对象
    pm = pluggy.PluginManager(HOOK_NAMESPACE)
    ### 添加气象预处理接口
    pm.add_hookspecs(PretreatmentSpec)
    ### 注册气象预处理插件
    pm.register(PretreatmentPlugin())
    result = pm.hook.meoteo_pretreatment(file_path=file_path,
                                         variable_name=variable_name,
                                         station_location=station_location,
                                         hdf5_store_path_pre=hdf5_store_path_pre,
                                         resolution_ratio=resolution_ratio,
                                         grid_size=grid_size)
    print(result)

    return result



####### 对外接口封装类 ########################################################################################
#############################################################################################################



class Meoteodata(object):
    '''
    类介绍:

        这是一个气象数据对象类,主要功能提供气象相关处理操作
    '''


    def __init__(self,base_folder_path,hdf5_store_path_pre,station_location,variable_name_list,resolution_ratio,grid_size,n_jobs):
        '''
        属性功能:

            定义一个初始化属性的功能方法

        参数:
            base_folder_path (str): 预处理数据目标文件夹
            hdf5_store_path_pre (str): hdf5存储路径前缀
            station_location (tuple): 场站坐标元组
            variable_name_list (list): 气象物理量列表
            resolution_ratio (float): 分辨率
            grid_size (int): 网格大小
            n_jobs (int): 并行个数
        '''

        self.base_folder_path = base_folder_path
        self.file_path_list = os.listdir(self.base_folder_path)
        self.hdf5_store_path_pre = hdf5_store_path_pre
        self.station_location = station_location
        self.variable_name_list = variable_name_list
        self.resolution_ratio = resolution_ratio
        self.grid_size = grid_size
        self.n_jobs = n_jobs


    def run(self):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            base_folder_path (str): 预处理数据目标文件夹
            hdf5_store_path_pre (str): hdf5存储路径前缀
            station_location (tuple): 场站坐标元组
            variable_name_list (list): 气象物理量列表
            resolution_ratio (float): 分辨率
            grid_size (int): 网格大小
            n_jobs (int): 并行个数

        返回：
            result (str): 运行结果信息,包含运行时间信息
        '''


        ### 配置初始参数
        base_folder_path = self.base_folder_path
        file_path_list = self.file_path_list
        hdf5_store_path_pre = self.hdf5_store_path_pre
        station_location = self.station_location
        variable_name_list = self.variable_name_list
        resolution_ratio = self.resolution_ratio
        grid_size = self.grid_size
        n_jobs = self.n_jobs
        ### 使用multiprocessing进行并行执行
        ### 开始执行(时间并行方式运行)
        start_time = time.time()
        ### 使用进程池循环
        for variable_name in variable_name_list:
            ### 创建pool对象
            pool = Pool(n_jobs) 
            print(variable_name)
            for file in file_path_list:
                file_path = base_folder_path + file
                ### 向进程池队列添加事件
                pool.apply_async(func=secondary_api_meoteo_pretreatment,args=(file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size))
            ### 关闭进程池
            pool.close()
            ### 回收进程池
            pool.join()
        end_time = time.time()
        parallel_runtime = end_time - start_time
        result = 'meoteodata run well done! Total time is {}'.format(parallel_runtime)

        return result



####### 工具函数集合 ###########################################################################################################################################################################
##############################################################################################################################################################################################



### 查询工具函数
def data_drill_up(hdf5_store_path_pre,variable_name,level_name,forecast_time):
    '''
    方法功能：

        定义一个从指定日期HDF5文件夹中进行数据上钻查询的方法，以预报时间为行索引，以变量和层级组合为列索引。

    参数：
        hdf5_store_path_pre (str): hdf5存储路径前缀
        variable_name_list (str): 气象物理量
        level_name (str): 层级名称
        forecast_time (int): 预报时间长度

    返回：
        tmp_concat_df (DataFrame): 组合拼接好的数据集合
    '''

    ### 开始第一层循环----预报时间
    ### 创建一个初始空dataframe用于concat
    tmp_concat_df = pd.DataFrame()
    for i in range(0,forecast_time,1):
        if len(str(i)) == 1:
            h5file_name = 'f0' + str(i)
        else:
            h5file_name = 'f' + str(i)
        # print(h5file_name)
        ### 从指定h5中读取对应ndarray数据
        tmp_ndarray = hdf5_read_ndarray(h5path='{}{}.h5'.format(hdf5_store_path_pre,h5file_name),var_name=variable_name,level_name=level_name) # level_100_m
        # print(tmp_ndarray)
        ### 获取网格个数，以供后续使用
        length = list(tmp_ndarray.shape)[0] * list(tmp_ndarray.shape)[1]
        # print(length)
        ### 将目标矩阵拉平，并转换为列表
        tmp_reshape_ndarray = tmp_ndarray.reshape(1,length)
        # print(tmp_reshape_ndarray)
        ### 按照宽表构建dataframe
        tmp_df = pd.DataFrame(tmp_reshape_ndarray)
        tmp_concat_df = pd.concat([tmp_concat_df,tmp_df],axis=0) ### 选择axis参数0,按行合并
    ### 重置索引
    tmp_concat_df = tmp_concat_df.reset_index(drop=True)
    ### 重新整理列名----var-level-location
    ### 创建一个空列表用于重新命名列名
    tmp_column_name_list = []
    ### 重新整理列名并添加到tmp_column_name_list中
    for i in range(0,length,1):
        tmp_column_name = str(variable_name) + ':' + str(level_name) + ':' + str(i)
        tmp_column_name_list.append(tmp_column_name)
    ### 重置tmp_concat_df列名
    tmp_concat_df.columns = tmp_column_name_list
    # ### 创建时间列
    # tmp_time_list = [i+1 for i in range(0,int(forecast_time),1)]
    # ### 向tmp_concat_df添加时间列
    # tmp_concat_df['time'] = tmp_time_list
    # print('-------------------------------------------------------------------------------------------------------------------------------------------------')
    # print(tmp_concat_df)
    # print(tmp_concat_df.time)
    result = 'Data concat well done!'
    print(result)

    return tmp_concat_df



### 数据插值工具函数
def data_interpolate(tmp_concat_df,index_delta,kind):
    '''
    函数功能：

        定义一个针对气象数据进行插值的函数

    参数：
        tmp_concat_df (dataframe): 拼接好的数据集合
        index_delta (float): 索引间隔
        kind (str): 插值方法

    返回：
        tmp_interpolate_df (dataframe): 插值完成的数据集合
    '''

    ### 创建一个空dataframe用来装插值后的变量列表
    tmp_interpolate_df = pd.DataFrame()
    ### 开始循环----dataframe列变量
    first_column_name = tmp_concat_df.columns[0]
    ### 选取变量
    tmp_array = tmp_concat_df[first_column_name].values
    # print(tmp_array,type(tmp_array))
    ### 确定原本的x值
    tmp_original_x = np.array(list(tmp_concat_df.index))
    for tmp_column_name in tmp_concat_df.columns:
        # print(tmp_column_name)
        ### 对数据进行插值
        ### 拟合曲线
        tmp_func = interp1d(tmp_original_x,tmp_array,kind=kind)
        ### 用拟合好的曲线在新的序列上计算新的值
        start_index = tmp_concat_df.index[0]
        end_index = tmp_concat_df.index[-1]
        # index_delta = 0.25
        tmp_new_x = np.arange(start_index,end_index+index_delta,index_delta)
        tmp_new_array = tmp_func(tmp_new_x)
        tmp_interpolate_df[tmp_column_name] = list(tmp_new_array)

    return tmp_interpolate_df



############################################################################################################################################################################################
############################################################################################################################################################################################


