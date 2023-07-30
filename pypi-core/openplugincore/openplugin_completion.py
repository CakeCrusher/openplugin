from ast import List
import os
import openai
from dotenv import load_dotenv
from .openplugin import OpenPlugin
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def openplugin_completion(openai_api_key: str, messages: list[dict], plugin_name: str = None, root_url: str = None, **chatgpt_args):
    # set environment variable to 
    os.environ["OPENAI_API_KEY"] = openai_api_key
    openai.api_key = openai_api_key
    if not plugin_name and not root_url:
        return openai.ChatCompletion.create(
            **chatgpt_args,
            messages=messages
        )
    plugin = OpenPlugin(plugin_name=plugin_name, root_url=root_url, openai_api_key=openai_api_key)
    try:
        function_response = plugin.fetch_plugin(
            messages=messages,
            **chatgpt_args
        )
    except ValueError as e:
        if "Not a plugin function" in str(e):
            return openai.ChatCompletion.create(
                **chatgpt_args,
                messages=messages
            )
        else:
            raise e
    all_chatgpt_args = {
        **chatgpt_args,
        "messages": messages + [function_response]
    }
    summarize = openai.ChatCompletion.create(**all_chatgpt_args)
    return summarize