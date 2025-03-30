import pymysql
#数据库配置
db=pymysql.connect(host='127.0.0.1',
                   user='root',
                   password='111111',
                   database='db_class_information')
cursor=db.cursor()
if __name__ == '__main__':
    #测试数据库连接
    try:
        sql='select 1;'
        cursor.execute(sql)
    except Exception as e:
        print(e)
    else:
        print('数据库连接成功！')
