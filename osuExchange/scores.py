from datetime import datetime

from osuExchange.api import get as api_get
from osuExchange.util import optional_object, optional_datetime
from osuExchange.typing import GameMode, JsonObject
from osuExchange.beatmaps import Beatmap, BeatmapsetCompact
from osuExchange.users import UserCompact

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
    
    # class GameMode:
    #     def __init__(self, json: JsonObject):

    # class Weight:
    #     def __init__(self, json: JsonObject):
    

    def __init__(self, json: JsonObject):
        self.id: int | None = json.get('id')
        self.best_id: int | None = json.get('best_id')
        self.user_id: int = json['user_id']
        self.accuracy: float = json['accuracy']
        self.mods: list[str] = json['mods'] 
        self.score: int = json['score']
        self.max_combo: int = json['max_combo']
        self.perfect: bool = json['perfect']
        self.statistics: Score.Statistics = json['statistics']
        self.pp: float | None = json.get('pp')
        self.rank: str = json['rank']
        self.created_at: datetime | None = optional_datetime(json, 'created_at')
        self.mode: GameMode = json['mode']
        self.mode_int: int = json['mode_int']
        self.replay: bool = json['replay']
        self.passed: bool = json['passed']
        self.current_user_attributes = json.get('current_user_attributes')

        self.beatmap: Beatmap | None =  optional_object(json, 'beatmap', Beatmap)
        self.beatmapset: BeatmapsetCompact | None = optional_object(json, 'beatmapset', BeatmapsetCompact)
        self.rank_country: int | None = json.get('rank_country')
        self.rank_global: int | None = json.get('rnak_global')
        # self.weight: Weight | None = optional_object(json, 'weight', Weight)
        self.user: UserCompact | None = optional_object(json, 'user', UserCompact)
        self.type: str | None = json.get('type')