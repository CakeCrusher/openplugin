import json
import os
import re
import requests
from openplugincore import OpenPlugin
from typing import Any, List, Dict, Union, Tuple, Callable
import openai
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

domain_input = input("Enter domain. (Ex. if manifest in \"https://todo.com/.well-known/ai-plugin.json\" then domain is \"todo.com\"): ")

# 1. Assign `all_plugins.json` to variable `all_plugins`
pypi_client_path = 'all_plugins.json'
with open(pypi_client_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
json_content = ''.join(lines)
try:
    all_plugins = json.loads(json_content)
except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")

# 2. Create `blacklist_list` dict
with open('blacklist.json', 'r', encoding='utf-8') as f:
    blacklist = json.load(f)
def aggregate_items(json_object):
    aggregate_list = []
    for key in json_object:
        aggregate_list.extend(json_object[key])
    return aggregate_list
blacklist_list = aggregate_items(blacklist)

# 3. Assign `plugins_info.json` to variable `plugins_info`
with open('openplugins_info.json', 'r', encoding='utf-8') as f:
    openplugins_info: dict = json.load(f)
first_openplugin_info = list(openplugins_info.keys())[0]

pluginToAdd = OpenPlugin(root_url="https://" + domain_input)
pluginToAdd_obj = {
    "domain": domain_input,
    "manifest": pluginToAdd.manifest,
}


# 4. Initiate a dict called openplugin_info. Execute an initial screening of plugins with the following loop:
# for plugin in all_plugins:
plugin = pluginToAdd_obj
def create_base_plugin_info(plugin: Any):
    print("4. create_base_plugin_info")
    openplugin_info = {
        **openplugins_info.get(plugin['manifest']['name_for_model'], {}),
        'namespace': plugin['manifest']['name_for_model'],
        'image': plugin['manifest'].get('logo_url', None),
        'description_for_human': plugin['manifest'].get('description_for_human', None),
        'description_for_model': plugin['manifest'].get('description_for_model', None),
        'domain': plugin['domain'],
        'openapi_url': plugin['manifest'].get('api', {}).get('url', None)
    }
    if plugin['manifest'].get('auth', {}).get('type', None) == 'none':
        openplugin_info['auth'] = False
    else:
        openplugin_info['auth'] = True
    if plugin['manifest']['name_for_model'] not in blacklist_list:
        openplugin_info['blacklisted'] = False
    else:
        openplugin_info['blacklisted'] = True
    return openplugin_info
openplugin_info = create_base_plugin_info(plugin)
openplugins_info[openplugin_info["namespace"]] = openplugin_info
with open('openplugins_info.json', 'w', encoding='utf-8') as f:
    json.dump(openplugins_info, f, indent=2, sort_keys=True)

# 5. Iterate through `plugins_info` and do the following:
openplugin_classes = {}
def test_whitelist(openplugin_info: Any):
    print("5. test_whitelist")
    root_url = "https://" + openplugin_info['domain']
    try:
        openplugin_class = OpenPlugin(openai_api_key=OPENAI_API_KEY, root_url=root_url)
        openplugin_info['whitelisted'] = True
    except Exception as e:
        openplugin_class = None
        openplugin_info['whitelisted'] = False
    return (openplugin_info, openplugin_class)
openplugin_info, openplugin_class = test_whitelist(openplugin_info)
if openplugin_class is not None:
    openplugin_classes[openplugin_info["namespace"]] = openplugin_class
if not openplugin_info["whitelisted"]:
    OpenPlugin(openai_api_key=OPENAI_API_KEY, root_url="https://" + openplugin_info['domain'])
with open('openplugins_info.json', 'w', encoding='utf-8') as f:
    json.dump(openplugins_info, f, indent=2, sort_keys=True)

# 6. iterate through `openplugin_classes`
def test_stimulation(openplugin_info: Any, openplugin_class: Any):
    print("6. test_stimulation")
    openplugin_info["stimulous_prompt"] = openplugin_info.get("stimulous_prompt", None)
    openplugin_info["stimulated"] = openplugin_info.get("stimulated", False)
    if not openplugin_info["auth"] and not openplugin_info["blacklisted"] and openplugin_info["whitelisted"]:
        try:
            if openplugin_info.get("stimulous_prompt", None) is None:
                generate_stimulation_prompt_prompt = {
                    "prompt": f"""
                    Please create a prompt that will trigger an model's plugin with the human description delimited by driple backticks.
                    If necessary also look at the model description also delimited by triple backticks.
                    Please do not ask anything from the AI you should provide all the information it needs in the prompt.
                    You should not be ambiguous or open ended in your prompt use specific examples.
                    Do not simply restate the description.
                    Human description:
                    ```
                    {openplugin_info["description_for_human"]}
                    ```
                    Model description:
                    ```
                    {openplugin_info["description_for_model"]}
                    ```
                    """,
                    "function": {
                    "name": "stimulous_prompt_generation",
                    "description": """
                    Generates a natural language phrase to that triggeres the AI plugin.
                    If approriate the phrase should include an example item/url (https://github.com/)/text/ect. even if you are not sure if it is real its ok to make it up.
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "stimulous_prompt": {
                            "type": "string",
                            "description": "The stimulous phrase to trigger the AI plugin"
                        },
                        },
                        "required": ["stimulous_prompt"]
                    }
                    }
                }
                generation = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    temperature=0,
                    messages=[{"role": "user", "content": generate_stimulation_prompt_prompt["prompt"]}],
                    functions=[generate_stimulation_prompt_prompt["function"]],
                    function_call={"name": "stimulous_prompt_generation"}
                )
                json_arguments = json.loads(generation["choices"][0]["message"]["function_call"]["arguments"])
                openplugin_info["stimulous_prompt"] = json_arguments["stimulous_prompt"]
            function_response = openplugin_class.fetch_plugin(
                prompt=openplugin_info["stimulous_prompt"],
                model="gpt-3.5-turbo-0613",
                temperature=0,
            )
            openplugin_info["stimulated"] = True
        except Exception as e:
            print(e)
            openplugin_info["stimulated"] = False
    return openplugin_info
openplugin_info = test_stimulation(openplugin_info, openplugin_class)
while not openplugin_info["stimulated"]:
    stimulous_prompt_input = input("Failed to stimulate.\nEnter stimulous prompt (prompt to stimulate your plugin): ")
    openplugin_info["stimulous_prompt"] = stimulous_prompt_input
    openplugin_info = test_stimulation(openplugin_info, openplugin_class)
with open('openplugins_info.json', 'w', encoding='utf-8') as f:
    json.dump(openplugins_info, f, indent=2, sort_keys=True)

# 7. Creaate a status for all plugins
openplugin_info["status"] = "supported"
with open('openplugins_info.json', 'w', encoding='utf-8') as f:
    json.dump(openplugins_info, f, indent=2, sort_keys=True)

# 8. Create a file called `openplugins_compressed.json` and save only plugins that are `tentative` or `supported`
with open('openplugins.json', 'r', encoding='utf-8') as f:
    openplugins = json.load(f)
openplugins[openplugin_info["namespace"]] = "https://" + openplugin_info["domain"]
with open('openplugins.json', 'w', encoding='utf-8') as f:
    json.dump(openplugins, f, indent=2, sort_keys=True)

# 9. create PLUGINS.md table
current_dir = os.getcwd()
root_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
pluginsmd_path = os.path.join(root_dir, 'PLUGINS.md')
plugins_md = """
# Plugins
Available plugins for OpenPlugin
Status:
- `tentative`: passed basic tests (may work)
- `supported`: passed complete prompt tests (should to work)

| Image | Namespace | Status | Description | Description for model |
| --- | --- | --- | --- | --- |
"""
def escape_special_markdown_chars(text):
    # Characters to escape: \ ` * _ { } [ ] ( ) # + !
    special_chars = r'\\|`|\*|_|{|}|\[|\]|\(|\)|#|\+|!'
    return re.sub(special_chars, lambda match: '\\' + match.group(), text)
def remove_line_breaks(text):
    return text.replace('\n', ' ').replace('\r', '')
# create two lists of plugins one supported_plugins and one tentative_plugins
supported_plugins = []
tentative_plugins = []
for _namespace, openplugin_info in openplugins_info.items():
    if openplugin_info["status"] == "tentative":
        tentative_plugins.append(openplugin_info)
    if openplugin_info["status"] == "supported":
        supported_plugins.append(openplugin_info)
# now sort the lists by their namespace keys considering that each plugin is a dict of {namespace: str, ...}
supported_plugins.sort(key=lambda x: x["namespace"])
tentative_plugins.sort(key=lambda x: x["namespace"])
# aggragate the lists so that supported_plugins is first and tentative_plugins is second 
ordered_openplugins_info = supported_plugins + tentative_plugins
for openplugin_info in ordered_openplugins_info:
        if openplugin_info["image"]:
            image = escape_special_markdown_chars(openplugin_info["image"])
        else:
            image = escape_special_markdown_chars("https://i.imgur.com/L3giCRt.png")
        namespace = escape_special_markdown_chars(openplugin_info["namespace"])
        status = escape_special_markdown_chars(openplugin_info["status"])
        description = escape_special_markdown_chars(remove_line_breaks(remove_line_breaks(openplugin_info["description_for_human"])))
        description_for_model = escape_special_markdown_chars(remove_line_breaks(openplugin_info["description_for_model"]))
        plugins_md += f"| ![{namespace} Logo]({image}) | {namespace} | {status} | {description} | {description_for_model} |\n"
with open(pluginsmd_path, 'w', encoding='utf-8') as f:
    f.write(plugins_md)

print("Plugin added successfully!\nYou may now commit, push your changes, and create the PR. Thank you for your contribution!")
