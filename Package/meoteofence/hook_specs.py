# -*- coding: utf-8 -*-
# author:shihua
# coder:shihua
# 这是一个hook技术接口类，主要功能提供气象数据预处理接口，主要技术hook
"""
模块介绍
-------

这是一个hook技术接口类，主要功能提供气象数据预处理接口，主要技术hook

设计模式：

    （1）  无 

关键点：    

    （1）hook_specs

主要功能：            

    （1）hook技术接口                               

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import pluggy
import meoteofence




####### hook技术接口类 ######################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）hook_specs                                                      ###
### 主要功能：                                                           ###
### （1）hook技术接口                                                     ###
############################################################################


####### hook技术接口类 #####################################################################################
##########################################################################################################



hook_spec = pluggy.HookspecMarker(meoteofence.HOOK_NAMESPACE)



class PretreatmentSpec(object):
    '''
    类介绍：

        这是一个预处理接口类
    '''


    @hook_spec
    def meoteo_pretreatment(self,file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size):
        '''
        方法功能：

            定义一个气象预处理的接口方法

        参数：
            file_path (str): 文件路径
            variable_name (str): 变量名称
            station_location (tuple): 场站坐标元组
            hdf5_store_path_pre (str): hdf5存储路径前缀
            resolution_ratio (float): 分辨率
            grid_size (int): 网格大小

        返回：
            无
        '''

        pass



###############################################################################################################################################
###############################################################################################################################################

