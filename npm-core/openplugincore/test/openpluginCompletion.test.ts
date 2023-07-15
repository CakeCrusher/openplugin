import 'isomorphic-fetch';
import { describe, expect, test } from '@jest/globals';
import { openpluginCompletion } from '../src/index'; // Adjust the import path as necessary
import dotenv from 'dotenv';
dotenv.config();

describe('openpluginCompletion todo', () => {
  test('with pluginName', async () => {
    const todo = `test_chat_completion_${Math.floor(Math.random() * 100000)}`;

    const completion = await openpluginCompletion(
      `add '${todo}' to my todo list`,
      '__testing__',
      undefined,
      process.env.OPENAI_API_KEY,
      { model: 'gpt-3.5-turbo-0613', temperature: 0 }
    );

    const todosRequest = await fetch('http://127.0.0.1:3333/todos');
    const todosBody = await todosRequest.json();

    expect(completion['choices'][0]['message']['content']).toContain(todo);
    expect(todosBody['todos']).toContain(todo);
  });

  test('with rootUrl', async () => {
    const todo = `test_chat_completion_${Math.floor(Math.random() * 100000)}`;

    const completion = await openpluginCompletion(
      `add '${todo}' to my todo list`,
      undefined,
      'http://127.0.0.1:3333',
      process.env.OPENAI_API_KEY,
      { model: 'gpt-3.5-turbo-0613', temperature: 0 }
    );

    const todosRequest = await fetch('http://127.0.0.1:3333/todos');
    const todosBody = await todosRequest.json();

    expect(completion['choices'][0]['message']['content']).toContain(todo);
    expect(todosBody['todos']).toContain(todo);
  });
});
