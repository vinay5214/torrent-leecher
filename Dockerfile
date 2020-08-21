FROM python:3.8.5-slim-buster

# http://bugs.python.org/issue19846
# https://github.com/SpEcHiDe/PublicLeech/pull/97
ENV LANG C.UTF-8

# sets the TimeZon, to be used inside the container
ENV TZ Asia/Kolkata

# copies 'requirements.txt' to root directory
COPY requirements.txt .

# install required packages
RUN apt update && apt install --no-install-recommends -y \
    wget curl \
    aria2 ffmpeg rclone \
    bash procps git \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir --upgrade -r requirements.txt

# copies required directories into container
COPY tobrot /app/tobrot
COPY aria2 /app/aria2

# set /app as working directory
WORKDIR /app

# specifies what command to run within the container
CMD ["python3", "-m", "tobrot"]
