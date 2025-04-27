#--kind python:default
#--web true

import os
import requests
import json
from requests.auth import HTTPBasicAuth

def main(args):
    api_host = os.environ.get("__OW_API_HOST")
    namespace = os.environ.get("__OW_NAMESPACE")
    
    headers = args.get("__ow_headers", None)
    print(f"Headers: {headers}")
    auth = None
    if headers:
        auth = headers.get("authorization", None)
    
    if not auth:
        print("No Auth header provided. Exiting.")
        return {"body": "No Auth header provided. Exiting.", "statusCode": 401, "headers": {"Content-Type": "application/json"}}

    action_name = "stream/stream"    
    
    invoke_url = f"{api_host}/api/v1/namespaces/{namespace}/actions/{action_name}?blocking=false"
    payload = {}
    for key, value in args.items():
        if key.startswith("__ow_"):
            continue
        payload[key] = value
        
    response = requests.post(
        invoke_url,
        auth=HTTPBasicAuth(*auth.split(':')),
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
        
    if 200 <= response.status_code <= 299:        
        print(f"Invoked action {invoke_url} ({response.status_code}). Returning 202 Accepted.")
        return {"body": "Accepted", "statusCode": 202, "headers": {"Content-Type": "application/json"}}
    
    print(f"Error invoking action {invoke_url} ({response.status_code}).")
    return {"body": "Error", "statusCode": 500, "headers": {"Content-Type": "application/json"}}
    
    
