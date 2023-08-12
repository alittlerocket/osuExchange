from typing import Literal, Any, TypeVar, Optional
from datetime import datetime

JsonObject = dict[str, Any]
GameMode = Literal['fruits', 'mania', 'osu', 'taiko']
ProfilePage = Literal['me', 'recent_activity', 'beatmaps', 'historical', 'kudosu', 'top_ranks', 'medals']

T = TypeVar('T')

def optional_object_list(json: JsonObject, key: str, cls: type[T]) -> Optional[list[T]]:
	l = json.get(key)
	return [cls(o) for o in l] if l else None

def optional_object(json: JsonObject, key: str, cls: type[T]) -> Optional[T]:
	o = json.get(key)
	return cls(o) if o else None

def optional_datetime(json: JsonObject, key: str) -> Optional[datetime]:
	s = json.get(key)
	return datetime.fromisoformat(s) if s else None
