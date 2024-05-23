FROM python:3.9-slim

WORKDIR /finance_app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
