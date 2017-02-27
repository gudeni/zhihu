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
    'host':'localhost',
    'db':'zhihu'
}

# 创建连接
connection = pymysql.connect(**config)
# 创建游标
cursor = connection.cursor()

# 创建数据库，表
def create_table_information(cur, table_name):
    database_name = 'zhihu'
    # 创建数据库
    cur.execute('create database if not exists '+database_name)
    cur.execute('use '+database_name)
    cur.execute('create table '+table_name
                    +'('
                    +'id int not null primary key,'
                    +'urlToken char(50) not null unique,'
                    +'name char(50) not null,'
                    +'gender int(1) not null,'
                    +'locations char(50) not null,'
                    +'employments char(100) not null,'
                    +'business char(100) not null,'
                    +'description char(100) not null,'
                    +'headline char(100) not null,'
                    +'voteupCount int(10) not null,'
                    +'favoritedCount int(10) not null,'
                    +'followerCount int(10) not null,'
                    +'thankedCount int(10) not null,'
                    +'answerCount int(10) not null,'
                    +'articlesCount int(10) not null,'
                    +'questionCount int(10) not null,'
                    +'followingQuestionCount int(10) not null,'
                    +'followingCount int(10) not null,'
                    +'sinaWeiboUrl char(50) not null,'
                    +'sinaWeiboName char(50) not null,'
                    +'logsCount int(4) not null'
                    +')')
    # 获取表结构
    cur.execute('desc '+table_name)
    # 获取所有返回结果
    row_1 = cur.fetchall()
    for row in row_1:
        print(row)

def create_table_ids(cur, table_name):
    database_name = 'zhihu'
    # 创建数据库
    cur.execute('create database if not exists '+database_name)
    cur.execute('use '+database_name)
    cur.execute('create table '+table_name
                    +'('
                    +'id int not null primary key,'
                    +'urlToken char(50) not null unique'
                    +')')
    # 获取表结构
    cur.execute('desc '+table_name)
    # 获取所有返回结果
    row_1 = cur.fetchall()
    for row in row_1:
        print(row)

def create_table_errorID(cur, table_name):
    database_name = 'zhihu'
    cur.execute('use '+database_name)
    cur.execute('create table '+table_name
                    +'('
                    +'id int not null primary key auto_increment,'
                    +'urlToken char(50) not null unique'
                    +')')
    # 获取表结构
    cur.execute('desc '+table_name)
    # 获取所有返回结果
    row_1 = cur.fetchall()
    for row in row_1:
        print(row)

t1 = 'b1_100'
t2 = 'b2_100'
t3 = 'b3_100'

create_table_information(cursor, t1)
create_table_ids(cursor, t2)
create_table_errorID(cursor, t3)

# 提交，不然无法保存新建或者修改的数据
connection.commit()
# 关闭游标
cursor.close()
# 关闭连接
connection.close()
