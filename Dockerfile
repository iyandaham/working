FROM python:3.5.3

WORKDIR /app

COPY requirements.txt .

EXPOSE 5000

FROM pip install -r requirements.txt

ENTRYPOINT '/user/local/bin/pyton' 'app.py'

COPY . .
