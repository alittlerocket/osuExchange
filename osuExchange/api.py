from requests import (
	get as requests_get,
	post as requests_post,
	Response
)

from osuExchange.typing import JsonObject

class OsuApiException(BaseException):
	def __init__(self, resp: Response):
		super().__init__(f'''
request:
	method: {resp.request.method}
	path: {resp.request.path_url}
	body: {resp.request.body}
response:
	code: {resp.status_code}
	body: {resp.content}
''')


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
	path: str,
	access_token: str | None = None,
	query_params: JsonObject | None = None,
	body_json: JsonObject | None = None
):
	headers = HEADERS_JSON.copy()
	headers['Authorization'] = f'Bearer {access_token}'
	resp = requests_get(BASE_URL + path, query_params, json=body_json, headers=headers)
	open('seasonal_backgrounds.json', 'w').write(resp.text)
	return error_check(resp).json()

def post(
	path: str,
	access_token: str | None = None,
	query_params: JsonObject | None = None,
	body_json: JsonObject | None = None
):
	headers = HEADERS_JSON.copy()
	headers['Authorization'] = f'Bearer {access_token}'
	resp = requests_post(BASE_URL + path, query_params, json=body_json, headers=headers)
	return error_check(resp).json()
