from osuExchange.endpoints import UsersEndpoints, BeatmapsEndpoints, Score
from osuExchange.auth import ClientCredentialsToken, OAuth2Scope, get_access_token, get_client_credentials_token
from osuExchange.typing import GameMode
from osuExchange import api

class BaseOsuApiClient:
	def __init__(self, token: ClientCredentialsToken):
		self.token = token
		self.users = UsersEndpoints(token.access_token)
		self.beatmaps = BeatmapsEndpoints(token.access_token)

	# https://osu.ppy.sh/docs/index.html#get-apiv2scoresmodescore
	def get_score(self, mode: GameMode, score_id: int) -> Score:
		return Score(api.get(f'/scores/{mode}/{score_id}', token=self.token.access_token).json())

class OsuUserClient(BaseOsuApiClient):
	def __init__(self, *, client_id: str, client_secret: str, redirect_uri: str, scopes: list[OAuth2Scope]):
		super().__init__(get_access_token(client_id, client_secret, redirect_uri, scopes))

class OsuApiClient(BaseOsuApiClient):
	def __init__(self, *, client_id: str, client_secret: str):
		super().__init__(get_client_credentials_token(client_id, client_secret))
