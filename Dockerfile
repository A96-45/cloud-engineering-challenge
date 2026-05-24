# Multi-stage build for cloud cost optimization dashboard

FROM python:3.9-slim as base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

FROM base as dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM dependencies as builder
COPY . .
RUN python -m py_compile app/*.py

FROM python:3.9-slim as runtime
WORKDIR /app
COPY --from=dependencies /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app .

ENV FLASK_APP=app.py
ENV PORT=5000

EXPOSE $PORT
CMD ["python", "app.py"]
