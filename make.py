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
from .home import home, homes, breaks
from .shuju import get_data
import re

qq_list = []
bullet_type = ""
tech_center = ""
armor = ""
medicine = ""

def set_make_data(data):
    global qq_list, bullet_type, tech_center, armor, medicine
    qq_list = data.get('qq_list', [])
    bullet_type = data.get('bullet_type', '')
    tech_center = data.get('tech_center', '')
    armor = data.get('armor', '')
    medicine = data.get('medicine', '')

# 登录广告关闭
def starts():
    res = FindImages.find_template(R.img("广告关闭.png"), rect=[1670,0,2400,341])
    if res:
        cx, cy = res["result"] 
        click(cx + random.randint(-33, 33), cy + random.randint(-33, 33))
    else:
        print("无广告")

# 检查是否在空闲中 / 废弃
def frees():
    res = Ocr.mlkitocr_v2(rect=[730,308,1072,490], pattern=r"空闲中")
    if res:
        print("空闲中")
        return True
    else:
        return False

# 滑动子弹索引 / 废弃
def scrolls():
    left, top, right, bottom = 492, 172, 757, 629
    total_height = bottom - top
    slide_ratio = random.uniform(0.5, 0.9)
    slide_distance = int(total_height * slide_ratio)
    y_start_min = top + slide_distance
    y_start = random.randint(y_start_min, bottom)
    y_end = y_start - slide_distance
    x_start = random.randint(left, right)
    x_end = x_start + random.randint(-30, 30)
    x_end = max(left, min(right, x_end))
    action.slide(x_start, y_start, x_end, y_end, dur=random.randint(250, 450))
    time.sleep(random.uniform(0.3, 0.8))

# 制造完成点击（收菜）
def finishs():
    res = Ocr.mlkitocr_v2(pattern=r"奖励")
    if res:
        print("制造完成，收菜")
        time.sleep(random.uniform(0.6, 1.2))
        item = res[0]
        cx, cy = item.center_x, item.center_y
        click(cx + random.randint(-220, 200), cy + random.randint(180, 250))
        time.sleep(random.uniform(0.6, 1.2))
        return True
    else:
        return False

# 查找物品 / 文字识别（用于技术中心，防具台，工作台）
def grepss(b):
    res = Ocr.mlkitocr_v2(rect=[0,0,770,837], pattern=b)
    if res:
        item = res[0]
        cx, cy = item.center_x, item.center_y
        click(cx + random.randint(-150, 150), cy + random.randint(-45, 45))
        time.sleep(random.uniform(0.5, 1))
        print(f"找到物品 {b}")
        return True
    else:
        print(f"未找到物品 {b}")
        return False

# 查找物品 / 图像识别（用于制药台）
def medicines(a):
    res = FindImages.find_template(R.img(f"{a}.png"), confidence=0.7, scale_range=[0.5, 2])
    if res:
        cx, cy = res["result"] 
        click(cx + random.randint(-140, 210), cy + random.randint(-40, 40))
        time.sleep(random.uniform(0.5, 1))
        print(f"点击 {a}")
        return True
    else:
        print(f"点击 {a} 失败")
        return False

# 查看是否在制造
def stops():
    res = Ocr.mlkitocr_v2(rect=[1532,869,2460,1080], pattern=r"中")
    if res:
        time_res = Ocr.mlkitocr_v2(rect=[1674, 495, 2400, 936])
        if time_res:
            text = time_res[0].text
            result = re.search(r"\d{2}:\d{2}:\d{2}", text)
            if result:
                return True, result.group()
        return True, "--"
    else:
        return False, "--"

# 查看剩余制造时间
def times():
    res = Ocr.mlkitocr_v2(rect=[1674, 495, 2400, 936])
    text = res[0].text
    result = re.search(r"\d{2}:\d{2}:\d{2}", text)
    if result:
        time_str = result.group()
        print("提取到的时间：", time_str)

# 查找子弹 / 废弃
def finds(a, b):   
    while True:
        res = Ocr.mlkitocr_v2(rect=[492, 172, 757, 629], pattern=a)
        if res:
            item = res[0]
            cx, cy = item.center_x, item.center_y
            click(cx + random.randint(-103, 103), cy + random.randint(-11, 11))
            time.sleep(random.uniform(0.6, 1))
            time.sleep(random.uniform(0.6, 1))
            findss(b)
            break
        else:
            scrolls()
            time.sleep(random.uniform(0.6, 1))

def findss(b):
    res = Ocr.mlkitocr_v2(rect=[0, 0, 986, 1080], pattern=b)
    if res:
        item = res[0]
        cx, cy = item.center_x, item.center_y
        x = cx + random.randint(-150, 150)
        y = cy + random.randint(-45, 45)
        click(x, y)

# 点击制造按钮 / 一键补齐
def build():
    res = Ocr.mlkitocr_v2(pattern=r"补齐")
    if res:
        item = res[0]
        cx, cy = item.center_x, item.center_y
        click(cx + random.randint(-170, 170), cy + random.randint(-30, 30))
        return True
    else:
        return False

# 点击制造按钮 / 生产
def builds():
    res = Ocr.mlkitocr_v2(rect=[1200, 715, 2460, 1080], pattern=r"生产")
    if res:
        item = res[0]
        cx, cy = item.center_x, item.center_y
        click(cx + random.randint(-170, 170), cy + random.randint(-30, 30))
        return True
    else:
        return False

# 制造按钮 / 生产（检测）
def build_s():
    res = Ocr.mlkitocr_v2(pattern=r"中止")
    if res:
        print("检测到中止按钮")
        return True
    else:
        return False

# 点击补齐的第二个按钮
def buttonss():
    res = FindColors.find("1199,914,#11BB76|1273,914,#11BA75|1358,914,#10BA75", ori=4)
    if res:
        print(res)
        cx = res.x
        cy = res.y
        click(cx + random.randint(-150, 80), cy + random.randint(-60, -15))

# 制造主流程
def wait_for_start():
    time.sleep(random.uniform(2, 3))
    start_time = time.time()
    while time.time() - start_time < 10:
        is_making, _ = stops()
        if is_making:
            print("制造已成功开始")
            return True
        time.sleep(0.5)
    print("等待制造开始超时")
    return False

def makess():
    max_retry = 3
    for attempt in range(max_retry):
        time.sleep(0.5)
        if build():
            print("检测到一键补齐，执行补齐流程")
            for sub_attempt in range(3):
                buttonss()
                time.sleep(random.uniform(1.5, 2.5))
                if builds():
                    print(f"生产按钮出现并已点击（第 {sub_attempt+1} 次）")
                    if wait_for_start():
                        return True
                    else:
                        print("制造未开始，重新尝试补齐")
                        continue
                else:
                    print(f"生产按钮未出现，第 {sub_attempt+1} 次重试 buttonss")
                    continue
            print("补齐流程多次尝试失败")
        else:
            print("可以直接生产")
            if builds():
                print("点击生产")
                if wait_for_start():
                    return True
            else:
                print("生产按钮未找到，可能无法制造")
        print(f"制造失败，第 {attempt+1} 次重试")
    print("制造失败（多次尝试均未开始）")
    return False

# ========== 进入特勤处 ==========
def makes():
    """进入特勤处，带重试"""
    max_retry = 5
    for attempt in range(max_retry):
        ssd()
        time.sleep(random.uniform(1, 2))
        res = Ocr.mlkitocr_v2(rect=[0, 0, 581, 231], pattern=r"处")
        if res:
            print("成功进入特勤处")
            return True
        else:
            print(f"未进入特勤处，第 {attempt+1} 次重试，返回主页")
            homes()
            time.sleep(random.uniform(2, 3))
    print("进入特勤处失败，超过最大重试次数")
    return False

def ssd():
    res = Ocr.mlkitocr_v2(rect=[0, 944, 1312, 1080], pattern=r"[\u4e00-\u9fa5]+处")
    if res:
        item = res[0]
        cx, cy = item.center_x, item.center_y 
        click(cx + random.randint(-50, 50), cy + random.randint(-20, 20))

# ========== 以下四个函数：只点击图标，不验证是否进入 ==========
def workss():
    """只点击工作台图标，返回是否点击成功（不验证进入）"""
    max_retry = 3
    for attempt in range(max_retry):
        res = FindImages.find_template(R.img("工作台.png"), confidence=0.8, scale_range=[0.5, 2])
        if res:
            cx, cy = res["result"]
            click(cx + random.randint(-79, 171), cy + random.randint(115, 234))
            time.sleep(random.uniform(0.6, 1.2))
            print("已点击工作台图标")
            return True
        print(f"点击工作台失败，第 {attempt+1} 次重试")
        time.sleep(random.uniform(1, 2))
    print("点击工作台失败")
    return False

# def check_workbench():
#     """检测是否已进入工作台界面"""
#     return bool(Ocr.mlkitocr_v2(rect=[0, 0, 367, 89], pattern=r"工作台"))

def armors():
    """只点击防具台图标，返回是否点击成功"""
    max_retry = 3
    for attempt in range(max_retry):
        res = FindImages.find_template(R.img("防具台.png"), confidence=0.7, scale_range=[0.5, 2])
        if res:
            cx, cy = res["result"]
            click(cx + random.randint(-100, 180), cy + random.randint(150, 250))
            time.sleep(random.uniform(0.6, 1.2))
            print("已点击防具台图标")
            return True
        print(f"点击防具台失败，第 {attempt+1} 次重试")
        time.sleep(random.uniform(1, 2))
    print("点击防具台失败")
    return False

# def check_armor():
#     """检测是否已进入防具台界面"""
#     return bool(Ocr.mlkitocr_v2(rect=[0, 0, 367, 89], pattern=r"防具台"))

def pharmacys():
    """只点击制药台图标，返回是否点击成功"""
    max_retry = 3
    for attempt in range(max_retry):
        res = FindImages.find_template(R.img("制药台.png"), confidence=0.7, scale_range=[0.5, 2])
        if res:
            cx, cy = res["result"]
            click(cx + random.randint(-94, 180), cy + random.randint(100, 240))
            time.sleep(random.uniform(1.5, 2))
            print("已点击制药台图标")
            return True
        print(f"点击制药台失败，第 {attempt+1} 次重试")
        time.sleep(random.uniform(1, 2))
    print("点击制药台失败")
    return False

# def check_pharmacy():
#     """检测是否已进入制药台界面（使用专用标识图）"""
#     return bool(FindImages.find_template(R.img("制药台识别成功标识.png"), confidence=0.7, scale_range=[0.5, 2]))

def shills():
    """只点击技术中心图标，返回是否点击成功"""
    max_retry = 3
    for attempt in range(max_retry):
        res = FindImages.find_template(R.img("技术中心.png"), confidence=0.7, scale_range=[0.5, 2])
        if res:
            cx, cy = res["result"]
            click(cx + random.randint(-100, 150), cy + random.randint(104, 234))
            time.sleep(random.uniform(0.6, 1.2))
            print("已点击技术中心图标")
            return True
        print(f"点击技术中心失败，第 {attempt+1} 次重试")
        time.sleep(random.uniform(1, 2))
    print("点击技术中心失败")
    return False

def check_tech():
    """检测是否已进入技术中心界面"""
    return bool(Ocr.mlkitocr_v2(rect=[0, 0, 367, 89], pattern=r"中心"))

def facilitys():
    """检测是否已进入制药台/防具台/工作台界面"""
    return bool(Ocr.mlkitocr_v2(rect=[0, 0, 367, 89], pattern=r"台"))
# ========== 其他辅助 ==========
def topss():
    res = FindImages.find_template(R.img("已解锁.png"), rect=[161, 259, 738, 355], confidence=0.7, scale_range=[0.5, 2])
    if res:
        cx, cy = res["result"] 
        click(cx + random.randint(-18, 550), cy + random.randint(45, 140))
        time.sleep(random.uniform(0.5, 1))
        print("点击置顶")
        return True
    else:
        print("点击置顶失败")
        return False

def get_remaining_time():
    try:
        res = Ocr.mlkitocr_v2(rect=[1723, 931, 2400, 1080], pattern=r"中止")
        if res:
            time_res = Ocr.mlkitocr_v2(rect=[1674, 495, 2400, 936])
            if time_res:
                text = time_res[0].text
                result = re.search(r"\d{2}:\d{2}:\d{2}", text)
                if result:
                    return result.group()
        return "--"
    except:
        return "--"