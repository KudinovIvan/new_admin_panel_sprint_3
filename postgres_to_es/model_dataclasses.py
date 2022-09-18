import uuid
import json
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Filmwork:
    title: str
    description: str
    type: str
    actors: json
    writers: json
    genre: list
    director: list
    actors_names: list
    writers_names: list
    imdb_rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
