<div>
  <img src="https://i.imgur.com/L3giCRt.png" alt="Your alt text" width="125" align="left">
    <h1><a href="https://www.openplugin.io/">OpenPlugin</h1>
  <h3>Integrate with OpenAI's ChatGPT plugins via API.<br/>The same powerful functionality as the ChatGPT api + plugins!</h3>
  <h3></h3>
</div>


[Join Discord Server](https://discord.gg/AfHcVutBUT) 

OpenPlugin official client, [openplugin.io](https://www.openplugin.io/), now in closed beta!

## Supported plugins [PLUGINS.md](https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md)
<i>demo</i>


https://github.com/CakeCrusher/openplugin/assets/37946988/d35c704d-a007-4e5f-b3ea-03df264c0f4e

## Project stucture
This repo contains 3 packages: [(pypi)`openplugincore`](https://github.com/CakeCrusher/openplugin/tree/main/pypi-core), [(pypi)`openpluginclient`](https://github.com/CakeCrusher/openplugin/tree/main/pypi-client), and [(npm)`openpluginclient`](https://github.com/CakeCrusher/openplugin/tree/main/npm-client/openpluginclient). (pypi)`openplugincore` is the meat of this project, it contains all the tools you need to call OpenAI plugins. Both (pypi)`openpluginclient` and (npm)`openpluginclient` ping an API that uses (pypi)`openplugincore` internally, does not need an OpenAI API key.

## Examples
- Generate trendy and informed articles: https://colab.research.google.com/drive/1dQsaFrqLdR0HzxXkj5DYmaZ8CtmqA1qt?usp=sharing

## Core Quickstart
### Node (js)
```shell
npm install openplugincore
```
simplest way to use `openplugincore`
```js
import { openpluginCompletion } from 'openplugincore';
import dotenv from 'dotenv'; // to get .env variables
dotenv.config(); // to get .env variables

const completion = await openpluginCompletion(
  "show me a gif of a gangster cat",
  "GifApi",
  undefined,
  process.env.OPENAI_API_KEY,
  {
    model: "gpt-3.5-turbo-0613",
    temperature: 0,
  }
);

console.log(completion.choices[0]);
```
or for more nuanced use
```js
import {OpenPlugin} from 'openplugincore'
import dotenv from 'dotenv' // to get .env variables
dotenv.config() // to get .env variables

const imageOpenplugin = new OpenPlugin("GifApi", undefined, process.env.OPENAI_API_KEY);
await imageOpenplugin.init();

const prompt = "show me a gif of a gangster cat"
const functionRes = await imageOpenplugin.fetchPlugin({
  prompt: prompt,
  model: "gpt-3.5-turbo-0613"
});

const completionRes = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
  },
  body: JSON.stringify({
    model: 'gpt-3.5-turbo-0613',
    messages: [
      {role: 'user', content: prompt},
      functionRes
    ],
    temperature: 0,
  }),
})

const completionResJson = await completionRes.json()
```
and to be respectful to plugin APIs you can use `OpenPluginMemo`
```js
import { OpenPluginMemo } from 'openplugincore';
import dotenv from 'dotenv';
dotenv.config();

const openpluginMemo =  new OpenPluginMemo()
await openpluginMemo.init()

const firstGifPlugin = await openpluginMemo.initPlugin("GifApi")
// same as OpenPlugin
const firstPrompt = "show me a gif of a gangster cat"

const firstFunctionRes = await firstGifPlugin.fetchPlugin({
  prompt: firstPrompt,
  model: "gpt-3.5-turbo-0613"
});

const firstCompletionRes = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
  },
  body: JSON.stringify({
    model: 'gpt-3.5-turbo-0613',
    messages: [
      {role: 'user', content: firstPrompt},
      firstFunctionRes
    ],
    temperature: 0,
  }),
})
const firstCompletionResJson = await firstCompletionRes.json()

console.log(firstCompletionResJson.choices[0]);
// finish same as OpenPlugin
```
### PyPI
`openplugincore` requires python version >= `3.10`
```shell
pip install openplugincore
```
simplest way to use `openplugincore`
```py
from openplugincore import openplugin_completion

openplugin_completion_generation = openplugin_completion(
    openai_api_key = OPENAI_API_KEY,
    plugin_name = "Ai_PDF",
    prompt = chatgpt_prompt,
    model = "gpt-3.5-turbo-0613",
    temperature = 0,
)

print(json.dumps(OpenPlugin_generation, indent=2))
```
or for more nuanced use
```py
from openplugincore import OpenPlugin

plugin = OpenPlugin("Ai_PDF", OPENAI_API_KEY)

function_response = plugin.fetch_plugin(
    prompt=chatgpt_prompt,
    model="gpt-3.5-turbo-0613",
    temperature=0,
)

import openai
openai.api_key = OPENAI_API_KEY

OpenPlugin_generation = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": chatgpt_prompt},
        function_response
    ],
    temperature = 0
)

print(json.dumps(OpenPlugin_generation, indent=2))
```   
<i>rough high level system design / docs</i>

![image](https://github.com/CakeCrusher/openplugin/assets/37946988/36b57d80-7eab-4ed0-9fff-c49885bf32e1)


## Client Quickstart
Public early access tokens: `__extra__-c22a34e2-89a8-48b2-8474-c664b577526b`, `__extra__-692df72b-ec3f-49e4-a1ce-fb1fbc34aebd`
### Python
```bash
pip install openpluginclient # PyPI install
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

### node (js)
```bash
npm install openpluginclient # npm install
```
```js
import {openpluginCompletion} from 'openpluginclient'

const pluginName = "ByByAI" // enter plugin "Namespace" as written on PLUGINS.md 
const completion = await openpluginCompletion({
  earlyAccessToken: "SebastianS-e54e2881-9aea-4d35-b243-d18600d1fc7b", // (required)
  pluginName: pluginName, // optional
  model: "gpt-3.5-turbo-0613", // optional
  messages: [ // regular ChatGPT messages argument (required)
      {
          "role": "user",
          "content": "Show me a Best Amazon products for puzzles"
      }
  ],
  temperature: 0, // optional
  // ...other openai.ChatCompletion.create arguments
})

// print as prettified JSON
console.log(completion)
```
<i>high level system design / docs</i>

![image](https://github.com/CakeCrusher/openplugin/assets/37946988/63da7efc-c556-495b-8738-9143b3faece1)

## Are you breaching OpenAI Terms of Service by using OpenPlugin?
No, I have gone through the Terms of Service particularly "service terms" and "usage policies" and  here are the takeaways.
As with most marketplace type things, the host, OpenAI, is not accountable for the plugins and their use outside of their platform `chat.openai.com`. They also never mention anything about accessing their data that is not explicitly shown to the user, therefore accessing their plugins' payload (how OpenPlugin gets knows about the marketplace plugins), which is used for them to display the plugins, is not against their ToS.

Primary sources:

https://openai.com/policies/terms-of-use

https://openai.com/policies/usage-policies

https://openai.com/policies/service-terms

## Disclaimer
As OpenPlugin is currently in an alpha state, you may run into errors. Despite some light testing being done by [migrations](https://github.com/CakeCrusher/openplugin-clients/blob/main/migrations/plugin_store/parser.ipynb) not all plugins are thuroughly tests. If you run into any errors, please report them [here](https://github.com/CakeCrusher/openplugin-clients/issues/new?assignees=CakeCrusher&labels=bug&projects=&template=bug_report.md&title=).

The errors work on a plugin by plugin basis, meaning some will work perfectly while others may not work at all. Some of the errors may be caused by the plugin itself therefore will aso err on [https://chat.openai.com/](https://chat.openai.com/) so double checking would be advisable.



Join Discord for updates: https://discord.gg/udP6X9YkD



