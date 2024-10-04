# pushplus_utils.py

import requests
import json


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
            print(result)
            if result['code'] == 200 and 'data' in result:
                return result['data']['accessKey'], result['data']['expiresIn']
            else:
                raise Exception(f"获取 AccessKey 失败: {result['msg']}",response.status_code)
        else:
            raise Exception(f"获取 AccessKey 失败: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {e}")



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