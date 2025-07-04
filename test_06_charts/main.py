import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

# 设置中文字体（例如使用 SimHei 或 Microsoft YaHei）
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 或者 ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示问题

# 读取Excel文件
file_path = r'C:\Users\Grand_Caster\Desktop\test\test.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 处理“年龄”字段，将 "N/A" 转换为 NaN 并转换为数值
df['年龄'] = pd.to_numeric(df['年龄'], errors='coerce')

# 提取行业信息
df['行业'] = df['信息'].apply(lambda x: x.split('：')[1] if isinstance(x, str) and '行业：' in x else '未知')

# 可视化 1: 富豪年龄分布（柱状图）
plt.figure(figsize=(10, 6))
sns.histplot(df['年龄'].dropna(), bins=20, kde=True, color='blue')
plt.title("富豪年龄分布")
plt.xlabel("年龄")
plt.ylabel("富豪数量")
plt.savefig(r'C:\Users\Grand_Caster\Desktop\test\富豪年龄分布.png')  # 保存图表到桌面
plt.close()  # 关闭当前图表

# 可视化 2: 行业分布（柱状图）
industry_counts = df['行业'].value_counts().head(10)
plt.figure(figsize=(12, 6))
industry_counts.plot(kind='bar', color='green')
plt.title("富豪行业分布（前10）")
plt.xlabel("行业")
plt.ylabel("富豪数量")
plt.xticks(rotation=45, ha='right')
plt.savefig(r'C:\Users\Grand_Caster\Desktop\test\富豪行业分布.png')  # 保存图表到桌面
plt.close()  # 关闭当前图表

# 可视化 3: 财富分布（柱状图）
plt.figure(figsize=(10, 6))
sns.histplot(df['财富'], bins=20, kde=True, color='orange')
plt.title("富豪财富分布")
plt.xlabel("财富（亿）")
plt.ylabel("富豪数量")
plt.savefig(r'C:\Users\Grand_Caster\Desktop\test\富豪财富分布.png')  # 保存图表到桌面
plt.close()  # 关闭当前图表

# 可视化 4: 年龄与财富的相关性热力图
plt.figure(figsize=(8, 6))
correlation_matrix = df[['年龄', '财富']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.title("年龄与财富的相关性")
plt.savefig(r'C:\Users\Grand_Caster\Desktop\test\年龄与财富相关性.png')  # 保存图表到桌面
plt.close()  # 关闭当前图表
