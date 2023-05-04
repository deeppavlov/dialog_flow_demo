"""
DNNC
----
This module includes queries to a local DNNC service.
"""
import requests
from dff.script import Message


DNNC_SERVICE = "http://localhost:4999/respond"


def get_intents(request: Message):
    """
    Query the local DNNC service extracting intents from the
    last user utterance.
    """
    if not request.text:
        return []
    request_body = {"dialog_contexts": [request.text]}
    try:
        response = requests.post(DNNC_SERVICE, json=request_body)
    except requests.RequestException:
        response = None
    if response and response.status_code == 200:
        return [response.json()[0][0]]
    return []
