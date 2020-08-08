FROM python:3.8.5-slim-buster

COPY requirements.txt /app/requirements.txt
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    wget curl \
    aria2 ffmpeg rclone \
    bash procps git \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY tobrot /app/tobrot
COPY ariac /app/ariac
WORKDIR /app

ENTRYPOINT ["python3", "-m", "tobrot"]
