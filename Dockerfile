FROM python:3.10-slim

LABEL org.opencontainers.image.source https://github.com/flexchar/instructor-embedding-api
LABEL org.opencontainers.image.description="API for creating embeddings using Instructor model."
LABEL org.opencontainers.image.licenses=MIT

ENV MODEL_NAME='hkunlp/instructor-large'
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

# https://github.com/HKUNLP/instructor-embedding/blob/main/README.md#installation
# RUN apt-get update && apt-get install -y wget && \
#     wget https://raw.githubusercontent.com/HKUNLP/instructor-embedding/main/requirements.txt && \
# pip install --no-cache-dir -r requirements.txt && \
#     pip install sanic InstructorEmbedding

# It seems that we can get away with just installing the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY download_model.py .
RUN python download_model.py

COPY main.py .

# Single processes performed better on a small ab test
CMD ["sanic", "main:app", "--single-process", "--host", "0.0.0.0", "--port", "8000"]