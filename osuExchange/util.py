from typing import TypeVar

T = TypeVar('T')

def list_of_objects_or_none(l: list[dict] | None, cls: type[T]) -> list[T] | None:
	return None if l is None else [cls(o) for o in l]

def object_or_none(o: dict | None, cls: type[T]) -> T | None:
	return None if o is None else cls(o)
