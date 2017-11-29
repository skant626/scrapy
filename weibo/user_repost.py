
"""这个程序主要在微博某个主题的搜索结果下，选取所有热门的评论，查看用户间的转发关系"""
import requests
import random
import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import hashlib
from threading import Timer
import re


#用户登录程序
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
        return(session)



#client = MongoClient('mongodb://admin:password@ip:端口/数据库名称')
#db = client.test
#collection = db.items

session = login("17086033563","tttt5555")

#用户转发关系爬虫
def repost(keyword):
    for j in range(200):
        print("This id",j," page")
        url = "https://weibo.cn/search/mblog?hideSearchFrame=&\
            keyword="+keyword+"&sort=hot&page="+(str)(j)#搜索的结果界面
        page = session.get(url)
        bsObj = BeautifulSoup(page.text,"html.parser",from_encoding="utf-8")
        repost_bsObj = bsObj.findAll("a",href=re.compile("https://weibo.cn/repost/.+"))
        poster_names = bsObj.findAll("a",{"class":"nk"},href=re.compile("https://weibo.cn/.+"))#发布者姓名标签
        
        for i,item in enumerate(repost_bsObj):
            print("--------------------------------------------------------")
            weight = item.text[3:-1]#转发数
            poster_uid = item.get("href").split("uid=")[1].split("&")[0]#发布者uid
            poster_name = poster_names[i].text#发布者昵称
            repost_page = session.get(item.get("href"))#转发者界面
            re_bsObj = BeautifulSoup(repost_page.text,"html.parser",from_encoding="utf-8")
            pagecount_page = re_bsObj.find("div",{"id":"pagelist"})#转发者界面的页数（int）

            for j in range(int(pagecount_page.text.split("/")[1][0:-1])):#对转发者界面循环
                print("#############################")
                repost_page_temper = session.get(item.get("href")+"&page="+str(j+1))#每个界面的转发者信息
                print(item.get("href")+"&page="+str(j+1))
                respost_bsObj = BeautifulSoup(repost_page_temper.text,"html.parser",from_encoding="utf-8")
                repost_users = respost_bsObj.findAll("div",{"class":"c"})
                for item1 in repost_users[3:]: 
                    temper = str(item1.find("a",href=re.compile("/.+")))
                    try:
                        uid = temper[10:].split(">")[0][0:-1]
                        nickname = temper[10:].split(">")[1].split("</a")[0]
                        print(poster_uid,uid)
    		    #存入数据库
                #        collection.insert_one({ "data_orgin":"weibo",
                 #                               "oragin_uid":poster_uid,
                  #                              "oragin_nickname":poster_name,
                   #                             "target_uid":uid,
                    #                            "target_name":nickname,
                     #                           "weight":weight
                      #                  })
                    except:
                        continue

repost(input("输入想要转发内容的主题："))
