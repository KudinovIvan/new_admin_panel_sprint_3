from datetime import datetime
from psycopg2 import connect as pgconnect, sql
import logging
import dataclasses
from datetime import datetime
from typing import List

from model_dataclasses import Filmwork
from decorator import backoff
from settings import Settings


class PG_DUMP:
    UPDATED = '''
    SELECT DISTINCT fm.id 
    FROM content.film_work AS fm
    LEFT OUTER JOIN content.person_film_work AS pfm ON fm.id = pfm.film_work_id
    LEFT OUTER JOIN content.person AS p ON pfm.person_id = p.id
    LEFT OUTER JOIN content.genre_film_work AS gfm ON fm.id = gfm.film_work_id
    LEFT OUTER JOIN content.genre AS g ON gfm.genre_id = g.id
    WHERE fm.updated_at > '{lasttime}'
    OR p.updated_at > '{lasttime}'
    OR g.updated_at > '{lasttime}'
    GROUP BY fm.id
    '''
    GETFILMSBYID = '''
    SELECT
        fm.title, fm.description, fm.type,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfm.role = 'actor') AS actors,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfm.role = 'writer') AS writers,
        COALESCE(ARRAY_AGG(DISTINCT g.name), '{0}') AS genres,
        COALESCE(ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfm.role = 'director'), '{0}') AS director,
        COALESCE(ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfm.role = 'actor'), '{0}') AS actor_names,
        COALESCE(ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfm.role = 'writer'), '{0}') AS writer_names, 
        fm.rating as imdb_rating, fm.id
    FROM content.film_work AS fm
    LEFT OUTER JOIN content.person_film_work AS pfm ON fm.id = pfm.film_work_id
    LEFT OUTER JOIN content.person AS p ON pfm.person_id = p.id
    LEFT OUTER JOIN content.genre_film_work AS gfm ON fm.id = gfm.film_work_id
    LEFT OUTER JOIN content.genre AS g ON gfm.genre_id = g.id
    WHERE fm.id IN ({1})
    GROUP BY fm.id
    ORDER BY fm.updated_at
    '''

    def __init__(self, conn):
        self.cnf = Settings()
        self.conn = conn

    @backoff()
    def _pg_id_query(self, sqlquery: str, query_args: datetime) -> list:
        """
        Получение id обновленных фильмов
        """
        with self.conn as conn, conn.cursor() as cur:
            cur.execute(sqlquery.format(lasttime=query_args))
            rows = cur.fetchmany(self.cnf.dump_size)
            current_fetch = cur.fetchmany(self.cnf.dump_size)
            while current_fetch:
                rows += current_fetch
                current_fetch = cur.fetchmany(self.cnf.dump_size)
        return [row[0] for row in rows]

    @backoff()
    def _pg_query(self, sqlquery: str, query_args: list):
        """
          Получение даных по обновленным фильмам
        """
        with self.conn as conn, conn.cursor() as cur:
            cur.execute(sqlquery.format({}, ", ".join(f"'{arg}'" for arg in query_args)))
            rows = cur.fetchmany(self.cnf.dump_size)
            current_fetch = cur.fetchmany(self.cnf.dump_size)
            while current_fetch:
                rows += current_fetch
                current_fetch = cur.fetchmany(self.cnf.dump_size)
        return rows

    def get_updated_id(self, updated_datetime: datetime) -> list:
        return self._pg_id_query(self.UPDATED, updated_datetime)

    def get_filmsbyid(self, ids: tuple) -> List[Filmwork]:
        return [Filmwork(*row) for row in self._pg_query(self.GETFILMSBYID, ids)]