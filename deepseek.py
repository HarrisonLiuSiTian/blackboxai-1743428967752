def process_query(query: str):
    """处理用户查询并返回意图和回复"""
    # 模拟意图判断
    if "假期" in query:
        return {"intent": "假期查询", "reply": "您的剩余假期为10天。"}
    elif "薪资" in query:
        return {"intent": "薪资查询", "reply": "您的薪资为8000元。"}
    elif "代办" in query:
        return {"intent": "代办查询", "reply": "您有3个待办事项。"}
    elif "个人信息" in query:
        return {"intent": "个人信息查询", "reply": "您的个人信息已更新。"}
    elif "统计" in query:
        return {"intent": "统计查询", "reply": "部门考勤统计已生成。"}
    else:
        return {"intent": "未知查询", "reply": "抱歉，我无法理解您的请求。"}