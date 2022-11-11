import pymysql
DBHost = 'localhost'
DBUser = 'root'
DBPass = 'root'
DBName = 'db1'


db = pymysql.connect(host=DBHost, user=DBUser, password=DBPass, database=DBName)
cursor = db.cursor()  # 游标设置
# cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
print('数据库链接成功！')
try:
    # cur.execute("drop table if exists TestTable") #删除表
    # sql = 'create table TestTable(Cno char(6) primary key,Cname char(20) not null,Credit int not null)' # 插入表
    sql = 'SELECT * FROM student'
    rowNum = cursor.execute(sql)  # 查询数据库信息
    print("success!")
    print(rowNum)
    result = cursor.fetchall()
    result_list = list(result)
    result_list.sort(key=lambda likes: likes[2])
    print(result_list)

except pymysql.Error as e:
    print("field")
cursor.close()
db.close()



