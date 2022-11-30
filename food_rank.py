import pymysql
import json


#  rank_all 返回总榜（字典格式，同推荐），rank_tag 返回类别榜.  code 为0代表没有匹配项，为空，code为1代表成功
#
#  设置返回食物个数，不足则返回剩下的
rec_num = 10
#  测试用例
tag = ""





def rank_all():
    db = connect_db()
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    result = []
    result_list = []
    try:
        sql = 'select food_id,food_name,food_loc,food_type,food_src,food_likes_num,food_price from food order by food_likes_num desc'
        print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        print("success!")
        # print(row_num)
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # result_list.sort(key=lambda likes: likes[5])
        # print(result_list)
    except pymysql.Error as e:
        print("field")
        cursor.close()
     # 大于需要个数，选择
    if len(result_list) > rec_num:
        count = 0
        result = []
        for food in result_list:
            if count >= rec_num:
                # print(len(result))
                result_dict = now_json(result)
                return result_dict
            else:
                result.append(result_list[count])
                count += 1
    #  为空
    if len(result_list) == 0:
        return "empty"
    # 不足需要个数，返回剩余的
    if len(result_list) <= rec_num:
        result_dict = now_json(result)
        return result_dict


def rank_tag(tag):
    db = connect_db()
    cursor = db.cursor()  # 游标设置
    # cursor = db.cursor(pymysql.cursors.DictCursor) # 字典查询
    result = []
    result_list = []
    tag_id = str(tag)
    if tag_id == "all":
        try:
            sql = 'select food_id,food_name,food_loc,food_type,food_src,food_likes_num,food_price from food order by food_likes_num desc'
            print(sql)
            row_num = cursor.execute(sql)  # 查询数据库信息
            print("success!")
            # print(row_num)
            result = cursor.fetchall()  # 保存查询的每一行到result
            result_list = list(result)  # 查询结果转化为列表
            # result_list.sort(key=lambda likes: likes[5])
            # print(result_list)
        except pymysql.Error as e:
            print("field")
            cursor.close()
        # 大于需要个数，选择
        if len(result_list) > rec_num:
            count = 0
            result = []
            for food in result_list:
                if count >= rec_num:
                    # print(len(result))
                    result_dict = now_json(result,1)
                    return result_dict
                else:
                    result.append(result_list[count])
                    count += 1
        #  为空
        if len(result_list) == 0:
            result_dict = now_json(result, 0)
            return result_dict
        # 不足需要个数，返回剩余的
        if len(result_list) <= rec_num:
            result_dict = now_json(result,2)
            return result_dict
    try:
        sql = 'select food_id,food_name,food_loc,food_type,food_src,food_likes_num,food_price from food where food_type=' + tag_id + ' order by food_likes_num'
        # print(sql)
        row_num = cursor.execute(sql)  # 查询数据库信息
        # print("success!")
        # print(row_num)
        result = cursor.fetchall()  # 保存查询的每一行到result
        result_list = list(result)  # 查询结果转化为列表
        # result_list.sort(key=lambda likes: likes[5])
        # print(result_list)
    except pymysql.Error as e:
        print("field")
        cursor.close()
     # 大于需要个数，选择
    if len(result_list) > rec_num:
        count = 0
        result = []
        for food in result_list:
            if count >= rec_num:
                # print(len(result))
                # 转字典
                result_dict = now_json(result,1)
                return result_dict
            else:
                result.append(result_list[count])
                count += 1
    #  为空
    if len(result_list) == 0:
        result_dict = now_json(result, 0)
        return result_dict
    # 不足需要个数，返回剩余的
    if len(result_list) <= rec_num:
        result_dict = now_json(result,2)
        return result_dict



#  连接数据库
def connect_db():
    db_host = '1.15.75.204'
    port = 3306
    db_user = 'db_food'
    db_password = 'k6safXijNhKzZNe7'
    db_name = 'db_food'
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    print('数据库链接成功！')
    return db


def now_json(result_list, code):
    result_json_0 = {"code": 1, "data": []}
    if code == 2:
        result_json_0["code"] = 2
    if code == 0:
        result_json_0["code"] = 0
        return result_json_0
    for food in result_list:
        result_json = {
            "data": [
                {
                    "img": food[4],
                    "id": food[0],
                    "name": food[1],
                    "location": food[2],
                    "like_nums": food[5],
                    "price": food[6],
                    "special": 1  # 0不是饭u推荐，1是饭u推荐
                }
            ]
        }
        result_json_0["data"] = result_json_0["data"]+result_json["data"]
    return result_json_0


print(rank_tag(tag))