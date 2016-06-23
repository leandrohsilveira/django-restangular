from http.client import HTTPConnection


class ConnectionTest:
	connection = HTTPConnection("cloud.bry.com.br")
	connection.request("GET", "/home/index.html")
	with connection.getresponse() as response:
		print(response.code)
		print(str(response.read()))