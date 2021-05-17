# coding: utf-8
# Author：南岛鹋 
# Blog: www.ndmiao.cn
# Date ：2021/2/24 16:23
# Tool ：PyCharm

import time
import pymysql
import requests
import json
import re

class get_main:
    def get_time(self):
        time_str = time.strftime("%Y{}%m{}%d{} %X")
        return time_str.format("年","月","日")

class get_sqldata:
    def get_conn(self):
        conn = pymysql.connect(host="127.0.0.1",
                       user="root",
                       password="123456",
                       db="cov",
                       charset="utf8")
        cursor = conn.cursor()
        return conn, cursor
    def close_conn(self, conn, cursor):
        cursor.close()
        conn.close()

    def query(self, sql, *args):
        conn, cursor = self.get_conn()
        cursor.execute(sql, args)
        conn.commit()
        res = cursor.fetchall()
        self.close_conn(conn, cursor)
        return res

    def global_confirm8(self):
        sql = "select country,confirm_add from " \
              "country_details order by confirm_add desc limit 6"
        res = self.query(sql)
        country = []
        confirm_add = []
        for k, v in res:
            country.append(k)
            confirm_add.append(int(v))
        return {"country":country,"confirm_add":confirm_add}

    def continent_confirm(self):
        sql = "select sum(confirm) as continent_confirm,continent from country_details " \
              "group by continent"
        res = self.query(sql)
        continents = []
        for k,v in res:
            continent = {}
            if v == "":
                pass
            elif v== "其他":
                pass
            else:
                continent['value'] = int(k)
                continent['name'] = v
                continents.append(continent)
        return continents

    def GlobalDaily(self):
        sql = "select ds,confirm,newAddConfirm,dead,heal from global_history"
        res = self.query(sql)
        day,confirm,nowconfirm,newAddConfirm,dead,heal = [],[],[],[],[],[]
        for a,b,c,d,e in res:
            day.append(a.strftime("%Y-%m-%d"))
            confirm.append(int(b))
            nowconfirm.append(int(b-d-e))
            newAddConfirm.append(int(c))
            dead.append(int(d))
            heal.append(int(e))
        return {'day':day,'confirm':confirm,'nowconfirm':nowconfirm,'newAddConfirm':newAddConfirm,'dead':dead,'heal':heal}

    def GlobalRate(self):
        sql = "select ds,deadRate,healRate from global_history"
        res = self.query(sql)
        day,deadRate,healRate = [],[],[]
        for a,b,c in res:
            day.append(a.strftime("%Y-%m-%d"))
            deadRate.append(b)
            healRate.append(c)
        return {'day':day,'deadRate':deadRate,'healRate':healRate}

    def WorldMap(self):
        sql = "select country,confirm from country_details"
        res = self.query(sql)
        data = []
        with open('country.json', 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
        for a,b in res:
            if a in ['圣基茨和尼维斯','圣文森特和格林纳丁斯','梵蒂冈','钻石号邮轮','马提尼克岛','马绍尔群岛']:
                pass
            else:
                data.append({'name':json_data[a],'value':int(b),'CnName':a})
        china_sql = "select confirm from china_history order by confirm desc limit 1"
        china_res = self.query(china_sql)
        for i in china_res:
            data.append({'name':'China','value':int(i[0]),'CnName':'中国'})
        return data

    def ChinaNum(self):
        sql = "select confirm,heal,dead from china_history order by confirm desc limit 1"
        res = self.query(sql)
        for a,b,c in res:
            data = {'nowconfirm':int(a-b-c),'confirm':int(a),'heal':int(b),'dead':int(c)}
        return data

    def ChinaDaily(self):
        sql = "select ds,confirm,heal,dead from china_history"
        res = self.query(sql)
        day,confirm,nowconfirm,dead,heal = [],[],[],[],[]
        for a,b,d,e in res:
            day.append(a.strftime("%Y-%m-%d"))
            confirm.append(int(b))
            nowconfirm.append(int(b-d-e))
            heal.append(int(d))
            dead.append(int(e))
        return {'day':day,'confirm':confirm,'nowconfirm':nowconfirm,'dead':dead,'heal':heal}

    def ChinaAdd(self):
        sql = "select ds,confirm_add,suspect_add,heal_add,dead_add from china_history"
        res = self.query(sql)
        day,confirm_add,suspect_add,heal_add,dead_add = [],[],[],[],[]
        for a,b,c,d,e in res:
            day.append(a.strftime("%Y-%m-%d"))
            confirm_add.append(int(b))
            suspect_add.append(int(c))
            heal_add.append(int(d))
            dead_add.append(int(e))
        return {'day':day,'confirm_add':confirm_add,'suspect_add':suspect_add,'heal_add':heal_add,'dead_add':dead_add}

    def ChinaCity(self):
        sql = "select city,confirm from " \
              "(select city,confirm from china_details " \
              "where update_time=(select update_time from china_details order by update_time desc limit 1) " \
              "and province not in ('香港','台湾','北京','上海','天津','重庆','湖北') and city not in ('境外输入') " \
              "union all " \
              "select province as city,sum(confirm) as confirm from china_details " \
              "where update_time=(select update_time from china_details order by update_time desc limit 1) " \
              "and province in ('香港','台湾','北京','上海','天津','重庆') group by province) as a " \
              "order by confirm desc limit 6"
        res = self.query(sql)
        city = []
        confirm = []
        for k, v in res:
            city.append(k)
            confirm.append(int(v))
        return {"city":city,"confirm":confirm}

    def ChinaProvince(self):
        sql = "select province,confirm from (select province,sum(confirm) as confirm from china_details " \
              "where update_time=(select update_time from china_details order by update_time desc limit 1) " \
              "group by province) as a order by confirm desc limit 6"
        res = self.query(sql)
        provinces = []
        for k,v in res:
            provinces.append({'name':k,'value':int(v)})
        return provinces

    def ChinaMap(self):
        sql = "select province,sum(confirm) from china_details " \
              "where update_time=(select update_time from china_details " \
              "order by update_time desc limit 1) " \
              "group by province"
        res = self.query(sql)
        china = []
        for k,v in res:
            china.append({'name':k,'value':int(v)})
        return china

    def login(self):
        sql = "select * from login"
        res = self.query(sql)
        for k,v,i in res:
            return {'name':k,'password':v}

    def Loadstatus(self,num):
        sql = "update login set status = "+str(num) +" where name='admin'"
        self.query(sql)

    def getStatus(self):
        sql = "select status from login"
        res = self.query(sql)
        return {'status':res[0][0]}

    def GetNews(self):
        sql = "select * from china_news order by pubtime desc limit 6"
        res = self.query(sql)
        data = []
        for a,b,c,d,e in res:
            data.append({'title':c,'url':d,'pic':e})
        return data

    def datalist(self,num):
        sql = ['select * from china_details',
               'select * from china_history',
               'select * from china_news',
               'select * from city_details',
               'select * from country_details',
               'select * from global_history']
        res = self.query(sql[num])
        if num == 0:
            title = [{'column_name': 'column_ID', 'column_comment': 'ID'},
                     {'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_province', 'column_comment': '省份'},
                     {'column_name': 'column_city', 'column_comment': '城市'},
                     {'column_name': 'column_confirm', 'column_comment': '累计确诊'},
                     {'column_name': 'column_confirm_add', 'column_comment': '新增确诊'},
                     {'column_name': 'column_heal', 'column_comment': '累计治愈'},
                     {'column_name': 'column_dead', 'column_comment': '累计死亡'}]
            data = []
            for a,b,c,d,e,f,g,h in res:
                data.append({'column_ID':a,'column_time':b.strftime("%Y-%m-%d"),'column_province':c,'column_city':d,'column_confirm':e,'column_confirm_add':f,'column_heal':g,'column_dead':h})
            return {'tableHead':title,'tableData':data}
        elif num == 1:
            title = [{'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_confirm', 'column_comment': '累计确诊'},
                     {'column_name': 'column_confirm_add', 'column_comment': '新增确诊'},
                     {'column_name': 'column_suspect', 'column_comment': '现存疑似'},
                     {'column_name': 'column_suspect_add', 'column_comment': '新增疑似'},
                     {'column_name': 'column_heal', 'column_comment': '累计治愈'},
                     {'column_name': 'column_heal_add', 'column_comment': '新增治愈'},
                     {'column_name': 'column_dead', 'column_comment': '累计死亡'},
                     {'column_name': 'column_dead_add', 'column_comment': '新增死亡'}]
            data = []
            for a,b,c,d,e,f,g,h,i in res:
                data.append({'column_time':a.strftime("%Y-%m-%d"),'column_confirm':b,'column_confirm_add':c,'column_suspect':d,'column_suspect_add':e,'column_heal':f,'column_heal_add':g,'column_dead':h,'column_dead_add':i})
            return {'tableHead': title, 'tableData': data}
        elif num == 2:
            title = [{'column_name': 'column_ID', 'column_comment': 'ID'},
                     {'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_title', 'column_comment': '标题'},
                     {'column_name': 'column_url', 'column_comment': '链接'},
                     {'column_name': 'column_pic', 'column_comment': '图片'}]
            data = []
            for a,b,c,d,e in res:
                data.append({'column_ID':a,'column_time':b.strftime("%Y-%m-%d"),'column_title':c,'column_url':d,'column_pic':e})
            return {'tableHead': title, 'tableData': data}
        elif num == 3:
            title = [{'column_name': 'column_ID', 'column_comment': 'ID'},
                     {'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_country', 'column_comment': '国家'},
                     {'column_name': 'column_city', 'column_comment': '城市'},
                     {'column_name': 'column_nameMap', 'column_comment': '地图标识'},
                     {'column_name': 'column_confirm', 'column_comment': '累计确诊'},
                     {'column_name': 'column_dead', 'column_comment': '累计死亡'},
                     {'column_name': 'column_heal', 'column_comment': '累计治愈'}]
            data = []
            for a,b,c,d,e,f,g,h in res:
                data.append({'column_ID':a,'column_time':b.strftime("%Y-%m-%d"),'column_country':c,'column_city':d,'column_nameMap':e,'column_confirm':f,'column_dead':g,'column_heal':h})
            return {'tableHead': title, 'tableData': data}
        elif num == 4:
            title = [{'column_name': 'column_ID', 'column_comment': 'ID'},
                    {'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_country', 'column_comment': '国家'},
                     {'column_name': 'column_continent', 'column_comment': '洲'},
                     {'column_name': 'column_confirm', 'column_comment': '累计确诊'},
                     {'column_name': 'column_confirm_add', 'column_comment': '新增确诊'},
                     {'column_name': 'column_dead', 'column_comment': '累计死亡'},
                     {'column_name': 'column_heal', 'column_comment': '累计治愈'},
                     {'column_name': 'column_nowConfirm', 'column_comment': '现存确诊'}]
            data = []
            for i,a,b,c,d,e,f,g,h in res:
                data.append({'column_ID':i,'column_time':a.strftime("%Y-%m-%d"),'column_country':b,'column_continent':c,'column_confirm':d,'column_confirm_add':e,'column_dead':f,'column_heal':g,'column_nowConfirm':h})
            return {'tableHead': title, 'tableData': data}
        elif num==5:
            title = [{'column_name': 'column_time', 'column_comment': '时间'},
                     {'column_name': 'column_confirm', 'column_comment': '累计确诊'},
                     {'column_name': 'column_dead', 'column_comment': '累计死亡'},
                     {'column_name': 'column_heal', 'column_comment': '累计治愈'},
                     {'column_name': 'column_newConfirm', 'column_comment': '累计新增'},
                     {'column_name': 'column_deadRate', 'column_comment': '死亡比率'},
                     {'column_name': 'column_healRate', 'column_comment': '治愈比率'}]
            data = []
            for a,b,c,d,e,f,g in res:
                data.append({'column_time':a.strftime("%Y-%m-%d"),'column_confirm':b,'column_dead':c,'column_heal':d,'column_newConfirm':e,'column_deadRate':f,'column_healRate':g})
            return {'tableHead': title, 'tableData': data}

    def zsgData(self,type,num,key):
        sqlhead = {'add':["insert into china_details values (","insert into china_history values (","insert into china_news values (","insert into city_details values (","insert into country_details values (","insert into global_history values ("],
                   'delete':["delete from china_details where id=","delete from china_history where ds=","delete from china_news where id=","delete from city_details where id=","delete from country_details where id=","delete from global_history where ds="],
                   'edit':["update china_details ","update china_history ","update china_news ","update city_details ","update country_details ","update global_history "]}
        if type=='add':
            sql = sqlhead['add'][num] + key
            self.query(sql)

        elif type=='delete':
            sql = sqlhead['delete'][num] + key
            print(sql)
            self.query(sql)

        elif type=='edit':
            sql = sqlhead['edit'][num] + key
            print(sql)
            self.query(sql)


class get_webdata():
    def get_urltext(self,url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        r = requests.get(url, headers)
        return r

    def get_global(self):
        url = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis"
        r = self.get_urltext(url)
        res = json.loads(r.text)
        data_all = res['data']['FAutoGlobalStatis']
        return {"nowConfirm": data_all["nowConfirm"],"confirm":data_all["confirm"],"heal":data_all["heal"],"dead":data_all["dead"]}

    def webdata(self):
        globaldata = self.get_global()
        return {"globaldata":globaldata}

    def news(self,url):
        headers = {

            'Host': 'channel.chinanews.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        }
        r = requests.get(url, headers=headers)
        url_data = r.text
        matchObj = re.match(r'(.*)specialcnsdata = (.*);', url_data, re.M | re.I)
        text = matchObj.group(2)
        news = json.loads(text)
        allnews = []
        for i in news['docList']:
            list = {'pubtime': i['pubtime'], 'title': i['title'], 'content_y': '中国新闻网',
                    'galleryphoto': i['galleryphoto'],'url':i['url']}
            allnews.append(list)
        return allnews

if __name__ == "__main__":
    print(get_webdata().news('http://channel.chinanews.com/cns/gjfyztscroll/5055.shtml?pager=0&pagenum=100'))
