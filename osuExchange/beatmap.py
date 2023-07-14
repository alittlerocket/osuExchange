from datetime import datetime
from typing import Sequence, Any

from osuExchange import api
from osuExchange.util import optional_datetime, optional_object, optional_object_list
from osuExchange.types import GameMode
		
# https://osu.ppy.sh/docs/#beatmapcompact
class BeatmapCompact:
	# https://osu.ppy.sh/docs/#beatmapcompact-failtimes
	class Failtimes:
		def __init__(self, json: dict):
			self.exit: list[int] | None = json.get('exit')
			self.fail: list[int] | None = json.get('fail')

	def __init__(self, json: dict):
		self.beatmapset_id: int = json['beatmapset_id']
		self.difficulty_rating: float = json['difficulty_rating']
		self.id: int = json['id']
		self.mode: str = json['mode']
		self.status: str = json['status']
		self.total_length: int = json['total_length']
		self.user_id: int = json['user_id']
		self.version: str = json['version']

		# Optional attributes
		self.beatmapset = json.get('beatmapset')
		self.checksum: str | None = json.get('checksum')
		self.failtimes = BeatmapCompact.Failtimes(json['failtimes'])
		self.max_combo: int | None = json.get('max_combo')

# https://osu.ppy.sh/docs/#beatmap
class Beatmap(BeatmapCompact):
	def __init__(self, json: dict):
		super().__init__(json)
		self.accuracy: float = json['accuracy']
		self.approach_rate: float = json['ar']
		self.bpm: float | None = json.get('bpm')
		self.convert: bool = json['convert']
		self.count_circles: int = json['count_circles']
		self.count_sliders: int = json['count_sliders']
		self.count_spinners: int = json['count_spinners']
		self.circle_size: float = json['cs']
		self.deleted_at: datetime | None = optional_datetime(json, 'deleted_at')
		self.hp_drain: float = json['drain']
		self.hit_length: int = json['hit_length']
		self.is_scoreable: bool = json['is_scoreable']
		self.last_updated: datetime = json['last_updated']
		self.mode_int: int = json['mode_int']
		self.pass_count: int = json['passcount']
		self.play_count: int = json['playcount']
		self.ranked: int = json['ranked']

# https://osu.ppy.sh/docs/#beatmapdifficultyattributes
class BeatmapDifficultyAttributes:
	def __init__(self, json: dict):
		self.max_combo: int = json['max_combo']
		self.star_rating: float = json['star_rating']

		# osu, taiko, fruits
		self.approach_rate: float | None = json['approach_rate']

		# taiko, mania
		self.great_hit_window: float | None = json['great_hit_window']

		# oau
		self.aim_difficulty: float | None = json['aim_difficulty']
		self.flashlight_difficulty: float | None = json['flashlight_difficulty']
		self.overall_difficulty: float | None = json['overall_difficulty']
		self.slider_factor: float | None = json['slider_factor']
		self.speed_difficulty: float | None = json['speed_difficulty']

		# taiko
		self.stamina_difficulty: float | None = json['stamina_difficulty']
		self.rhythm_difficulty: float | None = json['rhythm_difficulty']
		self.colour_difficulty: float | None = json['colour_difficulty']

def get_beatmap(access_token: str, id: int) -> Beatmap:
	return Beatmap(api.get(access_token, f'/beatmaps/{id}'))

def get_beatmaps(access_token: str, ids: list[int]) -> list[Beatmap]:
	return [Beatmap(o) for o in api.get(access_token, '/beatmaps', { 'ids[]': ids })['beatmaps']]

def get_beatmap_attributes(
	access_token: str,
	id: int,
	mods: Sequence[str] | None = None,
	ruleset: GameMode | None = None,
	ruleset_id: int | None = None
) -> BeatmapDifficultyAttributes:
	body: dict[str, Any] = {}

	if mods is not None:
		body['mods'] = mods
	
	if ruleset is not None:
		body['ruleset'] = ruleset
	
	if ruleset_id is not None:
		body['ruleset_id'] = ruleset_id
	
	return BeatmapDifficultyAttributes(api.post(access_token, f'/beatmaps/{id}/attributes', body_json=body))
