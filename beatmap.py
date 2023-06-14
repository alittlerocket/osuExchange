from api import get
from exception import OsuApiException
from structures import Beatmap, BeatmapAttributes

def get_beatmap(access_token: str, id: int) -> Beatmap:
	resp = get(access_token, f'/beatmaps/{id}')

	if resp.status_code >= 400:
		raise OsuApiException(resp)
	
	return Beatmap(resp.json())

def get_beatmap_attributes(
	access_token: str,
	id: int,

	# Optional parameters
	mods: tuple[str],
	ruleset: str,
	ruleset_id: int
) -> BeatmapAttributes:
	body = {}

	if mods is not None:
		body['mods'] = mods
	if ruleset is not None:
		body['ruleset'] = ruleset
	if ruleset_id is not None:
		body['ruleset_id'] = ruleset_id
	
	resp = get(access_token, f'/beatmaps/{id}/attributes', body_json=body)

	if resp.status_code >= 400:
		raise OsuApiException(resp)
	
	return BeatmapAttributes(resp.json())