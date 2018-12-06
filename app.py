import urllib
from urllib.request import urlopen

from flask import Flask, json
from urllib import request as my_request
from urllib import  parse
from flask.json import jsonify

app = Flask(__name__)
@app.route('/<boxId>')
def value1(boxId):
# 提取token
    login_data = parse.urlencode([
        ('username', 'hhjj543212012'),
        ('password', '0028Bytcjlie'),
        ('scope', 'openid offline_access fbox email profile'),
        ('client_id', 'shwd'),
        ('client_secret', '490b71a09dcb4858b365a5c944b829ca'),
        ('grant_type', 'password')
    ])
    req = my_request.Request('https://account.flexem.com/core/connect/token')

    with my_request.urlopen(req, data=login_data.encode('utf-8')) as f:
        access_token = f.read().decode('utf-8')
        token_dict = json.loads(access_token)
        token = token_dict['access_token']

    # 提取names
    # http://fbcs101.fbox360.com/api/v2/box/33338/dmon/grouped
    req = my_request.Request('http://fbcs101.fbox360.com/api/v2/box/'+boxId+'/dmon/grouped')
    req.add_header('Authorization','Bearer '+token)
    with my_request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        access_names = f.read().decode('utf-8')
        names_list = json.loads(access_names)
        print(names_list)
        names_dict1 = names_list[0]
        names_list2 = names_dict1['items']
        i = 0
        name_newlist = []
        while (i<len(names_list2)):
            names_dict = names_list2[i]
            name = names_dict['name']
            name_newlist.append(name)
            i = i+1
        print(type(name_newlist))
        name_post ={"names":name_newlist}
        name_json = json.dumps(name_post)
        print(name_json)
        print(type(name_json))

        # name_byte = bytes(name_json, 'utf8')
        # print(name_byte)
    # 获取盒子数据 方式是提交json不是byte
    headers = {"Content-Type": "application/json; charset=UTF-8","Authorization":"Bearer "+token}
    data = bytes(name_json, 'utf8')
    request = urllib.request.Request('http://fbcs101.fbox360.com/api/v2/box/'+boxId+'/dmon/value/get', headers=headers, data=data)
    response = urlopen(request)
    return response.read().decode('utf-8')







    # names = names_dict2['name']

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
