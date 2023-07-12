import 'isomorphic-fetch';
import { describe, expect, test } from '@jest/globals';
import { OpenPlugin } from '../src/index'; // Adjust the import path as necessary
import { todo_plugin as mock_todo_plugin } from './mockData'
import dotenv from 'dotenv';
dotenv.config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

describe('OpenPlugin', () => {
  test('should initiate with url', async () => {
    const plugin = new OpenPlugin(undefined, OPENAI_API_KEY, "http://127.0.0.1:3333");
    await plugin.init();
    expect(plugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
    expect(plugin.plugin_name).toEqual('todo');
    expect(plugin.functions?.length).toEqual(2);
    
    const addTodo_function = plugin.functions?.find((fn) => fn.name === 'addTodo');
    expect(addTodo_function).not.toBeNull();
    expect(addTodo_function?.description).toEqual(mock_todo_plugin.functions[0].description);
  });
});
