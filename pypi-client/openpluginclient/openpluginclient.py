import json
import requests
import os
from pathlib import Path

SUPPORTED_MODELS = ["gpt-4-0613", "gpt-3.5-turbo-0613"]

def get_supported_plugins():
    file_path = Path(__file__).parent / "plugins.json"
    with open(file_path, 'r') as f:
        return json.load(f)

def openplugin_completion(early_access_token: str, plugin_name: str = None, fail_silently: bool = False, **chatgpt_args):
    # Ensure an early access token is provided.
    if not early_access_token:
        raise ValueError(f"An early access token must be provided.")

    # Ensure the provided model is supported.
    model = chatgpt_args.get("model", "gpt-3.5-turbo-0613")
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model}. Try 'gpt-4-0613' or 'gpt-3.5-turbo-0613'.")

    # Ensure the plugin is supported.
    supported_plugins = get_supported_plugins()
    if plugin_name and plugin_name not in supported_plugins:
        raise ValueError(f"Unsupported plugin '{plugin_name}'. For full list of supported plugins, visit, https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md .")
    
    # Ensure messages are passed
    if not chatgpt_args.get("messages", None):
        raise ValueError(f"Messages must be passed to the openplugin_completion function.")
    # Ensure messages are not empty
    if len(chatgpt_args.get("messages", [])) == 0:
        raise ValueError(f"Messages cannot be empty.")

    body = {
        "early_access_token": early_access_token,
        "plugin_name": plugin_name,
        **chatgpt_args,
        "model": model,
        "messages": chatgpt_args.get("messages"),
    }

    try:
        server = "https://openplugin-api-30b78451a615.herokuapp.com"
        # server = "http://localhost:3000" # For local testing
        
        response = requests.post(f"{server}/chat_completion", json=body)
        json_response = response.json()
        if ('error' in json_response):
            raise Exception(f"Error: {json_response['error']}")
    except Exception as e:
        if fail_silently:
            return print(e)
        else:
            raise e

    return response.json()  # Assume server responds with json content
