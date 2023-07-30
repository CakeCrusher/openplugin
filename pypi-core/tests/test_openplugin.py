import json
import pytest
from .mock_data import todo_plugin
import os
from openplugincore import OpenPlugin, openplugin_completion
from openplugincore.utils.prompting import estimate_tokens
import random
import requests
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def test_initiate_todo_with_url():
    plugin = OpenPlugin(root_url="http://localhost:3333")
    assert plugin.manifest is not None
    assert plugin.manifest.get("name_for_model") == "todo"

@pytest.fixture
def todo_openplugin():
    plugin = OpenPlugin("__testing__")
    return plugin 

def test_initiate_todo(todo_openplugin):
    assert todo_openplugin.manifest is not None
    assert todo_openplugin.manifest.get("name_for_model") == "todo"

def test_openapi_to_functions_and_call_api_fn(todo_openplugin):
    # test functions
    assert len(todo_openplugin.functions) == 2
    addTodo = None
    getTodos = None
    for function in todo_openplugin.functions:
        if function["name"] == "addTodo":
            addTodo = function
        if function["name"] == "getTodos":
            getTodos = function
    
    assert addTodo is not None
    assert addTodo == todo_plugin["functions"][0]

    assert getTodos is not None
    assert getTodos == todo_plugin["functions"][1]

    # test call_api_fn
    request_out = todo_openplugin.call_api_fn(
        todo_plugin["llm_chain_out"]["name"],
        todo_plugin["llm_chain_out"]["arguments"]
    )
    assert request_out.json() == todo_plugin["request_out.json()"]


def test_fetch_plugin(todo_openplugin):
    response = todo_openplugin.fetch_plugin(
        messages=todo_plugin["messages"],
        model="gpt-3.5-turbo-0613"
    )
    assert response is not None
    assert response["role"] == "function"
    assert response["name"] == "addTodo"
    json_content = json.loads(response["content"])
    assert json_content["todo"] == "buy milk"

def test_truncated_response():
    yt_plugin = OpenPlugin('yt_caption_retriever', verbose=True)
    response = yt_plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": "summarize this video https://www.youtube.com/watch?v=gZVeRQkxCdc"
            }
        ],
        model='gpt-3.5-turbo-0613',
        truncate=True,
    )
    assert response is not None
    assert estimate_tokens(response['content']) > 3600 and estimate_tokens(response['content']) < 3800

def test_messages():
    plugin = OpenPlugin('__testing__', verbose=True)
    todo = f'test_chat_completion_{random.randint(0, 100000)}'

    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "system",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "user",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "assistant",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "user",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "assistant",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "user",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "assistant",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "user",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "assistant",
                "content": "hello this message consumes about 100 tokens I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing I will extend it just for the sake of testing"
            },
            {
                "role": "user",
                "content": f"add '{todo}' to my todo list"
            },
            {
                "role": "user",
                "content": "please add that to my todo list"
            }
        ],
        model='gpt-3.5-turbo-0613',
        truncate=True
    )

    todos_request = requests.get("http://localhost:3333/todos")
    todos_body = todos_request.json()

    assert todo in response["content"]
    assert todo in todos_body["todos"]