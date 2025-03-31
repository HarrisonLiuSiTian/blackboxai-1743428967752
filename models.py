from pydantic import BaseModel
from typing import List, Optional

class UserCredentials(BaseModel):
    """用户凭证模型"""
    username: str
    password: str

class Token(BaseModel):
    """Token 模型"""
    token: str
    expires: str

class QueryRequest(BaseModel):
    """查询请求模型"""
    query: str

class QueryResponse(BaseModel):
    """查询响应模型"""
    intent: str
    reply: str

class StatsReport(BaseModel):
    """统计报表模型"""
    department: str
    attendance: int
    employee_count: int