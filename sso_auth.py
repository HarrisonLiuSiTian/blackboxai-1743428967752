from fastapi import HTTPException, status
from models import UserCredentials
from datetime import datetime, timedelta
from typing import Optional
import jwt

# 模拟用户数据
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "普通员工",
        "hashed_password": "fakehashedpassword1",
        "role": "employee"
    },
    "manager1": {
        "username": "manager1",
        "full_name": "部门经理",
        "hashed_password": "fakehashedpassword2",
        "role": "manager"
    },
    "ceo": {
        "username": "ceo",
        "full_name": "CEO",
        "hashed_password": "fakehashedpassword3",
        "role": "ceo"
    }
}

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(credentials: UserCredentials):
    """用户登录"""
    user = fake_users_db.get(credentials.username)
    if not user or user['hashed_password'] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username'], "role": user['role']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str):
    """获取当前用户信息"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return fake_users_db.get(username)
    except jwt.PyJWTError:
        raise credentials_exception