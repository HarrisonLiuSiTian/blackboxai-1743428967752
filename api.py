from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sso_auth import login, get_current_user
from deepseek import process_query
from database import insert_query, get_history
from models import UserCredentials  # 添加此行以导入 UserCredentials

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class QueryRequest(BaseModel):
    query: str

@app.post("/login")
def login_user(credentials: UserCredentials):
    """用户登录接口"""
    return login(credentials)

@app.post("/query")
def query(request: QueryRequest, token: str = Depends(oauth2_scheme)):
    """查询接口"""
    user = get_current_user(token)
    response = process_query(request.query)
    insert_query(user['username'], request.query, response['reply'])
    return response

@app.get("/history")
def history(token: str = Depends(oauth2_scheme)):
    """获取用户查询历史记录"""
    user = get_current_user(token)
    return get_history(user['username'])

@app.get("/stats")
def stats(token: str = Depends(oauth2_scheme)):
    """获取统计报表接口"""
    user = get_current_user(token)
    if user['role'] != 'manager':
        raise HTTPException(status_code=403, detail="无权限访问")
    # 模拟返回统计数据
    return {"attendance": 95, "employee_count": 50}