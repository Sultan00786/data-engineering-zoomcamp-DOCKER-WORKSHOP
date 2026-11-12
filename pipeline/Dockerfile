# Simple Version
# FROM python:3.13.11-slim

# RUN pip install uv

# WORKDIR /app

# COPY . .

# RUN uv sync

# ENTRYPOINT ["uv", "run", "python", "pipeline.py"]



#Optimeze Version
FROM python:3.13

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock .python-version README.md ./
COPY ./src ./src
RUN uv sync --locked

COPY . .

ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]