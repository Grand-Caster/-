from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # 导入正则表达式模块

# 存储所有排名数据
all_data = []

# 启动 Playwright
with sync_playwright() as p:
    # 启动 Chromium 浏览器
    browser = p.chromium.launch(headless=True)  # headless=True 表示无界面启动
    page = browser.new_page()

    # 打开网页
    url = 'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich'
    page.goto(url)

    # 等待页面加载
    page.wait_for_timeout(5000)  # 等待5秒，确保页面加载完成


    # 获取所有数据
    def extract_data():
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # 提取排名信息
        rank = [em.text.strip() for em in
                soup.find_all('em', {'style': 'font-weight:bold;color:#333;font-style: italic;font-size:1.4rem;'})]

        # 提取姓名和年龄
        names = []
        ages = []
        for div in soup.find_all('div', class_='hs-index-list-name mb-2'):
            name = div.find('span', class_='hs-font-bold mb-2').text.strip()
            age_gender = div.find('em', class_='hs-index-list-gender mr-2').text.strip()

            # 使用正则表达式提取年龄（忽略性别信息）
            age_match = re.search(r'\d+', age_gender)  # 查找数字部分
            age = age_match.group(0) if age_match else "N/A"  # 获取匹配的数字，若没有则为 "N/A"

            names.append(name)
            ages.append(age)

        # 提取财富数据
        wealth = []
        for p in soup.find_all('p', style="font-weight:400;color:#333;margin-bottom:0;"):
            amount = p.find('em', style="font-size:1.4rem;margin:0 0.2rem;font-weight:bold;")
            if amount:
                wealth.append(amount.text.strip())
            else:
                wealth.append("N/A")

        # 提取公司数据
        company = [comp.text.strip() for comp in soup.find_all('p', class_='company mb-2')]

        # 提取信息数据
        info = [info.text.strip() for info in soup.find_all('p', class_='industry mb-2')]

        return rank, names, ages, wealth, company, info


    # 初始数据提取
    rank, names, ages, wealth, company, info = extract_data()
    all_data.extend(zip(rank, names, ages, wealth, company, info))


    # 获取当前页的排名，用于判断是否回到了第一页
    def is_first_page():
        rank, _, _, _, _, _ = extract_data()
        return rank[0] == '1'  # 如果当前排名为1，说明是第一页


    # 模拟翻页：通过定位“下一页”按钮进行翻页
    while True:
        try:
            # 查找“下一页”按钮并点击
            next_button = page.locator('li.page-item.page-next a.page-link')  # 定位到“下一页”按钮
            if next_button.is_visible():
                print("点击 '下一页' 按钮...")
                next_button.click()
                page.wait_for_timeout(5000)  # 等待5秒，确保新内容加载
                rank, names, ages, wealth, company, info = extract_data()  # 获取新一页的数据
                all_data.extend(zip(rank, names, ages, wealth, company, info))

                # 检查当前页面是否已经回到了第一页
                if is_first_page():
                    print("已经回到第一页，停止翻页")
                    break  # 如果回到了第一页，退出循环
            else:
                break  # 如果没有找到“下一页”按钮，则退出循环
        except Exception as e:
            print("翻页错误:", e)
            break  # 如果发生错误，跳出循环

    # 打印所有爬取到的数据
    for i, (r, n, a, w, c, inf) in enumerate(all_data):
        print(f"排名: {r}, 姓名: {n}, 年龄: {a}, 财富: {w}, 公司: {c}, 信息: {inf}")

    # 将数据保存到 Excel 文件
    df = pd.DataFrame(all_data, columns=['排名', '姓名', '年龄', '财富', '公司', '信息'])

    # 保存到指定路径
    file_path = r'C:\Users\Grand_Caster\Desktop\test\test.xlsx'
    df.to_excel(file_path, index=False, engine='openpyxl')

    print(f"数据已保存到 {file_path}")

    # 关闭浏览器
    browser.close()
