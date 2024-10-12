#1st party pre-installed libraries
import json
import logging
import os
from typing import Optional, Dict, Union, List

#3rd party libraries *from the requests installation*
import requests

def get_website(url: str, search_params: Union[Dict[str, str], None] = None) -> requests.Response:
    filtered_params = dict()
    if search_params:
        filtered_params = {k: v for k, v in search_params.items() if v}
    
    if filtered_params and filtered_params['q'] and type(filtered_params['q']) is dict:
        filtered_params['q'] = json.dumps({k: v for k, v in filtered_params['q'].items() if v})
        print(filtered_params)
    return __check_status(requests.get(url, params=filtered_params), search_params)

def post_website(url: str, post_params: Union[Dict[str, str], None] = None) -> requests.Response:
    filtered_params = dict()
    if post_params:
        filtered_params = {k: v for k, v in post_params.items() if v}
    return __check_status(requests.post(url, data=filtered_params), post_params)

def __check_status(req_response: requests.Response, params: Union[Dict[str, str], None] = None) -> requests.Response:
    try:
        req_response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed call to webpage: {e}")
        logging.error(f"Error: {req_response.status_code}")
        if params:
            logging.error(f"Caused by searching: {params}")
        logging.error(f"Response content: {req_response.text}")
        
    return req_response