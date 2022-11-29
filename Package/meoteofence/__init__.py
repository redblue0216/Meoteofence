# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个包入口文件，主要功能收集各种工具函数，主要技术__all__暴露指定函数
"""
模块介绍
-------

这是一个包入口文件，主要功能收集各种工具函数，主要技术__all__暴露指定函数

设计模式：

    （1）  无 

关键点：    

    （1）__all__

主要功能：            

    （1）基础操作工具集合                                

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import pygrib
from tables import *
import numpy as np
import pandas as pd



####### 基础工具集合类 ######################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）基础依赖                                                        ###
### 主要功能：                                                           ###
### （1）基础操作工具集合                                                 ###
############################################################################


####### 基础工具集合 #####################################################################################
########################################################################################################



### 暴露指定的公开接口
__all__ = ['get_coordinate_matrix_from_file',
           'convert_matrix_to_list',
           'get_coordinate_pairs_according_to_station',
           'form_base_coordinate',
           'combine_variable_and_levels',
           'hdf5_write_ndaray',
           'hdf5_read_ndarray',
           'obtain_data_and_cache_to_hdf5',
           'HOOK_NAMESPACE']



HOOK_NAMESPACE = 'meoteofence'



def get_initial_info_from_file(file_path,variable_name):
    '''
    函数功能：

        定义一个获取文件经纬度的函数

    参数：
        file_path (str): 文件路径
        variable_name (str): 变量名称

    返回：
        locations (object): 坐标点位信息
        variable_level_list (list): 层级列表
        grbs_obj (object): grbs对象
    ''' 

    ### 使用pygrib加载目标文件中的分层数据对象
    grbs = pygrib.open(file_path)
    grbs.seek(0)
    ### 缓存grbs对象
    grbs_obj = grbs.select(name=variable_name)
    ### 根据变量来获取经纬度表
    locations = grbs_obj[0].latlons()
    ### 根据变量来获取层级列表
    variable_level_list = []
    ### 获取grbs层级
    levels = len(grbs.select(name=variable_name))
    ### 遍历grbs以获取层级列表
    for i in range(0,levels,1):
        grb = grbs_obj[i]
        grb_str = str(grb)
        start_index = grb_str.find('level')
        sub_grb_str = grb_str[start_index:]
        sub_grb_str_split = sub_grb_str.split(':')
        variable_level_list.append(sub_grb_str_split[0].replace(' ','_'))

    return locations,variable_level_list,grbs_obj



def convert_matrix_to_list(locations):
    '''
    函数功能：

        定义一个将坐标信息转换为两个列表和坐标元组列表的函数

    参数：
        locations (object): pygrib获取的坐标信息

    返回：
        longitude (list): 纬度列表
        latitude (list): 经度列表
        longitude_latitude_list (list): 经纬度列表    
    '''

    ### 对经纬度进行处理，得到坐标点位数据对
    latitude_array = np.array(locations[0])
    longitude_array = np.array(locations[1])
    latitude_list = [list(set(latitude_array[i]))[0] for i in range(0,latitude_array.shape[0])]
    longitude_list = list(longitude_array[0])
    longitude_latitude_list = [(i,j) for i in latitude_list for j in longitude_list]

    return latitude_list,longitude_list,longitude_latitude_list



def get_coordinate_pairs_according_to_station(longitude_list,latitude_list,station_location):
    '''
    函数功能：

        定义一个以场站坐标为依据从两列表中选取坐标对的函数

    参数：
        longitude_list (list): 经度列表
        latitude_list (list): 纬度列表
        station_location (tuple): 场站坐标元组

    返回：
        upleft_standard_location (tuple): 选取的左上标准点位
        resolution_ratio (float): 网格分辨率
    '''

    ### 选取左上标准点位
    chanced_longitude_list = [i for i in longitude_list if i>=station_location[1]]
    chanced_latitude_list = [i for i in latitude_list if i>=station_location[0]]
    upleft_standard_location = (chanced_latitude_list[0],chanced_longitude_list[0])
    ### 计算网格分辨率
    resolution_ratio = chanced_latitude_list[1] - chanced_latitude_list[0]

    return upleft_standard_location,resolution_ratio



def form_base_coordinate(upleft_standard_location,resolution_ratio,grid_size):
    '''
    函数功能：

        定义一个对应形成矩阵的函数

    参数：
        upleft_standard_location (tuple): 左上标准点位
        resolution_ratio (float): 网格分辨率
        grid_size (int): 网格大小

    返回：
        upleft_grid_location (tuple): 目标网格左上点位
        upright_grid_location (tuple): 目标网格右上点位
        downleft_grid_location (tuple): 目标网格左下点位
        downright_grid_location (tuple): 目标网格右下点位
    '''

    ### 根据网格大小确定划分步长
    if grid_size % 2 == 0: ### 取余为0则为偶数
        up_step = grid_size / 2 -1
        left_step = grid_size / 2 -1
    else: ### 其他情况则为奇数
        up_step = int((grid_size-1) / 2)
        left_step = int((grid_size-1) / 2)
    ### 根据步长先锁定目标网格左上点位，然后根据网格大小参数确定目标网格的其余四点位
    upleft_grid_location = (upleft_standard_location[0]+up_step*resolution_ratio,upleft_standard_location[1]+left_step*resolution_ratio)
    upright_grid_location = (upleft_grid_location[0],upleft_grid_location[1]+(grid_size-1)*resolution_ratio)
    downleft_grid_location = (upleft_grid_location[0]-(grid_size-1)*resolution_ratio,upleft_grid_location[1])
    downright_grid_location = (upleft_grid_location[0]-(grid_size-1)*resolution_ratio,upleft_grid_location[1]+(grid_size-1)*resolution_ratio)

    return upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location
    


def combine_variable_and_levels(variable_name,variable_level_list):
    '''
    函数功能：

        定义一个组合变量与层级的函数

    参数：
        variable_name (str): 变量名称
        variable_level_list (list): 层级列表

    返回：
        variable_level_combine_list (list): 变量层级组合列表
    '''

    variable_level_combine_list = [variable_name+'_'+tmp_level for tmp_level in variable_level_list]

    return variable_level_combine_list



def hdf5_write_ndaray(h5path,var_name,level_name,ndarray_obj):
    '''
    函数功能：

        定义一个将ndarray写入H5文件的方法

    参数：
        h5path (str): hdf5文件路径
        var_name (str): 气象物理量名称，对应HDF5的组名称
        level_name (str): 气象空间维度层级名称，对应HDF5的数据集合名称
        ndarray_obj (numpy.ndarray): numpy的ndarray矩阵数据对象

    返回：
        result (str): 运行结果信息
    '''

    ### 打开文件流，以追加的模式打开
    h5file = open_file(filename=h5path,mode='a')
    ### 创建数据组
    try:
        data_group = h5file.create_group(where="/",name=var_name,title="meoteovar is {}".format(var_name))
    except:
        data_group = "/{}".format(var_name)
    ### 压缩算法选择
    filters = Filters(complevel=5,complib='blosc')
    ### 在数据组下写入数据对象
    try:
        h5file.create_earray(where=data_group,name=level_name,obj=ndarray_obj,filters=filters)
    except:
        pass
    ### 关闭文件流
    h5file.close()
    result = 'Hdf5 write data well done!'
    print(result)

    return result



def hdf5_read_ndarray(h5path,var_name,level_name):
    '''
    函数功能：

        定义一个hdf5读取数据的方法

    参数：
        h5path (str): hdf5文件路径
        var_name (str): 气象物理量名称，对应HDF5的组名称
        level_name (str): 气象空间维度层级名称，对应HDF5的数据集合名称

    返回：
        ndarray_obj (numpy.ndarray): numpy的ndarray矩阵数据对象
    '''

    ### 打开文件流
    h5file = open_file(filename=h5path,mode='r')
    ### 获取数据索引
    data_reader = h5file.get_node(where='/{}'.format(var_name),name=level_name)
    ### 获取数据帧
    data_ndarray = data_reader.read()
    ### 关闭文件流
    h5file.close()
    result = 'HDF5 read ndarray well done!'
    print(result)

    return data_ndarray



def obtain_data_and_cache_to_hdf5(grbs_obj,variable_name,variable_level_list,hdf5_name,upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location):
    '''
    函数功能：

        定义一个获取数据并缓存到HDF5中的函数

    参数：
        grbs_obj (object): grbs对象
        variable_name (str): 气象物理量名称
        variable_level_list (list): 变量层级列表
        hdf5_name (str): hdf5文件名称
        upleft_grid_location (tuple): 左上基准点位
        upright_grid_location (tuple): 右上基准点位
        downleft_grid_location (tuple): 左下基准点位
        downright_grid_location (tuple): 右下基准点位

    返回：
        result (str): 运行结果信息
    '''

    ### 根据变量层级遍历获取数据，grbs_obj为给定变量的grbs查询对象
    for i,tmp_var_level in enumerate(variable_level_list):
        print(i,tmp_var_level)
        grb = grbs_obj[i]
        tmp = grb.data(lat1=downleft_grid_location[0],lat2=upleft_grid_location[0],lon1=upleft_grid_location[1],lon2=upright_grid_location[1])
        ### 索引选择0,表示选择对应网格上的物理量矩阵
        # print(tmp[0],type(tmp[0]))
        # print(tmp[0].shape,grb)
        ### 根据hdf5_name创建一个H5文件对象
        result = hdf5_write_ndaray(h5path=hdf5_name,var_name=variable_name,level_name=tmp_var_level,ndarray_obj=tmp[0])
        print(result)



#####################################################################################################################################################################
#####################################################################################################################################################################


