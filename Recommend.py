import pymysql
import json

tag = [1, 2]
user_name = "小小杰"
# 返回食物id（10个）格式：（id，是否饭u推荐（1为是，0为否），id，是否饭u推荐）


def get_food(tag, user_name):
    db = connect_db()
    food_list_1 = []  # 食物列表，非饭友推荐
    food_list_0 = []  # 食物列表，饭友推荐
    # 获取非饭u推荐的食物列表
    for i in tag:
        # temp_list =[]
        temp_list = get_food_name(db, i)  # 从food中找出与此标签贴合的食物
        # 格式[(5, 'a', '食堂1', 1, 'http//', 10),()]
        food_list_1 = food_list_1 + temp_list
        # print(len(food_list_0))
    # 根据likes_num排序
    food_list_1.sort(key=lambda likes: likes[5])
    print("非饭u推荐的食物列表为")
    print(food_list_1)  # 输出非饭u推荐食物列表
    # 获取饭u推荐的食物列表
    # 获取好友列表
    friend_list = get_friend(db, user_name)
    if len(friend_list) != 0:  # 有好友则执行下一步
        for friend in friend_list:
            collections_list = get_collections(db, friend)
            if len(collections_list) !=0: # 好友有收藏则获取收藏食物列表
                for collection in collections_list :
                    food_list_0 = food_list_0 + get_food_name_u(db, collection)

    print("饭u推荐的食物列表为")
    print(food_list_0)  # 输出饭u推荐食物列表
    #  [(1, 'a', '食堂1', 2, 'http//', 20), (2, 'b', '食堂2', 3, 'http//', 25)]
    close_db(db)
    flag_u = 0   # 是否有饭u推荐标志位，0为没有，1为有
    for food_u in food_list_0:
        for food in food_list_1:
            if food == food_u:
                flag_u = 1
                continue
        food_list_1.append(food_u)  # 是饭u推荐且不在非饭u推荐列表中，加入非饭u推荐表
    food_list_1.sort(key=lambda likes: likes[5], reverse=True)
    result_json_0 ={"code": 1, "data": []}
    for food in food_list_1:
        flag_u = 0
        for food_u in food_list_0:
            if food_u == food:
                result_json = {
                    "data": [
                        {
                            "img": food[4],
                            "id": food[0],
                            "name": food[1],
                            "location": food[2],
                            "like_nums": food[5],
                            "special": 1  # 0不是饭u推荐，1是饭u推荐
                        }
                    ]
                }
                flag_u = 1
                break
        if flag_u == 0:
            result_json = {
                "data": [
                    {
                        "img": food[4],
                        "id": food[0],
                        "name": food[1],
                        "location": food[2],
                        "like_nums": food[5],
                        "special": 0  # 0不是饭u推荐，1是饭u推荐
                    }
                ]
            }
        result_json_0["data"] = result_json_0["data"]+result_json["data"]
    # print(result_json_0)
    print(json.dumps(result_json_0, indent=2, sort_keys=True, ensure_ascii=False))


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


# 获取非饭u推荐的食物列表
def get_food_name(db, tag_id):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        tag_id = str(tag_id)
        sql = 'select * from food where food_type=' + tag_id + ' order by food_likes_num'
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


def get_food_name_u(db, collection):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        collection = str(collection[0])
        sql = 'select * from food where food_id=' + collection
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


def get_friend(db, user_name):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        sql = 'select user_name2 from friends where user_name1=' + '\''+user_name + '\''
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


def get_collections(db, friend):
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    try:
        sql = 'select food_id from collection where user_name =' + '\''+friend[0] + '\''
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

get_food(tag, user_name)
