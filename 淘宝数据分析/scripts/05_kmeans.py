import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. 设置中文字体，防止图表乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 2. 读取我们刚刚导出的 RFM 数据
base_dir = r'E:/github练习文件夹/python练习文件/practice/淘宝数据分析/output'
rfm_file = os.path.join(base_dir, 'user_rfm.csv')
df = pd.read_csv(rfm_file)

# 先去掉可能存在的空值（如果有的话）
df = df.dropna()

print(f"✅ 成功读取 {len(df)} 个用户的 RFM 特征数据")

# 3. 数据标准化（K-Means 对数据范围极其敏感，必须标准化）
# 因为 recency 是几十，而 frequency 可能是几百，不标准化会导致聚类失效
features = ['recency', 'frequency', 'buy_count']
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# 4. 训练 K-Means 模型
# 我们设定 k=4，即分为 4 个群体
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(df_scaled)

# 5. 统计每个群体的特征（即聚类中心）
# 把标准化的中心点还原成真实数据
centers = scaler.inverse_transform(kmeans.cluster_centers_)
centers_df = pd.DataFrame(centers, columns=['平均最近活跃天数(R)', '平均活跃次数(F)', '平均购买次数(M)'])
centers_df['群体编号'] = range(k)
# 调整列顺序，便于查看
centers_df = centers_df[['群体编号', '平均最近活跃天数(R)', '平均活跃次数(F)', '平均购买次数(M)']]

print("\n--- 4个用户群体的特征中心 ---")
print(centers_df)

# 6. 可视化聚类结果（用散点图展示 F 和 M 的分布）
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='frequency',
    y='buy_count',
    hue='cluster',
    palette='viridis',
    data=df,
    alpha=0.7
)
plt.title('用户 K-Means 聚类分布图 (活跃度 vs 购买力)', fontsize=14)
plt.xlabel('活跃次数 (F)', fontsize=12)
plt.ylabel('购买次数 (M)', fontsize=12)
plt.legend(title='用户群体')
plt.grid(True, linestyle='--', alpha=0.5)

# 保存图片
save_path = os.path.join(base_dir, 'kmeans_clusters.png')
plt.savefig(save_path, dpi=300)
print(f"\n✅ 聚类图表已保存至：{save_path}")

# 7. 将带有聚类标签的数据保存，用于后续写报告
result_file = os.path.join(base_dir, 'user_clusters.csv')
df.to_csv(result_file, index=False)
print(f"✅ 带标签的用户数据已保存至：{result_file}")