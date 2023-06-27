import os
import time
import tkinter as tk
import matplotlib.pyplot as plt
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from PIL import Image, ImageTk

chinese_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))



print('运行时间：',chinese_time,'\n')


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

def data():
    mode = option_var.get()
    root.destroy()
    file = open('output.txt', 'w', encoding='utf-8')
    if mode == "1":
        print('已运行，请等待\n')
        for i in user_id_fir:
            name = user_id_fir[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            file.write(name + ' ' + ac_data + '\n')
    elif mode == "2":
        print('已运行，请等待\n')
        for i in user_id_sat:
            name = user_id_sat[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            file.write(name + ' ' + ac_data + '\n')
    elif mode == "3":
        print('已运行，请等待\n')
        for i in user_id_all:
            name = user_id_all[i]
            ac_data = find(acgo(i))
            print(name, ac_data)
            file.write(name + ' ' + ac_data + '\n')
    else:
        print('说人话!!!')
    file.close()
    print('\n'+'内容已成功写入到output.txt文件中。')

    # 调用函数进行排序
    binary_insertion_sort('output.txt', 'sorted_output.txt')


    # 调用函数生成可视化图像
    visualize_data('sorted_output.txt', 'ranking_visualization.png')

    tk_output()



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
    plt.figure(figsize=(10, 6))
    plt.bar(names, scores)

    # 添加标题和标签
    plt.title('排名情况')
    plt.xlabel('姓名')
    plt.ylabel('累计解题数')

    # 自动调整名称显示角度以避免重叠
    plt.xticks(rotation=45, ha='right')

    # 保存图像
    plt.tight_layout()
    plt.savefig(output_file)

    print(f"可视化图像已成功保存为{output_file}。")


def tk_output():
    # 创建Tkinter窗口
    window = tk.Tk()
    window.title("输出窗口")

    # 创建Matplotlib画布
    figure = Figure(figsize=(10, 6), dpi=100)
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

    # 指定文本文件路径
    path_to_file = r"sorted_output.txt"

    # 使用os模块的startfile()函数打开文本文件
    os.startfile(path_to_file)

    # 指定文本文件路径
    path_to_file = r"ranking_visualization.png"

    # 使用os模块的startfile()函数打开文本文件
    os.startfile(path_to_file)


    # 运行Tkinter事件循环
    window.mainloop()


# user_id对照字典，为防止有人改备注名、乱拉小号或备注名中存在非法字符导致程序报错，所以此字典由|疯子XUFUYU|人工统计于2023/6/25/15:19:23/
user_id_all = {"234895":"孔浩轩",
               "732967":"张辰奕",
               "735046":"倪晨皞",
               "751543":"王英航",
               "769326":"叶毅熙",
               "984802":"周韩",
               "1043436":"孙泽恩",
               "1404944":"杨沛铮",
               "1590475":"郎逸琳",
               "2029294":"唐伊辰",
               "2484958":"徐付豫",
               "3069027":"盛函",
               "3798554":"吴宇浩",
               "644850":"杨铮",
               "698775":"徐泽楷",
               "748554":"-",
               "1003581":"袁正赫",
               "1146500":"看他名字",
               "1490721":"陈卓燃",
               "1961609":"王皓煜",
               "2723979":"徐善豪",
               "2789929":"陆思源",
               "3225899":"孙雨泽"
               }

user_id_fir = {"644850":"杨铮",
               "698775":"徐泽楷",
               "748554":"-",
               "1003581":"袁正赫",
               "1146500":"看他名字",
               "1490721":"陈卓燃",
               "1961609":"王皓煜",
               "2723979":"徐善豪",
               "2789929":"陆思源",
               "3225899":"孙雨泽"
               }

user_id_sat = {"234895":"孔浩轩",
               "732967":"张辰奕",
               "735046":"倪晨皞",
               "751543":"王英航",
               "769326":"叶毅熙",
               "984802":"周韩",
               "1043436":"孙泽恩",
               "1404944":"杨沛铮",
               "1590475":"郎逸琳",
               "2029294":"唐伊辰",
               "2484958":"徐付豫",
               "3069027":"盛函",
               "3798554":"吴宇浩",
               }

msg('有人运行了你的程序！时间：{}'.format(chinese_time))

# user_input = input("请输入你要的方式：\n1.周五并排序并生成柱状图\n2.周六并排序并生成柱状图\n3.全部并排序并生成柱状图\n")

# data(user_input)

# 调用函数进行排序
# binary_insertion_sort('output.txt', 'sorted_output.txt')

# 调用函数生成可视化图像
# visualize_data('sorted_output.txt', 'ranking_visualization.png')


root = tk.Tk()
root.title("数据处理")
root.geometry("300x200")
center_window(root,300,200)
# 禁止窗口调整大小
root.resizable(width=False, height=False)

option_var = tk.StringVar()
option_var.set("1")

label = tk.Label(root, text="请选择数据处理方式:")
label.pack()

radio_btn1 = tk.Radiobutton(root, text="周五并排序并生成柱状图", variable=option_var, value="1")
radio_btn1.pack()

radio_btn2 = tk.Radiobutton(root, text="周六并排序并生成柱状图", variable=option_var, value="2")
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
