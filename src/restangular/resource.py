from src.restangular.provider import DjangoProvider


class WebResource:
	"""
	Base class for process web requests, mapping main http request methods (GET, POST, PUT and DELETE), for other methods override the "other" function.
	"""
	def __init__(self, switch={}):
		self.switch = switch


	def do_request(self, request, **kwargs):
		return self.switch.get(request.method, lambda request, **kwargs: DjangoProvider.raise_http_error("Method %s is not allowed." % request.method, 405))(request, **kwargs)


class PageResource(WebResource):
	"""
	Class to process a page load request
	"""

	template = None
	context = {}


	def get_context(self, **kwargs):
		return self.context


	def get_template(self):
		return self.template


	def get(self, request, **kwargs):
		return DjangoProvider.send_redirect()(request, self.template, self.get_context(**kwargs))


class StandardResources:
	def __init__(self, resource_name, service_resource_name="service"):
		self.resource_name = resource_name
		self.service_resource_name = service_resource_name


class StandardCrudResources(StandardResources):
	def __init__(self, switch={}, nested=None, *args, **kwargs):
		super(StandardCrudResources, self).__init__(*args, **kwargs)
		self.nested = nested
		self.__switch = {
			"GET": self.__handle_get,
			"POST": self.__handle_post,
			"PUT": self.__handle_put,
			"DELETE": self.__handle_delete,
		}
		self.switch = switch
		self.service_resource = WebResource(self.switch)

	allowed_filters = []
	allowed_max = [10, 15, 20]


	@property
	def switch(self):
		return self.__switch


	@switch.setter
	def switch(self, switch):
		self.__switch.update(switch)


	def __extract_id(self, params, **kwargs):
		if kwargs and ("pk" in kwargs or "id" in kwargs):
			if "pk" in kwargs:
				return kwargs["pk"]
			else:
				return kwargs["id"]
		elif params and ("pk" in params or "id" in params):
			if "pk" in params:
				return params["pk"]
			else:
				return params["id"]
		return None


	def __handle_get(self, request, **kwargs):
		id = self.__extract_id(request.GET, kwargs)
		if id:
			return self.find_service(kwargs.get("id", kwargs.get("pk")))
		else:
			first = request.GET.get("first", 0)
			max = request.GET.get("max", 10)
			filters = {}
			for param_name in request.GET:
				if param_name in self.allowed_filters:
					filters[param_name] = request.GET[param_name]

			if not max in self.allowed_max:
				max = 10
			return {
				"data": self.list_service(first, max, filters),
				"count": self.count_service(filters)
			}


	def __handle_post(self, request):
		self.create_service(self, request.POST)


	def __handle_put(self, request, **kwargs):
		id = self.__extract_id(request, kwargs)
		self.update_service(id, request.PUT)


	def __handle_delete(self, request, **kwargs):
		pass


	def find_service(self, id):
		pass


	def list_service(self, first=0, max=10, parameters={}):
		pass


	def count_service(self, **kwargs):
		pass


	def create_service(self, form):
		pass


	def update_service(self, form):
		pass