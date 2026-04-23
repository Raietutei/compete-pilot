🚀 赛创智航 (Compete-Pilot)
###高校双创竞赛点子孵化与评估专家 Agent

📝 项目简介 (Introduction)
赛创智航 是一款专为大学生设计的双创竞赛辅助工具。它结合了 DeepSeek-V3 大模型的深度推理能力，通过结构化 Prompt 工程，对用户提交的参赛点子进行全方位的“模拟评审”。项目不仅提供详细的文字建议，还通过动态雷达图将评估数据可视化，帮助参赛选手快速定位项目短板。

✨ 核心功能 (Features)
智能评审：模拟“互联网+”、“挑战杯”专家思维，从创新性、可行性等 5 个维度进行打分。

可视化分析：利用 Plotly 实时生成多维度雷达图，项目优劣势一目了然。

国产化驱动：后端完全接入国产之光 DeepSeek API，响应迅速，逻辑严密。

响应式界面：基于 Streamlit 构建，支持 PC 与移动端流畅访问。

🛠️ 技术架构 (Tech Stack)
Language: Python 3.11

Web Framework: Streamlit

AI Engine: DeepSeek-V3 (via OpenAI SDK)

Visualization: Plotly Graph Objects

Deployment: Streamlit Cloud + GitHub CI/CD

🚀 快速开始 (Quick Start)
1. 克隆项目 (Clone)
Bash
git clone https://github.com/Raietutei/compete-pilot.git
cd compete-pilot
2. 安装依赖 (Install)
Bash
pip install -r requirements.txt
3. 配置密钥 (Configuration)
在根目录下创建 .env 文件：

代码段
DEEPSEEK_API_KEY="your_deepseek_api_key_here"
4. 运行应用 (Run)
Bash
streamlit run app.py


📂 项目结构 (Project Structure)
Plaintext
├── app.py              # 程序主入口
├── requirements.txt    # 依赖库列表
├── .env                # 环境变量（本地开发用）
├── .streamlit/         # Streamlit 配置文件
│   └── secrets.toml    # 云端密钥模板
└── README.md           # 项目文档
🤝 贡献与支持 (Contribution)
本项目为 【智数未来挑战赛-AIGC赛道】 参赛作品。如果你觉得这个工具对你有帮助，欢迎点个 ⭐ Star 支持一下！

作者： 嘉仪 (Jiayi)

学校： 上海杉达学院 (Shanghai Sanda University)
