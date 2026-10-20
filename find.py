from ascript.android.action import click, slide
from ascript.android.node import Selector
from android.view.animation import AccelerateDecelerateInterpolator
import time
import random

# 封装随机偏移函数
def get_offset(count: int, low=-100, high=100):
    return [random.randint(low, high) for _ in range(count)]

def find_game():
    # 查找目标控件
    node = Selector(0).text("三角洲行动").find()
    if not node:
        print("未找到控件")
        return

    x, y = node.center_x, node.center_y
    print(f"初始坐标：{x}, {y}")

    # 向左滑：控件在屏幕外左侧
    if x < 0:
        max_step = min((-x // 540) + 1, 10)
        for _ in range(max_step):
            # 每一轮滑动都重新生成随机偏移
            slide_offset = get_offset(4, -100, 100)
            slide(
                157 + slide_offset[0],
                779 + slide_offset[1],
                930 + slide_offset[2],
                814 + slide_offset[3],
                500,
                AccelerateDecelerateInterpolator(),
                control_points=0
            )
            time.sleep(1)

    # 向右滑：控件在屏幕外右侧
    elif x > 0:
        max_step = min((x // 1080), 10)
        for _ in range(max_step):
            # 每一轮滑动都重新生成随机偏移
            slide_offset = get_offset(4, -100, 100)
            slide(
                930 + slide_offset[0],
                779 + slide_offset[1],
                157 + slide_offset[2],
                814 + slide_offset[3],
                500,
                AccelerateDecelerateInterpolator(),
                control_points=0
            )
            time.sleep(1)

    # 等待页面稳定，重新获取控件
    time.sleep(0.5)
    target_node = Selector(0).clickable(True).text("三角洲行动").find()
    if not target_node:
        print("滑动后仍未找到控件")
        return

    x1, y1 = target_node.center_x, target_node.center_y
    print(f"图标中心点：{x1}, {y1}")

    # 点击随机偏移（每次执行都不一样）
    click_offset = get_offset(2, -80, 80)
    final_x = x1 + click_offset[0]
    final_y = y1 + click_offset[1]
    print(f"实际点击坐标：{final_x}, {final_y}")
    click(final_x, final_y)

if __name__ == "__main__":
    find_game()