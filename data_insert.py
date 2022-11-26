import re
import pymysql
from datetime import datetime


def connect_db():
    db_host = '1.15.75.204'
    port = 3306
    db_user = 'db_food'
    db_password = 'k6safXijNhKzZNe7'
    db_name = 'db_food'
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name,autocommit=True)
    print('数据库链接成功！')
    return db




def get_num(db):
    cursor = db.cursor()  # 游标设置
    try:

        sql = 'select * from food '
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        return row_num
    except pymysql.Error as e:
        print("field")
        cursor.close()

# ['菠萝虾焗饭', '18', '玫瑰园二楼', '1', 'https://i.postimg.cc/3RYHpxW2/6-B006-B08-C0774741-C9-FD67-A03-B8124-E6-jpg.jpg\n']
txt_tables = []
db = connect_db()
f = open("test.txt", "r", encoding='utf-8')
line = f.readline()  # 读取第一行
num = get_num(db)
print(num)
while line:
    num += 1
    list = re.split(',', line)
    print(list)
    id_temp = num
    id = str(id_temp)
    name = list[0]
    loc = list[2]
    tag = list[3]
    src = list[4]
    likes = '0'
    descrip = "暂无"
    price = list[1]
    date = datetime.now()
    print(date)
    date = datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
    print(date)
    date =str(date)
    sql = 'insert into food(food_id,food_name,food_loc,food_type,food_src,food_likes_num,food_brief_description,food_price,create_time,update_time) values'
    sql1 ='('+id +',\''+name +'\',\''+loc+'\','+tag +',\''+src+'\','+likes+',\''+descrip+'\','+price+',\''+date+'\',\''+date+'\')'
    sql = sql+sql1
    print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    line = f.readline() # 读取下一行
print(txt_tables)
f.close()