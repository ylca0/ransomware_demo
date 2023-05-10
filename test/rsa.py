# import uuid
# import requests

# # 生成唯一uuid
# uid = uuid.uuid4()
# aes_key_encrypted_int = int(requests.post('http://127.0.0.1:5000/getKey', data={'uuid': uid}).text)

# print(aes_key_encrypted_int)


from Crypto.Cipher import AES

# 定义加密密钥和初始化向量
# key = b'16-byte-key-1234'
iv = b'16-byte-iv-56789'

# 加密函数
def encrypt_file(input_file_path, output_file_path, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(input_file_path, 'rb') as input_file:
        with open(output_file_path, 'wb') as output_file:
            # 写入IV（初始化向量）
            output_file.write(iv)
            # 加密文件内容
            while True:
                chunk = input_file.read(16 * 1024)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    # 如果数据块不是16的倍数，则填充0x00
                    chunk += b' ' * (16 - len(chunk) % 16)
                output_file.write(cipher.encrypt(chunk))

# 解密函数
def decrypt_file(input_file_path, output_file_path, key):
    with open(input_file_path, 'rb') as input_file:
        # 读取IV
        iv = input_file.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(output_file_path, 'wb') as output_file:
            # 解密文件内容
            while True:
                chunk = input_file.read(16 * 1024)
                if len(chunk) == 0:
                    break
                output_file.write(cipher.decrypt(chunk))

# 测试代码
input_file_path = 'm.txt'
encrypted_file_path = 'c.bin'
decrypted_file_path = 'mm.txt'

# 加密文件
key = b'16-byte-key-1234'
encrypt_file(input_file_path, encrypted_file_path, key)

# 解密文件
decrypt_file(encrypted_file_path, decrypted_file_path, key)
