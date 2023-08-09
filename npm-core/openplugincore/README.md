# NPM `openplugincore`
This is the meat of OpenPlugin, it contains all tools you need to interface with ChatGPT plugins as you do on ChatGPT Pro itself.

## Watch out
Issues and concerns to look out for
- `You exceeded your current quota` : If your run into an error suggesting `You exceeded your current quota` that could be for several reasons, refer to this [StackOverflow answer](https://stackoverflow.com/a/75898717/9622142) on how to resolve it.

## Quickstart
1. Install [openplugincore](https://www.npmjs.com/package/openplugincore)
```shell
npm install openplugincore
```
2. Set up `OPENAI_API_KEY` environment variable. With dotenv: create a `.env` file in the root of your project and add your OpenAI API key
```shell
OPENAI_API_KEY=your-api-key
```
3. Start using `openplugincore` in your project

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

console.log(completion.choices[0]);
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