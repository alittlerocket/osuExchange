from datetime import datetime

from osuExchange.api import get as api_get
from osuExchange.typing import JsonObject
from osuExchange.users import UserCompact

class SeasonalBackgrounds:
	class Background:
		def __init__(self, json: JsonObject):
			self.url = json['url']
			self.user = UserCompact(json['user'])

	def __init__(self, json: JsonObject):
		self.ends_at = datetime.fromisoformat(json['ends_at'])
		self.backgrounds = [SeasonalBackgrounds.Background(o) for o in json['backgrounds']]

def get_seasonal_backgrounds(access_token: str) -> SeasonalBackgrounds:
	return SeasonalBackgrounds(api_get('/seasonal-backgrounds', access_token))
