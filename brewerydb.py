import requests

DEFAULT_BASE_URI = "http://api.brewerydb.com/v2"
BASE_URI = ""
API_KEY = ""

simple_endpoints = ["beers", "beer/random", "breweries", "categories", "events",
                    "featured", "features", "fluidsizes", "glassware",
                    "locations", "guilds", "heartbeat", "ingredients", "menu", 
                    "search", "search/upc", "socialsites", "styles"]

single_param_endpoints = ["beer", "brewery", "category", "event",
                          "feature", "glass", "guild", "ingredient",
                          "location", "socialsite", "style", "menu"]

complex_endpoints = ["event:breweries", "event:beers", "beer:events", 
                     "brewery:events"]

double_param_endpoints = ["event:brewery", "event:beer"]

class BreweryDb:

    @staticmethod
    def __make_simple_endpoint_fun(name):
        @staticmethod
        def _function(options={}, method = 'get'):
            endpoint = "/" + name
            return BreweryDb._request(endpoint, options, method)
        return _function

    @staticmethod
    def __make_singlearg_endpoint_fun(name):
        @staticmethod
        def _function(id, options={}, method = 'get'):
            endpoint = "/" + name + "/" + id
            return BreweryDb._request(endpoint, options, method)
        return _function

    @staticmethod
    def __make_complex_endpoint_fun(name):
        @staticmethod
        def _function(id, options={}, method = 'get'):
            endpoint = "/" + name[0] + "/" + id + "/" + name[1]
            return BreweryDb._request(endpoint, options, method)
        return _function

    @staticmethod
    def __make_doublearg_endpoint_fun(name):
        @staticmethod
        def _function(base, id, options={}, method = 'get'):
            endpoint = "/" + name[0] + "/" + base + "/" + name[1] + "/" + id
            return BreweryDb._request(endpoint, options, method)
        return _function

    @staticmethod
    def _request(request, options, method):
        options.update({"key" : BreweryDb.API_KEY})
        if method == 'post':
            return requests.post(BreweryDb.BASE_URI + request, params=options).json()
        elif method == 'put':
            return requests.put(BreweryDb.BASE_URI + request, params=options).json()
        elif method == 'delete':
            return requests.delete(BreweryDb.BASE_URI + request, params=options).json()
        else:
            return requests.get(BreweryDb.BASE_URI + request, params=options).json()

    @staticmethod
    def configure(apikey=API_KEY, baseuri=DEFAULT_BASE_URI):
        BreweryDb.API_KEY = apikey
        BreweryDb.BASE_URI = baseuri
        
        for endpoint in simple_endpoints:
            fun = BreweryDb.__make_simple_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
            
        for endpoint in single_param_endpoints:
            fun = BreweryDb.__make_singlearg_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
            
        for endpoint in complex_endpoints:
            fun = BreweryDb.__make_complex_endpoint_fun(endpoint.split(':'))
            setattr(BreweryDb, endpoint.replace(':', '_'), fun)
            
        for endpoint in double_param_endpoints:
            fun = BreweryDb.__make_doublearg_endpoint_fun(endpoint.split(':'))
            setattr(BreweryDb, endpoint.replace(':', '_'), fun)
