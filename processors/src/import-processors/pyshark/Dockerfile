FROM python:3.8-alpine

WORKDIR /app

RUN apk add tshark
RUN chmod +x /usr/bin/dumpcap

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py main.py

CMD [ "python3", "main.py" ]