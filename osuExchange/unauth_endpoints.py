from osuExchange import api
from osuExchange.structures import Build, SeasonalBackgrounds

# https://osu.ppy.sh/docs/#get-changelog-build
def get_changelog_build(stream: str, build: str) -> Build:
	return Build(api.get(f'/changelog/{stream}/{build}').json())

# https://osu.ppy.sh/docs/index.html#get-apiv2seasonal-backgrounds
def get_seasonal_backgrounds() -> SeasonalBackgrounds:
	return SeasonalBackgrounds(api.get('/seasonal-backgrounds').json())
