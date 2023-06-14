from requests import Response

class OsuApiException(BaseException):
	def __init__(self, resp: Response):
		super().__init__(f'\nrequest:\n\tmethod: {resp.request.method}\n\tpath: {resp.request.path_url}\n\tbody: {resp.request.body}\nresponse:\n\tcode: {resp.status_code}\n\tbody: {resp.content}')