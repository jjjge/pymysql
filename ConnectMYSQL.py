import pymysql
DBHost = 'localhost'
DBUser = 'root'
DBPass = 'root'
DBName = 'db1'

try:
    db = pymysql.connect(host=DBHost,user=DBUser,password=DBPass,database=DBName)
    print('数据库链接成功！')
    cur = db.cursor()
    cur.execute("drop table if exists TestTable")
    sql = 'create table TestTable(Cno char(6) primary key,Cname char(20) not null,Ccredit int not null)'
    cur.execute(sql)
    print("success!")
except pymysql.Error as e:
    print("表格创建失败: "+str(e))

