FROM ubuntu:22.04
LABEL author="Pritish Saha - On behalf of KolKGP Convergence"

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip sqlite3 libsqlite3-dev python3-opencv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install -r requirements.txt