import 'isomorphic-fetch';
import { describe, expect, test } from '@jest/globals';
import { OpenPlugin } from '../src/index'; // Update this import path as needed
import { todo_plugin as mock_todo_plugin } from './mockData'; // Update this import path as needed

import dotenv from 'dotenv';
dotenv.config();

const openaiApiKey = process.env.OPENAI_API_KEY;

test.skip('scholarai', async () => {
  // demo non function_call
  const plugin = new OpenPlugin('scholarai', openaiApiKey, undefined, true);
  await plugin.init();
  expect(plugin.manifest).not.toBeNull();

  const chatgpt_prompt = 'When did ww2 happen?';
  const response = await plugin.fetchPlugin({
    prompt: chatgpt_prompt,
    model: 'gpt-3.5-turbo-0613',
    temperature: 0,
  });

  expect(response).not.toBeNull();
  expect(response.role).toEqual('function');

  const json_content = JSON.parse(response.content);

  expect(typeof json_content.total_num_results).toEqual('number');
}, 30000);

describe('OpenPlugin End to End Tests', () => {
  test('__testing__', async () => {
    const plugin = new OpenPlugin('__testing__');
    await plugin.init();

    expect(plugin.manifest).not.toBeNull();
    expect(typeof plugin.description).toEqual('string');

    let addTodo;
    let getTodos;
    expect(plugin.functions).not.toBeNull();
    for (let i = 0; i < plugin.functions!.length; i++) {
      if (plugin.functions![i].name === 'addTodo') {
        addTodo = plugin.functions![i];
      }
      if (plugin.functions![i].name === 'getTodos') {
        getTodos = plugin.functions![i];
      }
    }

    expect(addTodo).not.toBeNull();

    expect(addTodo).toEqual(mock_todo_plugin.functions[0]);

    expect(getTodos).not.toBeNull();
    expect(getTodos).toEqual(mock_todo_plugin.functions[1]);

    const response = await plugin.fetchPlugin({
      prompt: mock_todo_plugin.prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');
    expect(response.name).toEqual('addTodo');

    const json_content = JSON.parse(response.content);

    expect(json_content.todo).toEqual(
      mock_todo_plugin['request_out.json()'].todo
    );
  }, 30000);

  test('LGTM', async () => {
    const plugin = new OpenPlugin('LGTM', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt = 'Show me markdown for a 2 by 2 table with LGTM';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(json_content).toHaveProperty('image_url');
    expect(json_content.image_url.startsWith('https://lgtm.lol')).toBe(true);
  }, 30000);

  test('yt_caption_retriever', async () => {
    const plugin = new OpenPlugin(
      'yt_caption_retriever',
      undefined,
      openaiApiKey,
      true
    );
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'give me a 2 sentence summary of the following yt video https://www.youtube.com/watch?v=P310I19L3Ko';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(json_content.captions).toHaveProperty('en');
  }, 30000);

  test('twtData', async () => {
    const plugin = new OpenPlugin('twtData', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'show me the amount of people @Sebasti54919704 is following';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(json_content.stats.account_found).toBe(true);
  }, 30000);

  test('tailor_erp', async () => {
    const plugin = new OpenPlugin('tailor_erp', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt = 'create a CRM template with ERP generator';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(json_content.APP_ID).not.toBeNull();
  }, 30000);

  test('surge_ai_trends', async () => {
    const plugin = new OpenPlugin(
      'surge_ai_trends',
      undefined,
      openaiApiKey,
      true
    );
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt = 'What are the trending searches for "gpu" in amazon';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(Array.isArray(json_content.items)).toBe(true);
  }, 30000);

  test('speedy_marketing', async () => {
    const plugin = new OpenPlugin(
      'speedy_marketing',
      undefined,
      openaiApiKey,
      true
    );
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt = 'write me an SEO blog about react for marketing';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(typeof json_content.blog).toEqual('string');
  }, 30000);

  test('scholarai', async () => {
    const plugin = new OpenPlugin('scholarai', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'What scientific research exists for semantic representation of language through brain waves. dont sort.';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(typeof json_content.total_num_results).toEqual('number');
  }, 30000);

  test('rephrase', async () => {
    const plugin = new OpenPlugin('rephrase', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'I want to code a react ui with hello world please rephrase that';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(typeof json_content.rephrased.text).toEqual('string');
  }, 30000);

  test('DreamInterpreter', async () => {
    const plugin = new OpenPlugin(
      'DreamInterpreter',
      undefined,
      openaiApiKey,
      true
    );
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'I dreamt of being in a room without any windows getting smaller overtime';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(typeof json_content.dreamResult).toEqual('string');
  }, 30000);

  test.skip('portfoliopilot', async () => {
    // 400 status code when pinging api, probably misformatted args
    const plugin = new OpenPlugin(
      'portfoliopilot',
      undefined,
      openaiApiKey,
      true
    );
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'What stocks should I add for my long term tech portfolio';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(Array.isArray(json_content.top_stocks)).toBe(true);
  }, 30000);

  test.skip('C3_Glide', async () => {
    // 400 status code when pinging api, probably misformatted args
    const plugin = new OpenPlugin('C3_Glide', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'Provide me TAF for KJFK with reguards to aviation weather';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(Array.isArray(json_content.tafs)).toBe(true);
  }, 30000);

  test('Ai_PDF', async () => {
    const plugin = new OpenPlugin('Ai_PDF', undefined, openaiApiKey, true);
    await plugin.init();
    expect(plugin.manifest).not.toBeNull();

    const chatgpt_prompt =
      'Can I have my data be private according to this pdf https://www.unodc.org/pdf/criminal_justice/UN_Basic_Principles_on_the_Role_of_Lawyers.pdf';
    const response = await plugin.fetchPlugin({
      prompt: chatgpt_prompt,
      model: 'gpt-3.5-turbo-0613',
      temperature: 0,
    });

    expect(response).not.toBeNull();
    expect(response.role).toEqual('function');

    const json_content = JSON.parse(response.content);

    expect(typeof json_content[0]).toEqual('string');
  }, 30000);

  // TEMPLATE for testing a new plugin
  // 0. Test the plugin with a prompt in ChatGPT
  // 1. Make sure to replace the PLUGIN with the name of your plugin
  // 2. Make sure to replace the PLUGIN_PROMPT with the prompt you used on ChatGPT
  // 3. Replace the INTENTIONAL_FAILURE error with a test for the final output in json_content
  // 4. Remove the segments under the DELETE comment

  // test('PLUGIN', async () => {
  //   const plugin = new OpenPlugin("PLUGIN", undefined, openaiApiKey, true);
  //   await plugin.init();
  //   expect(plugin.manifest).not.toBeNull();

  //   // DELETE
  //   // if(!fs.existsSync('logs')) {
  //   //   fs.mkdirSync('logs');
  //   // }
  //   // fs.writeFileSync('logs/manifest.json', JSON.stringify(plugin.manifest, null, 2));
  //   // fs.writeFileSync('logs/functions.json', JSON.stringify(plugin.functions, null, 2));

  //   const chatgpt_prompt = 'PLUGIN_PROMPT';
  //   const response = await plugin.fetchPlugin({
  //     prompt: chatgpt_prompt,
  //     model: "gpt-3.5-turbo-0613",
  //     temperature: 0,
  //   });

  //   // DELETE
  //   // fs.writeFileSync('logs/plugin_response.json', JSON.stringify(response, null, 2));

  //   expect(response).not.toBeNull();
  //   expect(response.role).toEqual("function");

  //   const json_content = JSON.parse(response.content);

  //   // Replace the line below with a test for the final output in json_content
  //   throw new Error("INTENTIONAL_FAILURE");
  // }, 30000);
});
