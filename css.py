# ===== 4. 主循环（每个账号） =====
# for idx, qq in enumerate(qq_list):
#     check_pause()
#     print(f"\n=== 开始处理第 {idx+1}/{len(qq_list)} 个账号：{qq} ===")

#     # time.sleep(random.uniform(15, 20))

#     max_account_retry = 3
#     account_success = False

#     for retry in range(max_account_retry):
#         check_pause()
#         try:
#             # # ---------- 登录 ----------
#             # auto_login(qq)
#             # time.sleep(random.uniform(2, 4))

#             # # ---------- 关闭广告 ----------
#             # starts()
#             # time.sleep(random.uniform(2, 4))

#             # ---------- 进入特勤处（仅一次） ----------
#             if not makes():
#                 raise Exception("进入特勤处失败")

#             # ---------- 按顺序处理每个设施（循环制造模式） ----------
#             for name, item, enter_func, find_func, find_type in facility_order:
#                 check_pause()
#                 print(f"\n--- 开始处理 {name}:{item} ---")

#                 if name not in stats:
#                     stats[name] = []

#                 # ===== 该设施的处理循环（直到无法继续制造） =====
#                 facility_done = False
#                 while not facility_done:
#                     # 重置进入尝试标志
#                     entered = False
#                     max_enter_attempts = 3

#                     # 第一次尝试（不执行 finishs）
#                     for attempt in range(max_enter_attempts):
#                         check_pause()

#                         # 如果是第一次尝试，不执行 finishs；否则先执行 finishs
#                         if attempt > 0:
#                             print(f"第 {attempt+1} 次尝试进入，先执行 finishs() 检测完成界面")
#                             finishs()
#                             time.sleep(random.uniform(3, 4))

#                         # 尝试进入设施
#                         if enter_func():
#                             entered = True
#                             print(f"成功进入 {name}")
#                             break
#                         else:
#                             print(f"第 {attempt+1} 次进入 {name} 失败", end="")
#                             if attempt < max_enter_attempts - 1:
#                                 print(f"，等待 1~2 秒后重试")
#                                 time.sleep(random.uniform(1, 2))
#                             else:
#                                 print(f"，已尝试 {max_enter_attempts} 次，放弃该设施")
#                                 # 记录失败并跳出循环
#                                 stats[name].append({"success": False, "remaining": "--"})
#                                 breaks()
#                                 facility_done = True  # 结束该设施处理
#                                 break

#                     # 如果未进入，则跳过该设施（已记录）
#                     if not entered:
#                         break

#                     # 成功进入设施内部后，执行查找和制造
#                     # 1. 查找物品（最多3次）
#                     found = False
#                     max_find_attempts = 3
#                     for attempt in range(max_find_attempts):
#                         check_pause()
#                         if find_type == "ocr":
#                             success = find_func(item)
#                         else:
#                             success = find_func(item)
#                         if success:
#                             found = True
#                             print(f"第 {attempt+1} 次识别成功，在 {name} 中找到 {item}")
#                             break
#                         else:
#                             print(f"第 {attempt+1} 次识别失败", end="")
#                             if attempt < max_find_attempts - 1:
#                                 print(f"，执行 topss() 置顶")
#                                 topss()
#                                 time.sleep(random.uniform(1, 2))
#                             else:
#                                 print(f"，已尝试 {max_find_attempts} 次，放弃")

#                     if not found:
#                         print(f"{name} 未找到物品，结束该设施")
#                         stats[name].append({"success": False, "remaining": "--"})
#                         breaks()
#                         facility_done = True
#                         continue

#                     # 2. 检查是否正在制造
#                     is_making, remaining = stops()
#                     if is_making:
#                         print(f"{name} 正在制造中，剩余 {remaining}，跳过该设施")
#                         stats[name].append({"success": True, "remaining": remaining})
#                         breaks()
#                         facility_done = True
#                         continue

#                     # 3. 执行制造
#                     make_success = makess()
#                     if make_success:
#                         print(f"{name} 制造成功，准备重新开始该设施（新一轮制造）")
#                         # 获取剩余时间（可能为0）
#                         _, remaining = stops()
#                         # 记录本次制造成功（沿用原记录方式，每次制造都追加）
#                         stats[name].append({"success": True, "remaining": remaining})
#                         # 返回特勤处主界面，以便重新进入设施
#                         breaks()
#                         time.sleep(random.uniform(1, 2))
#                         # 继续 while 循环，重新尝试进入该设施
#                         # 注意：下一次循环的第一次尝试不会执行 finishs（符合需求）
#                         continue
#                     else:
#                         print(f"{name} 制造失败，结束该设施")
#                         stats[name].append({"success": False, "remaining": "--"})
#                         breaks()
#                         facility_done = True
#                         continue

#                 # 该设施处理完毕（无论是正常结束还是跳过），执行一次 breaks 确保返回主界面
#                 # 但内部已经调用过 breaks，此处可省略，但保留安全调用
#                 time.sleep(random.uniform(1, 2))

#             # ---------- 所有设施处理完毕，退出账号 ----------
#             # homes()
#             # ouputss()
#             time.sleep(random.uniform(2, 4))
#             account_success = True
#             print(f"账号 {qq} 处理成功")
#             break

#         except Exception as e:
#             print(f"账号 {qq} 第 {retry+1} 次尝试失败：{e}")
#             try:
#                 homes()
#                 ouputss()
#             except Exception as reset_err:
#                 print(f"重置状态时出错：{reset_err}")
#             time.sleep(random.uniform(5, 10))

#     if not account_success:
#         print(f"账号 {qq} 多次尝试均失败，跳过")

#     time.sleep(random.uniform(5, 10))
