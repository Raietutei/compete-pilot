import streamlit as st
import google.generativeai as genai
import os

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("未找到 API Key，请在 Secrets 中配置 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=api_key)

# 2. 页面基础设置
st.set_page_config(page_title="赛创智航 - 双创竞赛 Agent", page_icon="🚀", layout="wide")
st.title("🚀 赛创智航 (Compete-Pilot)")
st.subheader("高校双创竞赛点子孵化与评估专家")

# 3. 定义 AI 专家的“大脑逻辑” (System Prompt)
system_instruction = """
你现在是国家级“双创”大赛（如挑战杯、互联网+、智数未来）的首席评审专家，拥有10年评审经验。
当用户输入一个项目点子时，请严格按照以下结构输出极具专业性的评估报告：
1. 【赛道诊断】：判断该项目最适合哪个赛道（如 AIGC赛道、行业赋能等），是否符合大赛要求。
2. 【核心维度打分】：分别对“创新性”、“技术可行性”、“商业落地价值”进行打分（满分10分），并给出简短理由。
3. 【极客加分建议】：给出 2-3 个能极大提升“技术深度”或“现场演示效果”的具体建议。
4. 【避坑防御指南】：指出该点子在答辩时最容易被评委攻击的漏洞，并提供防御话术。
"""

# 4. 初始化大模型
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction
)

# 5. 构建前端交互界面
with st.form("idea_form"):
    user_idea = st.text_area(
        "💡 请详细描述你的参赛项目想法（越详细，评估越精准）：", 
        height=150, 
        placeholder="例如：我打算做一个面向大一新生的计算机导论智能助教，利用 RAG 技术结合教学大纲，并在前端实现算法的动态可视化..."
    )
    submitted = st.form_submit_button("🚀 一键生成评估报告")

# 6. 处理提交与 AI 生成逻辑
if submitted:
    if user_idea.strip() == "":
        st.warning("请先输入你的项目想法哦！")
    else:
        with st.spinner("专家评审团正在深度分析你的项目，请稍候..."):
            try:
                # 调用模型生成内容
                response = model.generate_content(user_idea)
                
                # 展示结果
                st.success("✅ 评估完成！请查看下方专属报告：")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"生成过程中出现错误: {e}")
