#1st party pre-installed libraries
import json
import logging
from typing import Dict, Union, List
from functools import wraps

#3rd party libraries *from the requests installation*
import requests

def filter_params_decorator(func):
    @wraps(func)
    def wrapper(url: str, params: Dict[str, str] = None, *args, **kwargs):
        filtered_params = {k: v for k, v in params.items() if v} if params else {}
        if filtered_params and 'q' in filtered_params and isinstance(filtered_params['q'], dict):
            filtered_params['q'] = json.dumps({k: v for k, v in filtered_params['q'].items() if v})
        return func(url, filtered_params, *args, **kwargs)
    return wrapper

@filter_params_decorator
def get_website(url: str, params: Dict[str, str] = None) -> requests.Response:
    return __check_status(requests.get(url, params=params), params)

@filter_params_decorator
def post_website(url: str, params: Dict[str, str] = None) -> requests.Response:
    return __check_status(requests.post(url, data=params), params)

def __check_status(req_response: requests.Response, params: Dict[str, str] = None) -> requests.Response:
    try:
        req_response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed call to webpage: {e}")
        logging.error(f"Error: {req_response.status_code}")
        if params:
            logging.error(f"Caused by searching: {params}")
        logging.error(f"Response content: {req_response.text}")
        
    return req_response