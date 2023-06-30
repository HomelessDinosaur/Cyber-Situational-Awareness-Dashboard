FROM python:3.8-slim-buster

WORKDIR /app
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py main.py
COPY high_risk.csv high_risk.csv

CMD [ "python3", "main.py" ]