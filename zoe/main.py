import endpoint

api_url = "Your API Endpoint URL."
bearer_token = "If required, please include your Bearer Token."

openapi_dict = endpoint.obtain_openapi_dict(api_url)
api_endpoints = endpoint.list_api_endpoints(openapi_dict, api_url)
endpoint.test_api_endpoints(api_endpoints, bearer_token)
