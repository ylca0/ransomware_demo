# coding : utf-8

import os
import winshell
import sys


def add_to_startup():
    """
    添加可执行文件快捷方式到Windows启动文件夹中
    """

    # 获取程序执行位置
    file_path = os.path.join(os.getcwd(), sys.argv[0])
    startup_folder = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    shortcut_name = os.path.splitext(os.path.basename(file_path))[0] + ".lnk"
    shortcut_path = os.path.join(startup_folder, shortcut_name)

    # 创建快捷方式
    winshell.CreateShortcut(Path=shortcut_path, Target=file_path)
