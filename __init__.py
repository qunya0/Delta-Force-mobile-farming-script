# __init__.py
from .find import find_game
from .login import auto_login, check_login_success, home_logins
from .make import (
    starts, workss, finishs, grepss, makess, stops, makes,
    shills, pharmacys, armors, medicines, set_make_data,
    topss,
    facilitys, check_tech
)
from .breaks import ouputss
from .shuju import shuju, get_data
from .home import homes, breaks
import time
import random
from ascript.android.ui import Loger, FloatWindow, WebWindow
from ascript.android.system import R
import json
import os
from airscript.ui.dialog import loger


# ===== 暂停控制 =====
pause_flag = False

def toggle_pause():
    global pause_flag
    pause_flag = not pause_flag
    status = "暂停" if pause_flag else "继续"
    print(f"⏸️ 脚本已{status}")

def check_pause():
    """在关键位置调用，检查是否需要暂停"""
    global pause_flag
    while pause_flag:
        time.sleep(0.2)

# ===== 统计变量 =====
stats = {}

# ===== 显示统计页面 =====
def show_result_page():
    try:
        template_path = R.ui("b.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        json_str = json.dumps(stats, ensure_ascii=False)
        new_content = html_content.replace("var injectedData = null;", f"var injectedData = {json_str};")
        output_path = R.ui("b_result.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"📊 统计文件已生成: {output_path}")
        win = WebWindow(output_path)
        win.show()
    except Exception as e:
        print(f"生成统计页面失败: {e}")

# ===== 添加悬浮窗按钮 =====
try:
    FloatWindow.add_menu(
        "pause_btn",
        R.img("pause.png"),
        toggle_pause
    )
    print("✅ 悬浮窗暂停按钮已添加")
except Exception as e:
    print(f"⚠️ 添加悬浮窗按钮失败: {e}")

# ===== 1. 获取配置数据 =====
shuju()
data = get_data()
qq_list = data['qq_list']
bullet_type = data['bullet_type']
tech_center = data['tech_center']
armor = data['armor']
medicine = data['medicine']

set_make_data(data)

from ascript.android.ui import Loger
from ascript.android.system import R
from airscript.ui.dialog import loger
import time

def tunner(k, v):
    print(k, v)

screen_width = 1080
screen_height = 2400
window_width = 300
window_height = 400
pos_x = screen_width - window_width
pos_y = (screen_height - window_height) // 2

loger = Loger()
loger.show()
time.sleep(0.5)

try:
    win_w = loger.getWidth()
    win_h = loger.getHeight()
except:
    win_w, win_h = 300, 400
if win_w == 0: win_w = 300
if win_h == 0: win_h = 400

screen_w, screen_h = 1080, 2400
pos_x = screen_w - win_w - 10
pos_y = (screen_h - win_h) // 2

loger.gravity(0)
loger.x(pos_x)
loger.y(0)

print("✅ 默认日志窗口已启动并右侧居中")

#===== 2. 启动或进入游戏 =====
if home_logins():
    print("在游戏内启动，直接进入主页")
    homes()
    homes()
    ouputss()
else:
    find_game()

#===== 3. 定义设施处理顺序 =====
facility_order = []
if tech_center:
    facility_order.append(("技术中心", tech_center, shills, check_tech, grepss, "ocr"))
if bullet_type:
    facility_order.append(("工作台", bullet_type, workss, facilitys, grepss, "ocr"))
if medicine:
    facility_order.append(("制药台", medicine, pharmacys, facilitys, medicines, "image"))
if armor:
    facility_order.append(("防具台", armor, armors, facilitys, grepss, "ocr"))


# ===== 4. 主循环（每个账号） =====
for idx, qq in enumerate(qq_list):
    check_pause()
    print(f"\n=== 开始处理第 {idx+1}/{len(qq_list)} 个账号：{qq} ===")
    time.sleep(random.uniform(15, 20))
    
    stats[qq] = {}

    max_account_retry = 3
    account_success = False

    for retry in range(max_account_retry):
        check_pause()
        try:
            # ---------- 登录 ----------
            auto_login(qq)
            time.sleep(random.uniform(2, 4))

            # ---------- 关闭广告 ----------
            starts()
            time.sleep(random.uniform(2, 4))

            # ---------- 进入特勤处 ----------
            if not makes():
                raise Exception("进入特勤处失败")

            # ---------- 按顺序处理每个设施 ----------
            for name, item, click_func, check_func, find_func, find_type in facility_order:
                check_pause()
                print(f"\n--- 开始处理 {name}:{item} ---")

                has_success = False
                making_detected = False
                fail_reason = None
                facility_done = False

                while not facility_done:
                    entered = False
                    max_enter_attempts = 3

                    for attempt in range(max_enter_attempts):
                        check_pause()

                        # ① 点击图标
                        click_success = click_func()
                        if click_success:
                            # ② 点击后立即检测收菜（优先清除弹窗）
                            if finishs():
                                print("点击后检测到收菜弹窗，已收菜，等待界面返回")
                                time.sleep(random.uniform(1, 2))
                                # 收菜后再次点击（因为可能退出了设施界面）
                                click_func()
                                time.sleep(random.uniform(0.5, 1))
                            
                            # ③ 检测是否进入界面
                            if check_func():
                                entered = True
                                print(f"成功进入 {name}")
                                break
                            else:
                                print(f"点击后未检测到 {name} 界面")
                                # ④ 二次收菜兜底
                                if finishs():
                                    print("二次收菜后重新尝试进入")
                                    if click_func() and check_func():
                                        entered = True
                                        print(f"收菜后成功进入 {name}")
                                        break
                                    else:
                                        print("收菜后仍无法进入")
                                else:
                                    print("无收菜弹窗")
                        else:
                            # 点击图标失败，尝试收菜后重试
                            print(f"点击 {name} 图标失败，尝试收菜")
                            if finishs():
                                print("收菜完成，重新尝试点击")
                                if click_func() and check_func():
                                    entered = True
                                    print(f"收菜后成功进入 {name}")
                                    break
                                else:
                                    print("收菜后仍无法进入")
                            else:
                                print("无收菜")

                        # 若未进入，且还有重试机会，等待后重试
                        if attempt < max_enter_attempts - 1:
                            print(f"等待 1~2 秒后重试")
                            time.sleep(random.uniform(1, 2))
                        else:
                            print(f"已尝试 {max_enter_attempts} 次，放弃该设施")
                            fail_reason = "enter_fail"
                            breaks()
                            facility_done = True
                            break

                    if not entered:
                        break

                    # ---------- 进入成功后，查找物品（优先收菜） ----------
                    found = False
                    max_find_attempts = 3
                    attempt = 0
                    while attempt < max_find_attempts:
                        check_pause()
                        if find_type == "ocr":
                            success = find_func(item)
                        else:
                            success = find_func(item)

                        if success:
                            found = True
                            print(f"第 {attempt+1} 次识别成功，在 {name} 中找到 {item}")
                            break
                        else:
                            print(f"第 {attempt+1} 次识别失败", end="")
                            # 优先尝试收菜，清除“奖励”弹窗
                            if finishs():
                                print("，检测到收菜弹窗，已收菜，重新尝试查找")
                                time.sleep(random.uniform(1, 2))
                                attempt += 1
                                continue
                            else:
                                if attempt < max_find_attempts - 1:
                                    print(f"，执行 topss() 置顶")
                                    topss()
                                    time.sleep(random.uniform(1, 2))
                                else:
                                    print(f"，已尝试 {max_find_attempts} 次，放弃")
                        attempt += 1

                    if not found:
                        print(f"{name} 未找到物品，结束该设施")
                        fail_reason = "not_found"
                        breaks()
                        facility_done = True
                        continue

                    # ---------- 检查是否正在制造 ----------
                    is_making, remaining = stops()
                    if is_making:
                        if has_success:
                            # 第二次进入，确认制造已成功开始
                            print(f"{name} 制造已成功（剩余 {remaining}）")
                            breaks()
                            facility_done = True
                            continue
                        else:
                            # 第一次进入，发现已在制造中
                            print(f"{name} 当前正在制造中（剩余 {remaining}），标记为制造中")
                            making_detected = True
                            breaks()
                            facility_done = True
                            continue

                    # ---------- 执行制造 ----------
                    make_success = makess()
                    if make_success:
                        print(f"{name} 制造成功")
                        has_success = True
                        _, remaining = stops()
                        breaks()
                        time.sleep(random.uniform(1, 2))
                        continue
                    else:
                        print(f"{name} 制造失败，结束该设施")
                        fail_reason = "make_fail"
                        breaks()
                        facility_done = True
                        continue

                # ---------- 记录最终状态 ----------
                if has_success:
                    stats[qq][name] = "success"
                    print(f"{name} 最终状态：成功")
                elif making_detected:
                    stats[qq][name] = "making"
                    print(f"{name} 最终状态：制造中")
                else:
                    if fail_reason is None:
                        fail_reason = "other_error"
                    stats[qq][name] = fail_reason
                    print(f"{name} 最终状态：{fail_reason}")

                time.sleep(random.uniform(1, 2))

            # ---------- 所有设施处理完毕，退出账号 ----------
            homes()
            ouputss()
            time.sleep(random.uniform(2, 4))
            account_success = True
            print(f"账号 {qq} 处理成功")
            break

        except Exception as e:
            print(f"账号 {qq} 第 {retry+1} 次尝试失败：{e}")
            # 异常时，标记当前尚未成功或制造中的设施为 other_error
            for name, _, _, _, _, _ in facility_order:
                if name not in stats[qq] or stats[qq][name] not in ["success", "making"]:
                    stats[qq][name] = "other_error"
            try:
                homes()
                ouputss()
            except Exception as reset_err:
                print(f"重置状态时出错：{reset_err}")
            time.sleep(random.uniform(5, 10))

    if not account_success:
        print(f"账号 {qq} 多次尝试均失败，跳过")

    time.sleep(random.uniform(5, 10))


print("所有账号处理完成")

# ===== 5. 显示统计页面 =====
show_result_page()
print("✅ 统计窗口已打开，请查看结果。脚本保持运行中，请手动停止。")
while True:
    time.sleep(1)