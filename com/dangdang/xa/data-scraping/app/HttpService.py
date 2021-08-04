import multiprocessing
import threading

from flask import Flask, request
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
    number = json_obj.get("number")
    products = json_obj.get("products")
    port = json_obj.get("port")
    threading.Thread(target=async_run, args=(number, account, passwd, products, port,)).start()
    data = {'data': "1"}
    return json.dumps(data, ensure_ascii=False)


def async_run(number, account, passwd, products, port):
    cmt.process_data(number, account, passwd, products, port)


@app.route("/heart", methods=["POST"])
def heart():
    get_data = request.get_data()
    json_obj = json.loads(get_data)
    number = json_obj.get("number")
    account = json_obj.get("account")
    cmt.heart(number, account)
    return "1"


if __name__ == '__main__':
    app.run(debug=True, port=10001, host="0.0.0.0")
