#查看
import pandas as pd
import os
file_path = r'E:/sql联系数据库来源/UserBehavior.csv'
output_path = 'E:/github练习文件夹/python练习文件/practice/淘宝数据分析/output/cleaned_user_behavior.csv'
print("正在读取文件，请稍后....")
columns = ['user_id','item_id','category_id','behavior_type','timestamp']
try:
    df = pd.read_csv(file_path,header=None,names=columns,nrows=1000000)
    print("数据读取成功")
except FileNotFoundError:
    print("找不到文件，请检查路径是否正确")
    exit()
except Exception as e:
    print("发生未知错误")
    exit()
 #数据清洗
print("\n---开始数据清洗---")
df.drop_duplicates(inplace=True)
df['time'] = pd.to_datetime(df['timestamp'],unit='s')
df['date'] = df['time'].dt.date
df['hour'] = df['time'].dt.hour
 #查看前五行
print("清洗数据前五行")
print(df.head())
print(f'\n清洗后总行数：{len(df)}')

 #保存文件
df.to_csv(output_path,index=False)
print(f"\n清洗完成，文件已保存到：{output_path}")