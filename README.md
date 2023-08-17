# osuExchange

![osuExchange Logo](logo.png)

An osu! API wrapper written in Python. Built to give developers a simple and easy-to-use interface to the osu! API.

## Usage

```
pip install osuExchange
```

## Users Endpoints
```Python
# https://osu.ppy.sh/docs/#get-user
def get(self, id_or_username: int | str, *, mode: Optional[GameMode] = None) -> User

# https://osu.ppy.sh/docs/#get-users
def get_many(self, user_ids: list[int]) -> list[UserCompact]

# https://osu.ppy.sh/docs/#get-user-recent-activity
def get_recent_activity(self, user_id: int) -> list[Event]
```

Example code:
```Python
from osuExchange.client import OsuApiClient

# Fill in your credentials down below from the osu website.
api = OsuApiClient(client_id=your_client_id, client_secret=your_client_secret)

# Get User object pertaining to "a sushi roll"
print(api.users.get(10652591))

# Get User object pertaining to "a sushi roll" AND "TrustyTrojan"
print(api.users.get([10652591, 12625512]))

# Get recent activity of user, "a sushi roll"
print(api.users.get_recent_activity(10652591))
```

## Beatmap Endpoints
```Python
# https://osu.ppy.sh/docs/#get-beatmap
def get(self, beatmap_id: int) -> Beatmap
	
# https://osu.ppy.sh/docs/#get-beatmaps
def get_many(self, beatmap_ids: list[int]) -> list[Beatmap]

# https://osu.ppy.sh/docs/#get-beatmap-attributes
def get_difficulty_attributes(self,
    beatmap_id: int, *,
    mods: Optional[Sequence[str]] = None,
    ruleset: Optional[GameMode] = None,
    ruleset_id: Optional[int] = None,
) -> BeatmapDifficultyAttributes
	
# https://osu.ppy.sh/docs/index.html#get-beatmap-scores
def get_scores(self, beatmap_id: int) -> BeatmapScores
	
# https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
def get_score(self, beatmap_id: int, user_id: int) -> BeatmapUserScore
	
# https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
def get_user_scores(self, beatmap_id: int, user_id: int) -> list[Score]
```

Example code:
```Python
from osuExchange.client import OsuApiClient

# Fill in your credentials down below from the osu website.
api = OsuApiClient(client_id=your_client_id, client_secret=your_client_secret)

# Get User object pertaining to a "Get Lucky" beatmap
print(api.beatmaps.get(242326))

# Get User object pertaining to "Get Lucky" AND "Bad Apple!!"
print(api.beatmaps.get_many([242326, 42152]))

# Get recent activity of user, "Bad Apple!!"
print(api.beatmaps.get_difficulty_attributes(42152))

# Return the top scores of "Blue Zenith"
print(api.beatmaps.get_scores(657916))

# Return a score of "Blue Zenith" played by "a sushi roll"
print(api.beatmaps.get_scores(657916, 10652591))

# Returns ALL recorded scores of "Remote Control!" played by "a sushi roll" 
print(get_user_scores(774965, 10652591))
```

## Non-auth Endpoints:
```Python
# https://osu.ppy.sh/docs/#get-changelog-build
def get_changelog_build(stream: str, build: str) -> Build

# https://osu.ppy.sh/docs/index.html#get-apiv2seasonal-backgrounds
def get_seasonal_backgrounds() -> SeasonalBackgrounds
```

Exmaple Code:
```Python
from osuExchange.unauth_endpoints import *

print(get_changelog_build("stable40" , "20210520.2"))

print(get_seasonal_backgrounds().backgrounds[1])
```


## Building

Install necessary packages:

```
pip install build
```

Run this command inside of the osuExchange environment:

```
python -m build
```
