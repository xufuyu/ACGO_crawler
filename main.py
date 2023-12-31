# -*- coding: utf-8 -*-
import time
import tkinter as tk
import matplotlib.pyplot as plt
import requests
from lxml import etree
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import ttk
import os
import datetime

if not os.path.exists('icon.ico'):
    icon = requests.get('https://www.acgo.cn/favicon.ico')
    with open('icon.ico', 'wb') as icon_file:
        icon_file.write(icon.content)


chinese_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))



print('运行时间：',chinese_time,'\n','Powered by 疯子XUFUYU','\n')


def msg(msg_text='TEST', msg_key='PDU23609TxBbjyT6HfCwEZUt4zLlxF2pfMOf7MGa9'):
    url = 'https://api2.pushdeer.com/message/push?pushkey={}&text={}'.format(msg_key,msg_text)
    response = requests.get(url)
    return response

def center_window(root_def, width, height):
    screenwidth = root_def.winfo_screenwidth()  # 获取显示屏宽度
    screenheight = root_def.winfo_screenheight()  # 获取显示屏高度
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
    root_def.geometry(size)  # 让窗口居中显示

def acgo(acgo_user_id='2484958'):
    # 设置Chrome选项，使其在无头模式下运行（可选）
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式，不显示浏览器窗口

    # 创建Chrome WebDriver，并设置Chrome选项
    driver = webdriver.Chrome(options=chrome_options)

    # 使用WebDriver打开目标网站
    driver.get('https://www.acgo.cn/person/' + acgo_user_id)  # 替换为要爬取的目标网站URL

    # 等待页面加载完成（可选），例如等待特定元素出现
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[1]/div[2]/div[1]/span[1]/span')))

    # 获取页面的完整HTML内容
    html = driver.page_source

    return html

    # 关闭WebDriver
    # noinspection PyUnreachableCode
    driver.quit()

def find(html):
    # 假设html_doc是HTML文档字符串
    root_tk = etree.HTML(html)

    # 使用给定的XPath表达式来查找目标<span>标签
    span_tag = root_tk.xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div[2]/div[1]/span[1]/span')

    # 提取标签内容
    span_content = span_tag[0].text if span_tag else None

    # 打印提取到的内容
    return span_content
dict_1 = []

def data():
    global dict_1
    mode = option_var.get()
    root.destroy()

    # 创建主窗口
    root_add = tk.Tk()
    center_window(root_add, 300, 100)
    root_add.iconbitmap('icon.ico')
    # 禁止窗口调整大小
    root_add.resizable(width=False, height=False)
    root_add.title("加载中---Powered by 疯子XUFUYU")

    # 创建Label小部件并显示文字
    tk.Label(root_add, text="加载中...").pack()

    # 设置加载动画参数
    progress_var = tk.DoubleVar()  # 加载进度变量，取值范围为0~100
    progress_var.set(0)  # 初始值为0

    # 创建加载动画组件
    progress_bar = ttk.Progressbar(root_add, variable=progress_var, maximum=100, mode='determinate', length=200)
    progress_bar.pack(pady=20)
    num = 0
    file = open('output.txt', 'w', encoding='utf-8')
    if mode == "1":
        print('已运行，请等待\n')
        for i in user_id_fir:
            name = user_id_fir[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            dict_1.append(int(ac_data))
            # 更新进度条
            num += 1
            progress_var.set(num * 100 / len(user_id_fir))
            root_add.update()
            file.write(name + ' ' + ac_data + '\n')

    elif mode == "2":
        print('已运行，请等待\n')
        for i in user_id_sat:
            name = user_id_sat[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            dict_1.append(int(ac_data))
            # 更新进度条
            num += 1
            progress_var.set(num * 100 / len(user_id_sat))
            root_add.update()
            file.write(name + ' ' + ac_data + '\n')

    elif mode == "3":
        print('已运行，请等待\n')
        for i in user_id_all:
            name = user_id_all[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            dict_1.append(int(ac_data))
            # 更新进度条
            num += 1
            progress_var.set(num * 100 / len(user_id_all))
            root_add.update()
            file.write(name + ' ' + ac_data + '\n')

    file.close()
    print('\n'+'内容已成功写入到output.txt文件中。')

    # 调用函数进行排序
    binary_insertion_sort('output.txt', 'sorted_output.txt')


    # 调用函数生成可视化图像
    visualize_data('sorted_output.txt', 'ranking_visualization.png')
    root_add.destroy()

    tk_output()

    # 运行主循环
    root_add.mainloop()

def binary_insertion_sort(input_file, output_file):
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 使用二分插入排序进行逆序排序
    for i in range(1, len(lines)):
        key = lines[i].split()
        name = key[0]
        score = int(key[1])

        low, high = 0, i - 1

        while low <= high:
            mid = (low + high) // 2
            if int(lines[mid].split()[1]) < score:
                high = mid - 1
            else:
                low = mid + 1

        for j in range(i - 1, low - 1, -1):
            lines[j + 1] = lines[j]

        lines[low] = f"{name} {score}"

    # 添加排名
    ranked_lines = [f"{i + 1}. {line}\n" for i, line in enumerate(lines)]

    # 写入排序后的结果到新的txt文档
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(ranked_lines)

    print("数据已成功逆序排序并写入到sorted_output.txt文件中。")



def visualize_data(input_file, output_file):
    global dict_1
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 去除空行
    lines = [line.strip() for line in lines if line.strip() != '']

    # 提取姓名和分数
    names = [line.split()[1] for line in lines]
    scores = [int(line.split()[2]) for line in lines]

    # 设置字体
    plt.rcParams['font.family'] = 'SimHei'  # 使用黑体作为字体

    # 创建柱状图
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.bar(names, scores)

    # 添加标题和标签
    ax.set_title('排名情况---Powered by 疯子XUFUYU')
    ax.set_xlabel('姓名')
    ax.set_ylabel('累计解题数')

    # 自动调整名称显示角度以避免重叠
    plt.xticks(rotation=45, ha='right')

    # 设置y轴刻度范围
    ax.set_ylim([0, max(dict_1) + 30])

    # 在每个柱上标出详细数据
    for i in range(len(names)):
        ax.text(names[i], scores[i], str(scores[i]), ha='center', va='bottom')

    # 添加生成时间到左上角
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ax.text(0.02, 0.98, f'Generated on: {current_time}', transform=ax.transAxes,
            fontsize=10, color='black', va='top', ha='left', backgroundcolor='white')

    # 保存图像
    plt.tight_layout()
    plt.savefig(output_file)




def tk_output():
    # 创建Tkinter窗口
    window = tk.Tk()
    window.title("输出窗口---Powered by 疯子XUFUYU")
    center_window(window, 1000, 600)
    window.iconbitmap('icon.ico')
    # 禁止窗口调整大小
    window.resizable(width=False, height=False)

    # 创建Matplotlib画布
    figure = Figure(figsize=(20, 12), dpi=100)
    canvas = FigureCanvasTkAgg(figure, master=window)

    # 在画布上绘制图像
    image_path = "ranking_visualization.png"
    image = figure.add_subplot(111)
    image.axis("off")
    image.imshow(plt.imread(image_path))

    # 添加Matplotlib导航工具栏
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    # 将画布放置在窗口中
    canvas.get_tk_widget().pack()

    # 运行Tkinter事件循环
    window.mainloop()


# user_id对照字典，为防止有人改备注名、乱拉小号或备注名中存在非法字符导致程序报错，所以此字典请自行更改
user_id_all = {"None":"None",# 字典前为user_id，后为自定义显示昵称
               "":""
               }

msg('有人运行了你的程序！时间：{}'.format(chinese_time))

# user_input = input("请输入你要的方式：\n1.周五并排序并生成柱状图\n2.周六并排序并生成柱状图\n3.全部并排序并生成柱状图\n")

# data(user_input)

# 调用函数进行排序
# binary_insertion_sort('output.txt', 'sorted_output.txt')

# 调用函数生成可视化图像
# visualize_data('sorted_output.txt', 'ranking_visualization.png')


root = tk.Tk()
root.title("数据处理---Powered by 疯子XUFUYU")
root.geometry("300x200")
center_window(root,300,200)
root.iconbitmap('icon.ico')
# 禁止窗口调整大小
root.resizable(width=False, height=False)

option_var = tk.StringVar()
option_var.set("1")

label = tk.Label(root, text="请选择数据处理方式:")
label.pack()

radio_btn1 = tk.Radiobutton(root, text="正在制作", variable=option_var, value="0")
radio_btn1.pack()

radio_btn2 = tk.Radiobutton(root, text="正在制作", variable=option_var, value="0")
radio_btn2.pack()

radio_btn3 = tk.Radiobutton(root, text="全部并排序并生成柱状图", variable=option_var, value="3")
radio_btn3.pack()

# 设置默认选项
option_var.set("3")
radio_btn3.select()  # 设置默认选项为选中状态


process_btn = tk.Button(root, text="处理数据", command=data)
process_btn.pack()

root.mainloop()

msg('安全运行未报错！时间：{}'.format(chinese_time))
