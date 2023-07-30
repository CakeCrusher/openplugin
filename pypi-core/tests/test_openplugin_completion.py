import json
import pytest
from .mock_data import todo_plugin
import os
from openplugincore import OpenPlugin, openplugin_completion
import random
import requests
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@pytest.fixture
def todo_openplugin():
    plugin = OpenPlugin("__testing__")
    return plugin 

def test_openplugin_completion():
    todo = f'test_chat_completion_{random.randint(0, 100000)}'

    completion = openplugin_completion(
        openai_api_key = OPENAI_API_KEY,
        plugin_name = "__testing__",
        messages = [
            {
                "role": "user",
                "content": f"add '{todo}' to my todo list"
            }
        ],
        model = "gpt-3.5-turbo-0613",
        temperature = 0,
    )

    todos_request = requests.get("http://localhost:3333/todos")
    todos_body = todos_request.json()
    
    assert todo in completion["choices"][0]["message"]["content"]
    assert todo in todos_body["todos"]

def test_openplugin_completion_with_url():
    todo = f'test_chat_completion_{random.randint(0, 100000)}'

    completion = openplugin_completion(
        openai_api_key = OPENAI_API_KEY,
        root_url = "http://localhost:3333",
        messages = [
            {
                "role": "user",
                "content": f"add '{todo}' to my todo list"
            }
        ],
        model = "gpt-3.5-turbo-0613",
        temperature = 0,
    )

    todos_request = requests.get("http://localhost:3333/todos")
    todos_body = todos_request.json()
    
    assert todo in completion["choices"][0]["message"]["content"]
    assert todo in todos_body["todos"]

