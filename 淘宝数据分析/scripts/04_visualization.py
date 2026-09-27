import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体，防止图表里的中文显示为方块
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 文件路径
base_dir = r'E:/github练习文件夹/python练习文件/practice/淘宝数据分析/output'
daily_file = os.path.join(base_dir, 'daily_active.csv')
hourly_file = os.path.join(base_dir, 'hourly_active.csv')

# 1. 读取数据
df_daily = pd.read_csv(daily_file)
df_hourly = pd.read_csv(hourly_file)

# 2. 创建画布，准备画两张子图（一行两列）
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# --- 第一张图：按日期活跃趋势 ---
axes[0].plot(df_daily['日期'], df_daily['活跃用户数'], marker='o', color='b', linewidth=2)
axes[0].set_title('每日活跃用户数 (DAU) 趋势', fontsize=14)
axes[0].set_xlabel('日期')
axes[0].set_ylabel('活跃用户数')
axes[0].tick_params(axis='x', rotation=45)  # X轴日期倾斜，防重叠
axes[0].grid(True, linestyle='--', alpha=0.6)

# --- 第二张图：按小时活跃趋势 ---
axes[1].plot(df_hourly['小时'], df_hourly['活跃用户数'], marker='s', color='r', linewidth=2)
axes[1].set_title('每小时活跃用户数分布', fontsize=14)
axes[1].set_xlabel('小时 (0-23点)')
axes[1].set_ylabel('活跃用户数')
axes[1].set_xticks(range(0, 24)) # 强制显示 0-23 的所有刻度
axes[1].grid(True, linestyle='--', alpha=0.6)

# 3. 调整布局并保存
plt.tight_layout()
save_path = os.path.join(base_dir, 'active_analysis.png')
plt.savefig(save_path, dpi=300)
print(f"✅ 图表已保存至：{save_path}")

# 4. 在 PyCharm 里弹窗显示（如果你使用的是科学模式）
plt.show()