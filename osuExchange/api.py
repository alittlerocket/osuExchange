from osuExchange.typing import JsonObject, Optional
import requests

class OsuApiException(BaseException):
	def __init__(self, resp: requests.Response):
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

DEFAULT_HEADERS = {
	'Accept': 'application/json',
	'Content-Type': 'application/json'
}

def error_check(resp: requests.Response) -> requests.Response:
	if resp.status_code >= 400:
		raise OsuApiException(resp)
	return resp

def make_headers(token: Optional[str]) -> dict[str, str]:
	if token:
		headers = DEFAULT_HEADERS.copy()
		headers['Authorization'] = f'Bearer {token}'
		return headers
	return DEFAULT_HEADERS

def get(
	path: str, *,
	token: Optional[str] = None,
	params: Optional[JsonObject] = None,
	json: Optional[JsonObject] = None
) -> requests.Response:
	return error_check(requests.get(BASE_URL + path, params, json=json, headers=make_headers(token)))

def post(
	path: str, *,
	token: Optional[str] = None,
	params: Optional[JsonObject] = None,
	json: Optional[JsonObject] = None
) -> requests.Response:
	return error_check(requests.post(BASE_URL + path, params, json=json, headers=make_headers(token)))

def delete(
	path: str, *,
	token: Optional[str] = None,
	params: Optional[JsonObject] = None,
	json: Optional[JsonObject] = None
) -> requests.Response:
	return error_check(requests.delete(BASE_URL + path, params=params, json=json, headers=make_headers(token)))
