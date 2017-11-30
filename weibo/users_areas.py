import requests
import random
import urllib.request
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
import time
import hashlib
from threading import Timer
import re

def login(username,password):
    session = requests.session()
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36']

    headers = {
        'User_Agent': random.choice(user_agents),
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Origin': 'https://passport.weibo.cn',
        'Host': 'passport.weibo.cn'
    }
    post_data = {
        'username': '',
        'password': '',
        'savestate': '1',
        'ec': '0',
        'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
        'entry': 'mweibo'
    }
    login_url = 'https://passport.weibo.cn/sso/login'

    post_data['username'] = username
    post_data['password'] = password
    r = session.post(login_url, data=post_data, headers=headers)
    if r.status_code != 200:
        return False
    else:
        print("模拟登陆成功,当前登陆账号为：" + username)
    return session


#client = MongoClient('mongodb://admin:password@ip:端口/数据库')
#db = client.reposter1
#db2 = client.poster1
#collection = db.items
#collection1 = db2.items


session = login("15337197841","tttt5555")
def areas(session,keyword):
    for j in range(200):
        print("This id",j," page")
        url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&sort=hot&page="+(str)(j)
        page = session.get(url)
        bsObj = BeautifulSoup(page.text,"html.parser",from_encoding="utf-8")
        repost_bsObj = bsObj.findAll("a",href=re.compile("https://weibo.cn/repost/.+"))
        for item in repost_bsObj:
            print(item.get("href"))
            repost_page = session.get(item.get("href"))
            respost_bsObj = BeautifulSoup(repost_page.text,"html.parser",from_encoding="utf-8")
            #print(respost_bsObj)
            repost_users = respost_bsObj.findAll("div",{"class":"c"})
            times = respost_bsObj.findAll("span",{"class":"ct"})

            poster_uid = item.get("href").split("uid=")[1].split("&")[0]
            userpageInfo = session.get("https://weibo.cn/"+poster_uid+"/info")
            InfobsObj = BeautifulSoup(userpageInfo.text,"html.parser",from_encoding="utf-8")
            INfopage_content = InfobsObj.findAll("div",{"class","c"})
            try:
                print("...POSTER--------\n",str(INfopage_content)[str(INfopage_content).index("地区:")+3:\
                    str(INfopage_content).index("地区:")+20].split("<br/>")[0])

                print(str(INfopage_content)[str(INfopage_content).index("生日")+3:\
                    str(INfopage_content).index("生日:")+20].split("<br/>")[0])
            except:
                continue


            ii = 0
            print(len(times))
            print(len(repost_users[3:]))
            for i,item1 in enumerate(repost_users[3:]):
                temper = str(item1.find("a")).split(">")[0].split("\"")
                print(temper)
                if len(temper)>1:
                    ii+=1
                    if temper[1][0:3] != "/u/":
                        userpage = session.get("https://weibo.cn/"+temper[1])
                        userbsobj = BeautifulSoup(userpage.text,"html.parser",from_encoding="utf-8")
                        userpage_content = userbsobj.find("span",{"class","ctt"})
                        try:
                            uid = str(userpage_content)[str(userpage_content).index("uid=")+4:\
                            str(userpage_content).index("uid=")+14]
                            uidurl = "https://weibo.cn/"+uid+"/info"
                        except:
                            continue
                    else:
                        uidurl = "https://weibo.cn"+temper[1][2:]+"/info"

                    print(uidurl)
                    userpageInfo = session.get(uidurl)
                    InfobsObj = BeautifulSoup(userpageInfo.text,"html.parser",from_encoding="utf-8")
                    INfopage_content = InfobsObj.findAll("div",{"class","c"})
                    try:
                        print(str(INfopage_content)[str(INfopage_content).index("地区:")+3:\
                           str(INfopage_content).index("地区:")+20].split("<br/>")[0])

                        print(str(INfopage_content)[str(INfopage_content).index("生日")+3:\
                            str(INfopage_content).index("生日:")+20].split("<br/>")[0])
                    except:
                        continue
                else:
                    print("#######################not 2################")

areas(session,input("请输入主题，将爬取该主题下发帖人的地理位置和生日等信息：\n"))
