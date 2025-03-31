import sqlite3
from config import DB_PATH

def init_db():
    """初始化数据库及表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query_text TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_query(user_id, query, response):
    """插入查询记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO queries (user_id, query_text, response)
        VALUES (?, ?, ?)
    ''', (user_id, query, response))
    conn.commit()
    conn.close()

def get_history(user_id):
    """获取用户的查询历史记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM queries
        WHERE user_id = ? AND created_at >= datetime('now', '-7 days')
    ''', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

# 初始化数据库
init_db()