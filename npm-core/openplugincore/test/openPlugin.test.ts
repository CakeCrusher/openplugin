import 'isomorphic-fetch';
import { beforeEach, describe, expect, test } from '@jest/globals';
import { OpenPlugin } from '../src/index'; // Adjust the import path as necessary
import { todo_plugin as mock_todo_plugin } from './mockData';
import dotenv from 'dotenv';
import { estimateTokens } from '../src/util/prompting';
dotenv.config();

const openaiApiKey = process.env.OPENAI_API_KEY;

describe('OpenPlugin todo', () => {
  describe('todo rootUrl tests', () => {
    test('initiate with url', async () => {
      const todo_openplugin = new OpenPlugin(
        undefined,
        'http://127.0.0.1:3333',
        openaiApiKey
      );
      await todo_openplugin.init();
      expect(todo_openplugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
      expect(todo_openplugin.pluginName).toEqual('todo');
      expect(todo_openplugin.functions?.length).toEqual(2);

      const addTodo_function = todo_openplugin.functions?.find(
        (fn) => fn.name === 'addTodo'
      );
      expect(addTodo_function).not.toBeNull();
      expect(addTodo_function?.description).toEqual(
        mock_todo_plugin.functions[0].description
      );
    });
  });

  describe('todo pluginName tests', () => {
    const pluginName = '__testing__';
    let todo_openplugin: OpenPlugin;

    beforeEach(async () => {
      todo_openplugin = new OpenPlugin(pluginName);
      await todo_openplugin.init();
    });

    test('initiate with pluginName', async () => {
      expect(todo_openplugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
      expect(todo_openplugin.pluginName).toEqual(pluginName);
      expect(todo_openplugin.functions?.length).toEqual(2);

      const addTodo_function = todo_openplugin.functions?.find(
        (fn) => fn.name === 'addTodo'
      );
      expect(addTodo_function).not.toBeNull();
      expect(addTodo_function?.description).toEqual(
        mock_todo_plugin.functions[0].description
      );
    }, 30000);

    test('fetch plugin', async () => {
      const response = await todo_openplugin.fetchPlugin({
        prompt: mock_todo_plugin.prompt,
        model: 'gpt-3.5-turbo-0613',
      });

      expect(response).not.toBeNull();
      expect(response.role).toEqual('function');
      expect(response.name).toEqual('addTodo');

      const json_content = JSON.parse(response.content);
      expect(json_content.todo).toEqual(
        mock_todo_plugin['request_out.json()'].todo
      );
    }, 30000);
  });
});

test('truncated response test', async () => {
  const ytPlugin = new OpenPlugin('yt_caption_retriever');
  await ytPlugin.init();
  const response = await ytPlugin.fetchPlugin({
    prompt: 'summarize this video https://www.youtube.com/watch?v=gZVeRQkxCdc',
    model: 'gpt-3.5-turbo-0613',
    truncate: true,
  });
  console.log(JSON.stringify(response, null, 2));
  expect(estimateTokens(response.content)).toBe(3691);
}, 30000);
