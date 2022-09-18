import json
from dataclasses import asdict
from typing import List
from elasticsearch import Elasticsearch, TransportError
from elasticsearch.exceptions import RequestError
import logging

from model_dataclasses import Filmwork
from decorator import backoff
from settings import Settings


class ES_LOAD:
    def __init__(self, conn):
        self.cnf = Settings()
        self.conn = conn

    @backoff()
    def create_index(self, index_name: str, index_body: str):
        """
        Создание индекса в es
        """
        try:
            self.conn.indices.create(index_name, body=index_body)
        except RequestError as e:
            if e.error == 'resource_already_exists_exception':
                pass
            else:
                raise e

    @backoff()
    def bulk_update(self, docs: List[Filmwork]) -> bool:
        """
        Запись данных в es
        """
        if not docs:
            logging.warning('No more data to update in elastic')
            return None
        body = []
        for doc in docs:
            index = {"index" : {"_index" : self.cnf.elastic_index, "_id" : doc.id}}
            body.append(json.dumps(index))
            body.append(json.dumps(asdict(doc)))
        results = self.conn.bulk(body)
        if results['errors']:
            error = [result['index'] for result in results['items'] if result['index']['status'] != 200]
            logging.error(results['took'])
            logging.error(results['errors'])
            logging.error(error)
            return None
        return True