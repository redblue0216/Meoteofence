# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个hook技术具体实现类，主要功能提供气象数据预处理具体实现，主要技术hook
"""
模块介绍
-------

这是一个hook技术具体实现类，主要功能提供气象数据预处理具体实现，主要技术hook

设计模式：

    （1）  无 

关键点：    

    （1）hook_impl

主要功能：            

    （1）hook技术具体实现                             

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import pluggy
import meoteofence
from meoteofence import get_initial_info_from_file,convert_matrix_to_list,get_coordinate_pairs_according_to_station,form_base_coordinate,combine_variable_and_levels,hdf5_write_ndaray,hdf5_read_ndarray,obtain_data_and_cache_to_hdf5
import pygrib 
import numpy as np
import os
import time



####### hook技术具体实现类 ###################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）hook_impl                                                      ###
### 主要功能：                                                           ###
### （1）hook技术具体实现                                                 ###
############################################################################


####### hook技术具体实现类 #####################################################################################
#############################################################################################################



hook_impl = pluggy.HookimplMarker(meoteofence.HOOK_NAMESPACE)



class PretreatmentPlugin(object):
    '''
    类介绍：

        这是一个预处理具体实现
    '''


    @hook_impl
    def meoteo_pretreatment(self,file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size):
        '''
        方法功能：

            定义一个气象预处理的具体实现方法

        参数：
            file_path (str): 文件路径
            variable_name (str): 变量名称
            station_location (tuple): 场站坐标元组
            hdf5_store_path_pre (str): hdf5存储路径前缀
            resolution_ratio (float): 分辨率
            grid_size (int): 网格大小

        返回：
            result (str): 运行结果信息
        '''

        ### 获取经纬度列表和坐标点位
        locations,variable_level_list,grbs_obj = get_initial_info_from_file(file_path=file_path,variable_name=variable_name)
        ### 将经纬度坐标转换为两个列表
        latitude_list,longitude_list,longtitude_latitude_list = convert_matrix_to_list(locations=locations)
        # print(latitude_list,longitude_list,longtitude_latitude_list)
        ### 以场站坐标为依据从两个列表中选取坐标对，示例使用longtitude-31.23,latitude-90.24
        # station_location = (31.23,90.24)
        upleft_standard_location,resolution_ratio = get_coordinate_pairs_according_to_station(longitude_list=longitude_list,latitude_list=latitude_list,station_location=station_location)
        # print(upleft_standard_location,resolution_ratio)
        ### 对应形成坐标矩阵
        upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location= form_base_coordinate(upleft_standard_location=upleft_standard_location,resolution_ratio=resolution_ratio,grid_size=grid_size)
        # print(upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location)
        ### 组合变量与层级得到宽表字段
        variable_level_combine_list = combine_variable_and_levels(variable_name=variable_name,variable_level_list=variable_level_list)
        # print(variable_level_combine_list)
        ### 获取数据并缓存到HDF5中
        ### 配置HDF5文件路径
        hdf5_file_path = file_path.split('.')[-2]+'.'+'h5'
        hdf5_file_path = hdf5_store_path_pre + hdf5_file_path
        # print(hdf5_file_path)
        ### 开始向HDF5缓存
        obtain_data_and_cache_to_hdf5(grbs_obj=grbs_obj,
                                    variable_name=variable_name,
                                    variable_level_list=variable_level_list,
                                    hdf5_name=hdf5_file_path,
                                    upleft_grid_location=upleft_grid_location,
                                    upright_grid_location=upright_grid_location,
                                    downleft_grid_location=downleft_grid_location,
                                    downright_grid_location=downright_grid_location)    
        print('======================================================>>>>>>',file_path,hdf5_file_path)
        result = "meoteo-pretreatment well done!"
        print(result)

        return result



###############################################################################################################################################
###############################################################################################################################################


