from requests import get
from exception import OsuApiException
from json import JSONEncoder
from models import *

def get_beatmap(id: int, access_token: str) -> Beatmap:
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': f'Bearer {access_token}'
	}

	resp = get(f'https://osu.ppy.sh/api/v2/beatmaps/{id}', headers=headers)

	if resp.status_code >= 400:
		raise OsuApiException(resp)
	
	return Beatmap(resp.json())

def get_beatmap_attributes(
	id: int,
	access_token: str,
	mods: tuple[str],
	ruleset: str,
	ruleset_id: int
) -> BeatmapAttributes:
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json',
		'Authorization': f'Bearer {access_token}'
	}

	json_encoder = JSONEncoder()

	body = {
		'mods': mods,
		
	}