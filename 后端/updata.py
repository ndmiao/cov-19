# coding: utf-8
# Author：南岛鹋 
# Blog: www.ndmiao.cn
# Date ：2021/2/27 21:09
# Tool ：PyCharm
import sys

import pymysql
import time
import json
import traceback  #追踪异常
import requests

def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="123456",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def get_urltext(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    r = requests.get(url, headers)
    return r


def get_china_history():
    """
    :return: 返回历史数据
    """
    url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare"
    r = get_urltext(url)
    res = json.loads(r.text)
    data_all = res['data']

    history = {}  # 历史数据
    for i in data_all['chinaDayList']:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y.%m.%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all['chinaDayAddList']:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y.%m.%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})
    return history


def get_china_details():
    """
    :return: 返回历史数据和当日详细数据
    """
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    r = get_urltext(url)
    res = json.loads(r.text)
    data_all = json.loads(res['data'])

    details = []
    update_time = data_all["lastUpdateTime"]
    data_country = data_all["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return details

def insert_china_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_china_details()  #  0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        #sql = "update china_details set update_time=%s,confirm=%s,confirm_add=%s,heal=%s,dead=%s where province=%s and city=%s"
        sql = "insert into china_details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from china_details order by id desc limit 1)' #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始插入最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}插入最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_china_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_china_details()  #  0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        sql = "update china_details set update_time=%s,confirm=%s,confirm_add=%s,heal=%s,dead=%s where province=%s and city=%s"
        # sql = "insert into china_details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from china_details order by id desc limit 1)' #对比当前最大时间戳
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, [item[0],item[3],item[4],item[5],item[6],item[1],item[2]])
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def china_details():
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        sql = "select count(*) from china_details"
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        if num > 1:
            update_china_details()
        else:
            insert_china_details()
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_china_history()  #  0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into china_history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from china_history where ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def get_city_details():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoforeignList'
    r = get_urltext(url)
    res = json.loads(r.text)
    data = res['data']
    data_all = data['FAutoforeignList']

    city_details = []
    for i in data_all:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y.%m.%d", tup)
        country = i["name"]
        country_confirm = i["confirm"]
        dead = i["dead"]
        heal = i["heal"]
        #         print(i.setdefault('children',0))
        try:
            for j in i['children']:
                city_ds = i["y"] + "." + j["date"]
                tup = time.strptime(city_ds, "%Y.%m.%d")
                city_ds = time.strftime("%Y.%m.%d", tup)
                city = j["name"]
                nameMap = j["nameMap"]
                city_confirm = j["confirm"]
                city_dead = j["dead"]
                city_heal = j["heal"]
                city_details.append([city_ds, country, city, nameMap, city_confirm, city_dead, city_heal])
        except:
            city_details.append([ds, country, country, '', country_confirm, dead, heal])
    return city_details


def get_country_details():
    url = "https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist"
    r = get_urltext(url)
    res = json.loads(r.text)
    data_all = res['data']

    country_details = []
    for i in data_all:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y.%m.%d", tup)
        country = i["name"]
        continent = i["continent"]
        confirm = i["confirm"]
        confirmAdd = i["confirmAdd"]
        dead = i["dead"]
        heal = i["heal"]
        nowConfirm = i["nowConfirm"]
        country_details.append([ds, country, continent, confirm, confirmAdd, dead, heal, nowConfirm])
    return country_details

def update_country_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_country_details()
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        update_sql = "update country_details set update_time=%s,confirm=%s,confirm_add=%s,dead=%s,heal=%s,nowConfirm=%s where country=%s"
        #sql = "insert into country_details(update_time,country,continent,confirm,confirm_add,dead,heal,nowConfirm) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from country_details where country=%s)'
        for i in li:
            cursor.execute(sql_query,[i[0],i[1]])
            if not cursor.fetchone()[0]:
                cursor.execute(update_sql,[i[0],i[3],i[4],i[5],i[6],i[7],i[1]])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_country_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_country_details()
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        # update_sql = "update country_details set update_time=%s,confirm=%s,confirm_add=%s,dead=%s,heal=%s,nowConfirm=%s where country=%s"
        sql = "insert into country_details(update_time,country,continent,confirm,confirm_add,dead,heal,nowConfirm) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select update_time from country_details where country=%s"
        for i in li:
            if not cursor.execute(sql_query, i[1]):
                cursor.execute(sql,i)
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据插入完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def country_details():
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        sql = "select count(*) from country_details"
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        if num > 1:
            update_country_details()
        else:
            insert_country_details()
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



def insert_city_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_city_details()
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        # update_sql = "update country_details set update_time=%s,confirm=%s,confirm_add=%s,dead=%s,heal=%s,nowConfirm=%s where country=%s"
        sql = "insert into city_details(update_time,country,city,nameMap,confirm,dead,heal) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select update_time from city_details where country=%s and city=%s"
        for i in li:
            if not cursor.execute(sql_query, [i[1],i[2]]):
                cursor.execute(sql,i)
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_city_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_city_details()
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        update_sql = "update city_details set update_time=%s,confirm=%s,dead=%s,heal=%s where country=%s and city=%s"
        #sql = "insert into city_details(update_time,country,continent,confirm,confirm_add,dead,heal,nowConfirm) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from city_details where country=%s and city=%s)'
        for i in li:
            cursor.execute(sql_query,[i[0],i[1],i[2]])
            if not cursor.fetchone()[0]:
                cursor.execute(update_sql,[i[0],i[4],i[5],i[6],i[1],i[2]])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def city_details():
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        sql = "select count(*) from city_details"
        cursor.execute(sql)
        num = cursor.fetchall()[0][0]
        if num > 1:
            update_city_details()
        else:
            insert_city_details()

    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def get_global_history():
    url = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis,FAutoGlobalDailyList,FAutoCountryConfirmAdd"
    r = get_urltext(url)
    res = json.loads(r.text)
    data_all = res['data']

    gd = []
    for i in data_all['FAutoGlobalDailyList']:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y.%m.%d", tup)
        confirm = i['all']['confirm']
        dead = i['all']['dead']
        heal = i['all']['heal']
        newAddConfirm = i['all']['newAddConfirm']
        deadRate = i['all']['deadRate']
        healRate = i['all']['healRate']
        gd.append([ds, confirm, dead, heal, newAddConfirm, deadRate, healRate])

    return gd

def update_global_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        gh = get_global_history()  #  0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into global_history values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from global_history where ds=%s"
        for i in gh:
            if not cursor.execute(sql_query, i[0]):
                cursor.execute(sql, i)
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



if __name__ == "__main__":
    print(sys.argv)
    print("更新china_details中...")
    china_details()
    print("更新china_history中...")
    update_history()
    print("更新city_details中...")
    city_details()
    print("更新country_details中...")
    country_details()
    print("更新global_history中...")
    update_global_history()
