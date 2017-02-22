# -*- coding:utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import json
import threading


# 配置requests headers
Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                  'Host': 'www.zhihu.com'}
_session = requests.session()
_session.headers.update(Default_Header)

BASE_URL = 'https://www.zhihu.com/'
peopleList = []
errorList = []
lockStart = 1

def getNextPeople(id, count):
    # print("正在追踪：", id)
    url = 'https://www.zhihu.com/people/'+id+'/following'
    html = _session.get(url).content
    # with open(r'C:\Users\lilin\PycharmProjects\lianxi\zhihu_text\html\\'+id+'.html', 'wb') as f:
    #     f.write(html)

    bsObj_following = BeautifulSoup(html, "html.parser")
    items = bsObj_following.find('div', {'id':'data'})['data-state']
    items = json.loads(items.replace("'", ' '))
    # print(items)
    # 获取关注第一页id列表
    ids = items['people']['followingByUser'][id]['ids']
    ids = [i for i in ids if i != None]
    users = items['entities']['users']
    followers = {}
    for i in ids:
        followers[i] = int(users[i]['followerCount'])
    followers = sorted(followers.items(), key=lambda d:d[1], reverse = True)
    # print("关注列表：", followers)

    for i in followers:
        if i[0] not in peopleList:
            next = i[0]
            peopleList.append(next)
            break
        next = None

    # print(next)
    if next == None:
        count += 1
        return getNextPeople(peopleList[count], count)
    print("关注热度:%-9s  追踪对象：%-10s" % (users[next]['followerCount'], users[next]['name']))
    return next

def start(a):
    x = 0
    while True:
        try:
            a = getNextPeople(a,x)
        except Exception as e:
            print("发生了一个错误：",e)
            print("错误追踪对象：",peopleList[-1])
            a = peopleList[x]
            x += 1
            continue

if __name__ == '__main__':

    start('li-lin-55-94-41')

