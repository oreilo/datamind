FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd -r -u 10001 datamind && mkdir -p /app/data && chown datamind /app/data
USER datamind
EXPOSE 8000
CMD ["uvicorn","datamind.api:app","--host","0.0.0.0","--port","8000"]
