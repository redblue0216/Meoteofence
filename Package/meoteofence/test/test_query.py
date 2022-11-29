from meoteofence import hdf5_read_ndarray
import pandas as pd
import numpy as np



### 参数配置
### 自己手动制定需要的变量和层级和目标文件夹
hdf5_store_path_pre = './data_handled/20221122/'
variable_name = 'Wind speed (gust)' # 'Temperature'
level_name = 'level_0' # level_100_M
### 设置预报时间
forecast_time = 24



### 开始第一层循环----预报时间
### 创建一个初始空dataframe用于concat
tmp_concat_df = pd.DataFrame()
for i in range(0,forecast_time,1):
    if len(str(i)) == 1:
        h5file_name = 'f0' + str(i)
    else:
        h5file_name = 'f' + str(i)
    print(h5file_name)
    ### 从指定h5中读取对应ndarray数据
    tmp_ndarray = hdf5_read_ndarray(h5path='{}{}.h5'.format(hdf5_store_path_pre,h5file_name),var_name=variable_name,level_name=level_name) # level_100_m
    print(tmp_ndarray)
    ### 获取网格个数，以供后续使用
    length = list(tmp_ndarray.shape)[0] * list(tmp_ndarray.shape)[1]
    print(length)
    ### 将目标矩阵拉平，并转换为列表
    tmp_reshape_ndarray = tmp_ndarray.reshape(1,length)
    print(tmp_reshape_ndarray)
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
print('-------------------------------------------------------------------------------------------------------------------------------------------------')
print(tmp_concat_df)
# print(tmp_concat_df.time)




