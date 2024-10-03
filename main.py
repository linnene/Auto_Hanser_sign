import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pushplus_utils import get_access_key, send_pushplus_message
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

# 读取配置文件
with open('./setting.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)

your_username = settings['Set']['NAME']
your_password = settings['Set']['PASSWORD']
Token = settings['Set']['PUSHPIUS-TOKEN']
SecretKey = settings['Set']['SECRETKEY']  


# 初始化 WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
url = "https://2550505.com/" 
driver.get(url)

# 获取 AccessKey
try:
    access_key, expire_in = get_access_key(SecretKey, Token)  
    print(f"获取 AccessKey 成功，有效期: {expire_in} 秒")
except Exception as e:
    print(f"获取 AccessKey 失败: {e}")
    driver.quit()
    exit(1)

# 查找“登录”按钮
try:
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'h-button') and contains(@class, 'h-button--small') and text()='登录']"))
    )
    print("Login button found, proceeding to login.")

    # 找到“登录”按钮，执行登录操作
    login_button.click()
    print("Navigating to login page...")

    # 等待跳转到登录页面并输入用户名和密码
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='昵称/UID']"))
    )
    username_field = driver.find_element(By.XPATH, "//input[@type='text' and @placeholder='昵称/UID']")
    password_field = driver.find_element(By.XPATH, "//input[@type='password' and @placeholder='密码']")

    username_field.send_keys(your_username)
    password_field.send_keys(your_password)
    
    # 查找并点击提交按钮
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='h-button']/span[text()='登录']"))
    )
    submit_button.click()

    # 等待登录后跳转回首页
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sign-btn"))
    )
    print("Logged in successfully.")
    send_pushplus_message(Token, access_key, "登录成功", "你已经成功登录。")

except TimeoutException:
    print("Login button not found, assuming already logged in.")
    # 未找到“登录”按钮，直接执行签到操作

# 尝试点击签到按钮
try:
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sign-btn"))
    )
    sign_in_button.click()
    print("Signed in successfully.")
    send_pushplus_message(Token, access_key, "每日签到成功", "你今天已经成功签到。")
except TimeoutException:
    print("Sign in button not found.")
    send_pushplus_message(Token, access_key, "签到失败", "未找到签到按钮，请手动检查。")
except Exception as e:
    print(f"签到过程中出现错误: {e}")
    send_pushplus_message(Token, access_key, "签到失败", f"签到失败，请检查错误: {e}")

# 关闭浏览器
driver.quit()