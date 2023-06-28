# openplugin-client
The same powerful functionality as the ChatGPT API + ChatGPT plugins!

## Supported plugins [PLUGINS.md](https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md)

## Quickstart
```bash
pip install openpluginclient # PyPI install
# NPM package coming soon!
```
```py
from openpluginclient import openplugin_completion

plugin_name = "ByByAI" # enter plugin "Namespace" as written on PLUGINS.md 
completion = openplugin_completion(
    early_access_token = "YOUR_EARLY_ACCESS_TOKEN", # (required)
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
```sh
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Here are some of the best Amazon products for puzzles:\n\n1. [ALL4JIG 1500 Piece Rotating Puzzle Board with Drawers and Cover](https://www.amazon.com/dp/B09WTSKMVW/?tag=ttd0e-20) - $69.99\n   - Spinning LAZY SUSAN ... innovative, and challenging jigsaw puzzle from Ceaco.\n\nYou can find more details and purchase these puzzles on Amazon.",
        "role": "assistant"
      }
    }
  ],
  "created": 1687911893,
  "id": "chatcmpl-7WDHJ2KUgj3QjxJq0uwU4duhXMD8b",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 379,
    "prompt_tokens": 752,
    "total_tokens": 1131
  }
}
```

## Disclaimer
As OpenPlugin is currently in an alpha state, you may run into errors. Despite some light testing being done by [migrations](https://github.com/CakeCrusher/openplugin-clients/blob/main/migrations/plugin_store/parser.ipynb) not all plugins are thuroughly tests. If you run into any errors, please report them [here](https://github.com/CakeCrusher/openplugin-clients/issues/new?assignees=CakeCrusher&labels=bug&projects=&template=bug_report.md&title=).

The errors work on a plugin by plugin basis, meaning some will work perfectly while others may not work at all. Some of the errors may be caused by the plugin itself therefore will aso err on [https://chat.openai.com/](https://chat.openai.com/) so double checking would be advisable.



Join Discord for updates: https://discord.gg/udP6X9YkD



