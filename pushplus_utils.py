import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_access_key(secret_key, token, timeout=200):
    url = "https://www.pushplus.plus/api/common/openApi/getAccessKey"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "token": token,
        "secretKey": secret_key
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200 and 'data' in result:
                return result['data']['accessKey'], result['data']['expiresIn']
            else:
                raise Exception(f"获取 AccessKey 失败: {result['msg']}")
        else:
            raise Exception(f"获取 AccessKey 失败: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {e}")

def send_pushplus_message(token, access_key, title, content, timeout=120):
    url = "https://www.pushplus.plus/send"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "token": token,
        "accessKey": access_key,
        "title": title,
        "content": content
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                print("消息发送成功")
            else:
                raise Exception(f"消息发送失败: {result['msg']}")
        else:
            raise Exception(f"消息发送失败: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {e}")

def send_email(smtp_server, smtp_port, smtp_user, smtp_password, to_email, subject, body):
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        session = smtplib.SMTP(smtp_server, smtp_port)
        session.starttls()
        session.login(smtp_user, smtp_password)
        text = message.as_string()
        session.sendmail(smtp_user, to_email, text)
        print(f"邮件发送成功: {to_email}")
        session.quit()
    except Exception as e:
        raise Exception(f"邮件发送失败: {e}")