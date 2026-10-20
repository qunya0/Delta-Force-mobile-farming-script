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
from .home import home,homes,breaks


def breakss():
    res = FindImages.find_template(R.img("设置.png"), rect=[1812,0,2400,284])
    if res :
        cx, cy = map(int, res["result"])
        click(cx + random.randint(-25, 25), cy + random.randint(-35, 35))
        time.sleep(random.uniform(0.6, 1))
    
def breaksss():
    res = Ocr.mlkitocr_v2(rect=[1830,890,2400,1080], pattern=r"退出登录")
    if  res:
        item = res[0]
        cx = item.center_x
        cy = item.center_y
        click(cx + random.randint(-127, 127), cy + random.randint(-27, 27))
        time.sleep(random.uniform(0.6, 1))



def out():
    res = Ocr.mlkitocr_v2(rect=[1096,604,1971,1080], pattern=r"确认")
    if res:
        item = res[0]
        cx = item.center_x
        cy = item.center_y
        click(cx + random.randint(-207, 207), cy + random.randint(-36, 36))


def ouputss():
    """退出登录流程，带重试"""
    max_retry = 3
    for attempt in range(max_retry):
        breakss()   # 点击设置
        time.sleep(random.uniform(2,3))
        breaksss()  # 点击退出登录
        time.sleep(random.uniform(2.5,3))
        out()       # 确认
        # 验证是否已退出（可检测“登录”按钮出现）
        time.sleep(random.uniform(2,3))
        # 简单检测：如果主页出现，则认为退出成功（由调用者判断）
        break