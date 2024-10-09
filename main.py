import json
import sys
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pushplus_utils import get_access_key, send_pushplus_message, send_email

# Set stdout encoding to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load settings from JSON files
def load_settings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

settings = load_settings('./setting.json')
server = load_settings('./sever.json')

# Extract settings
your_username = settings['Set']['NAME']
your_password = settings['Set']['PASSWORD']
use_email = settings['Set']['USE_EMAIL']
to_email = settings['Set']['TO_EMAIL']
Token = settings['Set']['PUSHPIUS-TOKEN']

SecretKey = server['Sc']['SECRETKEY']
smtp_server = server['Sc']['SMTP_SERVER']
smtp_port = server['Sc']['SMTP_PORT']
smtp_user = server['Sc']['SMTP_USER']
smtp_password = server['Sc']['SMTP_PASSWORD']

# Send notification
def send_notification(subject, body):
    if use_email:
        send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body)
    else:
        send_pushplus_message(Token, access_key, subject, body)

# Initialize WebDriver
def init_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

driver = init_webdriver()
url = "https://2550505.com/"
driver.get(url)

# Get access key if not using email
if not use_email:
    try:
        access_key, expire_in = get_access_key(SecretKey, Token)
        print(f"获取 AccessKey 成功，有效期: {expire_in} 秒")
    except Exception as e:
        print(f"获取 AccessKey 失败: {e}")
        driver.quit()
        sys.exit(1)

# Perform login
def login():
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'h-button') and contains(@class, 'h-button--small') and text()='登录']"))
        )
        print("Login button found, proceeding to login.")
        login_button.click()
        print("Navigating to login page...")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='昵称/UID']"))
        )
        username_field = driver.find_element(By.XPATH, "//input[@type='text' and @placeholder='昵称/UID']")
        password_field = driver.find_element(By.XPATH, "//input[@type='password' and @placeholder='密码']")

        username_field.send_keys(your_username)
        password_field.send_keys(your_password)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='h-button']/span[text()='登录']"))
        )
        submit_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sign-btn"))
        )
        print("Logged in successfully.")
        send_notification("登录成功", "你已经成功登录。")
    except TimeoutException:
        print("Login button not found, assuming already logged in.")

login()

# Perform sign-in
def sign_in():
    try:
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sign-btn"))
        )
        sign_in_button.click()
        print("Signed in successfully.")
        send_notification("每日签到成功", "你今天已经成功签到。")
    except TimeoutException:
        print("Sign in button not found.")
        send_notification("你今天已经签到过了", "等待明天吧")
    except Exception as e:
        print(f"签到过程中出现错误: {e}")
        send_notification("签到失败", f"签到失败，请检查错误: {e}")

sign_in()

# Close the browser
driver.quit()