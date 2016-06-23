from http.client import HTTPException


class DjangoProvider:

	@staticmethod
	def send_redirect():
		return lambda page: print("Redirect to %(page)s" % {"page": page})

	@staticmethod
	def raise_http_error(message, code=500):
		raise HTTPException(message, code)

class HTTPException(Exception):
	def __init__(self, message, code=500):
		self.message
		self.code