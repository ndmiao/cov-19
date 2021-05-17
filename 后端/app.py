# coding: utf-8
# Author：南岛鹋 
# Blog: www.ndmiao.cn
# Date ：2021/2/24 16:20
# Tool ：PyCharm


import urllib


from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

from utils import get_main, get_webdata, get_sqldata

DEBUG = False

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def firstpage():
    return redirect('http://localhost:8080/')


@app.route('/gettime', methods=['GET'])
def get_time():
    return get_main().get_time()


@app.route('/getGlobalStasis', methods=['GET'])
def get_GlobalStatis():
    return jsonify(get_webdata().webdata())


@app.route('/getGlobalData', methods=['GET'])
def get_Globaldata():
    country = get_sqldata().global_confirm8()
    continent = get_sqldata().continent_confirm()
    globalhistory = get_sqldata().GlobalDaily()
    globalrate = get_sqldata().GlobalRate()
    globaldata = {"global_confirm8":country,"continent_confirm":continent,"globalhistory":globalhistory,'globalrate':globalrate}
    return jsonify(globaldata)

@app.route('/getWorldMap',methods=['GET'])
def get_WorldMap():
    worldmap = get_sqldata().WorldMap()
    return jsonify(worldmap)

@app.route('/getChina',methods=['GET'])
def get_China():
    ChinaNum = get_sqldata().ChinaNum()
    data = {"ChinaNum":ChinaNum}
    return jsonify(data)

@app.route('/getnews',methods=['GET'])
def get_news():
    News = get_sqldata().GetNews()
    return jsonify(News)

@app.route('/ChinaMain',methods=['GET'])
def get_ChinaMain():
    ChinaDaily = get_sqldata().ChinaDaily()
    ChinaAdd = get_sqldata().ChinaAdd()
    ChinaCity = get_sqldata().ChinaCity()
    ChinaProvince = get_sqldata().ChinaProvince()
    China = get_sqldata().ChinaMap()
    data = {"ChinaDaily":ChinaDaily,'ChinaAdd':ChinaAdd,'ChinaCity':ChinaCity,'ChinaProvince':ChinaProvince,'China':China}
    return jsonify(data)

@app.route('/News',methods=['GET'])
def get_News():
    ChinaNews = get_webdata().news("https://channel.chinanews.com/cns/s/5013.shtml?pager=0&pagenum=100")
    WorldNews = get_webdata().news("http://channel.chinanews.com/cns/gjfyztscroll/5055.shtml?pager=0&pagenum=100")
    return jsonify({'ChinaNews': ChinaNews, 'WorldNews': WorldNews})

@app.route('/pass', methods=['GET', 'POST'])
def get_pass():
    login_data = get_sqldata().login()
    response_object = {'code': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        id = post_data.get('userName')
        password = post_data.get('password')
        status = post_data.get('status')
        if id == login_data['name'] and password == login_data['password']:
            get_sqldata().Loadstatus(status)
            return jsonify(response_object)
        else:
            return jsonify({'code': 'error'})

@app.route('/getstatus',methods=['GET'])
def get_status():
    loginStatus = get_sqldata().getStatus()
    return jsonify(loginStatus)

@app.route('/datalist', methods=['GET', 'POST'])
def get_datalist():
    response_object = {'code': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        num = post_data['num']
        response_object['datalist'] = get_sqldata().datalist(num)
        return jsonify(response_object)

@app.route('/addData', methods=['GET', 'POST'])
def addData():
    if request.method == 'POST':
        post_data = request.get_json()
        data = [v[0] for k, v in urllib.parse.parse_qs(post_data['data']).items()]
        sql = ''
        for i in data:
            sql = sql + "'" + i + "'" + ","
        str = sql[::-1].replace(",", ")", 1)[::-1]
        print(post_data['type'],post_data['num'],str)
        get_sqldata().zsgData(post_data['type'],post_data['num'],str)
        return '1'

@app.route('/deleteData', methods=['GET', 'POST'])
def deleteData():
    if request.method == 'POST':
        post_data = request.get_json()
        data = dict([(k,v[0]) for k, v in urllib.parse.parse_qs(post_data['data']).items()])
        try:
            str = data['column_ID']
        except:
            str = "'"+data['column_time']+"'"
        get_sqldata().zsgData(post_data['type'], post_data['num'], str)
        return '1'

@app.route('/editData', methods=['GET', 'POST'])
def editData():
    if request.method == 'POST':
        post_data = request.get_json()
        data = dict([(k, v[0]) for k, v in urllib.parse.parse_qs(post_data['data']).items()])
        str = "set "
        if post_data['num'] == 0:
            str += "id="+data['column_ID']+",update_time='"+data['column_time']+"',province='"+data['column_province']+"',city='"+data['column_city']+"',confirm="+data['column_confirm']+",confirm_add="+data['column_confirm_add']+",heal="+data['column_heal']+",dead="+data['column_dead']
        elif post_data['num'] == 1:
            str += "ds='"+data['column_time']+"',confirm="+data['column_confirm']+",confirm_add="+data['column_confirm_add']+",suspect="+data['column_suspect']+",suspect_add="+data['column_suspect_add']+",heal="+data['column_heal']+",heal_add="+data['column_heal_add']+",dead="+data['column_dead']+",dead_add="+data['column_dead_add']
        elif post_data['num'] == 2:
            str += "id=" + data['column_ID'] +",pubtime='"+data['column_time']+"',title='"+data['column_title']+"',sources='"+data['column_url']+"',galleryphoto='"+data['column_pic']+"'"
        elif post_data['num'] == 3:
            str += "id=" + data['column_ID'] +",update_time='"+data['column_time']+"',country='"+data['column_country']+"',city='"+data['column_city']+"',nameMap='"+data['column_nameMap']+"',confirm="+data['column_confirm']+",dead="+data['column_dead']+",heal="+data['column_heal']
        elif post_data['num'] == 4:
            str += "id=" + data['column_ID'] + ",update_time='" + data['column_time'] +"',country='"+data['column_country']+"',continent='"+data['column_continent']+"',confirm="+data['column_confirm']+",confirm_add="+data['column_confirm_add']+",heal="+data['column_heal']+",dead="+data['column_dead']+",nowConfirm="+data['column_nowConfirm']
        elif post_data['num'] == 5:
            str += "ds='"+data['column_time'] +"',confirm="+data['column_confirm']+",dead="+data['column_dead']+",heal="+data['column_heal']+",newAddConfirm="+data['column_newConfirm']+",deadRate="+data['column_deadRate']+",healRate="+data['column_healRate']
        try:
            str = str + " where id = " + data['column_ID']
        except:
            str = str + " where ds = " + "'"+data['column_time']+"'"
        get_sqldata().zsgData(post_data['type'], post_data['num'], str)
        print(str)
        print(data)
    return '1'


if __name__ == '__main__':
    # 运行flask app
    app.debug = True
    app.run(host='127.0.0.1', port=5000)  # debug=True
