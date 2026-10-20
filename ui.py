"""
配置界面模块 - 适配新字段
支持子弹型号、技术中心、护甲、药品（下拉选择）
"""
from ascript.android.ui import WebWindow
from ascript.android.system import R
import json
import time
import re

# 允许的药品选项
ALLOWED_MEDICINE = ["红头修", "红甲修", "金头修", "金甲修", "金大药"]

_config_result = {
    'qqList': [],
    'bulletType': '',
    'techCenter': '',
    'armor': '',
    'medicine': ''
}
_window_closed = False
_window = None


def main(html_file='a.html', timeout=300):
    """获取用户配置"""
    global _config_result, _window_closed, _window

    _config_result = {
        'qqList': [],
        'bulletType': '',
        'techCenter': '',
        'armor': '',
        'medicine': ''
    }
    _window_closed = False

    try:
        _window = WebWindow(R.ui(html_file))

        @_window.tunner()
        def config_data(key, data):
            """接收配置数据"""
            global _config_result, _window_closed
            try:
                # data 是 JSON 字符串
                _config_result = json.loads(data)

                # 数据验证
                errors = []

                # 验证QQ号
                qq_list = _config_result.get('qqList', [])
                if not qq_list:
                    errors.append("QQ号列表不能为空")
                else:
                    for qq in qq_list:
                        if not re.match(r'^[1-9]\d{4,10}$', qq):
                            errors.append(f"无效的QQ号: {qq}")

                # 验证子弹型号（可选，有格式要求）
                bullet_type = _config_result.get('bulletType', '')
                if bullet_type and not re.match(r'^[A-Za-z0-9.*×xX\s\-/]{2,20}$', bullet_type):
                    errors.append(f"无效的子弹型号: {bullet_type}")

                # 验证技术中心（可选，仅做长度限制）
                tech_center = _config_result.get('techCenter', '')
                if tech_center and len(tech_center) > 50:
                    errors.append("技术中心长度不能超过50个字符")

                # 验证护甲（可选，仅做长度限制）
                armor = _config_result.get('armor', '')
                if armor and len(armor) > 50:
                    errors.append("护甲长度不能超过50个字符")

                # 验证药品（必须为允许列表中的值）
                medicine = _config_result.get('medicine', '')
                if medicine not in ALLOWED_MEDICINE:
                    errors.append(f"无效的药品选项: {medicine}，可选: {', '.join(ALLOWED_MEDICINE)}")

                # 如果有错误，打印并返回
                if errors:
                    print("=" * 50)
                    print("❌ 数据验证失败:")
                    for err in errors:
                        print(f"  - {err}")
                    print("=" * 50)
                    return {"status": "error", "message": "; ".join(errors)}

                print("=" * 50)
                print("✅ 收到配置:")
                print(f"  👤 账号数量: {len(qq_list)}")
                print(f"  📋 QQ列表: {qq_list}")
                print(f"  🔫 子弹型号: {bullet_type or '未设置'}")
                print(f"  🏢 技术中心: {tech_center or '未设置'}")
                print(f"  🛡️ 护甲: {armor or '未设置'}")
                print(f"  💊 药品: {medicine}")
                print(f"  🕐 时间戳: {_config_result.get('timestamp', '未知')}")
                print("=" * 50)

                # 标记关闭
                _window_closed = True
                try:
                    _window.close()
                except:
                    pass

                return {"status": "success", "message": f"接收成功，共 {len(qq_list)} 个账号"}

            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                return {"status": "error", "message": f"JSON解析失败: {str(e)}"}
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                return {"status": "error", "message": str(e)}

        # 显示窗口
        _window.show()
        print("🚀 配置界面已打开")
        print("💡 请填写信息后点击保存")
        print("📝 药品选项: " + ", ".join(ALLOWED_MEDICINE))

        # 等待
        start_time = time.time()
        while not _window_closed and (time.time() - start_time) < timeout:
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            if elapsed % 10 == 0 and elapsed > 0:
                print(f"⏳ 等待中... {elapsed}秒")

        if _window_closed:
            print("✅ 配置已接收")
        else:
            print("⏰ 超时")
            try:
                _window.close()
            except:
                pass

    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

    return _config_result


# 以下为便捷获取函数（根据新字段调整）
def get_qq_list():
    return _config_result.get('qqList', [])


def get_bullet_type():
    return _config_result.get('bulletType', '')


def get_tech_center():
    return _config_result.get('techCenter', '')


def get_armor():
    return _config_result.get('armor', '')


def get_medicine():
    return _config_result.get('medicine', '')


def get_config():
    """获取完整配置字典"""
    return _config_result


if __name__ == '__main__':
    config = main()
    print("\n" + "=" * 50)
    print("📋 最终配置结果:")
    print(f"  QQ列表: {config.get('qqList', [])}")
    print(f"  子弹型号: {config.get('bulletType', '未设置')}")
    print(f"  技术中心: {config.get('techCenter', '未设置')}")
    print(f"  护甲: {config.get('armor', '未设置')}")
    print(f"  药品: {config.get('medicine', '未设置')}")
    print(f"  账号数量: {len(config.get('qqList', []))}")
    print(f"  时间戳: {config.get('timestamp', '未知')}")
    print("=" * 50)