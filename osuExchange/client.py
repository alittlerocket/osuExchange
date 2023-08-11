from osuExchange.users import get_user, get_users, User, UserCompact
from osuExchange.beatmaps import get_beatmap, get_beatmaps, Beatmap
from osuExchange.scores import get_beatmap_scores, get_score, get_user_beatmap_scores, BeatmapScores, Score
from osuExchange.seasonalbg import get_seasonal_backgrounds, SeasonalBackgrounds
from osuExchange.auth import get_access_token, get_client_credentials_token, ClientCredentialsToken, OAuth2Scope
from osuExchange.typing import GameMode, Literal
from typing import Optional

class BaseOsuApiClient:
	def __init__(self, token: ClientCredentialsToken):
		self.token = token

	def get_user(self, id: int, *, mode: Optional[GameMode] = None, key: Optional[Literal['id', 'username']] = None) -> User:
		return get_user(self.token.access_token, id, mode, key)
	
	def get_users(self, users: list[int]) -> list[UserCompact]:
		return get_users(self.token.access_token, users)
	
	def get_beatmap(self, id: int) -> Beatmap:
		return get_beatmap(self.token.access_token, id)
	
	def get_beatmaps(self, ids: list[int]) -> list[Beatmap]:
		return get_beatmaps(self.token.access_token, ids)

	def get_beatmap_scores(self, id: int) -> BeatmapScores:
		return get_beatmap_scores(self.token.access_token, id)

	def get_score(self, id: int, *, mode: GameMode) -> Score:
		return get_score(self.token.access_token, mode, id)
	
	def get_user_beatmap_scores(self, *, beatmap_id: int, user_id: int) -> list[Score]:
		return get_user_beatmap_scores(self.token.access_token, beatmap_id, user_id)
	
	def get_seasonal_backgrounds(self) -> SeasonalBackgrounds:
		return get_seasonal_backgrounds(self.token.access_token)
	
class OsuUserClient(BaseOsuApiClient):
	def __init__(self, *, client_id: str, client_secret: str, redirect_uri: str, scopes: list[OAuth2Scope]):
		super().__init__(get_access_token(client_id, client_secret, redirect_uri, scopes))

class OsuApiClient(BaseOsuApiClient):
	def __init__(self, *, client_id: str, client_secret: str):
		super().__init__(get_client_credentials_token(client_id, client_secret))
