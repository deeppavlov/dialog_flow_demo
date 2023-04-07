"""
DNNC
---------
This module includes queries to a local DNNC service.
"""
import requests


DNNC_SERVICE = "http://localhost:4999/respond"


def get_intents(request: str):
    """
    Query the local DNNC service extracting intents from the
    last user utterance.
    """
    request_body = {"dialog_contexts": [request]}
    try:
        response = requests.post(DNNC_SERVICE, json=request_body)
    except requests.RequestException:
        response = None
    if response and response.status_code == 200:
        return [response.json()[0][0]]
    return []
