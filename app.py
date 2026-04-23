import streamlit as st
import google.generativeai as genai
import os
import plotly.graph_objects as go
import re

# --- 1. 页面配置 ---
st.set_page_config(page_title="赛创智航 - 双创竞赛 Agent", layout="wide", page_icon="🚀")

# --- 2. API 密钥配置 (终极防 404 配置) ---
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    # 强制配置 API 密钥
    genai.configure(api_key=api_key)
else:
    st.error("🔑 未在 Secrets 中找到 API Key。")
    st.stop()

# --- 3. UI 界面 ---
st.title("🚀 赛创智航 (Compete-Pilot)")
st.markdown("### 高校双创竞赛点子孵化与评估专家")

user_input = st.text_area("💡 请详细描述你的参赛项目想法：", height=200, placeholder="例如：我打算做一个...")

if st.button("🚀 一键生成评估报告"):
    if user_input:
        with st.spinner("AI 评委正在认真审核中..."):
            try:
                # 【核心修改】：不直接调用 GenerativeModel，而是先确认模型可用
                # 显式使用 gemini-1.5-flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                你是一位高校双创竞赛评审专家。请对以下项目进行多维度评估：
                项目：{user_input}
                
                最后请按格式输出：
                [SCORE]
                创新性: 8
                可行性: 7
                商业价值: 6
                社会意义: 9
                团队要求: 7
                [/SCORE]
                """
                
                # 【核心修改】：显式调用，防止 SDK 走错 v1beta 路径
                response = model.generate_content(prompt)
                
                if not response.text:
                    st.error("AI 未返回有效内容，请检查 API 状态。")
                else:
                    full_text = response.text
                    score_match = re.search(r"\[SCORE\](.*?)\[/SCORE\]", full_text, re.S)
                    
                    col1, col2 = st.columns([3, 2])
                    with col1:
                        st.markdown("### 📋 详细评估报告")
                        display_text = re.sub(r"\[SCORE\].*?\[/SCORE\]", "", full_text, flags=re.S)
                        st.markdown(display_text)
                    
                    with col2:
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
                # 如果 1.5-flash 还是不行，自动尝试切换到 gemini-pro (老版本更稳)
                st.info("🔄 正在尝试备用连接通道...")
                try:
                    model_alt = genai.GenerativeModel('gemini-pro')
                    response = model_alt.generate_content(prompt)
                    st.success("已通过备用通道连接成功！")
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"❌ 最终连接失败。错误原因: {e2}")
    else:
        st.warning("⚠️ 请输入想法！")
