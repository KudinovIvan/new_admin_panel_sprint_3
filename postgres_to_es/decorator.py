import random
from functools import wraps
import logging
from time import sleep
from sys import stdout

logging_logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)


def _sleep_time(
        start_sleep_time: float,
        border_sleep_time: float,
        factor: int,
        attempt: int,
        logger: logging.Logger
    ) -> float:
    try:
        sleep_time = random.uniform(start_sleep_time, start_sleep_time * factor) * factor ** attempt
    except OverflowError:
        logger.warning('Sleep_time will be set to border_sleep_time')
        sleep_time = border_sleep_time
    return min(border_sleep_time, sleep_time)


def backoff(
        start_sleep_time=0.1,
        border_sleep_time=30,
        factor=2,
        tries=20,
        logger=logging_logger,
        logger_formatter=logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    ):
    """
    Декоратор по отслеживанию всех ошибок, связанных с работой
    ES и PostgreSQL
    :param start_sleep_time: начальное время отката
    :param border_sleep_time: максимальное время ожидания
    :param factor: - множитель для времени ожидания
    :param tries: число попыток до возникновения каких-либо исключений
    :param logger: логгер,
    :param logger_formatter: формат вывода сообщений в логгере
    """
    def decorator(target):
        @wraps(target)
        def retry(*args, **kwargs):
            handler.setFormatter(logger_formatter)
            logger.addHandler(handler)
            available_tries = tries
            attempt = 0
            while available_tries:
                sleep_time = _sleep_time(start_sleep_time, border_sleep_time, factor, attempt, logger)
                try:
                    ret = target(*args, **kwargs)
                except Exception as e:
                    available_tries -= 1
                    attempt += 1
                    logger.error(f'Exception is catched {e}')
                    logger.warning(f'Wait fo {sleep_time} seconds and try again')
                    sleep(sleep_time)
                else:
                    return ret
        return retry
    return decorator
