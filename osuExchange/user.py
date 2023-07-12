from api import get
from exception import OsuApiException
from datetime import datetime

class UserCompact:
	def __init__(self, json: dict):
		self.avatar_url: str = json['avatar_url']
		self.country_code: str = json['country_code']
		self.default_group: str = json['default_group']
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

class Covers:
	def __init__(self, json: dict):
		self.cover: str = json['cover']
		self.cover_2x: str = json['cover@2x']
		self.card: str = json['card']
		self.card_2x: str = json['card@2x']
		self.list: str = json['list']
		self.list_2x: str = json['list@2x']
		self.slimcover: str = json['slimcover']
		self.slimcover_2x: str = json['slimcover@2x']

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

def get_user_beatmaps(
    access_token: str,
    user: int,
    type: str,
    limit: int | None = None,
    offset: str | None = None
) -> list[BeatmapPlaycount] | list[Beatmapset]:
    resp = get(access_token, f'/users/{user}/beatmapsets/{type}')

    if resp.status_code >= 400:
        raise OsuApiException(resp)
    
    return resp.json()

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