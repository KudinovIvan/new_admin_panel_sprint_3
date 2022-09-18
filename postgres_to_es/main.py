from contextlib import contextmanager
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import psycopg2
import logging
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from time import sleep

from index import MOVIE_INDEX as index_body
from settings import Settings
from decorator import backoff
from etl_redis import ETLRedis
from pg_dump import PG_DUMP
from es_load import ES_LOAD


@contextmanager
def conn_context_es(host: str, port: str):
    """
    Подключение к es
    """

    @backoff(logger=logging.getLogger('main::conn_context_es'))
    def connect(host: str, port: str):
        conn = Elasticsearch(f"{host}://{host}:{port}")
        return conn

    conn = connect(host, port)
    yield conn


@contextmanager
def conn_context_postgres(dsl: dict):
    """
    Подключение к postgres
    """

    @backoff(logger=logging.getLogger('main::conn_context_postgres'))
    def connect(dsl: dict):
        conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        return conn

    conn = connect(dsl)
    yield conn


def postgres_to_es(es_conn: Elasticsearch, pg_conn: _connection):
    """
    Основной скрипт по выгрузке данных в es
    """
    redis = ETLRedis()
    pg_dump = PG_DUMP(pg_conn)
    es_load = ES_LOAD(es_conn)
    lasttime = redis.get_lasttime()
    for ids in pg_dump.get_updated_id(lasttime):
        films = pg_dump.get_filmsbyid(ids)
        redis.set_lasttime(datetime.now())
        es_load.create_index(settings.elastic_index, index_body)
        es_load.bulk_update(films)


if __name__ == '__main__':
    settings = Settings()
    dsl = {
        'dbname': settings.postgres_name,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port
    }
    with conn_context_es(settings.elastic_host, settings.elastic_port) as es_conn, \
            conn_context_postgres(dsl) as pg_conn:
        while True:
            postgres_to_es(es_conn, pg_conn)
            sleep(10)