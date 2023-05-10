# coding : utf-8


from encrypt import *
from rich import print as print


def decrypt(ened_files_full_path, aes_key):
    for file in ened_files_full_path:

        tmp_file_path = file + '_decrypted'
        decrypt_file(file, tmp_file_path, aes_key)
        os.remove(file)
        os.rename(tmp_file_path, file)

        
        print("解密完成：" + file)