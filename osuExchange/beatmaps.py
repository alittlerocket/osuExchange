from datetime import datetime
from typing import Sequence
from enum import Enum

from osuExchange import api
from osuExchange.util import optional_datetime, optional_object_list, optional_object
from osuExchange.typing import GameMode, JsonObject

class RankStatus(Enum):
	GRAVEYARD = -2
	WIP = -1
	PENDING = 0
	RANKED = 1
	APPROVED = 2
	QUALIFIED = 3
	LOVED = 4

	@staticmethod
	def from_str(s: str):
		return RankStatus[s.upper()]
	
	@staticmethod
	def from_int(n: int):
		return RankStatus(n)

class Nomination:
	def __init__(self, json: JsonObject):
		self.beatmapset_id: int = json['beatmapset_id']
		self.rulesets: list[GameMode] = json['rulesets']
		self.reset: bool = json['reset']
		self.user_id: int = json['user_id']

# https://osu.ppy.sh/docs/#beatmapsetcompact
class BeatmapsetCompact:
	class Covers:
		def __init__(self, json: JsonObject):
			self.cover: str = json['cover']
			self.cover2x: str = json['cover@2x']
			self.card: str = json['card']
			self.card2x: str = json['card@2x']
			self.list: str = json['list']
			self.list2x: str = json['list@2x']
			self.slimcover: str = json['slimcover']
			self.slimcover2x: str = json['slimcover@2x']

	def __init__(self, json: JsonObject):
		self.artist: str = json['artist']
		self.artist_unicode: str = json['artist_unicode']
		self.covers = BeatmapsetCompact.Covers(json['covers'])
		self.creator: str = json['creator']
		self.favorite_count: int = json['favourite_count']
		self.id: int = json['id']
		self.nsfw: bool = json['nsfw']
		self.offset: int = json['offset']
		self.play_count: int = json['play_count']
		self.preview_url: str = json['preview_url']
		self.source: str = json['source']
		self.status: str = json['status']
		self.spotlight: bool = json['spotlight']
		self.title: str = json['title']
		self.title_unicode: str = json['title_unicode']
		self.user_id: int = json['user_id']
		self.video: bool = json['video']

		# Optional fields
		self.beatmaps = optional_object_list(json, 'beatmaps', Beatmap)
		self.converts = json.get('converts')
		self.current_nominations = optional_object_list(json, 'nominations', Nomination)
		self.current_user_attributes = json.get('current_user_attributes')
		self.description: str | None = json.get('description')
		self.discussions = json.get('discussions')
		self.events = json.get('events')
		self.genre = json.get('genre')
		self.has_favorited: bool | None = json.get('has_favourited')
		self.language = json.get('language')
		self.nominations = json.get('nominations')
		self.pack_tags = json.get('pack_tags')
		self.ratings = json.get('ratings')
		self.recent_favorites = json.get('recent_favourites')
		self.related_users = json.get('related_users')
		self.user = json.get('user')
		self.track_id = json.get('track_id')

class Beatmapset(BeatmapsetCompact):
	class Availability:
		def __init__(self, json: JsonObject):
			self.download_disabled: bool = json['download_disabled']
			self.more_information: str | None = json.get('more_information')

	class Hype:
		def __init__(self, json: JsonObject):
			self.current: int = json['current']
			self.required: int = json['required']

	class NominationsSummary:
		def __init__(self, json: JsonObject):
			self.current: int = json['current']
			self.required: int = json['required']

	def __init__(self, json: JsonObject):
		super().__init__(json)
		self.availability = Beatmapset.Availability(json['availability'])
		self.bpm: float = json['bpm']
		self.can_be_hyped: bool = json['can_be_hyped']
		self.deleted_at = optional_datetime(json, 'deleted_at')
		self.discussion_locked: bool = json['discussion_locked']
		self.hype = optional_object(json, 'hype', Beatmapset.Hype)
		self.is_scoreable: bool = json['is_scoreable']
		self.last_updated = datetime.fromisoformat(json['last_updated'])
		self.legacy_thread_url: str | None = json.get('legacy_thread_url')
		self.nominations_summary = Beatmapset.NominationsSummary(json['nominations_summary'])
		self.ranked: RankStatus = RankStatus.from_int(json['ranked'])
		self.ranked_date = optional_datetime(json, 'ranked_date')
		self.source: str = json['source']
		self.storyboard: bool = json['storyboard']
		self.submitted_date = optional_datetime(json, 'submitted_date')
		self.tags: str = json['tags']
		
# https://osu.ppy.sh/docs/#beatmapcompact
class BeatmapCompact:
	# https://osu.ppy.sh/docs/#beatmapcompact-failtimes
	class Failtimes:
		def __init__(self, json: JsonObject):
			self.exit: list[int] | None = json.get('exit')
			self.fail: list[int] | None = json.get('fail')

	def __init__(self, json: JsonObject):
		self.beatmapset_id: int = json['beatmapset_id']
		self.difficulty_rating: float = json['difficulty_rating']
		self.id: int = json['id']
		self.mode: str = json['mode']
		self.status: str = json['status']
		self.total_length: int = json['total_length']
		self.user_id: int = json['user_id']
		self.version: str = json['version']

		# Optional attributes
		self.beatmapset = optional_object(json, 'beatmapset', Beatmapset)
		self.checksum: str | None = json.get('checksum')
		self.failtimes = BeatmapCompact.Failtimes(json['failtimes'])
		self.max_combo: int | None = json.get('max_combo')

# https://osu.ppy.sh/docs/#beatmap
class Beatmap(BeatmapCompact):
	def __init__(self, json: JsonObject):
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
	def __init__(self, json: JsonObject):
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
	return Beatmap(api.get(f'/beatmaps/{id}', access_token).json())

def get_beatmaps(access_token: str, ids: list[int]) -> list[Beatmap]:
	return [Beatmap(o) for o in api.get('/beatmaps', access_token, query_params={ 'ids[]': ids }).json()['beatmaps']]

def get_beatmap_attributes(
	access_token: str,
	id: int,
	mods: Sequence[str] | None = None,
	ruleset: GameMode | None = None,
	ruleset_id: int | None = None
) -> BeatmapDifficultyAttributes:
	body: JsonObject = {}

	if mods is not None:
		body['mods'] = mods
	
	if ruleset is not None:
		body['ruleset'] = ruleset
	
	if ruleset_id is not None:
		body['ruleset_id'] = ruleset_id

	kwargs = {
		'path': f'/beatmaps/{id}/attributes',
		'access_token': access_token,
		'body_json': body
	}

	return BeatmapDifficultyAttributes(api.post(f'/beatmaps/{id}/attributes', access_token, body_json=body).json())
