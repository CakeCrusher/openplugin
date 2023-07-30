import os
import pytest
import requests
from openplugincore import OpenPluginMemo
from dotenv import load_dotenv
from .mock_data import todo_plugin
import json
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def test_full_suite():
    open_plugin_memo = OpenPluginMemo()
    open_plugin_memo.init()

    todo_openplugin = open_plugin_memo.init_plugin('__testing__')
    assert todo_openplugin.manifest is not None
    assert len(todo_openplugin.functions) == 2

    response = todo_openplugin.fetch_plugin(
        messages=todo_plugin["messages"],
        model='gpt-3.5-turbo-0613',
    )

    assert response is not None
    assert response['role'] == 'function'
    assert response['name'] == 'addTodo'

    json_content = json.loads(response['content'])
    assert json_content['todo'] == todo_plugin['request_out.json()']['todo']

def test_retrieve_plugins():
    open_plugin_memo = OpenPluginMemo()
    open_plugin_memo.init()

    todo_openplugin = open_plugin_memo.get_plugin('__testing__')
    assert todo_openplugin is None

    todo_openplugin = open_plugin_memo.init_plugin('__testing__')
    assert todo_openplugin is not None

    todo_openplugin = open_plugin_memo.get_plugin('__testing__')
    assert todo_openplugin is not None

    open_plugin_memo.remove_plugin('__testing__')
    todo_openplugin = open_plugin_memo.get_plugin('__testing__')
    assert todo_openplugin is None
