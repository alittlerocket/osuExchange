from requests import (
	get as requests_get,
	post as requests_post,
	Response
)

from typing import Any
from osuExchange.exception import OsuApiException

BASE_URL = 'https://osu.ppy.sh/api/v2'

HEADERS_JSON = {
	'Accept': 'application/json',
	'Content-Type': 'application/json'
}

def error_check(resp: Response) -> Response:
	if resp.status_code >= 400:
		raise OsuApiException(resp)
	return resp

def get(
	access_token: str,
	path: str,
	query_params: dict[str, Any] | None = None,
	body_json: dict[str, Any] | None = None
):
	headers = HEADERS_JSON.copy()
	headers['Authorization'] = f'Bearer {access_token}'
	resp = requests_get(BASE_URL + path, query_params, json=body_json, headers=headers)
	return error_check(resp).json()

def post(
	access_token: str,
	path: str,
	query_params: dict[str, Any] | None = None,
	body_json: dict[str, Any] | None = None
):
	headers = HEADERS_JSON.copy()
	headers['Authorization'] = f'Bearer {access_token}'
	resp = requests_post(BASE_URL + path, query_params, json=body_json, headers=headers)
	return error_check(resp).json()
