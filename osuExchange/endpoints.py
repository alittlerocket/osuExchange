from typing import Sequence, Literal, Optional
from osuExchange import api
from osuExchange.typing import GameMode, JsonObject
from osuExchange.structures import (
    User, UserCompact, Event, Beatmap, BeatmapDifficultyAttributes, BeatmapScores, Score,
    BeatmapUserScore
)

class UsersEndpoints:
	def __init__(self, token: str):
		self.token = token
		
	# https://osu.ppy.sh/docs/#get-user
	def get(self, id_or_username: int | str, *, mode: Optional[GameMode] = None) -> User:
		return User(api.get(f'/users/{id_or_username}{f"/{mode}" if mode else ""}', token=self.token).json())

	# https://osu.ppy.sh/docs/#get-users
	def get_many(self, user_ids: list[int]) -> list[UserCompact]:
		return [UserCompact(o) for o in api.get('/users', token=self.token, params={ 'ids[]': user_ids }).json()['users']]
	
	# https://osu.ppy.sh/docs/#get-user-recent-activity
	def get_recent_activity(self, user_id: int) -> list[Event]:
		return [Event(o) for o in api.get(f'/users/{user_id}/recent_activity').json()]

class BeatmapsEndpoints:
	def __init__(self, token: str):
		self.token = token

	# https://osu.ppy.sh/docs/#get-beatmap
	def get(self, beatmap_id: int) -> Beatmap:
		return Beatmap(api.get(f'/beatmaps/{beatmap_id}', token=self.token).json())
	
	# https://osu.ppy.sh/docs/#get-beatmaps
	def get_many(self, beatmap_ids: list[int]) -> list[Beatmap]:
		return [Beatmap(o) for o in api.get('/beatmaps', token=self.token, params={ 'ids[]': beatmap_ids }).json()['beatmaps']]

	# https://osu.ppy.sh/docs/#get-beatmap-attributes
	def get_difficulty_attributes(self,
		beatmap_id: int, *,
		mods: Optional[Sequence[str]] = None,
		ruleset: Optional[GameMode] = None,
		ruleset_id: Optional[int] = None,
	) -> BeatmapDifficultyAttributes:
		body_params: JsonObject = {}
		if mods:
			body_params['mods'] = mods
		if ruleset:
			body_params['ruleset'] = ruleset
		if ruleset_id:
			body_params['ruleset_id'] = ruleset_id
		return BeatmapDifficultyAttributes(api.post(f'/beatmaps/{beatmap_id}/attributes', token=self.token, json=body_params).json()['attributes'])
	
	# https://osu.ppy.sh/docs/index.html#get-beatmap-scores
	def get_scores(self, beatmap_id: int) -> BeatmapScores:
		return BeatmapScores(api.get(f'/beatmaps/{beatmap_id}/scores', token=self.token).json())
	
	# https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
	def get_score(self, beatmap_id: int, user_id: int) -> BeatmapUserScore:
		return BeatmapUserScore(api.get(f'/beatmaps/{beatmap_id}/scores/users/{user_id}', token=self.token).json())
	
	# https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
	def get_user_scores(self, beatmap_id: int, user_id: int) -> list[Score]:
		return [Score(o) for o in api.get(f'/beatmaps/{beatmap_id}/scores/users/{user_id}/all', token=self.token).json()['scores']]
