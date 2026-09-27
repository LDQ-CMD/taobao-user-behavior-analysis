淘宝用户行为数据分析项目 - 全流程复盘文档
一、 项目概述
项目名称：淘宝用户行为数据分析 (Taobao User Behavior Analysis)

数据集来源：阿里天池公开数据集 (UserBehavior.csv)

数据规模：原始数据约3.5GB，抽样清洗后提取100万条记录

技术栈：Python (Pandas, Matplotlib, Seaborn, Scikit-learn), MySQL, Navicat

核心目标：通过数据清洗、SQL多维度分析、可视化及机器学习聚类，挖掘用户行为规律，输出业务运营优化建议。

二、 项目整体步骤 (宏观流程)
整个项目遵循了数据分析的标准闭环：
环境准备 ➔ 数据获取与清洗 ➔ 数据入库 ➔ SQL业务分析 ➔ 数据可视化 ➔ 机器学习挖掘 ➔ 输出业务洞察

三、 具体实操步骤与核心产出 (微观细节)
阶段1：环境准备与数据获取
任务：搭建开发环境，获取并存放原始数据。

核心操作：

在 PyCharm 的虚拟环境安装 pandas, numpy, matplotlib, seaborn, scikit-learn, sqlalchemy, pymysql。
从阿里天池下载 UserBehavior.csv.zip (905MB)，解压后存放于项目 data 文件夹。
⚠️ 踩坑与解决：

问题：PyCharm 直接打开 3.5GB 的 CSV 导致内存溢出报错 java.lang.NegativeArraySizeException。

解决：调整项目结构，确保数据文件不在 .idea 配置目录中，且不在 PyCharm 中双击打开大文件。

阶段2：数据清洗 (Pandas)
任务：对百万级数据进行去重、格式转换，保存为干净的中间文件。

核心操作：

使用 pd.read_csv(..., nrows=1000000) 抽样读取前100万行，避免内存崩溃。
定义列名：['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp']。
数据去重：df.drop_duplicates(inplace=True)。
时间戳转换：pd.to_datetime(df['timestamp'], unit='s')，拆分出 date (日期) 和 hour (小时) 字段。
产出物：cleaned_user_behavior.csv (约70MB，包含清洗后的100万条数据)。

⚠️ 踩坑与解决：

问题：权限报错 PermissionError。

解决：修正 output_path，必须精确到 xxx.csv 文件，且避免写入 .idea 目录。

阶段3：数据入库 (Python + MySQL)
任务：将清洗后的数据导入关系型数据库，为 SQL 分析做准备。

核心操作：

在 Navicat 中创建数据库 taobao_analysis (字符集 utf8mb4)。
编写 Python 脚本连接数据库：create_engine('mysql+pymysql://root:密码@localhost:3306/taobao_analysis')。
使用 df.to_sql('user_behavior', con=engine, if_exists='replace', index=False) 将数据整表写入。
⚠️ 踩坑与解决：

问题：驱动名称拼写错误 NoSuchModuleError。

解决：将连接字符串中的 mysql+pysql 修正为 mysql+pymysql。

阶段4：SQL业务分析 (Navicat)
任务：通过 SQL 查询，计算核心业务指标。

核心操作与产出：

基础概览：统计总记录数（100万）和独立用户数（9739人）。
漏斗转化分析：计算浏览(pv)、加购(cart)、收藏(fav)、购买(buy)的独立用户数及转化率（浏览到加购转化率75.45%，加购到购买转化率91.34%）。
用户活跃度分析：
按日期统计 DAU，发现峰值在 12-02（9314人），符合大促蓄水规律。
按小时统计活跃度，发现存在午休（12-14点）和晚间（20-22点）双高峰特征。
阶段5：数据可视化 (Python)
任务：将 SQL 分析结果绘制为折线图，用于直观展示。

核心操作：

从 Navicat 将 DAU 和每小时活跃度结果导出为 daily_active.csv 和 hourly_active.csv。
使用 matplotlib.pyplot 和 seaborn 绘图。
配置中文字体 plt.rcParams['font.sans-serif'] = ['SimHei'] 防止乱码。
产出物：active_analysis.png (包含 DAU 趋势和每小时活跃分布的双折线图)。

阶段6：K-Means 用户聚类 (机器学习)
任务：基于 RFM 模型对用户进行分群画像。

核心操作：

在 SQL 中提取特征：recency (最近活跃天数)、frequency (活跃总次数)、buy_count (购买次数，替代M值)，导出为 user_rfm.csv。
数据标准化：由于 R、F、M 数量级差异大，使用 StandardScaler 进行标准化。
模型训练：设定 k=4，运行 KMeans(n_clusters=4, random_state=42)。
结果还原与可视化：将聚类中心还原为真实数据，使用 seaborn.scatterplot 绘制散点图。
产出物：

kmeans_clusters.png (用户聚类散点图)

user_clusters.csv (带聚类标签的用户数据)

四、 业务成果与洞察 (项目亮点)
通过上述分析，最终得出了以下核心业务洞察，可在面试或报告中展示：

转化漏斗痛点：虽然加购到购买的转化率极高（91.34%），但浏览到加购仍有流失。高转化率说明样本期（大促前夕）用户购买意愿极强。

用户活跃规律：中午12-14点和晚上20-22点为流量高峰，建议电商运营将秒杀、直播等活动安排在这些时间段。

四大用户画像 (基于K-Means聚类)：

高价值用户 (群体3)：活跃度高且购买次数多（黄点）。策略：VIP客服、会员折扣，重点留存。

高频潜力用户 (群体2)：活跃度高但购买次数低（绿点）。策略：定向发放满减优惠券，解决“只逛不买”问题。

低频/流失用户 (群体0和1)：活跃度和购买频次双低（紫点和蓝点）。策略：推送爆款、新人礼包进行拉新和促活。


<img width="3000" height="1800" alt="kmeans_clusters" src="https://github.com/user-attachments/assets/f031c03b-40d2-4b5c-b68a-b819a14fa4b9" />

<img width="4500" height="1500" alt="active_analysis" src="https://github.com/user-attachments/assets/5f84ad90-d858-4185-98d9-0398d3de0871" />
