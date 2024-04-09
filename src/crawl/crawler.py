import csv  # 保存csv
import cpca  # 给出地址的省市区
from time import sleep  # 用来睡眠，防止爬太快

# 以下包是爬虫所需要的包
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import random
import pandas as pd
from utils import get_path, log, log_wrap, global_sleep
from driver import get_driver


# 用来判断xpath找到的位置元素是否存在
def is_element(driver, xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return True
    except:
        return False


# 用来判断class_name找到的位置元素是否存在
def is_element2(driver, class_name):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        return True
    except:
        return False


@log_wrap("景点搜索中...")
def findCity(driver, city):
    url = f"https://you.ctrip.com/globalsearch/?keyword={city}"
    driver.get(url)
    global_sleep()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "guide-main-item-top"))
    ).click()
    n1 = driver.window_handles
    driver.close()
    driver.switch_to.window(n1[-1])
    global_sleep()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "entry-item-text"))
    ).click()
    n1 = driver.window_handles
    driver.close()
    driver.switch_to.window(n1[-1])
    global_sleep()


@log_wrap("收集数据总量中...")
def crawl_num(driver):
    page_index = (By.CLASS_NAME, "numpage")
    sights_index = (
        By.XPATH,
        "/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[12]/p",
    )
    page_num = (
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(page_index)).text
    )
    sights_num = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located(sights_index))
        .text
    )
    page_num = int(page_num)
    sights_num = sights_num.split("/")[1][1:-1]
    sights_num = int(sights_num)

    log(f"一共有{page_num}页,共有{sights_num}个景点")

    return sights_num


@log_wrap("数据采集开始")
def crawl(driver, amount, city):
    count = 1
    data = []
    fail_num = 0
    fail_row = []
    while count <= amount:
        global_sleep()
        title_num = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "leftimg"))
        )
        for i in range(len(title_num)):
            try:
                log(f"采集进度 ——►  {count} / {amount}")
                title_num[i].click()
                n = driver.window_handles
                driver.switch_to.window(n[-1])
                global_sleep()

                name_xpath = "/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[1]/div[1]/h1"
                score_xpath = "/html/body/div[2]/div[2]/div/div[3]/div/div[3]/div[2]/div[2]/div/p[1]"
                name = (
                    WebDriverWait(driver, 10)
                    .until(EC.presence_of_element_located((By.XPATH, name_xpath)))
                    .text
                )
                if is_element(driver, score_xpath):
                    score = (
                        WebDriverWait(driver, 10)
                        .until(EC.presence_of_element_located((By.XPATH, score_xpath)))
                        .text
                    )
                else:
                    score = "空"

                temp = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "baseInfoText"))
                )
                address = "空"
                phone = "空"
                if len(temp) == 3:
                    address = temp[0].text
                    phone = temp[2].text
                else:
                    address = temp[0].text
                temp_list = []
                temp_list.append(address)

                introduct = "空"
                open = "空"
                server = "空"
                discount = "空"
                if is_element2(driver, "moduleTitle") and is_element2(
                    driver, "moduleContent"
                ):
                    introduct_titles = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "moduleTitle")
                        )
                    )
                    introducts = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, "moduleContent")
                        )
                    )
                    for m in range(len(introduct_titles)):
                        if introduct_titles[m].text == "介绍":
                            introduct = introducts[m].text[:-3].replace("\n", " ")
                        elif introduct_titles[m].text == "优待政策":
                            discount = introducts[m].text
                        elif introduct_titles[m].text == "服务设施":
                            server = introducts[m].text
                        elif introduct_titles[m].text == "开放时间":
                            open = introducts[m].text

                data.append(
                    [name, score, address, open, phone, introduct, discount, server]
                )

            except:
                log(f"第{count}条爬取失败\n")
                fail_num += 1
                fail_row.append(str(count))

            finally:
                # 多余窗口关闭
                global_sleep()
                n1 = driver.window_handles
                if (len(n1)) > 1:
                    driver.close()
                    driver.switch_to.window(n1[0])
                    global_sleep()
                    # sleep(5)
                count += 1
                if count > amount:
                    break
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[2]/div[2]/div[4]/div/div[2]/div/div[3]/div[12]/div/a[7]",
                )
            )
        ).click()
    return data


@log_wrap("写入单问题json")
def transform_json(city):

    questions = ["的位置", "的营业时间", "的联系电话", "的介绍", "的优惠政策", "的服务"]

    form = {
        "instruction": "现在你是一个杭州旅游向导，请根据问题给出回答：",
        "input": "",
        "output": "",
    }
    with open(get_path(city=city, suffix=".csv"), "r", encoding="utf-8") as f:
        datas = csv.DictReader(f)
        headers = datas.fieldnames
        temp = headers[2:]
        for data in datas:
            for index in range(len(questions)):
                form["input"] = data["name"] + questions[index]
                form["output"] = data[temp[index]]
                if form["output"] != "空":
                    with open(
                        get_path(city=city, suffix=".json"), "r", encoding="utf-8"
                    ) as fs:
                        result = json.load(fs)
                    result.append(form)
                    with open(
                        get_path(city=city, suffix=".json"), "w", encoding="utf-8"
                    ) as fs:
                        json.dump(result, fs, ensure_ascii=False, indent=1)


@log_wrap("写入多问题json")
def transform_json_more(city):
    questions = ["的位置", "的营业时间", "的联系电话", "的介绍", "的优惠政策", "的服务"]

    form = {
        "instruction": "现在你是一个杭州旅游向导，请根据问题给出回答：",
        "input": "",
        "output": "",
        "history": [],
    }
    lst = [0, 1, 2, 3, 4, 5]

    with open(get_path(city=city, suffix=".csv"), "r", encoding="utf-8") as f:
        datas = csv.DictReader(f)
        headers = datas.fieldnames
        temp = headers[2:]

        for data in datas:
            random.shuffle(lst)

            indexs = 0
            while data[temp[lst[indexs]]] == "空":
                indexs += 1
            form["history"] = []
            form["input"] = data["name"] + questions[lst[indexs]]
            form["output"] = data[temp[lst[indexs]]]
            for k in lst[indexs + 1 :]:
                if data[temp[k]] == "空":
                    continue
                append_lst = []
                append_lst.append(data["name"] + questions[k])
                append_lst.append(data[temp[k]])
                form["history"].append(append_lst)

            with open(get_path(city=city, suffix="more"), "r", encoding="utf-8") as fs:
                result = json.load(fs)
            result.append(form)
            with open(get_path(city=city, suffix="more"), "w", encoding="utf-8") as fs:
                json.dump(result, fs, ensure_ascii=False, indent=1)


def run(city: str, amount: int, map_name:str):
    # 获取driver
    driver = get_driver()

    # 查询城市
    findCity(driver, city)

    city = map_name

    # 采集的数据量
    amount = amount if amount is not None else 10

    # 总页数
    page_num = crawl_num(driver)

    # 采集的数据
    data = crawl(driver, min(amount, page_num), city)

    # 项目数据根路径
    path = get_path(city=city, suffix=".csv")
    with open(path, "w+", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        title = [
            "name",
            "score",
            "address",
            "open",
            "phone",
            "introduct",
            "discount",
            "server",
        ]
        csv_writer.writerow(title)
        csv_writer.writerows(data)

    data_csv = pd.read_csv(get_path(city=city, suffix=".csv"))
    data_csv = data_csv.drop_duplicates()
    data_csv.to_csv(get_path(city=city, suffix=".csv"), index=False)

    # 初始化json
    with open(get_path(city=city, suffix=".json"), "w", encoding="utf-8") as f:
        json.dump([], f)
    with open(get_path(city=city, suffix="more"), "w", encoding="utf-8") as f:
        json.dump([], f)

    transform_json(city)
    transform_json_more(city)

    # 关闭driver
    driver.close()
