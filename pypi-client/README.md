# PyPI `openpluginclient`
This outsources the request to an OpenPlugin API that uses `openpluginclient`, so you dont need to worry about the OpenAI api key.

## Quickstart
1. Install [openpluginclient](https://pypi.org/project/openpluginclient/)
2. Start using `openpluginclient` in your project

```py
from openpluginclient import openplugin_completion

plugin_name = "ByByAI" # enter plugin "Namespace" as written on PLUGINS.md 
completion = openplugin_completion(
    early_access_token = "__extra__-c22a34e2-89a8-48b2-8474-c664b577526b", # (required)
    plugin_name = plugin_name, # optional
    model = "gpt-3.5-turbo-0613", # optional
    messages = [ # regular ChatGPT messages argument (required)
        {
            "role": "user",
            "content": "Show me a Best Amazon products for puzzles"
        }
    ],
    temperature = 0, # optional
    # ...other openai.ChatCompletion.create arguments
)

print(completion)
```
