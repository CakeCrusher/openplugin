# PyPI `openplugincore`
This is the meat of OpenPlugin, it contains all tools you need to interface with ChatGPT plugins as you do on ChatGPT Pro itself.

`openplugincore` requires python version >= `3.10`

## Quickstart
1. Install [openplugincore](https://pypi.org/project/openplugincore/)
```shell
pip install openplugincore
```
2. Assign `OPENAI_API_KEY` environment variable with your OpenAI API key
3. Start using `openplugincore` in your project

simplest way to use `openplugincore`
```py
from openplugincore import openplugin_completion

openplugin_completion_generation = openplugin_completion(
    openai_api_key = os.environ["OPENAI_API_KEY"],
    plugin_name = "NewsPilot",
    truncate = True, # Defaults to True. Truncates the plugin API response to ensure the LLM's token limit is not exceeded
    messages = [
        {
            "role": "user",
            "content": "Show me the current news in ukraine"
        }
    ],
    model = "gpt-3.5-turbo-0613",
    temperature = 0,
)

print(json.dumps(openplugin_completion_generation, indent=2))
```
or for more nuanced use
```py
from openplugincore import OpenPlugin

plugin = OpenPlugin("GifApi", os.environ["OPENAI_API_KEY"])

messages = [
    {
        "role": "user",
        "content": "show me a gif of a gangster cat"
    }
]

function_response = plugin.fetch_plugin(
    model="gpt-3.5-turbo-0613",
    messages = messages,
    truncate = True, # Truncates the plugin API response to ensure the LLM's token limit is not exceeded
    temperature=0,
)

import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

OpenPlugin_generation = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages= messages + [function_response],
    temperature = 0
)

print(json.dumps(OpenPlugin_generation, indent=2))
```
and to be respectful to plugin APIs you can use `OpenPluginMemo`
```py
from openplugincore import OpenPluginMemo

open_plugin_memo = OpenPluginMemo() # Stores the plugin's config in memory so that it does not need to call the API to fetch the config every time the plugin is initialize.
open_plugin_memo.init()

plugin = open_plugin_memo.get_plugin('GifApi') # returns the plugin if it is already initialized, otherwise returns None
if plugin is None: # in this demo it returns None
    plugin = open_plugin_memo.init_plugin('GifApi') # initializes the plugin

# the rest is the same as using the OpenPlugin class
messages = [
    {
        "role": "user",
        "content": "show me a gif of a gangster cat"
    }
]

function_response = plugin.fetch_plugin(
    model="gpt-3.5-turbo-0613",
    messages = messages,
    truncate = True, # Truncates the plugin API response to ensure the LLM's token limit is not exceeded
    temperature=0,
)

import openai
openai.api_key = os.environ["OPENAI_API_KEY"]

OpenPlugin_generation = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages= messages + [function_response],
    temperature = 0
)

print(json.dumps(OpenPlugin_generation, indent=2))
```