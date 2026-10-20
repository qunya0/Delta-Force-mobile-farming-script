from .ui import main

qq_list = []
bullet_type = ""
tech_center = ""
armor = ""
medicine = ""
_run_flag = False


def shuju():
    """获取配置数据（仅执行一次）"""
    global qq_list, bullet_type, tech_center, armor, medicine, _run_flag
    if _run_flag:
        return
    cfg = main()
    qq_list = cfg.get("qqList", [])
    bullet_type = cfg.get("bulletType", "")
    tech_center = cfg.get("techCenter", "")
    armor = cfg.get("armor", "")
    medicine = cfg.get("medicine", "")
    _run_flag = True


def get_data():
    """返回所有配置数据（字典形式）"""
    return {
        "qq_list": qq_list,
        "bullet_type": bullet_type,
        "tech_center": tech_center,
        "armor": armor,
        "medicine": medicine
    }

