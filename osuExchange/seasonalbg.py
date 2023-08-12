from osuExchange.structures import SeasonalBackgrounds
from osuExchange import api

# https://osu.ppy.sh/docs/index.html#get-apiv2seasonal-backgrounds
def get_seasonal_backgrounds() -> SeasonalBackgrounds:
	return SeasonalBackgrounds(api.get('/seasonal-backgrounds').json())
