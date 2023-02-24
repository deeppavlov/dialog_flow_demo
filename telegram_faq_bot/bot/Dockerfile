# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster as base

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# cache mfaq model
RUN ["python3", "-c", "from sentence_transformers import SentenceTransformer; _ = SentenceTransformer('clips/mfaq')"]

COPY bot/ ./bot

FROM base as test
COPY test.py ./
RUN ["pytest", "test.py"]

FROM base as prod
COPY run.py ./
CMD ["python3", "run.py"]
