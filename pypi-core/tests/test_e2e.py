import json
import pytest
import os
import openai
from .mock_data import todo_plugin
from openplugincore import OpenPlugin

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def test_initiate_and_fetch_todo():
    plugin = OpenPlugin("__testing__")
    assert plugin.manifest is not None
    assert plugin.manifest.get("name_for_model") == "todo"

    for function in plugin.functions:
        if function["name"] == "addTodo":
            addTodo = function
        if function["name"] == "getTodos":
            getTodos = function
    
    assert addTodo is not None
    assert addTodo == todo_plugin["functions"][0]

    assert getTodos is not None
    assert getTodos == todo_plugin["functions"][1]

    # fetch after chatgpt response
    response = plugin.fetch_plugin(
        messages=todo_plugin["messages"],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )
    assert response is not None
    assert response["role"] == "function"
    assert response["name"] == "addTodo"
    json_content = json.loads(response["content"])
    assert json_content["todo"] == "buy milk"

def test_initiate_and_fetch_LGTM():
    plugin = OpenPlugin("LGTM")
    assert plugin.manifest is not None

    # # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'Show me markdown for a 2 by 2 table with LGTM'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])
    # # ensure that the json_content has a key of image_url and that is starts with https://lgtm.lol
    assert "image_url" in json_content
    assert json_content["image_url"].startswith("https://lgtm.lol")


def test_initiate_and_fetch_yt_caption_retriever():
    plugin = OpenPlugin("yt_caption_retriever")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'give me a 2 sentence summary of the following yt video https://www.youtube.com/watch?v=P310I19L3Ko'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert "en" in json_content["captions"]

def test_initiate_and_fetch_twtData():
    plugin = OpenPlugin("twtData")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'show me the amount of people @Sebasti54919704 is following'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert json_content["stats"]["account_found"] == True
    

def test_initiate_and_fetch_surge_ai_trends():
    plugin = OpenPlugin("surge_ai_trends")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'What are the trnding searches for "gpu" in amazon'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # assert that json_content.items is a list
    assert isinstance(json_content["items"], list)

def test_initiate_and_fetch_speedy_marketing():
    plugin = OpenPlugin("speedy_marketing")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'write me an SEO blog about react for marketing'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["blog"], str)

@pytest.mark.skip(reason="Not whitelisted")
def test_initiate_and_fetch_scholarai():
    plugin = OpenPlugin("scholarai")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'What scientific research exists for semantic representation of language through brain waves. show me one.'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])
    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["total_num_results"], int)

def test_initiate_and_fetch_rephrase():
    plugin = OpenPlugin("rephrase")
    assert plugin.manifest is not None

    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'I want to code a react ui with hello world please rephrase that'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["rephrased"]["text"], str)

def test_initiate_and_fetch_DreamInterpreter():
    plugin = OpenPlugin("DreamInterpreter", verbose=True)
    assert plugin.manifest is not None
    
    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'I dreamt of being in a room without any windows getting smaller overtime'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["dreamResult"], str)

def test_initiate_and_fetch_portfoliopilot():
    plugin = OpenPlugin("portfoliopilot", verbose=True)
    assert plugin.manifest is not None
    
    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'What stocks should I add for my long term tech portfolio'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["top_stocks"], list)

def test_initiate_and_fetch_C3_Glide():
    plugin = OpenPlugin("C3_Glide", verbose=True)
    assert plugin.manifest is not None
    
    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'Provide me TAF for KJFK with reguards to aviation weather'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content["tafs"], list)

@pytest.mark.skip(reason="Could not parse: requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1")
def test_initiate_and_fetch_Ai_PDF():
    plugin = OpenPlugin("Ai_PDF", verbose=True)
    assert plugin.manifest is not None
    
    # create chatgpt request that will call the addTodo function
    chatgpt_prompt = 'Can I have my data be private according to this pdf https://www.unodc.org/pdf/criminal_justice/UN_Basic_Principles_on_the_Role_of_Lawyers.pdf'
    response = plugin.fetch_plugin(
        messages=[
            {
                "role": "user",
                "content": chatgpt_prompt
            }
        ],
        model="gpt-3.5-turbo-0613",
        temperature=0,
    )

    assert response is not None
    assert response["role"] == "function"
    json_content = json.loads(response["content"])

    # Replace the line below with a test for the final output in json_content
    assert isinstance(json_content[0], str)

"""
TEMPLATE for testing a new plugin
0. test the plugin with a prompt in ChatGPT
1. make sure to replace the PLUGIN with the name of your plugin
2. make sure to replace the PLUGIN_PROMPT with the prompt you used on ChatGPT
3. replace the INTENTIONAL_FAILURE error with a test for the final output in json_content
4. remove the segments under the DELETE comment
"""
# def test_initiate_and_fetch_PLUGIN():
#     plugin = OpenPlugin("PLUGIN", verbose=True)
#     assert plugin.manifest is not None

#     # DELETE
#     if not os.path.exists("logs"):
#         os.makedirs("logs")
#     with open("logs/manifest.json", "w") as f:
#         f.write(json.dumps(plugin.manifest, indent=2))
#     with open("logs/functions.json", "w") as f:
#         f.write(json.dumps(plugin.functions, indent=2))
    
#     # create chatgpt request that will call the addTodo function
#     chatgpt_prompt = 'PLUGIN_PROMPT'
#     response = plugin.fetch_plugin(
#         messages=[
#             {
#                 "role": "user",
#                 "content": chatgpt_prompt
#             }
#         ],
#         model="gpt-3.5-turbo-0613",
#         temperature=0,
#     )

#     # DELETE
#     with open("logs/plugin_response.json", "w") as f:
#         f.write(json.dumps(response, indent=2))

#     assert response is not None
#     assert response["role"] == "function"
#     json_content = json.loads(response["content"])

#     # Replace the line below with a test for the final output in json_content
#     raise Exception("INTENTIONAL_FAILURE")

