import streamlit as st
from google import genai
import os
import plotly.graph_objects as go
import re

# --- 1. 页面配置 ---
st.set_page_config(page_title="赛创智航 - 双创竞赛 Agent", layout="wide", page_icon="🚀")

# --- 2. API 密钥配置 (适配 2026 最新官方库) ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    # 使用最新的 Client 初始化方式
    client = genai.Client(api_key=api_key)
else:
    st.error("🔑 未在 Secrets 中找到 GEMINI_API_KEY，请检查配置。")
    st.stop()

# --- 3. UI 界面设计 ---
st.title("🚀 赛创智航 (Compete-Pilot)")
st.markdown("### 高校双创竞赛点子孵化与评估专家")

with st.expander("📌 使用指南", expanded=False):
    st.write("输入你的参赛点子（如：项目背景、核心功能、创新点），AI 将作为专家为你提供评估报告和维度雷达图。")

# 输入框
user_input = st.text_area("💡 请详细描述你的参赛项目想法：", height=200, placeholder="例如：我打算做一个基于 RAG 技术的计算机辅助教学工具...")

# --- 4. 核心逻辑 ---
if st.button("🚀 一键生成评估报告"):
    if user_input:
        with st.spinner("AI 评委正在认真审核中，请稍候..."):
            # 构造专业 Prompt
            prompt = f"""
            你是一位资深的高校双创竞赛评审专家（互联网+、挑战杯）。
            请对以下项目进行多维度评估，给出专业、客观的改进建议。
            
            项目描述：{user_input}
            
            请在回答的【最后】，严格按照以下 TOML 格式输出评分（0-10分）：
            [SCORE]
            创新性: 8
            可行性: 7
            商业价值: 6
            社会意义: 9
            团队要求: 7
            [/SCORE]
            """
            
            try:
                # 使用最新的生成调用方式
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                full_text = response.text
                
                # 提取评分数据
                score_match = re.search(r"\[SCORE\](.*?)\[/SCORE\]", full_text, re.S)
                
                # 页面布局：左侧报告，右侧雷达图
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("### 📋 详细评估报告")
                    # 去掉评分标记后显示正文
                    display_text = re.sub(r"\[SCORE\].*?\[/SCORE\]", "", full_text, flags=re.S)
                    st.markdown(display_text)
                
                with col2:
                    if score_match:
                        st.markdown("### 📊 维度评估图")
                        score_lines = score_match.group(1).strip().split('\n')
                        categories = []
                        values = []
                        for line in score_lines:
                            if ":" in line:
                                cat, val = line.split(':')
                                categories.append(cat.strip())
                                values.append(float(val.strip()))
                        
                        # 画雷达图 (Plotly)
                        fig = go.Figure(data=go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name='项目评分',
                            line_color='#FF4B4B'
                        ))
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(visible=True, range=[0, 10])
                            ),
                            showlegend=False,
                            margin=dict(l=40, r=40, t=40, b=40)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠️ 评分图表生成失败，请尝试重新生成。")
                        
            except Exception as e:
                st.error(f"❌ 生成失败，请检查网络或 API 状态：{e}")
    else:
        st.warning("⚠️ 请先输入你的项目想法！")

# 底部页脚
st.markdown("---")
st.caption("© 2026 赛创智航 - 由 Google Gemini 1.5 Flash 提供动力支持")
