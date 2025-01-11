# 使用官方的 Python 镜像作为基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 安装依赖库
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# 复制 requirements.txt 并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 运行 Streamlit 应用
CMD ["streamlit", "run", "src/ollama_ocr/app.py"]