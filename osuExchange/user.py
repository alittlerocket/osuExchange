from api import get
from exception import OsuApiException
from datetime import datetime
from typing import Literal
from osuExchange.util import list_of_objects_or_none, object_or_none

# https://osu.ppy.sh/docs/#usercompact
class UserCompact:
	class ProfileBanner:
		def __init__(self, json: dict):
			self.id: int = json['id']
			self.tournament_id: int = json['tournament_id']
			self.image: str = json['image']

	class RankHighest:
		def __init__(self, json: dict):
			self.rank: int = json['rank']
			self.updated_at: datetime = datetime.fromisoformat(json['updated_at'])

	class AccountHistory:
		def __init__(self, json: dict):
			self.description: str = json['description']
			self.id: int = json['id']
			self.length_seconds: int = json['length']
			self.permanent: bool = json['permanent']
			self.timestamp: datetime = datetime.fromisoformat(json['timestamp'])
			self.type: Literal['note', 'restriction', 'silence'] = json['type']

	class Badge:
		def __init__(self, json: dict):
			self.awarded_at: datetime = datetime.fromisoformat(json['awarded_at'])
			self.description: str = json['description']
			self.image_url: str = json['image_url']
			self.url: str = json['url']

	class MonthlyPlaycount:
		def __init__(self, json: dict):
			self.start_date: str = json['start_date']
			self.count: int = json['count']

	class Page:
		def __init__(self, json: dict):
			self.html: str = json['html']
			self.raw: str = json['raw']

	def __init__(self, json: dict):
		self.avatar_url: str = json['avatar_url']
		self.country_code: str = json['country_code']
		self.default_group: str | None = json['default_group']
		self.id: int = json['id']
		self.is_active: bool = json['is_active']
		self.is_bot: bool = json['is_bot']
		self.is_deleted: bool = json['is_deleted']
		self.is_online: bool = json['is_online']
		self.is_supporter: bool = json['is_supporter']
		self.last_visit: datetime = datetime.fromisoformat(json['last_visit'])
		self.pm_friends_only: bool = json['pm_friends_only']
		self.profile_colour: str | None = json['profile_colour']
		self.username: str = json['username']
		
		# Optional attributes
		self.account_history = [UserCompact.AccountHistory(o) for o in json['account_history']]
		self.active_tournament_banner = object_or_none(json['active_tournament_banner'], UserCompact.ProfileBanner)
		self.badges = [UserCompact.Badge(o) for o in json['badges']]
		self.beatmap_playcounts_count: int = json['beatmap_playcounts_count']
		self.blocks = json['blocks']
		self.country = json['country']
		self.cover = json['cover']
		self.favourite_beatmapset_count: int = json['favourite_beatmapset_count']
		self.follower_count: int = json['follower_count']
		self.friends = json['friends']
		self.graveyard_beatmapset_count = json['graveyard_beatmapset_count']
		self.groups = json['groups'] # https://osu.ppy.sh/docs/#usergroup not well documented, implement later
		self.is_restricted: bool | None = json['is_restricted']
		self.loved_beatmapset_count: int = json['loved_beatmapset_count']
		self.monthly_playcounts = [UserCompact.MonthlyPlaycount(o) for o in json['monthly_playcounts']]
		self.page = UserCompact.Page(json['page'])
		self.pending_beatmapset_count: int = json['pending_beatmapset_count']
		self.previous_usernames: list[str] = json['previous_usernames']
		self.rank_highest = object_or_none(json['rank_highest'], UserCompact.RankHighest)
		#self.rank_history ... 

# https://osu.ppy.sh/docs/#user
class User(UserCompact):
	def __init__(self, json: dict):
		super().__init__(json)
		self.cover_url: str = json['cover_url'] #deprecated user cover.url instead
		self.discord: str | None = json['discord']
		self.has_supported: bool = json['has_supported']
		self.interests: str | None = json['interests']
		self.join_date: datetime = datetime.fromisoformat(json['join_date'])
		#self.kudosu_available: int = json['kudosu_available']
		#self.kudosu_total: int = json['kudosu_total']
		self.location: str | None = json['location']
		self.max_blocks: int = json['max_blocks']
		self.max_friends: int = json['max_friends']
		self.occupation: str | None = json['occupation']
		#self.playmode: 
		self.playstyle: list [str] = json['playstyle']
		self.post_count: int = json['post_count']
		#self.profile_order:
		self.title: str | None = json['title']
		self.title_url: str | None = json['title_url']
		self.twitter: str | None = json['twitter']
		self.website: str | None = json['website']

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

def get_user(
    access_token: str,
    user: int,
    mode: str | None = None,
    key: str | None = None
) -> User:
    resp = get(access_token, f'/users/{user}/{mode}')

    if resp.status_code >= 400:
        raise OsuApiException(resp)
    
    return User(resp.json())

# def get_users(
#     access_token: str,
#     ids: list[int]
# ) -> list[UserCompact]:
#     resp = get(access_token, f'/users')

#     if resp.status_code >= 400:
#         raise OsuApiException(resp)
    
#     return 