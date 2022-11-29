from meoteofence.interface import data_drill_up
from scipy.interpolate import interp1d
import numpy as np 
import pandas as pd



### 根据变量和层级对指定文件夹下的数据进行上钻操作
tmp_concat_df_a = data_drill_up(hdf5_store_path_pre='./data_handled/20221123/',
                                 variable_name = 'Wind speed (gust)',
                                 level_name = 'level_0',
                                 forecast_time = 24)
tmp_concat_df_b = data_drill_up(hdf5_store_path_pre='./data_handled/20221124/',
                                 variable_name = 'Wind speed (gust)',
                                 level_name = 'level_0',
                                 forecast_time = 24)
tmp_concat_df = pd.concat([tmp_concat_df_a,tmp_concat_df_b],axis=0)
tmp_concat_df = tmp_concat_df.reset_index(drop=True)
# print(tmp_concat_df)   

def data_interpolate(tmp_concat_df,index_delta,kind):
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

tmp_interpolate_df = data_interpolate(tmp_concat_df=tmp_concat_df,index_delta=0.25,kind='linear')
tmp_target_df = tmp_interpolate_df.iloc[:96,:]
print(tmp_target_df)




