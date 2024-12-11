# thanks to https://github.com/saidsef/scapy-containerised for this
FROM alpine:latest

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

WORKDIR /usr/app/src

RUN python -m venv .venv
RUN .venv/bin/pip install scapy

RUN apk add --update --no-cache libcap libpcap-dev libpcap

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache -r requirements.txt -Csetup-args=-Dblas=blas -Csetup-args=-Dlapack=lapack

COPY main.py .

CMD [ ".venv/bin/python", "./main.py"]
