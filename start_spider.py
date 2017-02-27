# python 3.6
# mysql 5.6.35
# -*- coding:utf-8 -*-
import pymysql.cursors
import requests
import time
from bs4 import BeautifulSoup
import json
import pymysql.cursors
import threading


class ZHIHU(object):

    def __init__(self, session, connection, cursor, lock, config):
        self.session = session
        self.connection = connection
        self.cursor = cursor
        self.table_information = 'b1_100'
        self.table_ids = 'b2_100'
        self.table_errorID = 'b3_100'
        self.items = []
        self.lock = lock
        self.followers = []
        self.Default_Header = config

    def get_item(self,id, page):
        _session = requests.session()
        _session.headers.update(Default_Header)
        url = 'https://www.zhihu.com/people/' + id + '/following' + '?page=' + str(page)
        html = _session.get(url).content
        # print(html)
        # with open(r'C:\Users\lilin\PycharmProjects\lianxi\zhihu_text\data\\'+id+'index.html', 'wb') as f:
        #     f.write(html)
        bsObj_following = BeautifulSoup(html, "html.parser")
        item = bsObj_following.find('div', {'id': 'data'})['data-state']
        # with open(id+'_data.html', 'wb') as f:
        #     f.write(item.encode())
        item = json.loads(item.replace("'", ' '))
        # print(item)
        return item

    def get_id(self,id, item):

        # 获取20个ID中100热度以上的ID
        ids = item['people']['followingByUser'][id]['ids']
        ids = [i for i in ids if i != None]
        # print(ids)
        users = item['entities']['users']
        hot = 100
        # print(id,page)
        for i in ids:
            if int(users[i]['followerCount']) >= hot:
                self.followers.append(i)

    def get_ids(self,id, personal):
        pages = int(personal['followingCount']/20+1)
        if pages > 1:
            for page in range(pages):
                try:
                    item = self.get_item(id, page)
                    self.get_id(id,item)
                    print(len(self.followers))
                except:
                    print(len(self.followers))
                    continue

    def get_information(self,id):
        item = self.get_item(id=id,page=1)
        x = item['entities']['users'][id]
        personal_information = {}
        information = ['urlToken','name','gender',
                       'description','headline',
                       'voteupCount','favoritedCount',
                       'followerCount','thankedCount',
                       'answerCount','articlesCount',
                       'questionCount','followingQuestionCount',
                       'followingCount','sinaWeiboUrl',
                       'sinaWeiboName','logsCount']
        for i in information:
            try:
                personal_information[i] = x[i]
            except:
                personal_information[i] = ' '
        try:
            personal_information['employments'] = x['employments'][0]['company']['name']
        except:
            personal_information['employments'] = ' '
        try:
            personal_information['business'] = x['business']['name']
        except:
            personal_information['business'] = ' '
        try:
            personal_information['locations'] = x['locations'][0]['name']
        except:
            personal_information['locations'] = ' '
        # print(personal)

        self.get_id(id,item)
        return personal_information

    def get_nextID(self,count):
        self.cursor.execute("select urlToken from "+self.table_ids+" where id>="+str(count+1)+" and id<"+str(count+11))
        ids = self.cursor.fetchall()
        result = []
        for i in ids:
            result.append(i[0])
        return result


    def insert_table_ids(self,q):
        self.cursor.execute("select max(id) from " + self.table_ids)
        b = self.cursor.fetchall()[0][0]
        if b == None:
            b = 1
        else:
            b = int(b) + 1
        for i in q:
            try:
                print('获取新ID:',i)
                self.cursor.execute("insert into " + self.table_ids + "(id,urlToken) values (%d,'%s')" % (b, i))
            except:
                continue
            b += 1
        # 提交，不然无法保存新建或者修改的数据
        self.connection.commit()

    def insert_table_information(self, p):
        self.cursor.execute("select max(id) from " + self.table_information)
        b = self.cursor.fetchall()[0][0]
        if b == None:
            b = 1
        else:
            b = int(b) + 1
        try:
            self.cursor.execute("insert into " + self.table_information +
                        " (id,urlToken,name,gender,voteupCount,favoritedCount," +
                       "followerCount,thankedCount,answerCount,articlesCount,questionCount," +
                       "followingQuestionCount,followingCount,sinaWeiboUrl,sinaWeiboName,logsCount," +
                       "locations,description,headline,employments,business) values " +
                       "(%d,'%s','%s',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s','%s',%d,'%s','%s','%s','%s','%s')" %
                       (b, p['urlToken'], p['name'], p['gender'], p['voteupCount'], p['favoritedCount'],
                        p['followerCount'], p['thankedCount'], p['answerCount'], p['articlesCount'], p['questionCount'],
                        p['followingQuestionCount'], p['followingCount'], p['sinaWeiboUrl'], p['sinaWeiboName'],
                        p['logsCount'],
                        p['locations'], p['description'], p['headline'], p['employments'], p['business']))
        except:
            self.insert_table_errorID(id)
        # 提交，不然无法保存新建或者修改的数据
        self.connection.commit()

    def insert_table_errorID(self, id):
        try:
            self.cursor.execute("insert into " + self.table_errorID + "(urlToken) values ('%s')" % (id))
        except:
            pass
        self.connection.commit()

    def start(self):
        self.cursor.execute("select max(id) from " + self.table_information)
        count = self.cursor.fetchall()[0][0]
        if count == None:
            ID = ['sgai']
            count = 0
        else:
            self.cursor.execute("select max(id) from " + self.table_errorID)
            error_count = self.cursor.fetchall()[0][0]
            if error_count == None:
                error_count = 0
            ID = self.get_nextID(int(count)+int(error_count))
        flag_getids = True
        while True:
            for id in ID:
                try:
                    personal = self.get_information(id)
                    self.insert_table_information(personal)
                    print(id)
                except:
                    self.insert_table_errorID(id)
                    continue
                try:
                    if flag_getids:
                        self.get_ids(id, personal)
                        if len(self.followers) != 0:
                            self.insert_table_ids(self.followers)
                        self.followers = []
                except Exception as e:
                    print(e)
                    if len(self.followers) != 0:
                        self.insert_table_ids(self.followers)
                    self.followers = []
                    continue

            ID = self.get_nextID(count)
            self.cursor.execute("select max(id) from " + self.table_information)
            get_count = self.cursor.fetchall()[0][0]
            self.cursor.execute("select max(id) from " + self.table_ids)
            notget_count = self.cursor.fetchall()[0][0]
            print("抓取 %d/%d 用户信息.\n" % (get_count, notget_count))
            if (notget_count - get_count) > 20000:
                flag_getids = False
            elif (notget_count - get_count) < 1000:
                flag_getids = True
            self.followers = []
            count += 10


# 配置requests headers
Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                  'Host': 'www.zhihu.com'}
_session = requests.session()
_session.headers.update(Default_Header)

# 配置数据库参数：
config = {
    'user': 'root',
    'passwd': '',
    'charset': 'utf8',
    'port': 3306,
    'host': 'localhost',
    'db': 'zhihu'}
con = pymysql.connect(**config)
cur = con.cursor()
lock = threading.Lock()

if __name__ == '__main__':
    zhihu = ZHIHU(session=_session,connection=con,cursor=cur,lock=lock,config=Default_Header)
    zhihu.start()
