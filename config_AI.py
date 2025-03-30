import requests
import time
import json #接受
import re #正则表达式库
def post_AI(user_postmessage):
    url='http://127.0.0.1:11434/api/chat'
    headers={
        'Content-Type': 'application/json',
        'Authorization': ''
    }
    data={
        "model": "qwen2.5:3b",
        "messages": [{
            "role": "system",
            "content": "你是一个专业的 MySQL 数据库工程师，请根据我的需求解释 SQL 语句确保将最终查询语句用 {} 包裹，例如：{SELECT * FROM user}。如果未按要求包裹，请重新生成。最后你需要解释这个语句，一定要解释语句"
            },
            {
            "role": "user",
            "content": user_postmessage
            }
        ],
        'stream': False

    }
    response = requests.post(url, headers=headers, json=data, proxies={"http": None, "https": None})
    #处理流式输出
    sentence=''
    json_data={}
    for line in response.iter_lines():
        if line:
                json_data=json.loads(line.decode('utf-8'))#将字节流转化为json格式

                print(json_data['message']['content'],end='')#得到输出语句
                #正则匹配生成的sql语句
                matches = re.findall(r'\{([^}]+)\}', json_data['message']['content'])
                if matches:
                    sentence = matches[0]
                    print('\nSQL 语句：'+sentence)
    return json_data['message']['content'],json_data['model'],sentence
if __name__ == '__main__':
    user_postmessage = input("请输入你要发送的消息：")
    A,B,C=post_AI(user_postmessage)
    print(A)
    print('==========')
    print(B)
    print('==========')
    print(C)