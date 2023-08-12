from osuExchange.typing import (
	JsonObject, GameMode, ProfilePage,
	optional_datetime, optional_object, optional_object_list,
	Optional, Literal, datetime
)
from osuExchange.enums import RankStatus

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
		self.description: Optional[str] = json.get('description')
		self.discussions = json.get('discussions')
		self.events = json.get('events')
		self.genre = json.get('genre')
		self.has_favorited: Optional[bool] = json.get('has_favourited')
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
			self.more_information: Optional[str] = json.get('more_information')

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
		self.legacy_thread_url: Optional[str] = json.get('legacy_thread_url')
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
			self.exit: Optional[list[int]] = json.get('exit')
			self.fail: Optional[list[int]] = json.get('fail')

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
		self.checksum: Optional[str] = json.get('checksum')
		self.failtimes = BeatmapCompact.Failtimes(json['failtimes'])
		self.max_combo: Optional[int] = json.get('max_combo')

# https://osu.ppy.sh/docs/#beatmap
class Beatmap(BeatmapCompact):
	def __init__(self, json: JsonObject):
		super().__init__(json)
		self.accuracy: float = json['accuracy']
		self.approach_rate: float = json['ar']
		self.bpm: Optional[float] = json.get('bpm')
		self.convert: bool = json['convert']
		self.count_circles: int = json['count_circles']
		self.count_sliders: int = json['count_sliders']
		self.count_spinners: int = json['count_spinners']
		self.circle_size: float = json['cs']
		self.deleted_at = optional_datetime(json, 'deleted_at')
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
		self.approach_rate: Optional[float] = json.get('approach_rate')

		# taiko, mania
		self.great_hit_window: Optional[float] = json.get('great_hit_window')

		# oau
		self.aim_difficulty: Optional[float] = json.get('aim_difficulty')
		self.flashlight_difficulty: Optional[float] = json.get('flashlight_difficulty')
		self.overall_difficulty: Optional[float] = json.get('overall_difficulty')
		self.slider_factor: Optional[float] = json.get('slider_factor')
		self.speed_difficulty: Optional[float] = json.get('speed_difficulty')

		# taiko
		self.stamina_difficulty: Optional[float] = json.get('stamina_difficulty')
		self.rhythm_difficulty: Optional[float] = json.get('rhythm_difficulty')
		self.colour_difficulty: Optional[float] = json.get('colour_difficulty')

# https://osu.ppy.sh/docs/#usercompact
class UserCompact:
	class ProfileBanner:
		def __init__(self, json: JsonObject):
			self.id: int = json['id']
			self.tournament_id: int = json['tournament_id']
			self.image: str = json['image']

	class RankHighest:
		def __init__(self, json: JsonObject):
			self.rank: int = json['rank']
			self.updated_at: datetime = datetime.fromisoformat(json['updated_at'])

	class AccountHistory:
		def __init__(self, json: JsonObject):
			self.description: str = json['description']
			self.id: int = json['id']
			self.length_seconds: int = json['length']
			self.permanent: bool = json['permanent']
			self.timestamp: datetime = datetime.fromisoformat(json['timestamp'])
			self.type: Literal['note', 'restriction', 'silence'] = json['type']

	class Badge:
		def __init__(self, json: JsonObject):
			self.awarded_at: datetime = datetime.fromisoformat(json['awarded_at'])
			self.description: str = json['description']
			self.image_url: str = json['image_url']
			self.url: str = json['url']

	class MonthlyPlaycount:
		def __init__(self, json: JsonObject):
			self.start_date: str = json['start_date']
			self.count: int = json['count']

	class Page:
		def __init__(self, json: JsonObject):
			self.html: str = json['html']
			self.raw: str = json['raw']

	class Country:
		def __init__(self, json: JsonObject):
			self.code: str = json['code']
			self.name: str = json['name']

	class Achievement:
		def __init__(self, json: JsonObject):
			self.achieved_at: datetime = datetime.fromisoformat(json['achieved_at'])
			self.achievement_id: int = json['achievement_id']

	def __init__(self, json: JsonObject):
		self.avatar_url: str = json['avatar_url']
		self.country_code: str = json['country_code']
		self.default_group: Optional[str] = json.get('default_group')
		self.id: int = json['id']
		self.is_active: bool = json['is_active']
		self.is_bot: bool = json['is_bot']
		self.is_deleted: bool = json['is_deleted']
		self.is_online: bool = json['is_online']
		self.is_supporter: bool = json['is_supporter']
		self.last_visit = optional_datetime(json, 'last_visit')
		self.pm_friends_only: bool = json['pm_friends_only']
		self.profile_colour: Optional[str] = json['profile_colour']
		self.username: str = json['username']

		# Optional attributes
		self.account_history = optional_object_list(json, 'account_history', UserCompact.AccountHistory)
		self.active_tournament_banner = optional_object(json, 'active_tournament_banner', UserCompact.ProfileBanner)
		self.badges = optional_object_list(json, 'badges', UserCompact.Badge)
		self.beatmap_playcounts_count: Optional[int] = json.get('beatmap_playcounts_count')
		self.blocks = json.get('blocks')
		self.country = optional_object(json, 'country', UserCompact.Country)
		self.cover = json.get('cover')
		self.favourite_beatmapset_count: Optional[int] = json.get('favourite_beatmapset_count')
		self.follower_count: Optional[int] = json.get('follower_count')
		self.friends = json.get('friends')
		self.graveyard_beatmapset_count: Optional[int] = json.get('graveyard_beatmapset_count')
		#self.groups = json['groups'] # https://osu.ppy.sh/docs/#usergroup not well documented, implement later
		self.is_restricted: Optional[bool] = json.get('is_restricted')
		self.loved_beatmapset_count: Optional[int] = json.get('loved_beatmapset_count')
		self.monthly_playcounts = optional_object_list(json, 'monthly_playcounts', UserCompact.MonthlyPlaycount)
		self.page = optional_object(json, 'page', UserCompact.Page)
		self.pending_beatmapset_count: Optional[int] = json.get('pending_beatmapset_count')
		self.previous_usernames: Optional[list[str]] = json.get('previous_usernames')
		self.rank_highest = optional_object(json, 'rank_highest', UserCompact.RankHighest)
		#self.rank_history
		self.ranked_beatmapset_count: Optional[int] = json.get('ranked_beatmapset_count')
		self.replays_watched_counts: Optional[int] = json.get('replays_watched_counts')
		self.scores_best_count: Optional[int] = json.get('scores_best_count')
		self.scores_first_count: Optional[int] = json.get('scores_first_count')
		self.scores_recent_count: Optional[int] = json.get('scores_recent_count')
		#self.statistics
		#self.statistics_rulesets
		self.support_level: Optional[int] = json.get('support_level')
		self.unread_pm_count: Optional[int] = json.get('unread_pm_count')
		self.user_achievements = optional_object_list(json, 'user_achievements', UserCompact.Achievement)
		#self.user_preferences

# https://osu.ppy.sh/docs/#user
class User(UserCompact):
	class Cover:
		def __init__(self, json: JsonObject):
			self.custom_url: str = json['custom_url']
			self.url: str = json['url']
			self.id = json['id']

	class Kudosu:
		def __init__(self, json: JsonObject):
			self.total: int = json['total']
			self.available: int = json['available']

	def __init__(self, json: JsonObject):
		super().__init__(json)
		self.discord: Optional[str] = json.get('discord')
		self.has_supported: bool = json['has_supported']
		self.interests: Optional[str] = json.get('interests')
		self.join_date: datetime = json['join_date']
		self.kudosu = User.Kudosu(json['kudosu'])
		self.location: Optional[str] = json.get('location')
		self.max_blocks: int = json['max_blocks']
		self.max_friends: int = json['max_friends']
		self.occupation: Optional[str] = json.get('occupation')
		self.playmode: GameMode = json['playmode']
		self.playstyle: list[str] = json['playstyle']
		self.post_count: int = json['post_count']
		self.profile_order: list[ProfilePage] = json['profile_order']
		self.title: Optional[str] = json.get('title')
		self.title_url: Optional[str] = json.get('title_url')
		self.twitter: Optional[str] = json.get('twitter')
		self.website: Optional[str] = json.get('website')

# https://osu.ppy.sh/docs/#event-user
class EventUser:
	def __init__(self, json: JsonObject):
		self.username: str = json['username']
		self.url: str = json['url']
		self.previous_username: Optional[str] = json['previousUsername']

# https://osu.ppy.sh/docs/#event-beatmap
class EventBeatmap:
	def __init__(self, json: JsonObject):
		self.title: str = json['title']
		self.url: str = json['url']

# https://osu.ppy.sh/docs/#event-beatmapset
class EventBeatmapset:
	def __init__(self, json: JsonObject):
		self.title: str = json['title']
		self.url: str = json['url']

# https://osu.ppy.sh/docs/#event
class Event:
	# https://osu.ppy.sh/docs/#event-type
	Type = Literal[
		'achievement',
		'beatmapPlaycount',
		'beatmapsetApprove',
		'beatmapsetDelete',
		'beatmapsetRevive',
		'beatmapsetUpdate',
		'beatmapsetUpload',
		'rank',
		'rankLost',
		'userSupportAgain',
		'userSupportFirst',
		'userSupportGift',
		'usernameChange'
	]

	def __init__(self, json: JsonObject):
		# these attributes are always present
		self.created_at = datetime.fromisoformat(json['created_at'])
		self.id: int = json['id']
		self.type: Event.Type = json['type']

		## shared between several events
		self.mode: Optional[GameMode] = json.get('mode')

		

		beatmap = json.get('beatmap')
		self.beatmap = EventBeatmap(beatmap) if beatmap else None

		beatmapset = json.get('beatmapset')
		self.beatmapset = EventBeatmapset(beatmapset) if beatmapset else None

		user = json.get('user')
		self.user = EventUser(user) if user else None

		## achievement
		achievement = json.get('achievement')
		self.achievement = User.Achievement(achievement) if achievement else None
		# self.user

		## beatmapPlaycount
		# self.beatmap
		self.count = json.get('count')		

		## beatmapsetApprove
		self.approval: Optional[Literal['ranked', 'approved', 'qualified', 'loved']] = json.get('approval')
		# self.beatmapset
		# self.user

		## beatmapsetDelete
		# self.beatmapset

		## beatmapsetRevive
		# self.beatmapset
		# self.user

		## beatmapsetUpdate
		# self.beatmapset
		# self.user

		## beatmapsetUpload
		# self.beatmapset
		# self.user

		## rank
		# scoreRank???????????????
		self.rank: Optional[int] = json.get('rank')
		# self.beatmap
		# self.user
		# self.mode

		## rankLost
		# self.mode
		# self.beatmap
		# self.user

		## userSupportAgain
		# self.user

		## userSupportFirst
		# self.user

		## userSupportGift
		# self.user

		## usernameChange
		# self.user

# https://osu.ppy.sh/docs/index.html#score
class Score:
	class Statistics:
		def __init__(self, json: JsonObject):
			self.count_50: int = json['count_50']
			self.count_100: int = json['count_100']
			self.count_300: int = json['count_300']
			self.count_geki: int = json['count_geki']
			self.count_katu: int = json['count_katu']
			self.count_miss: int = json['count_miss']

	def __init__(self, json: JsonObject):
		self.id: Optional[int] = json.get('id')
		self.best_id: Optional[int] = json.get('best_id')
		self.user_id: int = json['user_id']
		self.accuracy: float = json['accuracy']
		self.mods: list[str] = json['mods']
		self.score: int = json['score']
		self.max_combo: int = json['max_combo']
		self.perfect: bool = json['perfect']
		self.statistics: Score.Statistics = json['statistics']
		self.pp: Optional[float] = json.get('pp')
		self.rank: str = json['rank']
		self.created_at = optional_datetime(json, 'created_at')
		self.mode: GameMode = json['mode']
		self.mode_int: int = json['mode_int']
		self.replay: bool = json['replay']
		self.passed: bool = json['passed']
		self.current_user_attributes = json.get('current_user_attributes')

		# Optional attributes
		self.beatmap = optional_object(json, 'beatmap', Beatmap)
		self.beatmapset = optional_object(json, 'beatmapset', BeatmapsetCompact)
		self.rank_country: Optional[int] = json.get('rank_country')
		self.rank_global: Optional[int] = json.get('rank_global')
		# self.weight = optional_object(json, 'weight', Weight)
		self.user = optional_object(json, 'user', UserCompact)
		self.type: Optional[str] = json.get('type')

#https://osu.ppy.sh/docs/index.html#beatmapuserscore
class BeatmapUserScore:
	def __init__(self, json: JsonObject):
		self.position: int = json['position']
		self.score = Score(json['score'])

#https://osu.ppy.sh/docs/index.html#beatmapscores
class BeatmapScores:
	def __init__(self, json: JsonObject):
		self.scores: list[Score] = [Score(o) for o in json['scores']]
		self.userScore = optional_object(json, 'userScore', BeatmapUserScore)

class SeasonalBackgrounds:
	"""Represents a Seasonal Backgrounds object from the osu! API."""

	class Background:
		def __init__(self, json: JsonObject):
			self.url: str = json['url']
			self.user = UserCompact(json['user'])

	def __init__(self, json: JsonObject):
		self.ends_at = datetime.fromisoformat(json['ends_at'])
		self.backgrounds = [SeasonalBackgrounds.Background(o) for o in json['backgrounds']]
