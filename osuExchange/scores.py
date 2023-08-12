from datetime import datetime
from typing import Literal, Optional

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
        self.id: Optional[int] = json.get('id')
        self.best_id: Optional[int] = json.get('best_id')
        self.user_id: int = json['user_id']
        self.accuracy: float = json['accuracy']
        self.mods: list[str] = json['mods'] 
        self.score: int = json['score']
        self.max_combo: int = json['max_combo']
        self.perfect: bool = json['perfect']
        self.statistics: Score.Statistics = json['statistics']
        self.pp: Optional[float] = json.get('pp')
        self.rank: str = json['rank']
        self.created_at: Optional[datetime] = optional_datetime(json, 'created_at')
        self.mode: GameMode = json['mode']
        self.mode_int: int = json['mode_int']
        self.replay: bool = json['replay']
        self.passed: bool = json['passed']
        self.current_user_attributes = json.get('current_user_attributes')

        self.beatmap: Optional[Beatmap] =  optional_object(json, 'beatmap', Beatmap)
        self.beatmapset: Optional[BeatmapsetCompact] = optional_object(json, 'beatmapset', BeatmapsetCompact)
        self.rank_country: Optional[int] = json.get('rank_country')
        self.rank_global: Optional[int] = json.get('rnak_global')
        # self.weight: Weight | None = optional_object(json, 'weight', Weight)
        self.user: Optional[UserCompact] = optional_object(json, 'user', UserCompact)
        self.type: Optional[str] = json.get('type')


#https://osu.ppy.sh/docs/index.html#beatmapuserscore
class BeatmapUserScore:
    def __init__(self, json: JsonObject):
        self.position: int = json['position']
        self.score: Score = json['score']


#https://osu.ppy.sh/docs/index.html#beatmapscores
class BeatmapScores:
    def __init__(self, json: JsonObject):
        self.scores: list[Score] = [Score(o) for o in json['scores']]

        #Note: will be moved to user_score in the future
        self.userScore: Optional[BeatmapUserScore] = json.get('userScore')


def get_beatmap_scores(access_token: str, id: int) -> BeatmapScores:
	return BeatmapScores(api_get(f'/beatmaps/{id}/scores', access_token).json())


def get_user_beatmap_scores(access_token:str, beatmap_id: int, user_id: int) -> list[Score]:
    return [Score(o) for o in api_get(f'/beatmaps/{beatmap_id}/scores/users/{user_id}/all', access_token).json()['scores']]


def get_score(access_token: str, mode: GameMode | str, id: int) -> Score:
    #couldn't figure out path
    return Score(api_get(f'/scores/{mode}/{id}', access_token).json())