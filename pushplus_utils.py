# pushplus_utils.py

import requests
import json
import time

def get_access_key(secret_key, token, timeout=200, retries=20, backoff_factor=0.3):
    url = "https://www.pushplus.plus/api/common/openApi/getAccessKey"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "token": token,
        "secretKey": secret_key
    }

    for attempt in range(retries):
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
            print(f"请求失败: {e}, 尝试重试 {attempt + 1}/{retries}")
            time.sleep(backoff_factor * (2 ** attempt))
    raise Exception("获取 AccessKey 失败: 超过最大重试次数")



def send_pushplus_message(token, access_key, title, content):
    url = "http://www.pushplus.plus/send/"
    headers = {
        "Content-Type": "application/json",
        "AccessKey": access_key  
    }
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "txt"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers,timeout=120)
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print(f"消息发送失败: {response.text}")