# thanks to https://github.com/saidsef/scapy-containerised for this
FROM alpine:latest

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
#RUN python3 -m ensurepip
#RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /usr/app/src

RUN python -m venv .venv
RUN .venv/bin/pip install scapy

RUN apk add --update --no-cache libcap libpcap-dev libpcap

#RUN apk add -U --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
#        build-base gcc musl-dev cmake autoconf python3-dev libstdc++ openblas-dev jpeg-dev zlib-dev \
#        bison libpng libpng-dev freetype freetype-dev libffi libffi-dev openssl openssl-dev \
#        tcpdump imagemagick graphviz curl texlive libressl libpcap libpcap-dev libjpeg xdg-utils && \
#    pip3 install --no-cache -r requirements.txt -Csetup-args=-Dblas=blas -Csetup-args=-Dlapack=lapack && \
#    rm -rfv /var/cache/apk/*

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache -r requirements.txt -Csetup-args=-Dblas=blas -Csetup-args=-Dlapack=lapack

COPY . .

#CMD [ "ls", "-a" ]
CMD [ ".venv/bin/python", "./main.py"]
