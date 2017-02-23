import pymysql.cursors

# 配置参数：
# port默认3306
# password 无
# host就是本地 127.0.0.1

config = {
    'user':'root',
    'passwd': '',
    'charset':'utf8',
    'port':3306,
    'host':'localhost'
}

# 创建连接
connection = pymysql.connect(**config)
# 创建游标
cursor = connection.cursor()

# 创建数据库，表
def create_database(cur):
    database_name = 'zhihu'
    table_name = 't2'
    # 创建数据库
    cur.execute('create database if not exists '+database_name)
    cur.execute('use '+database_name)
    cur.execute('create table '+table_name
                    +'('
                    +'id int not null primary key auto_increment,'
                    +'urlToken char(20) not null unique,'
                    +'name char(20) not null,'
                    +'gender int(1) not null,'
                    +'locations char(50) not null,'
                    +'employments char(50) not null,'
                    +'business char(50) not null,'
                    +'description char(50) not null,'
                    +'headline char(50) not null,'
                    +'voteupCount int(10) not null,'
                    +'favoritedCount int(10) not null,'
                    +'followerCount int(10) not null,'
                    +'thankedCount int(10) not null,'
                    +'answerCount int(10) not null,'
                    +'articlesCount int(10) not null,'
                    +'questionCount int(10) not null,'
                    +'followingQuestionCount int(10) not null,'
                    +'followingCount int(10) not null,'
                    +'sinaWeiboUrl char(40) not null,'
                    +'sinaWeiboName char(20) not null,'
                    +'logsCount int(4) not null'
                    +')')
    # 获取表结构
    cur.execute('desc '+table_name)
    # 获取所有返回结果
    row_1 = cur.fetchall()
    for row in row_1:
        print(row)

# create_database(cursor)

cursor.execute("use zhihu")
# cursor.execute("select max(id) from t1")
cursor.execute("select urlToken from a where id>0")
get = cursor.fetchall()
print(get)
peopleList = []
for i in get:
    peopleList.append(i[0])
print(peopleList)


# 提交，不然无法保存新建或者修改的数据
connection.commit()
# 关闭游标
cursor.close()
# 关闭连接
connection.close()
