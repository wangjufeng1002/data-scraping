import multiprocessing
import threading

from flask import Flask, request, send_from_directory
from flask_cors import *
import json
import app as cmt

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
    addr = json_obj.get("addr")
    port = json_obj.get("port")
    task_id = json_obj.get("task_id")
    task_label = json_obj.get("task_label")
    threading.Thread(target=async_run_phone, args=(addr, account, products, task_id, task_label, addr, port)).start()
    data = {'data': "1"}
    return json.dumps(data, ensure_ascii=False)


def async_run_phone(addr, account, products, task_id, task_label, ip, port):
    cmt.run_phone(addr, "0", account, products, task_id, task_label, ip, port)


def async_run(account, passwd, products, port, task_id, task_label):
    cmt.process_data(account, passwd, products, port, task_id, task_label)


@app.route('/get_proxy_app', methods=['GET'])
def return_proxy_app():
    return send_from_directory('', 'Postern-3.1.2.apk')


@app.route("/heart", methods=["POST"])
def heart():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    number = json_obj.get("number")
    account = json_obj.get("account")
    port = json_obj.get("port")
    cmt.heart(number, account, port)
    return "1"


@app.route("/test", methods=["GET"])
def test():
    return "success"


if __name__ == '__main__':
    app.run(debug=True, port=10001, host="0.0.0.0")
