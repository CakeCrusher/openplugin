import 'isomorphic-fetch';
import { beforeEach, describe, expect, test } from '@jest/globals';
import { todo_plugin as mock_todo_plugin } from './mockData';
import { OpenPluginMemo } from '../src/openpluginMemo';
import dotenv from 'dotenv';
dotenv.config();

describe('configMemo todo', () => {
  test('full suite', async () => {
    const openPluginMemo = new OpenPluginMemo();
    await openPluginMemo.init();
    const todoOpenplugin = await openPluginMemo.initPlugin('__testing__');
    expect(todoOpenplugin.manifest).not.toBeNull(); // If manifest is private, we need to use bracket notation to access it.
    expect(todoOpenplugin.functions?.length).toEqual(2);
    
    const response = await todoOpenplugin.fetch_plugin({
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
  });
});
describe('retrieve plugins', () => {
  test('retrieve plugins', async () => {
    const openPluginMemo = new OpenPluginMemo();
    await openPluginMemo.init();
    
    let todoOpenplugin = openPluginMemo.getPlugin('__testing__');
    expect(todoOpenplugin).toBeUndefined();
    
    todoOpenplugin = await openPluginMemo.initPlugin('__testing__');
    expect(todoOpenplugin).not.toBeUndefined();

    todoOpenplugin = openPluginMemo.getPlugin('__testing__');
    expect(todoOpenplugin).not.toBeUndefined();
    
    openPluginMemo.removePlugin('__testing__');
    todoOpenplugin = openPluginMemo.getPlugin('__testing__');
    expect(todoOpenplugin).toBeUndefined();

  });
});