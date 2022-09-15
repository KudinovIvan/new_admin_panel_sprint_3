FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 6
ENV UWSGI_THREADS 3
ENV UWSGI_HARAKIRI 240

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install netcat -y \
    && mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/

RUN mkdir -p /app/media/ \
    && mkdir -p /app/static \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY uwsgi.ini /etc/

COPY entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /app/

EXPOSE 8080

ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]
