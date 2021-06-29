from flask import Flask, request
from entity import Header, Book
import json
import entity
import dataReptiledb
import drag

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "hello world"


@app.route("/headers/json", methods=["POST"])
def headers():
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    name = get_Data.get('name')
    age = get_Data.get('age')
    print(name, age)
    return "hello world"


@app.route("/insertHeaders", methods=["POST"])
def insertHeaders():
    # 获取传入的参数
    get_Data = request.get_data()
    jsonObj = json.loads(get_Data)
    if jsonObj.get("account") is None or jsonObj.get("password") is None:
        return "请检查账号密码"
    jsonObj.setdefault("cookie", " ")
    jsonObj.setdefault("referer", "https://detail.tmall.com/")
    jsonObj.setdefault("user-agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36")
    jsonObj.setdefault("status", 0)
    # 传入的参数为bytes类型，需要转化成json
    header = json.loads(json.dumps(jsonObj), object_hook=entity.headerHandler)
    result = dataReptiledb.insetHeaders(header)
    return result[1]

@app.route("/updateHeaders", methods=["POST"])
def updateHeaders():
    # 获取传入的参数
    get_Data = request.get_data()
    jsonObj = json.loads(get_Data)
    print(jsonObj)
    if (jsonObj.get("account") is None and  jsonObj.get("id") is None ) or jsonObj.get("cookie") is None:
        return "更新条件 账号或id 必须存在一个 ， cookie 不能为空"
    jsonObj.setdefault("referer", "https://detail.tmall.com/")
    jsonObj.setdefault("user-agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36")
    jsonObj.setdefault("status", 1)
    # 传入的参数为bytes类型，需要转化成json
    header = json.loads(json.dumps(jsonObj), object_hook=entity.headerHandler)
    result = dataReptiledb.updateHeaders(header)
    return result[1]
@app.route("/getInvalidHeaders", methods=["GET"])
def getInvalidHeaders():
    headers = dataReptiledb.getHeadersByStatus(0)
    return json.dumps(headers)


@app.route("/refresh",methods=["GET"])
def refreshCookie():
    drag.process()

if __name__ == '__main__':
    dataReptiledb.init(None,"./logs/db-http-service.log")
    app.run(debug=True,port=10001)
