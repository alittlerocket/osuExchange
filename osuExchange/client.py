from osuExchange.users import get_user, get_users, User, UserCompact
from osuExchange.beatmaps import get_beatmap, get_beatmaps, Beatmap
from osuExchange.typing import GameMode, Literal

class OAuth2Client:
	def __init__(self, access_token: str):
		self.access_token = access_token

	def get_user(self,
	    id: int,
		mode: GameMode | None,
		key: Literal['id', 'username'] | None
	) -> User:
		return get_user(self.access_token, id, mode, key)
	
	def get_users(self, users: list[int]) -> list[UserCompact]:
		return get_users(self.access_token, users)
	
	def get_beatmap(self, id: int) -> Beatmap:
		return get_beatmap(self.access_token, id)
	
	def get_beatmaps(self, ids: list[int]) -> list[Beatmap]:
		return get_beatmaps(self.access_token, ids)