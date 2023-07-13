FROM python:3.10-slim

ENV MODEL_NAME='hkunlp/instructor-large'
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# https://github.com/HKUNLP/instructor-embedding/blob/main/README.md#installation
RUN apt-get update && apt-get install -y wget && \
    wget https://raw.githubusercontent.com/HKUNLP/instructor-embedding/main/requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install sanic InstructorEmbedding

COPY download_model.py .
RUN python download_model.py

COPY main.py .

CMD ["python", "main.py"]

# Health check using /health ping
HEALTHCHECK --interval=5s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1
