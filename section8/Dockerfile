FROM python:3-slim

RUN apt-get clean && apt-get -y update
RUN apt-get -y install nginx python3-dev build-essential

COPY mysite.conf /etc/nginx/sites-enabled/default

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

COPY ["app.py", "db.py", "security.py", "./"]
COPY models ./models
COPY resources ./resources
COPY data ./data

COPY ["uwsgi.ini", "startup.sh", "./"]

RUN chmod +x startup.sh

EXPOSE 80

CMD ["./startup.sh"]