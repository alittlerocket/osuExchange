from enum import Enum

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

class OAuth2Scope(Enum):
	CHAT_WRITE = 'chat.write'
	DELEGATE = 'delegate'
	FORUM_WRITE = 'forum.write'
	FRIENDS_READ = 'friends.read'
	IDENTIFY = 'identify'
	PUBLIC = 'public'
