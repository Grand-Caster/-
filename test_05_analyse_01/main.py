import pandas as pd

# 读取Excel文件
file_path = r'C:\Users\Grand_Caster\Desktop\test\test.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 处理“行业”信息：一些富豪可能属于多个行业，拆分多个行业
df['行业'] = df['信息'].apply(lambda x: x.split('：')[1] if pd.notnull(x) else '')

# 进一步处理行业：如果一个富豪属于多个行业，拆分为多个行业
df_industries = df.explode('行业')  # 将每个富豪的多个行业拆分为多行

# 去除行业列中的空值（防止影响统计）
df_industries = df_industries[df_industries['行业'].notna()]

# 统计每个行业的富豪数量和财富总和
industry_stats = df_industries.groupby('行业').agg(
    富豪数量=('排名', 'count'),  # 统计每个行业的富豪数量
    财富总和=('财富', 'sum')  # 计算每个行业的财富总和
).reset_index()

# 按财富总和排序，找出财富最多的行业
industry_stats = industry_stats.sort_values(by='财富总和', ascending=False)

# 打印出行业统计数据
print(industry_stats)

# 你可以选择将数据保存到新的 Excel 文件
output_file = r'C:\Users\Grand_Caster\Desktop\test\industry_analysis.xlsx'
industry_stats.to_excel(output_file, index=False, engine='openpyxl')

print(f"行业统计结果已保存到 {output_file}")
