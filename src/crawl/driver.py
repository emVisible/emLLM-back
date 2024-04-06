from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_driver():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"

    options = webdriver.FirefoxOptions()

    # 无头模式，不显示窗口
    options.add_argument("--headless")
    # 禁止加载图片
    options.set_preference("permissions.default.image", 2)
    # 禁止加载css样式表
    options.set_preference("permissions.default.stylesheet", 2)
    # 禁用 gpu
    options.add_argument("--disable-gpu")
    # 沙盒模式
    options.add_argument("--no-sandbox")

    driver = webdriver.Firefox(options=options)
    return driver
