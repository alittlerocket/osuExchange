from datetime import datetime
from typing import Literal

from osuExchange.api import get as api_get
from osuExchange.util import optional_object, optional_datetime
from osuExchange.typing import GameMode, JsonObject
from osuExchange.beatmaps import Beatmap, BeatmapsetCompact
from osuExchange.users import UserCompact, User


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
        self.userScore: BeatmapUserScore | None = json.get('userScore')

#Not sure if this is needed
#https://circleguard.github.io/ossapi/appendix.html#ossapi.replay.Replay
class Replay:
    def __init__(self, json: JsonObject):
        self.beatmap: Beatmap
        self.user: User

def get_beatmap_scores(access_token: str, id: int) -> BeatmapScores:
	return BeatmapScores(api_get(f'/beatmaps/{id}/scores', access_token).json())


def get_user_beatmap_scores(access_token:str, beatmap_id: int, user_id: int) -> list[Score]:
    return [Score(o) for o in api_get(f'/beatmaps/{beatmap_id}/scores/users/{user_id}/all', access_token).json()['scores']]


def get_score(access_token: str, mode: GameMode | str, id: int) -> Score:
    #couldn't figure out path
    return Score(api_get(f'/scores/{mode}/{id}', access_token).json())

def download_score(access_token: str, mode: GameMode | str, id: int, raw: Literal[False]) -> Replay:
    #couldn't figure out path
    return Replay(api_get(f'/scores/{mode}/{id}/download', access_token).json())