from datetime import datetime, timedelta
from redis import Redis

from decorator import backoff
from settings import Settings


class ETLRedis:
    def __init__(self):
        cnf = Settings()
        self.redis = Redis(
            host=cnf.broker_host,
            port=cnf.broker_port,
            decode_responses=True,
        )

    @backoff()
    def set_lasttime(self, lasttime: datetime):
        """
        Сохранение последнего datetime получения данных из PostgreSQL
        """
        key = ':lasttime'
        self.redis.set(key, lasttime.isoformat())

    @backoff()
    def get_lasttime(self) -> datetime:
        """
        Получение последнего datetime получения данных из PostgreSQL
        """
        key = ':lasttime'
        if self.redis.get(key) is None:
            return datetime(1970, 1, 1)
        return datetime.fromisoformat(self.redis.get(key))
