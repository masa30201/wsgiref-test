FROM python:3.12-slim

# ログ即時出力 & .pyc 非生成（デバッグしやすくなる）
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY app.py .

EXPOSE 8000
CMD ["python", "app.py"]
