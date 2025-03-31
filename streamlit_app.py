import streamlit as st
import requests

# 设置 API 地址
API_URL = "http://127.0.0.1:8000"

# 设置页面配置
st.set_page_config(
    page_title="人力资源 AI Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .ai-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# 登录页面
def login():
    st.title("🔐 登录")
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            username = st.text_input("👤 用户名")
            password = st.text_input("🔑 密码", type="password")
            if st.button("登录", key="login_button"):
                try:
                    response = requests.post(
                        f"{API_URL}/login",
                        json={"username": username, "password": password}
                    )
                    if response.status_code == 200:
                        st.session_state.token = response.json()["access_token"]
                        st.session_state.username = username
                        st.success("✅ 登录成功！")
                        st.experimental_rerun()
                    else:
                        st.error("❌ 登录失败，请检查用户名和密码。")
                except Exception as e:
                    st.error(f"❌ 连接服务器失败: {str(e)}")

# 主页面
def main_page():
    st.title("🤖 人力资源 AI Agent")
    
    # 侧边栏
    st.sidebar.title("📋 导航")
    option = st.sidebar.selectbox(
        "选择功能",
        ["💬 智能查询", "📊 历史记录", "📈 统计报表"]
    )

    if option == "💬 智能查询":
        st.subheader("智能查询")
        query = st.text_input("🔍 请输入您的查询", placeholder="例如：查询假期、薪资、考勤等")
        if st.button("发送", key="query_button"):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"query": query},
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                if response.status_code == 200:
                    result = response.json()
                    # 用户问题
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <b>您的问题：</b><br>{query}
                    </div>
                    """, unsafe_allow_html=True)
                    # AI回答
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <b>AI助手回答：</b><br>{result['reply']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ 查询失败，请重试。")
            except Exception as e:
                st.error(f"❌ 连接服务器失败: {str(e)}")

    elif option == "📊 历史记录":
        st.subheader("历史记录")
        try:
            response = requests.get(
                f"{API_URL}/history",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if response.status_code == 200:
                history = response.json()
                for record in history:
                    with st.expander(f"查询时间: {record[4]}", expanded=False):
                        st.markdown(f"""
                        <div class="chat-message user-message">
                            <b>查询内容：</b><br>{record[2]}
                        </div>
                        <div class="chat-message ai-message">
                            <b>AI回复：</b><br>{record[3]}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("❌ 获取历史记录失败。")
        except Exception as e:
            st.error(f"❌ 连接服务器失败: {str(e)}")

    elif option == "📈 统计报表":
        st.subheader("统计报表")
        try:
            response = requests.get(
                f"{API_URL}/stats",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            if response.status_code == 200:
                stats = response.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("考勤率", f"{stats['attendance']}%")
                with col2:
                    st.metric("员工总数", stats['employee_count'])
                
                # 添加图表示例
                st.bar_chart({"考勤率": [stats['attendance']]})
            else:
                st.error("❌ 获取统计报表失败。")
        except Exception as e:
            st.error(f"❌ 连接服务器失败: {str(e)}")

# 启动应用
if "token" not in st.session_state:
    login()
else:
    main_page()