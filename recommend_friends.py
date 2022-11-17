import pymysql
import json

# 调用第一个方法即可
# rec_num_1 为想要推荐的人数(第9行，默认为10)
# user_name = '杰哥'  # 测试用例


def get_new_friends(user_name):
    rec_num_1 = 10
    db = connect_db()
    # 获取当前用户的用户tags 格式=('杰哥', 0, 1, 0, 0, 1, 1, 0, 0)
    my_tags_list = get_tags(user_name, db)
    tags = my_tags_list[0]
    # print(tags)
    # 获取用户tag数量tag_num
    tag_num = 0
    for tag in tags:
        if tag == 1:
            tag_num += 1
    # print(tag_num)
    # 获取用户的tag分数，用于查找相近的人
    my_tag_score = get_tag_score(tags)
    # print(my_tag_score)
    # 获取当前用户的好友数，方便确定推送的人数
    my_friends_num = get_friends_num(user_name, db)
    # 获取所有用户数量
    user_num = get_all_users(db)
    # 确定推荐数量
    rec_num = my_friends_num + rec_num_1 + 1
    # 返回的js格式列表
    result_json_0 = {"code": 1, "data": []}
    # rec_num = 3
    if rec_num > user_num:
        result_json_0["code"] = 0
        return result_json_0
    # 获取 rec_num 数量的用户tag
    friend_list_temp_1 = get_new_friends_list(db, rec_num)
    # print(friend_list_temp_1)
    # 获取所有好友的 tag,,加上自己，方便后续去重
    friend_list_temp_2 = get_friends_list(user_name, db) + my_tags_list
    # print(friend_list_temp_2)
    # 去重
    arr1 = set(friend_list_temp_1)
    arr2 = set(friend_list_temp_2)
    friend_list = arr1 - arr2
    friend_list = list(friend_list)
    print(friend_list)
    if len(friend_list) < rec_num_1:
        result_json_0["code"] = 0
        return result_json_0
    temp_num = 0
    friend_list_final = []
    for friend in friend_list:
        # 计算相似度
        count = 0  # 计数器
        count_temp = 0  # 计数器
        for i in friend:
            if i != friend[0]:  # 不是第一个
                count_temp += 1
                if i == tags[count_temp] and i == 1:
                    count += 1
                else:
                    count -= 0.25
                    continue
        if count <= 0:
            temp_tuple = ('0%',)
            friend = friend + temp_tuple
            friend_list_final.append(friend)
            temp_num += 1
            continue
        if count >= tag_num:
            temp_tuple = ('100%',)
            friend = friend + temp_tuple
            friend_list_final.append(friend)
            temp_num += 1
            continue
        else:
            temp_sim = count / tag_num * 100
            temp_sim = round(temp_sim, 2)
            temp_sim_str = str(temp_sim)
            temp_tuple = (temp_sim_str + '%',)
            friend = friend + temp_tuple
            friend_list_final.append(friend)
    for friend in friend_list_final:
        information = get_user_inform(friend[0], db)
        print(information)
        result_json = {
            "data": [
                {
                    "img": information[0][0],
                    "sex":information[0][1],
                    "id": friend[0],
                    "similarity": friend[9],
                }
            ]
        }
        result_json_0["data"] = result_json_0["data"]+result_json["data"]
        temp_num += 1
        if temp_num >= 10:
            return result_json_0
    # 结束后关闭数据库
    # return result_json_0 # 测试
    close_db(db)


#  连接数据库
def connect_db():
    db_host = 'localhost'
    db_user = 'root'
    db_password = 'root'
    db_name = 'food'
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    print('数据库链接成功！')
    return db


#  关闭数据库
def close_db(db):
    db.close()
    print("数据库已关闭")


def get_tags(user_name, db):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        user_name = str(user_name)
        sql = 'select * from tag where user_name=' + '\'' + user_name + '\''
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # result_list.sort(key=lambda likes: likes[5])
        # print(result_list)
        return result_list
    except pymysql.Error as e:
        print("field")
        cursor.close()


def get_tag_score(tags):
    score = 0
    count = 0
    for tag in tags:
        if tag != tags[0]:      #不是第一个
            if tag == 1:
                score += count
        count += 1
    return score


def get_friends_num(user_name,db):
    cursor = db.cursor()  # 游标设置
    try:
        user_name = str(user_name)
        sql = 'select * from friends where user_name1 =' + '\'' + user_name + '\''
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        return row_num
    except pymysql.Error as e:
        print("field")
        cursor.close()


def get_friends_list(user_name,db):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        user_name = str(user_name)
        sql = 'select user_name2 from friends where user_name1=' + '\'' + user_name + '\''
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # print(result_list)
        tag_list = []
        for friend in result_list:
            tag1 = get_tags(friend[0], db)
            tag_list += tag1
        # result_list.sort(key=lambda likes: likes[5])
        # print(tag_list)
        return tag_list
    except pymysql.Error as e:
        print("field")
        cursor.close()

def get_all_users(db):
    cursor = db.cursor()  # 游标设置
    try:
        sql = 'select * from user'
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        return row_num
    except pymysql.Error as e:
        print("field")
        cursor.close()


def get_new_friends_list(db,rec_num):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        rec_num = str(rec_num)
        sql = 'select * from tag order by rand() limit '+rec_num
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # result_list.sort(key=lambda likes: likes[5])
        # print(result_list)
        return result_list
    except pymysql.Error as e:
        print("field")
        cursor.close()

def get_user_inform(user_name, db):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        user_name = str(user_name)
        sql = 'select user_head,user_sex from user where user_name=' + '\'' + user_name + '\''
        # sql = 'select * from user where user_name=' + '\'' + user_name + '\''
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # print(result_list)
        return result_list
    except pymysql.Error as e:
        print("field")
        cursor.close()

# print(get_new_friends(user_name))