import pandas as pd
from sqlalchemy import create_engine
import os
#指定文件路径
csv_path = 'E:/github练习文件夹/python练习文件/practice/淘宝数据分析/output/cleaned_user_behavior.csv'

#数据库配置连接
user = 'root'
password = '123456'
host = 'localhost'
port = '3306'
database = 'taobao_analysis'

#创建数据库引擎（负责和MySQL建立连接）
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')

#读取csv数据
print('正在读取数据，请稍后')
df = pd.read_csv(csv_path)
print(f'读取成功，共{len(df)}行数据')

#写入MySQL数据库
print("正在导入数据库，这可能需要十几秒钟")
df.to_sql(name='user_behavior',con=engine,if_exists='replace',index=False)
print("导入成功，请去navicat查看")