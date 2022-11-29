import pluggy
from meoteofence.hook_specs import PretreatmentSpec
from meoteofence.hook_impl import PretreatmentPlugin
from meoteofence import HOOK_NAMESPACE
from meoteofence import hdf5_read_ndarray
import time
import os
from multiprocessing import Pool

# ### 创建hook插件管理对象
# pm = pluggy.PluginManager(HOOK_NAMESPACE)
# ### 添加气象预处理接口
# pm.add_hookspecs(PretreatmentSpec)
# ### 注册气象预处理插件
# pm.register(PretreatmentPlugin())
# ### 开始执行(顺序循环方式运行)
# start_time = time.time()
# ### 配置初始参数
# file_path_list = os.listdir('./data/20221122')
# hdf5_store_path_pre = './data_handled/20221122/'
# station_location = (31.23,90.24)
# variable_name_list = ['Temperature','Relative humidity','Total Cloud Cover','Wind speed (gust)']
# ### 使用for循环
# for variable_name in variable_name_list:
#     print(variable_name)
#     for file in file_path_list:
#         file_path = './data/20221122/' + file
#         result = pm.hook.meoteo_pretreatment(file_path=file_path,
#                                              variable_name=variable_name,
#                                              station_location=station_location,
#                                              hdf5_store_path_pre=hdf5_store_path_pre,
#                                              resolution_ratio=0.25,
#                                              grid_size=6)
# print(result)
# end_time = time.time()
# sequential_runtime = end_time - start_time
# print('-------------------------- total time is {}'.format(sequential_runtime))






# def test_func():
## 使用multiprocessing进行并行执行
## 整理一个二级API
def secondary_api_meoteo_pretreatment(file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size):
    ### 创建hook插件管理对象
    pm = pluggy.PluginManager(HOOK_NAMESPACE)
    ### 添加气象预处理接口
    pm.add_hookspecs(PretreatmentSpec)
    ### 注册气象预处理插件
    pm.register(PretreatmentPlugin())
    ### 开始执行气象预处理程序
    result = pm.hook.meoteo_pretreatment(file_path=file_path,
                                            variable_name=variable_name,
                                            station_location=station_location,
                                            hdf5_store_path_pre=hdf5_store_path_pre,
                                            resolution_ratio=resolution_ratio,
                                            grid_size=grid_size)
    print(result)

    return result


folder_path = './data/20221122/'
hdf5_store_path_pre = './data_handled/20221122/'
station_location = (31.23,90.24)
variable_name_list = ['Temperature','Relative humidity','Total Cloud Cover','Wind speed (gust)']
resolution_ratio = 0.25
grid_size = 6
n_jobs = 4

def test_func(folder_path,hdf5_store_path_pre,station_location,variable_name_list,resolution_ratio,grid_size,n_jobs):
    ### 开始执行(时间并行方式运行)
    start_time = time.time()
    ### 配置初始参数
    # folder_path = './data/20221122/'
    file_path_list = os.listdir(folder_path)
    # hdf5_store_path_pre = './data_handled/20221122/'
    # station_location = (31.23,90.24)
    # variable_name_list = ['Temperature','Relative humidity','Total Cloud Cover','Wind speed (gust)']
    # resolution_ratio = 0.25
    # grid_size = 6
    # n_jobs = 4
    ### 使用进程池循环
    for variable_name in variable_name_list:
        ### 创建pool对象
        pool = Pool(n_jobs) 
        print(variable_name)
        for file in file_path_list:
            file_path = folder_path + file
            ### 向进程池队列添加事件
            pool.apply_async(func=secondary_api_meoteo_pretreatment,args=(file_path,variable_name,station_location,hdf5_store_path_pre,resolution_ratio,grid_size))
        ### 关闭进程池
        pool.close()
        ### 回收进程池
        pool.join()
    end_time = time.time()
    parallel_runtime = end_time - start_time
    print('-------------------------- total time is {}'.format(parallel_runtime))### 开始执行(时间并行方式运行)





test_func(folder_path,hdf5_store_path_pre,station_location,variable_name_list,resolution_ratio,grid_size,n_jobs)
### 从指定h5中读取对应ndarray数据
variable_name = 'Wind speed (gust)'#'Temperature' # 'Wind speed (gust)'
tmp_ndarray = hdf5_read_ndarray(h5path='./data_handled/20221122/f23.h5',var_name=variable_name,level_name='level_0') # level_100_m
print(tmp_ndarray)


