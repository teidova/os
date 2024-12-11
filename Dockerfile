FROM python:latest

LABEL Maintainer="roushan.me17"

WORKDIR /usr/app/src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py"]
