import requests

DEFAULT_BASE_URI = "http://api.brewerydb.com/v2"
BASE_URI = ""
API_KEY = ""

simple_endpoints = ["beers", "breweries", "categories", "events",
                    "featured", "features", "fluidsizes", "glassware",
                    "locations", "guilds", "heartbeat", "ingredients",
                    "search", "search/upc", "socialsites", "styles"]

single_param_endpoints = ["beer", "brewery", "category", "event",
                          "feature", "glass", "guild", "ingredient",
                          "location", "socialsite", "style", "menu"]

complex_endpoints = ["event:breweries", "event:beers", "beer;events", 
                     "brewery:events"]

double_param_endpoints = ["event:brewery", "event:beer"]

class BreweryDb:

    @staticmethod
    def __make_simple_endpoint_fun(name, method = 'get'):
        @staticmethod
        def _function(options={}):
            if method == 'post':
                return BreweryDb._post("/" + name, options)
            else:
                return BreweryDb._get("/" + name, options)
        return _function

    @staticmethod
    def __make_singlearg_endpoint_fun(name, method = 'get'):
        @staticmethod
        def _function(id, options={}):
            if method == 'post':
                return BreweryDb._post("/" + name + "/" + id, options)
            else:
                return BreweryDb._get("/" + name + "/" + id, options)
        return _function

    @staticmethod
    def __make_complex_endpoint_fun(name, method = 'get'):
        @staticmethod
        def _function(id, options={}):
            if method == 'post':
                return BreweryDb._post("/" + name[0] + "/" + id + "/" + name[1], options)
            else:
                return BreweryDb._get("/" + name[0] + "/" + id + "/" + name[1], options)
        return _function

    @staticmethod
    def __make_doublearg_endpoint_fun(name, method = 'get'):
        @staticmethod
        def _function(base, id, options={}):
            if method == 'post':
                return BreweryDb._post("/" + name[0] + "/" + base + "/" + name[1] + "/" + id, options)
            else:
                return BreweryDb._get("/" + name[0] + "/" + base + "/" + name[1] + "/" + id, options)
        return _function

    @staticmethod
    def _get(request, options):
        options.update({"key" : BreweryDb.API_KEY})
        return requests.get(BreweryDb.BASE_URI + request, params=options).json()

    @staticmethod
    def _post(request, options):
        options.update({"key" : BreweryDb.API_KEY})
        return requests.post(BreweryDb.BASE_URI + request, params=options).json()

    @staticmethod
    def configure(apikey=API_KEY, baseuri=DEFAULT_BASE_URI):
        BreweryDb.API_KEY = apikey
        BreweryDb.BASE_URI = baseuri
        
        for endpoint in simple_endpoints:
            fun = BreweryDb.__make_simple_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
            fun_post = BreweryDb.__make_simple_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_') + '_post', fun_post)
            
        for endpoint in single_param_endpoints:
            fun = BreweryDb.__make_singlearg_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
            fun_post = BreweryDb.__make_singlearg_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_') + '_post', fun_post)
            
        for endpoint in complex_endpoints:
            fun = BreweryDb.__make_complex_endpoint_fun(endpoint.split(':'))
            setattr(BreweryDb, endpoint.replace(':', '_'), fun)
            fun_post = BreweryDb.__make_complex_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace(':', '_') + '_post', fun_post)
            
        for endpoint in double_param_endpoints:
            fun = BreweryDb.__make_doublearg_endpoint_fun(endpoint.split(':'))
            setattr(BreweryDb, endpoint.replace(':', '_'), fun)
            fun_post = BreweryDb.__make_doublearg_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace(':', '_') + '_post', fun_post)
