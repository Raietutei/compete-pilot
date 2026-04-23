import streamlit as st
import google.generativeai as genai
import os
import plotly.graph_objects as go
import re

# 页面配置
st.set_page_config(page_title="赛创智航 - 双创竞赛 Agent", layout="wide")

# 密钥配置 (云端优先)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    os.environ["GOOGLE_API_USE_MTLS"] = "never"
else:
    st.error("🔑 未配置 API Key")
    st.stop()

st.title("🚀 赛创智航 (Compete-Pilot)")
st.markdown("### 高校双创竞赛点子孵化与评估专家")

# 输入框
user_input = st.text_area("💡 请详细描述你的参赛项目想法：", height=200, placeholder="例如：我打算做一个面向大一新生的计算机导论智能助教...")

if st.button("🚀 一键生成评估报告"):
    if user_input:
        with st.spinner("AI 评委正在认真审核中..."):
            model = genai.GenerativeModel('gemini-pro')
            
            # 构造 Prompt，要求 AI 输出特定格式的评分
            prompt = f"""
            你是一位资深的高校双创竞赛评审专家（如互联网+、挑战杯）。
            请对以下项目想法进行多维度评估，并给出改进建议。
            
            项目内容：{user_input}
            
            请在回答的最后，务必按照以下格式输出评分（0-10分）：
            [SCORE]
            创新性: 8
            可行性: 7
            商业价值: 6
            社会意义: 9
            团队要求: 7
            [/SCORE]
            """
            
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # 尝试提取评分数据用于画图
                score_match = re.search(r"\[SCORE\](.*?)\[/SCORE\]", full_text, re.S)
                
                # 分两栏显示
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("### 📋 详细评估报告")
                    # 移除文本中的评分标记再显示
                    display_text = re.sub(r"\[SCORE\].*?\[/SCORE\]", "", full_text, flags=re.S)
                    st.write(display_text)
                
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
                        
                        # 画雷达图
                        fig = go.Figure(data=go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            line_color='#FF4B4B'
                        ))
                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
            except Exception as e:
                st.error(f"生成失败：{e}")
    else:
        st.warning("请输入你的项目想法！")
