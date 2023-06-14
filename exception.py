from requests import Response

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