import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import re

# 1. 尝试加载本地环境变量
load_dotenv()

# 2. 页面配置
st.set_page_config(page_title="赛创智航 - 双创竞赛 Agent", layout="wide", page_icon="🚀")

# 3. 获取 API Key (优先读取云端 Secrets，本地则读取 .env)
def get_api_key():
    # 尝试读取 Streamlit 云端 Secrets
    if "DEEPSEEK_API_KEY" in st.secrets:
        return st.secrets["DEEPSEEK_API_KEY"]
    # 否则读取本地环境变量
    return os.getenv("DEEPSEEK_API_KEY")

api_key = get_api_key()

if api_key:
    # 初始化 DeepSeek 客户端
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
else:
    st.error("🔑 未找到 API Key。请检查本地 .env 或云端 Secrets 配置。")
    st.stop()

# --- UI 界面 ---
st.title("🚀 赛创智航 (Compete-Pilot)")
st.markdown("### 高校双创竞赛点子孵化与评估专家")

user_input = st.text_area("💡 请详细描述你的参赛项目想法：", height=200, placeholder="例如：我打算做一个基于 RAG 技术的计算机辅助教学工具...")

if st.button("🚀 一键生成评估报告"):
    if user_input:
        with st.spinner("国内 AI 专家正在火速审核中..."):
            try:
                prompt = f"""
                你是一位资深的高校双创竞赛评审专家。请对以下项目进行多维度评估，并给出改进建议。
                项目内容：{user_input}
                
                请在回答的最后，严格按照以下格式输出评分（0-10分）：
                [SCORE]
                创新性: 8
                可行性: 7
                商业价值: 6
                社会意义: 9
                团队要求: 7
                [/SCORE]
                """
                
                # 调用 DeepSeek API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一位专业的双创竞赛评审专家。"},
                        {"role": "user", "content": prompt},
                    ]
                )
                
                full_text = response.choices[0].message.content
                
                # 页面布局
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown("### 📋 详细评估报告")
                    display_text = re.sub(r"\[SCORE\].*?\[/SCORE\]", "", full_text, flags=re.S)
                    st.markdown(display_text)
                
                with col2:
                    score_match = re.search(r"\[SCORE\](.*?)\[/SCORE\]", full_text, re.S)
                    if score_match:
                        st.markdown("### 📊 维度评估图")
                        score_lines = score_match.group(1).strip().split('\n')
                        categories, values = [], []
                        for line in score_lines:
                            if ":" in line:
                                cat, val = line.split(':')
                                categories.append(cat.strip())
                                values.append(float(val.strip()))
                        
                        fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', line_color='#FF4B4B'))
                        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ 运行出错：{e}")
    else:
        st.warning("⚠️ 请先输入想法！")

st.markdown("---")
st.caption("© 2026 赛创智航 - Powered by DeepSeek")
