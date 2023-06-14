from requests import ( get as requests_get, Response )

BASE_URL = 'https://osu.ppy.sh/api/v2'

HEADERS_JSON = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def get(
    access_token: str,
    path: str,
    body_json: dict[str, *] | None = None
) -> Response:
    headers = HEADERS_JSON.copy()
    headers['Authorization'] = f'Bearer {access_token}'
    return requests_get(BASE_URL + path, data=body_json, headers=headers)
