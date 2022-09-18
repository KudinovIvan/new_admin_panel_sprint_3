import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    postgres_name: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    broker_host: str
    broker_port: str

    elastic_host: str
    elastic_port: str
    elastic_index: str
    dump_size: int

    class Config:
        env_file = os.environ.get('PATH')