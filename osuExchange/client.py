from osuExchange.users import get_user, get_users, User, UserCompact
from osuExchange.beatmaps import get_beatmap, get_beatmaps, Beatmap
from osuExchange.scores import get_beatmap_scores, get_score, get_user_beatmap_scores, BeatmapScores, Score, BeatmapUserScore
from osuExchange.seasonalbg import get_seasonal_backgrounds, SeasonalBackgrounds
from osuExchange.auth import get_access_token, get_client_credentials_token, ClientCredentialsToken, UserAccessToken, OAuth2Scope
from osuExchange.typing import GameMode, Literal

class OAuth2Client:
	def __init__(self):
		self.token_obj: ClientCredentialsToken | UserAccessToken | None = None

	def get_user_access_token(self,
		client_id: str, 
		client_secret: str, 
		redirect_uri: str,
		scopes: list[OAuth2Scope]
	) -> None:
		self.token_obj = get_access_token(client_id, client_secret, redirect_uri, scopes)
		
	def get_client_credentials_token(
		self,
		client_id: str,
		client_secret: str
	) -> None:
		self.token_obj = get_client_credentials_token(client_id, client_secret)

	def __raise_authenticate__(self):
		return Exception('self.token_obj is None; please authenticate')

	def get_user(self,
		id: int,
		mode: GameMode | None,
		key: Literal['id', 'username'] | None
	) -> User:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_user(self.token_obj.access_token, id, mode, key)
	
	def get_users(self, users: list[int]) -> list[UserCompact]:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_users(self.token_obj.access_token, users)
	
	def get_beatmap(self, id: int) -> Beatmap:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_beatmap(self.token_obj.access_token, id)
	
	def get_beatmaps(self, ids: list[int]) -> list[Beatmap]:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_beatmaps(self.token_obj.access_token, ids)

	def get_beatmap_scores(self, id: int) -> BeatmapScores:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_beatmap_scores(self.token_obj.access_token, id)

	def get_score(self, mode: GameMode | str, id: int) -> Score:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_score(self.token_obj.access_token, mode, id)
	
	def get_user_beatmap_scores(self, beatmap_id: int, user_id: int) -> list[Score]:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_user_beatmap_scores(self.token_obj.access_token, beatmap_id, user_id)
	
	def get_seasonal_backgrounds(self) -> SeasonalBackgrounds:
		if self.token_obj is None:
			raise self.__raise_authenticate__()
		return get_seasonal_backgrounds(self.token_obj.access_token)