from typing import Literal, Any

JsonObject = dict[str, Any]
GameMode = Literal['fruits', 'mania', 'osu', 'taiko']
ProfilePage = Literal['me', 'recent_activity', 'beatmaps', 'historical', 'kudosu', 'top_ranks', 'medals']
