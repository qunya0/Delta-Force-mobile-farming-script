# 导入动作库常用函数
from ascript.android.action import click, slide, Touch, gesture
from ascript.android import action
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device
import time
import random


# 检测是否在初始界面
def home():
    res = FindColors.find("2091,1021,#17BD75|2094,913,#14CA7A|2268,961,#0E8853|1905,972,#16D180", ori=5)
    if res:
        print("在初始界面/home")
        return True
    else:
        print("不在初始页面执行返回/home")
        return False


# 返回按钮
def breaks():
    res = FindImages.find_template(R.img("返回.png"), rect=[0,0,672,262])
    if res:  # 增加空值判断，避免找不到图片崩溃
        cx, cy = res["result"] 
        click(cx + random.randint(-19, 19), cy + random.randint(-22, 22))
    else:
        print("未找到返回按钮")


#异常返回主界面
def homes():
    max_retry = 3
    for attempt in range(max_retry):
        if home():
            print("已在主页")
            return True
        breaks()
        time.sleep(random.uniform(1, 2))
    print("无法返回主页")
    return False