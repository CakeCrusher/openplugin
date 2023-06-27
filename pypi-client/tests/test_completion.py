import os
import sys
import random
import requests
import pytest
# check if there is an environmental variable set for IS_GITHUB_ACTION
if "IS_GITHUB_ACTION" in os.environ:
    print("Running in Github Action")
else:
    sys.path.insert(0, './')

EARLY_ACCESS_TOKEN = os.environ.get("EARLY_ACCESS_TOKEN")
DEVELOPMENT = os.environ.get("DEVELOPMENT") == "true"
print("DEVELOPMENT", DEVELOPMENT)

from openpluginclient import openplugin_completion

@pytest.mark.skipif(not DEVELOPMENT, reason="Skipping test. Not in DEVELOPMENT mode")
def test_openplugin_completion_todo():
    todo = f'test_chat_completion_{random.randint(0, 100000)}'

    completion = openplugin_completion(
        early_access_token = EARLY_ACCESS_TOKEN,
        plugin_name = "__testing__",
        model = "gpt-3.5-turbo-0613",
        messages = [{"role": "user", "content": f"add '{todo}' to my todo list"}],
        temperature = 0,
    )

    todos_request = requests.get("http://localhost:3333/todos")
    todos_body = todos_request.json()
    
    assert todo in completion["choices"][0]["message"]["content"]
    assert todo in todos_body["todos"]

def test_openplugin_completion_ImageSearch():
    completion = openplugin_completion(
        early_access_token = EARLY_ACCESS_TOKEN,
        plugin_name = "ImageSearch",
        model = "gpt-3.5-turbo-0613",
        messages = [{"role": "user", "content": f"show me an image of a dog"}],
        temperature = 0,
    )

    assert 'dog' in completion["choices"][0]["message"]["content"].lower()

# def test_experiment():
#     completion = openplugin_completion(
#         early_access_token = EARLY_ACCESS_TOKEN,
#         plugin_name = "ImageSearch",
#         model = "gpt-3.5-turbo-0613",
#         messages = [{"role": "user", "content": f"show me an image of a dog"}],
#         temperature = 0,
#     )
#     print("completion", completion)
#     raise Exception("completion")