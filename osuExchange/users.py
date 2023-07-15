from datetime import datetime
from typing import Literal

from osuExchange.api import get as api_get
from osuExchange.util import optional_object_list, optional_object, optional_datetime
from osuExchange.typing import GameMode, JsonObject, ProfilePage

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
		self.default_group: str | None = json.get('default_group')
		self.id: int = json['id']
		self.is_active: bool = json['is_active']
		self.is_bot: bool = json['is_bot']
		self.is_deleted: bool = json['is_deleted']
		self.is_online: bool = json['is_online']
		self.is_supporter: bool = json['is_supporter']
		self.last_visit = optional_datetime(json, 'last_visit')
		self.pm_friends_only: bool = json['pm_friends_only']
		self.profile_colour: str | None = json['profile_colour']
		self.username: str = json['username']

		# Optional attributes
		self.account_history = optional_object_list(json, 'account_history', UserCompact.AccountHistory)
		self.active_tournament_banner = optional_object(json, 'active_tournament_banner', UserCompact.ProfileBanner)
		self.badges = optional_object_list(json, 'badges', UserCompact.Badge)
		self.beatmap_playcounts_count: int | None = json.get('beatmap_playcounts_count')
		self.blocks = json.get('blocks')
		self.country = optional_object(json, 'country', UserCompact.Country)
		self.cover = json.get('cover')
		self.favourite_beatmapset_count: int | None = json.get('favourite_beatmapset_count')
		self.follower_count: int | None = json.get('follower_count')
		self.friends = json.get('friends')
		self.graveyard_beatmapset_count: int | None = json.get('graveyard_beatmapset_count')
		#self.groups = json['groups'] # https://osu.ppy.sh/docs/#usergroup not well documented, implement later
		self.is_restricted: bool | None = json.get('is_restricted')
		self.loved_beatmapset_count: int | None = json.get('loved_beatmapset_count')
		self.monthly_playcounts = optional_object_list(json, 'monthly_playcounts', UserCompact.MonthlyPlaycount)
		self.page = optional_object(json, 'page', UserCompact.Page)
		self.pending_beatmapset_count: int | None = json.get('pending_beatmapset_count')
		self.previous_usernames: list[str] | None = json.get('previous_usernames')
		self.rank_highest = optional_object(json, 'rank_highest', UserCompact.RankHighest)
		#self.rank_history
		self.ranked_beatmapset_count: int | None = json.get('ranked_beatmapset_count')
		self.replays_watched_counts: int | None = json.get('replays_watched_counts')
		self.scores_best_count: int | None = json.get('scores_best_count')
		self.scores_first_count: int | None = json.get('scores_first_count')
		self.scores_recent_count: int | None = json.get('scores_recent_count')
		#self.statistics
		#self.statistics_rulesets
		self.support_level: int | None = json.get('support_level')
		self.unread_pm_count: int | None = json.get('unread_pm_count')
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
		self.discord: str | None = json.get('discord')
		self.has_supported: bool = json['has_supported']
		self.interests: str | None = json.get('interests')
		self.join_date: datetime = json['join_date']
		self.kudosu = User.Kudosu(json['kudosu'])
		self.location: str | None = json.get('location')
		self.max_blocks: int = json['max_blocks']
		self.max_friends: int = json['max_friends']
		self.occupation: str | None = json.get('occupation')
		self.playmode: GameMode = json['playmode']
		self.playstyle: list[str] = json['playstyle']
		self.post_count: int = json['post_count']
		self.profile_order: list[ProfilePage] = json['profile_order']
		self.title: str | None = json.get('title')
		self.title_url: str | None = json.get('title_url')
		self.twitter: str | None = json.get('twitter')
		self.website: str | None = json.get('website')

# def get_user_beatmaps(
#     access_token: str,
#     user: int,
#     type: str,
#     limit: int | None = None,
#     offset: str | None = None
# ) -> list[BeatmapPlaycount] | list[Beatmapset]:
#     resp = get(access_token, f'/users/{user}/beatmapsets/{type}')
#     if resp.status_code >= 400:
#         raise OsuApiException(resp)
#     return resp.json()

# https://osu.ppy.sh/docs/#get-user
def get_user(
	access_token: str,
	id: int,
	mode: GameMode | None = None,
	key: Literal['id', 'username'] | None = None
) -> User:
	path = f'/users/{id}'

	if mode is not None:
		path += f'/{mode}'
	
	if key is not None:
		path += f'?key={key}'
	
	return User(api_get(access_token, path).json())

# https://osu.ppy.sh/docs/#get-users
def get_users(
	access_token: str,
	ids: list[int]
) -> list[UserCompact]:
	return [UserCompact(o) for o in api_get(access_token, '/users', { 'ids[]': ids }).json()['users']]
