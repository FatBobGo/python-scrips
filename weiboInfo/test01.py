# -*- coding:utf-8 -*-
import requests
import re

url = "https://m.weibo.cn/api/container/getIndex"
#请求的url

#设置请求头文件信息
headers = {
    "Host": "m.weibo.cn",
    "Referer": "https://m.weibo.cn/u/1739928273",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Accept":'application/json, text/plain, */*',
    "X-Requested-With":"XMLHttpRequest",


'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close'

}

# headers = {
#     "Host": "m.weibo.cn",
#     "Referer": "https://m.weibo.cn/u/1739928273",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "Accept":'application/json, text/plain, */*',
#     "X-Requested-With":"XMLHttpRequest",
# }
#请求头

params = {
            "type": "uid",
        #   "value": "1739928273",
        #   "containerid": "1076031739928273",
            "value":"1350995007",
            "containerid":"1076031350995007",
            "page": "1"}
#请求携带的参数


# res = requests.get(url,headers=headers,params=params).content
# print(res)

import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

res = requests.get(url,headers=headers,params=params)
print(res.encoding)
cards  = res.json().get("data").get("cards")
print(len(cards))
print(cards)
#获取carads下的所有项
index=1
for card in cards:
    if card.get("card_type") == 9:
        print(index)
        index+=1
        text = card.get("mblog").get("text")
        patten = re.compile(r"(.*?)<span.*>(.*?)")
        text = re.sub(patten, "", text)
        print(text)
