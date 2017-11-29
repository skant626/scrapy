"""
This program use search function in "www.coolapk.com",download some apps you need. 
"""
import requests
from bs4 import BeautifulSoup
import re
import os

with open("appnames.txt","r") as f:
    appnames = [item[0:-1] for item in f.readlines()]
    appnames = appnames[0:-1]

def downloadapk(apkname):
    search_url = "https://www.coolapk.com/search?q="+apkname
    apkpages = requests.get(search_url)
    bsObj = BeautifulSoup(apkpages.text,"html.parser",from_encoding="utf-8")
    page_content = bsObj.findAll("a",href=re.compile("/apk/com.+"))
    url = "https://www.coolapk.com"+page_content[1].get('href')#获取搜索界面的第二个apk的链接，第一个是酷安市场coolapk.apk
    session = requests.session()
    #print(url)
    #第一个请求头，使用火狐FireBug进行抓包分析，这个不需要模拟登陆，没什么难度
    headers = {
                "Host": "www.coolapk.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Referer": "https://www.coolapk.com/search?q=%E4%B8%80%E4%B8%AA%E6%9C%A8%E5%87%BD",
                "Cookie": "SESSID=0d2f3a61_5a1e387d417e61_67146849_1511929981_2623; \
                Hm_lvt_7132d8577cc4aa4ae4ee939cd42eb02b=1511929986; \
                Hm_lpvt_7132d8577cc4aa4ae4ee939cd42eb02b=1511931923",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0"

    }

    r = session.get(url,headers=headers)#get请求所获得apk链接，获得单个apk的界面
    bsObj = BeautifulSoup(r.text,"html.parser",from_encoding="utf-8")
    #获取界面内apk的资源链接
    page_content = bsObj.find(text=re.compile("window.location.href"))
    click_url = str(page_content).split("= \"")[1].split("\";")[0]#处理后获得的链接
    #第二个请求头，用于对资源链接进行get请求
    redirect_down_headers = {
                        "Host": "dl.coolapk.com",
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Cookie": "SESSID=0d2f3a61_5a1e387d417e61_67146849_1511929981_2623;Hm_lvt_7132d8577cc4aa4ae4ee939cd42eb02b=1511929986;Hm_lpvt_7132d8577cc4aa4ae4ee939cd42eb02b=1511931993",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",

    }
    #这里有个坑，用上述的资源链接请求后，服务器会进行重定向，而requests的get请求会自动追踪重定向，我们只需获得返回响应头中的Location
    redirect_down_page = requests.get(click_url,headers=redirect_down_headers,allow_redirects=False)
    testType=redirect_down_page.headers

    real_down_page = requests.get(testType["Location"])#真实链接
    #下载
    with open(apkname+".apk", "wb") as code:
         code.write(real_down_page.content)
    print(apkname+" 下载完毕！")
for item in appnames:
    downloadapk(item)

