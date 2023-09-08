import base64
import hashlib
import json
import os
import time
import requests
from os import environ, path
from sys import exit
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def load_send():
    global send, mg
    cur_path = path.abspath(path.dirname(__file__))
    if path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            print("加载通知服务成功！")
        except:
            send = False
            print("加载通知服务失败~")
    else:
        send = False
        print("加载通知服务失败~")

#通知服务
#load_send()
send_msg = ''
# 设置要发送的 GET 请求的 URL
dturl = "https://www.kxdao.net/plugin.php?id=ahome_dayquestion:pop"

#本地运行
cookies = [
  
]
#青龙运行
#cookies = environ.get("kxd_ck").split("#")
for item in cookies:
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
      "Referer": "https://www.kxdao.net/index.php",
      "Host":"www.kxdao.net",
      "Sec-Ch-Ua":'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
      "Sec-Ch-Ua-Mobile":"?0",
      "Sec-Ch-Ua-Platform":"'Windows'",
      "Sec-Fetch-Dest":"empty",
      "Sec-Fetch-Mode":"cors",
      "Sec-Fetch-Site":"same-origin",
      "X-Requested-With":"XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
      "Cookie":item
  }
  #获取formhash，构造数据
  formhashres = requests.get("https://www.kxdao.net/", headers=headers, verify=False)
  soup = BeautifulSoup(formhashres.content, 'html.parser')
  el = soup.find("input",attrs={'type': 'hidden', 'name': 'formhash'})
  formhash = el["value"]
  data = {
      "formhash": formhash,
      "answer": "1",
      "submit": "true",
  }
  #答题
  responsedt = requests.post(dturl, headers=headers, data=data,verify=False)
  soup = BeautifulSoup(responsedt.text, 'html.parser')
  name = soup.find("a",attrs={'title': '访问我的空间'}).text
  send_msg += name + "\n"
  el = soup.select("#messagetext p")
  if(len(el) > 0):
      send_msg += el[0].text + "\n"
  #签到
  qdurl = "https://www.kxdao.net/plugin.php?id=dsu_amupper&ppersubmit=true&formhash=" + formhash + "&infloat=yes&handlekey=dsu_amupper&inajax=1&ajaxtarget=fwin_content_dsu_amupper"
  responseqd = requests.get(qdurl, headers=headers,verify=False)
  soup = BeautifulSoup(responseqd.text.split("[CDATA[")[1].split("]]>")[0], 'html.parser')
  el = soup.find_all("div",attrs={'class': 'alert_error'})
  if(len(el) > 0):
    send_msg += responseqd.text.split("showDialog(\'")[1].split("\', \'alert")[0] + "\n\n"
  else:
      el = soup.find_all("div",attrs={'class': 'alert_right'})
      if(len(el)>0):
        send_msg += responseqd.text.split("showDialog(\'")[1].split("\', \'right")[0] + "\n\n"
  time.sleep(1.5)
  

print(send_msg)
#send('科学刀', send_msg)
