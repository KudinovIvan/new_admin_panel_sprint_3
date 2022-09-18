import random
from functools import wraps
import logging
from time import sleep


def backoff():
    """
    Декоратор по отслеживанию всех ошибок, связанных с работой
    ES и PostgreSQL
    """
    def decorator(target):
        @wraps(target)
        def retry(*args, **kwargs):
            sleep_time = 10
            while True:
                try:
                    ret = target(*args, **kwargs)
                except Exception as e:
                    logging.error(f'Exception is catched {e}')
                    logging.warning(f'Wait fo {sleep_time} seconds and try again')
                    sleep(sleep_time)
                else:
                    return ret
        return retry
    return decorator
