from typing import TypeVar
from datetime import datetime

from osuExchange.types import JsonObject

T = TypeVar('T')

def optional_object_list(json: JsonObject, key: str, cls: type[T]) -> list[T] | None:
	try:
		l = json[key]
		return None if l is None else [cls(o) for o in l]
	except KeyError:
		return None

def optional_object(json: JsonObject, key: str, cls: type[T]) -> T | None:
	try:
		o = json[key]
		return None if o is None else cls(o)
	except KeyError:
		return None

def optional_datetime(json: JsonObject, key: str) -> datetime | None:
	try:
		return datetime.fromisoformat(json[key])
	except KeyError:
		return None
