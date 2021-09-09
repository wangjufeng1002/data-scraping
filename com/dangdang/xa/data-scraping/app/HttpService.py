import multiprocessing
import threading

from flask import Flask, request, send_from_directory
from flask_cors import *
import json
import app as cmt
import searchBook

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/process", methods=["POST"])
def run():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    account = json_obj.get("account")
    passwd = json_obj.get("password")
    products = json_obj.get("products")
    port = json_obj.get("port")
    task_id = json_obj.get("task_id")
    task_label = json_obj.get("task_label")
    threading.Thread(target=async_run, args=(account, passwd, products, port, task_id, task_label)).start()
    data = {'data': "1"}
    return json.dumps(data, ensure_ascii=False)


@app.route("/process_phone", methods=["POST"])
def run_phone():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    account = json_obj.get("account")
    products = json_obj.get("products")
    addr = json_obj.get("port")
    task_id = json_obj.get("task_id")
    task_label = json_obj.get("task_label")
    threading.Thread(target=async_run_phone, args=(addr, account, products, task_id, task_label, addr)).start()
    data = {'data': "1"}
    return json.dumps(data, ensure_ascii=False)


def async_run_phone(addr, account, products, task_id, task_label, port):
    cmt.run_phone(addr, "0", account, products, task_id, task_label, port)


def async_run(account, passwd, products, port, task_id, task_label):
    cmt.process_data(account, passwd, products, port, task_id, task_label)


def async_heart(account, addr):
    cmt.heart(account, addr)


@app.route('/get_proxy_app', methods=['GET'])
def return_proxy_app():
    return send_from_directory('', 'Postern-3.1.2.apk')


@app.route("/heart", methods=["POST"])
def heart():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    number = json_obj.get("number")
    account = json_obj.get("account")
    addr = json_obj.get("port")
    multiprocessing.Process(target=async_heart,args=(account,addr)).start()
    return "1"


@app.route("/test", methods=["GET"])
def test():
    return "success"


@app.route("/search", methods=["POST"])
def async_search():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    words = json_obj.get("words")
    shop = json_obj.get("shop")
    threading.Thread(target=searchBook.search_api, args=(words, shop)).start()
    return "1"


if __name__ == '__main__':
    app.run(debug=True, port=10001, host="0.0.0.0")
