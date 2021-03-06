# -*- coding:utf-8 -*-
import pymysql.cursors
import requests
import time
from bs4 import BeautifulSoup
import json
import pymysql.cursors
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
getList = []


# 配置参数：
# port默认3306
# password 无
# host就是本地 127.0.0.1
t1 = 't1'
t2 = 't2'
config = {
    'user': 'root',
    'passwd': '',
    'charset': 'utf8',
    'port': 3306,
    'host': 'localhost',
    'db': 'zhihu'
}
# 创建连接
connection = pymysql.connect(**config)
# 创建游标
cursor = connection.cursor()



def getNextPeople(id):
    # print("正在追踪：", id)
    url = 'https://www.zhihu.com/people/'+id+'/following'
    html = _session.get(url).content
    # print(html)
    with open('index.html', 'wb') as f:
        f.write(html)
    bsObj_following = BeautifulSoup(html, "html.parser")
    items = bsObj_following.find('div', {'id':'data'})['data-state']
    items = json.loads(items.replace("'", ' '))
    # print(items)

    def get_ids():
        # print(items)
        # 获取20个ID中5000热度以上的ID
        ids = items['people']['followingByUser'][id]['ids']
        ids = [i for i in ids if i != None]
        users = items['entities']['users']
        followers = []
        hot = 5000
        for i in ids:
            if int(users[i]['followerCount']) >= hot:
                followers.append(i)
        # followers = sorted(followers.items(), key=lambda x:x[1], reverse = True)
        # print(followers)
        return followers

    def get_information():
        x = items['entities']['users'][id]
        personal = {}
        information = ['urlToken','name','gender','description','headline','voteupCount','favoritedCount','followerCount','thankedCount','answerCount','articlesCount','questionCount','followingQuestionCount','followingCount','sinaWeiboUrl','sinaWeiboName','logsCount']
        for i in information:
            try:
                personal[i] = x[i]
            except:
                personal[i] = ' '

        try:
            personal['employments'] = x['employments'][0]['company']['name']
        except:
            personal['employments'] = ' '

        try:
            personal['business'] = x['business']['name']
        except:
            personal['business'] = ' '

        try:
            personal['locations'] = x['locations'][0]['name']
        except:
            personal['locations'] = ' '

        # print(personal)
        return personal

    return get_information(),get_ids()

def insert_table(p, q):
    cursor.execute("insert into "+t1+" (urlToken,name,gender,voteupCount,favoritedCount,"+
                   "followerCount,thankedCount,answerCount,articlesCount,questionCount,"+
                   "followingQuestionCount,followingCount,sinaWeiboUrl,sinaWeiboName,logsCount,"+
                   "locations,description,headline,employments,business) values "+
                   "('%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s','%s',%d,'%s','%s','%s','%s','%s')" %
                   (p['urlToken'], p['name'], p['gender'], p['voteupCount'], p['favoritedCount'],
                    p['followerCount'], p['thankedCount'], p['answerCount'], p['articlesCount'],p['questionCount'],
                    p['followingQuestionCount'], p['followingCount'],p['sinaWeiboUrl'], p['sinaWeiboName'], p['logsCount'],
                    p['locations'],p['description'],p['headline'],p['employments'],p['business']))

    for i in q:
        try:
            cursor.execute("insert into "+t2+"(urlToken) values ('%s')" % i)
        except:
            continue
    # 提交，不然无法保存新建或者修改的数据
    connection.commit()

def nextID(c):
    cursor.execute("select urlToken from "+t2+" where id>"+str(c)+" and id<"+str(c+10))
    x = cursor.fetchall()
    a = []
    for i in x:
        a.append(i[0])
    return a

def start(x):
    if x ==None:
        ID = ['sgai']
        x = 1
    else:
        x = x / 10 + 1
        ID = nextID(x)
    while True:
        for id in ID:
            try:
                information,ids = getNextPeople(id)
            except Exception as e:
                print(e)
                continue
            insert_table(information, ids)
        print("已经抓取 %d 组用户信息..." % (x))
        x += 1
        ID = nextID(x)

if __name__ == '__main__':
    cursor.execute("select max(id) from "+t1)
    # for i in get:
    #     getList.append(i[0])
    #     peopleList.append(i[0])
    # a = lambda x:0 if len(x)==0 else len(x)-1
    start(cursor.fetchall()[0][0])

