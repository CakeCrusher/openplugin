import 'isomorphic-fetch';
import { beforeEach, describe, expect, test } from '@jest/globals';
import { OpenPlugin, openpluginCompletion } from '../src/index'; // Adjust the import path as necessary
import { todo_plugin as mock_todo_plugin } from './mockData';
import dotenv from 'dotenv';
dotenv.config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

describe('openpluginCompletion todo', () => {
  test('with plugin_name', async () => {
    const todo = `test_chat_completion_${Math.floor(Math.random() * 100000)}`;

    const completion = await openpluginCompletion(
      `add '${todo}' to my todo list`,
      process.env.OPENAI_API_KEY,
      '__testing__',
      undefined,
      { model: 'gpt-3.5-turbo-0613', temperature: 0 }
    );

    const todosRequest = await fetch('http://127.0.0.1:3333/todos');
    const todosBody = await todosRequest.json();

    expect(completion['choices'][0]['message']['content']).toContain(todo);
    expect(todosBody['todos']).toContain(todo);
  });

  test('with root_url', async () => {
    const todo = `test_chat_completion_${Math.floor(Math.random() * 100000)}`;

    const completion = await openpluginCompletion(
      `add '${todo}' to my todo list`,
      process.env.OPENAI_API_KEY,
      undefined,
      'http://127.0.0.1:3333',
      { model: 'gpt-3.5-turbo-0613', temperature: 0 }
    );

    const todosRequest = await fetch('http://127.0.0.1:3333/todos');
    const todosBody = await todosRequest.json();

    expect(completion['choices'][0]['message']['content']).toContain(todo);
    expect(todosBody['todos']).toContain(todo);
  });
});

describe('OpenPlugin todo', () => {
  describe('todo root_url tests', () => {
    test('initiate with url', async () => {
      const todo_openplugin = new OpenPlugin(
        undefined,
        OPENAI_API_KEY,
        'http://127.0.0.1:3333'
      );
      await todo_openplugin.init();
      expect(todo_openplugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
      expect(todo_openplugin.plugin_name).toEqual('todo');
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

  describe('todo plugin_name tests', () => {
    const plugin_name = '__testing__';
    let todo_openplugin: OpenPlugin;

    beforeEach(async () => {
      todo_openplugin = new OpenPlugin(plugin_name);
      await todo_openplugin.init();
    });

    test('initiate with plugin_name', async () => {
      expect(todo_openplugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
      expect(todo_openplugin.plugin_name).toEqual(plugin_name);
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
      const response = await todo_openplugin.fetch_plugin({
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
