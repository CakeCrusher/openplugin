# NPM `openpluginclient`
This outsources the request to an OpenPlugin API that uses `openpluginclient`, so you dont need to worry about the OpenAI api key.

## Quickstart
1. Install [openpluginclient](https://www.npmjs.com/package/openpluginclient)
```shell
npm install openpluginclient
```
2. Start using `openpluginclient` in your project

```js
import {openpluginCompletion} from 'openpluginclient'

const pluginName = "ByByAI" // enter plugin "Namespace" as written on PLUGINS.md 
const completion = await openpluginCompletion({
  earlyAccessToken: "__extra__-c22a34e2-89a8-48b2-8474-c664b577526b", // (required)
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