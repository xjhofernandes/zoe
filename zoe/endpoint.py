import json
import time

import requests
from requests.models import Response


def request_api_endpoints(
        endpoint: str,
        method: str,
        encoded_headers=None,
        data=None
) -> Response:
    """
    Perform a request to the specified API endpoint.

    Parameters:
        endpoint: str
            the URL to send the request to.
        method: str
            the HTTP method to use for the request.
        encoded_headers: optional
            the headers to include in the request.
        data: optional
            the data to send in the request.

    Returns:
        Response
            The response object from the request.
    """
    response = requests.request(
        method,
        headers=encoded_headers,
        url=endpoint,
        data=data
    )

    return response


def obtain_openapi_dict(api_url: str) -> dict:
    """
    Obtain the OpenAPI specification from the specified URL.

    Parameters:
        api_url: str
            the URL to send the request to.

    Returns:
        dict
            the OpenAPI specification as a dictionary.
    """
    api_url += "/openapi.json"
    contents = requests.get(api_url)
    try:
        openapi_dict = contents.json()

        return openapi_dict
    except Exception as e:
        print(f"Error: {e}")


def list_all_http_methods(api_path: dict) -> list[str]:
    """
    Obtain a list of all HTTP methods defined in the OpenAPI specification.

    Returns:
        List[str]
            List of all HTTP methods defined in the OpenAPI specification.
    """
    return api_path.keys()


def obtain_get_endpoint(api_endpoint: str, api_dict: dict) -> dict:
    """
    Obtain the endpoint dictionary for a GET request.

    Parameters:
        api_endpoint: str
            the URL to send the request to.
        api_dict: dict
            the OpenAPI specification as a dictionary.

    Returns:
        dict
            the endpoint dictionary for a GET request.
    """
    first_query_paramn = True
    for parameter in api_dict["parameters"]:
        if parameter["in"] == "path":
            api_endpoint = api_endpoint.replace(
                "{" + parameter["name"] + "}", str(
                    parameter["schema"]["const"]
                )
            )

        elif parameter["in"] == "query":
            if first_query_paramn:
                api_endpoint = api_endpoint + "?"
                first_query_paramn = False
            else:
                api_endpoint = api_endpoint + "&"
            if "schema" in parameter.keys():
                if "const" in parameter["schema"].keys():
                    api_endpoint = api_endpoint + parameter["name"] + "=" + str(parameter["schema"]["const"])  # noqa: E501
                elif "default" in parameter["schema"].keys():
                    api_endpoint = api_endpoint + parameter["name"] + "=" + str(parameter["schema"]["default"])  # noqa: E501
                else:
                    api_endpoint = api_endpoint + parameter["name"] + "=" + str(parameter["example"])  # noqa: E501

    endpoint_dict = {
        "url": api_endpoint,
        "method": "GET",
        "data": None
    }

    return endpoint_dict


def generate_endpoint_dict(
        api_endpoint: str,
        api_dict: dict,
        method: str
) -> list:
    """
    Generate an endpoint dictionary based on the given
    API endpoint, API dictionary, and method.

    Parameters:
        api_endpoint : str
            The URL to send the request to.
        api_dict : dict
            The OpenAPI specification as a dictionary.
        method : str
            The HTTP method to use for the request.

    Returns:
        list
            The endpoint dictionary for the specified method.

    Note:
        - This function currently only supports the "GET" method.
        Support for other methods will be added in future iterations.
    """
    if method.lower() == "get":
        endpoint_dict = obtain_get_endpoint(api_endpoint, api_dict)

        return endpoint_dict
    elif method.lower() == "post":
        # TBD - add support for POST

        return None
    elif method.lower() == "patch":
        # TBD - add support for POST

        return None
    elif method.lower() == "put":
        # TBD - add support for PUT

        return None
    elif method.lower() == "delete":
        # TBD - add support for PUT

        return None
    else:
        raise ValueError(f"Invalid method: {method}")


def list_api_endpoints(api_dict: dict, api_url: str) -> list:
    """
    List all API endpoints in the OpenAPI specification.

    Parameters:
        api_dict: dict
            the OpenAPI specification as a dictionary.
        api_url: str
            the URL to send the request to.

    Returns:
        list
            the list of API endpoints in the OpenAPI specification.
    """
    api_endpoints = []

    for path in api_dict["paths"]:
        path_http_methods = list_all_http_methods(api_dict["paths"][path])

        for method in path_http_methods:
            new_path = api_url + path
            endpoint_dict = generate_endpoint_dict(
                new_path, api_dict["paths"][path][method], method
            )

            print(endpoint_dict)
            api_endpoints.append(endpoint_dict)

    return api_endpoints


def test_api_endpoints(
        api_endpoints: list,
        bearer_token: str = None
) -> None:
    for endpoint in api_endpoints:
        if bearer_token is not None:
            headers = {
                "Authorization": f"Bearer {bearer_token}"
            }
            encoded_headers = {key.encode('utf-8'): value.encode('utf-8') for key, value in headers.items()}  # noqa: E501
        else:
            encoded_headers = None

        try:
            start_time = time.perf_counter()
            response = request_api_endpoints(
                endpoint["url"],
                method=endpoint["method"],
                data=endpoint["data"],
                encoded_headers=encoded_headers
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000
            response.close()

            url = endpoint["url"]
            method = endpoint["url"]

            print(f"Checked: {url} ({method})")
            print(f"Status: {response.status_code} (took {elapsed_ms:.2f} ms)")
        except json.JSONDecodeError:
            print("Error: Invalid JSON data")
        except Exception as e:
            print(f"Error: {e}")
