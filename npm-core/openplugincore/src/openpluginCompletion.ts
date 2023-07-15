import 'isomorphic-fetch';
import { fetchChatCompletion } from './util/fetching';
import { OpenPlugin } from './openPlugin';

type ChatgptFunctionMessage = {
  role: 'function';
  name: string;
  content: string;
};

export async function openpluginCompletion(
  prompt: string,
  pluginName: string | undefined = undefined,
  rootUrl: string | undefined = undefined,
  openaiApiKey: string | undefined = process.env.OPENAI_API_KEY,
  chatgptArgs: object
) {
  if (!openaiApiKey) {
    throw new Error(
      'openaiApiKey not found. You can pass in the parameter openaiApiKey. You can also set the environment variable openaiApiKey=<API-KEY>.'
    );
  }

  process.env.OPENAI_API_KEY = openaiApiKey;
  if (!pluginName && !rootUrl) {
    console.log('NO PLUGIN NAME OR ROOT URL');
    const res = await fetchChatCompletion({
      ...chatgptArgs,
      messages: [{ role: 'user', content: prompt }],
    });
    const json = await res.json();
    return json;
  }

  const plugin = new OpenPlugin(pluginName, rootUrl, openaiApiKey);
  await plugin.init();
  let functionResponse: ChatgptFunctionMessage;
  try {
    functionResponse = await plugin.fetchPlugin({
      prompt: prompt,
      ...chatgptArgs,
    });
  } catch (e: any) {
    if (
      e instanceof Error &&
      (e.message.includes('Not a plugin function') ||
        e.message.includes('No function_call'))
    ) {
      const res = await fetchChatCompletion({
        ...chatgptArgs,
        messages: [{ role: 'user', content: prompt }],
      });
      const json = await res.json();
      return json;
    } else {
      throw e;
    }
  }
  const allChatgptArgs = {
    ...chatgptArgs,
    messages: [{ role: 'user', content: prompt }, functionResponse],
  };
  const summarize = await fetchChatCompletion(allChatgptArgs);
  const summarizeJson = await summarize.json();
  return summarizeJson;
}
