from meoteofence import get_initial_info_from_file,convert_matrix_to_list,get_coordinate_pairs_according_to_station,form_base_coordinate,combine_variable_and_levels,hdf5_write_ndaray,hdf5_read_ndarray,obtain_data_and_cache_to_hdf5
import pygrib 
import numpy as np
import os
import time

### 使用pygrib加载目标文件中的分层数据对象
file_path='./data/20221122/gfs.pgrb2.f19.grib2'
grbs = pygrib.open(file_path)
grbs.seek(0)
for grb in grbs:
    print(grb)


# ### 获取经纬度列表和坐标点位
# file_path='./data/20221122/gfs.pgrb2.f19.grib2'
# variable_name = 'Temperature' # Wind speed (gust) # Relative humidity # Total Cloud Cover
# locations,variable_level_list,grbs_obj = get_initial_info_from_file(file_path=file_path,variable_name=variable_name)


# ### 将经纬度坐标转换为两个列表
# latitude_list,longitude_list,longtitude_latitude_list = convert_matrix_to_list(locations=locations)
# # print(latitude_list,longitude_list,longtitude_latitude_list)


# ### 以场站坐标为依据从两个列表中选取坐标对，示例使用longtitude-31.23,latitude-90.24
# station_location = (31.23,90.24)
# upleft_standard_location,resolution_ratio = get_coordinate_pairs_according_to_station(longitude_list=longitude_list,latitude_list=latitude_list,station_location=station_location)
# print(upleft_standard_location,resolution_ratio)


# ### 对应形成坐标矩阵
# upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location= form_base_coordinate(upleft_standard_location=upleft_standard_location,resolution_ratio=0.25,grid_size=6)
# print(upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location)


# ### 组合变量与层级得到宽表字段
# variable_level_combine_list = combine_variable_and_levels(variable_name=variable_name,variable_level_list=variable_level_list)
# print(variable_level_combine_list)


# ### 获取数据并缓存到HDF5中
# obtain_data_and_cache_to_hdf5(grbs_obj=grbs_obj,
#                               variable_name=variable_name,
#                               variable_level_list=variable_level_list,
#                               hdf5_name='./data_handled/20221122/gfs.pgrb2.f19.h5',
#                               upleft_grid_location=upleft_grid_location,
#                               upright_grid_location=upright_grid_location,
#                               downleft_grid_location=downleft_grid_location,
#                               downright_grid_location=downright_grid_location)


# ### 从指定h5中读取对应ndarray数据
# tmp_ndarray = hdf5_read_ndarray(h5path='./data_handled/20221122/gfs.pgrb2.f00.h5',var_name=variable_name,level_name='level_100_m')
# print(tmp_ndarray)

### 整合成函数
def meoteo_pretreatment(file_path,variable_name,station_location):
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
    upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location= form_base_coordinate(upleft_standard_location=upleft_standard_location,resolution_ratio=0.25,grid_size=6)
    # print(upleft_grid_location,upright_grid_location,downleft_grid_location,downright_grid_location)
    ### 组合变量与层级得到宽表字段
    variable_level_combine_list = combine_variable_and_levels(variable_name=variable_name,variable_level_list=variable_level_list)
    # print(variable_level_combine_list)
    ### 获取数据并缓存到HDF5中
    ### 配置HDF5文件路径
    hdf5_file_path = file_path.split('.')[-2]+'.'+'h5'
    hdf5_file_path = hdf5_store_path_pre + hdf5_file_path
    print(hdf5_file_path)
    ### 开始向HDF5缓存
    obtain_data_and_cache_to_hdf5(grbs_obj=grbs_obj,
                                variable_name=variable_name,
                                variable_level_list=variable_level_list,
                                hdf5_name=hdf5_file_path,
                                upleft_grid_location=upleft_grid_location,
                                upright_grid_location=upright_grid_location,
                                downleft_grid_location=downleft_grid_location,
                                downright_grid_location=downright_grid_location)    
    print('======================================================>>>>>>',file)






### 根据预报时间开始顺序循环运行并统计时间
start_time = time.time()
### 配置初始参数
file_path_list = os.listdir('./data/20221122')
hdf5_store_path_pre = './data_handled/20221122/'
station_location = (31.23,90.24)
### 遍历变量列表处理
# variable_name = 'Wind speed (gust)' #'Temperature'
for variable_name in ['Temperature','Relative humidity','Total Cloud Cover','Wind speed (gust)']:
    print(variable_name)
    for file in file_path_list:
        file_path = './data/20221122/' + file
        meoteo_pretreatment(file_path=file_path,variable_name=variable_name,station_location=station_location)
end_time = time.time()
print('*************** total time is {}'.format(end_time-start_time))






### 从指定h5中读取对应ndarray数据
variable_name = 'Wind speed (gust)'#'Temperature' # 'Wind speed (gust)'
tmp_ndarray = hdf5_read_ndarray(h5path='./data_handled/20221122/f23.h5',var_name=variable_name,level_name='level_0') # level_100_m
print(tmp_ndarray)
