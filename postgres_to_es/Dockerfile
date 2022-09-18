FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install netcat -y \
    && mkdir -p /app

RUN mkdir -p /postgres_to_es

WORKDIR /postgres_to_es

COPY requirements.txt /postgres_to_es/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /postgres_to_es/

ENTRYPOINT ["bash", "/usr/src/app/entrypoint.sh"]
