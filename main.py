import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def msg(msg_text='TEST', msg_key='PDU23609TxBbjyT6HfCwEZUt4zLlxF2pfMOf7MGa9'):
    url = 'https://api2.pushdeer.com/message/push?pushkey={}&text={}'.format(msg_key,msg_text)
    response = requests.get(url)
    return response

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
    root = etree.HTML(html)

    # 使用给定的XPath表达式来查找目标<span>标签
    span_tag = root.xpath('//*[@id="__next"]/div/main/div[2]/div[1]/div[2]/div[1]/span[1]/span')

    # 提取标签内容
    span_content = span_tag[0].text if span_tag else None

    # 打印提取到的内容
    return span_content

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

msg('有人运行了你的程序！')

user_input = input("请输入你要的方式：\n1.周五\n2.周六\n3.全部\n4.周五并排序\n5.周六并排序\n6.全部并排序\n")

if user_input == "1":
    print('已运行，请等待')
    for i in user_id_fir:
        name = user_id_fir[i]
        data = find(acgo(i))
        print(name, data)
elif user_input == "2":
    print('已运行，请等待')
    for i in user_id_sat:
        name = user_id_sat[i]
        data = find(acgo(i))
        print(name, data)
elif user_input == "3":
    print('已运行，请等待')
    for i in user_id_all:
        name = user_id_all[i]
        data = find(acgo(i))
        print(name, data)
elif user_input == "4":
    print('给你做出自动爬取就已经不错了，还想要自动排序？想得美！已为你自动选择1')
    print('已运行，请等待')
    for i in user_id_fir:
        name = user_id_fir[i]
        data = find(acgo(i))
        print(name, data)
elif user_input == "5":
    print('给你做出自动爬取就已经不错了，还想要自动排序？想得美！已为你自动选择2')
    print('已运行，请等待')
    for i in user_id_sat:
        name = user_id_sat[i]
        data = find(acgo(i))
        print(name, data)
elif user_input == "6":
    print('给你做出自动爬取就已经不错了，还想要自动排序？想得美！已为你自动选择3')
    print('已运行，请等待')
    for i in user_id_all:
        name = user_id_all[i]
        data = find(acgo(i))
        print(name, data)
else:
    print('说人话!!!')
