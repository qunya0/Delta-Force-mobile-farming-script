from ascript.android.screen.color_tools import ana_colors_r
# 导入动作库常用函数
from ascript.android.action import click, slide, Touch, gesture
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
from ascript.android.screen import capture, FindColors, FindImages, Ocr



#检测是否在游戏内/主界面特征图片查找，区别于homes/homess多点找色：
def home_logins():
    res = FindImages.find_template(R.img("设置.png"), rect=[1812,0,2400,284])
    if res :
        print("是在游戏主页面启动，将退出至登录界面")
        return True

# ===================== 真人时间配置项（防检测优化版） =====================
# 页面扫描间隔：拉长基础间隔+加大波动，避免高频机械轮询
WAIT_SCAN_MIN = 0.9
WAIT_SCAN_MAX = 2.2
# 点击前思考停顿
WAIT_BEFORE_CLICK_MIN = 0.3
WAIT_BEFORE_CLICK_MAX = 0.9
# 点击后短加载等待
WAIT_AFTER_CLICK_SHORT_MIN = 0.8
WAIT_AFTER_CLICK_SHORT_MAX = 1.8
# 点击后长页面跳转等待
WAIT_AFTER_CLICK_LONG_MIN = 1.8
WAIT_AFTER_CLICK_LONG_MAX = 3.0
# 小概率网络卡顿延长时长
STALL_CHANCE = 0.08
STALL_MIN = 2.5
STALL_MAX = 4.5
# 小概率本轮跳过检测（模拟人走神/没看屏幕），打破严格循环周期
SKIP_DETECT_CHANCE = 0.12

# ===================== 公共工具函数 =====================
def human_sleep(min_sec, max_sec):
    """正态分布真人休眠 + 小概率网络卡顿"""
    mu = (min_sec + max_sec) / 2
    sigma = (max_sec - min_sec) / 4
    t = random.normalvariate(mu, sigma)
    t = max(min_sec, min(t, max_sec))
    # 8%概率触发网络卡顿
    if random.random() < STALL_CHANCE:
        t = random.uniform(STALL_MIN, STALL_MAX)
    time.sleep(t)

def human_click(x1, y1, x2, y2):
    """带微小坐标抖动的真人点击"""
    base_x = random.randint(x1, x2)
    base_y = random.randint(y1, y2)
    offset_x = random.randint(-4, 4)
    offset_y = random.randint(-4, 4)
    click(base_x + offset_x, base_y + offset_y)

def check_login_success():
    """公共：检测登录成功色点标志，抽离复用避免重复代码"""
    res = Ocr.mlkitocr_v2(rect=[1793,948,2239,1030], pattern=r"开始游戏")
    # 无匹配时返回无效坐标，用于上层判断
    if not res:
        return -1, -1
    item = res[0]
    return item.center_x, item.center_y

def try_skip_login():
    """入口预检测：检查是否已经处于登录成功状态，是则直接跳过整个登录流程"""
    print("--- 预检测：检查是否已登录 ---")
    human_sleep(WAIT_SCAN_MIN, WAIT_SCAN_MAX)
    cx, cy = check_login_success()
    if cx > 0 and cy > 0:
        print("检测到已登录状态，点击继续，跳过登录流程")
        human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
        click(cx + random.randint(-181, 181), cy + random.randint(-30, 30))
        return True
    print("未检测到已登录状态，进入完整登录流程")
    return False

#检测到没勾选用户协议
def rootss():
    res = FindImages.find_template(R.img("用户协议_no.png"), rect=[0,652,2460,1080], confidence=0.7)
    if res:
        cx, cy = res["result"] 
        click(cx + random.randint(-20,20), cy + random.randint(-20,20)) 



# ===================== 登录流程函数 =====================
def login():
    """
    处理用户协议 + QQ登录选择
    返回值说明：
    - "qq_clicked" : 已点击QQ登录按钮，需继续执行login_s授权
    - "auto_done"  : 检测到自动登录成功，无需执行后续步骤
    - False        : 登录超时失败
    说明：验证用户协议.png 为已勾选状态的图标
    """
    
    # ========== 阶段1：专门处理用户协议（6次尝试，每3次检测自动登录） ==========
    print("--- 阶段1:检查用户协议 ---")
    for i in range(6):  # 最多6次勾选尝试
        human_sleep(WAIT_SCAN_MIN, WAIT_SCAN_MAX)
        res = FindImages.find_template(R.img("验证用户协议.png"), rect=[0,737,2121,1080], confidence=0.8)
        if res:
            # 找到勾选图标 = 已勾选，直接进入下一阶段
            print("用户协议已勾选，进入下一阶段")
            break
        else:
            # 没找到勾选图标 = 未勾选，执行点击
            print(f"勾选用户协议（第{i+1}次尝试）")
            human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
            rootss()
            human_sleep(WAIT_AFTER_CLICK_SHORT_MIN, WAIT_AFTER_CLICK_SHORT_MAX)

        # 每3次循环，验证一次是否已自动登录
        if (i + 1) % 3 == 0:
            print(f"  第{i+1}次协议循环，例行检测自动登录状态")
            cx, cy = check_login_success()
            if cx > 0 and cy > 0:
                print("检测到已登录状态，点击继续，跳过登录流程")
                human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
                click(cx + random.randint(-181, 181), cy + random.randint(-30, 30))
                return "auto_done"
    else:
        print("警告：多次尝试后仍未检测到协议已勾选")

    # ========== 阶段2：等待QQ登录 + 每5次检测自动登录 ==========
    print("--- 阶段2：等待QQ登录按钮出现 ---")
    for i in range(15):
        human_sleep(WAIT_SCAN_MIN, WAIT_SCAN_MAX)
        
        # 小概率跳过本轮检测，模拟人走神/视线离开屏幕，打破严格周期性
        if random.random() < SKIP_DETECT_CHANCE:
            print(f"  等待页面加载中...({i+1}/15)")
            continue

        # 1. 优先检测QQ登录按钮（核心目标，每轮必查）
        qq_login = FindImages.find_template(R.img("qq_login.png"), rect=[0,647,2304,1080], confidence=0.7)
        if qq_login:
            print(f"找到QQ登录按钮(第{i+1}次检测)，点击...")
            human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
            cx, cy = qq_login["result"] 
            click(cx + random.randint(-150, 150), cy + random.randint(-25, 25))
            human_sleep(WAIT_AFTER_CLICK_LONG_MIN, WAIT_AFTER_CLICK_LONG_MAX)
            return "qq_clicked"

        # 2. 兜底：隔一轮检测一次协议状态，减少高频识图调用
        if i % 2 == 0:
            protocol_checked = FindImages.find_template(R.img("验证用户协议.png"), rect=[0,647,2304,1080], confidence=0.7)
            if not protocol_checked:
                print("  检测到协议未勾选，重新勾选...")
                human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
                rootss()
                human_sleep(WAIT_AFTER_CLICK_SHORT_MIN, WAIT_AFTER_CLICK_SHORT_MAX)
            else:
                print(f"  等待QQ登录中...({i+1}/15)")
        else:
            print(f"  等待QQ登录中...({i+1}/15)")

        # 3. 每5次循环，验证一次是否已自动登录
        if (i + 1) % 5 == 0:
            print(f"  第{i+1}次循环，例行检测自动登录状态")
            cx, cy = check_login_success()
            if cx > 0 and cy > 0:
                print("检测到已登录状态，点击继续，跳过登录流程")
                human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
                click(cx + random.randint(-181, 181), cy + random.randint(-30, 30))
                return "auto_done"

    print("login() 超时：未找到QQ登录按钮")
    return False


def login_s():
    """
    处理添加账号 + QQ授权 + 登录成功确认
    循环执行直到完成
    """
    max_attempts = 15

    for i in range(max_attempts):
        print(f"login_s 第{i+1}次检测...")
        human_sleep(WAIT_SCAN_MIN, WAIT_SCAN_MAX)

        # 小概率跳过本轮检测
        if random.random() < SKIP_DETECT_CHANCE:
            print(f"  等待授权页面响应...({i+1}/{max_attempts})")
            continue

        # 步骤1：检测登录同意/需要检测2次
        res = Ocr.mlkitocr_v2(rect=[0,1319,1080,2340], pattern=r"同意")
        if res:
            print("找到同意按钮，点击...")
            human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
            item = res[0]
            cx = item.center_x
            cy = item.center_y
            click(cx + random.randint(-200, 200), cy + random.randint(-50, 50))
            human_sleep(WAIT_AFTER_CLICK_SHORT_MIN, WAIT_AFTER_CLICK_SHORT_MAX)
            continue

        # # 步骤2：检测QQ授权同意/废弃
        # res = Ocr.mlkitocr_v2(rect=[0,1319,1080,2340], pattern=r"同意")
        # if res:
        #     print("找到QQ同意按钮，点击...")
        #     human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
        #     item = res[0]
        #     cx = item.center_x
        #     cy = item.center_y
        #     click(cx + random.randint(-210, 210), cy + random.randint(-41, 41))
        #     human_sleep(WAIT_AFTER_CLICK_SHORT_MIN, WAIT_AFTER_CLICK_SHORT_MAX)
        #     continue

        # 步骤3：检测登录成功标志
        cx, cy = check_login_success()
        if cx > 0 and cy > 0:
            print("检测到已登录状态，点击继续，跳过登录流程")
            human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
            click(cx + random.randint(-181, 181), cy + random.randint(-30, 30))
            print("login_s 完成！")
            return True

        print(f"未检测到任何特征，等待重试...")

    print("login_s() 超时：登录未完成")
    return False


#选择切换qq账号
def change_qqs():
    res = Ocr.mlkitocr_v2(pattern=r"账号")
    if res:
        human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
        item = res[0]
        cx = item.center_x
        cy = item.center_y
        click( cx + random.randint(-72, 72),  cy + random.randint(-16, 16))
    else:
        print("切换账号异常")

#选择qq号
def change_qqss(b):
    res = Ocr.mlkitocr_v2(rect=[0,702,1080,2400], pattern=b)
    if res:
        item = res[0]
        cx = item.center_x
        cy = item.center_y
        print(cx,cy)
        x = cx + random.randint(-243, 579)
        y = cy + random.randint(-90, 28)
        human_sleep(WAIT_BEFORE_CLICK_MIN, WAIT_BEFORE_CLICK_MAX)
        click(x, y)
        print(x,y)







def auto_login(b):
    """总入口：按状态分支执行，自动登录成功则跳过授权"""
    print("=== 开始自动登录 ===")
    
    # 第一步：入口预检测，已登录直接结束
    if try_skip_login():
        print("=== 已登录，流程提前结束 ===")
        return

    # 第二步：执行协议+QQ登录阶段，根据返回值分支
    login_result = login()
    if not login_result:
        print("第一阶段登录失败，终止流程")
        return
    elif login_result == "auto_done":
        print("=== 自动登录成功，跳过授权步骤，流程结束 ===")
        return
    else:
        time.sleep(random.uniform(4,5))
        change_qqs()
        time.sleep(random.uniform(2,3))
        print("切换账号")
        change_qqss(b)
        # 只有点击了QQ登录按钮，才走授权流程
        time.sleep(random.uniform(2,3))
        login_s()
        print("=== 登录流程结束 ===")


if __name__ == "__main__":
    auto_login()