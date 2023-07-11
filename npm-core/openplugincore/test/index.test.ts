import { describe, expect, test } from '@jest/globals';
import { openpluginCompletion } from '../src/index';
import dotenv from 'dotenv';
import 'isomorphic-fetch';
dotenv.config();

describe('openpluginCompletion', () => {
  const todo = `test_chat_completion_${Math.floor(Math.random() * 100000)}`;
  const EARLY_ACCESS_TOKEN = process.env.EARLY_ACCESS_TOKEN;
  const OPENPLUGIN_DEVELOPMENT = process.env.OPENPLUGIN_DEVELOPMENT === 'true';

  if (OPENPLUGIN_DEVELOPMENT) {
    test('adds todo', async () => {
      const completion = await openpluginCompletion({
        earlyAccessToken: EARLY_ACCESS_TOKEN!,
        pluginName: '__testing__',
        model: 'gpt-3.5-turbo-0613',
        messages: [{ role: 'user', content: `add '${todo}' to my todo list` }],
        temperature: 0,
      });

      const todosResponse = await fetch('http://127.0.0.1:3333/todos');
      const todosBody: any = await todosResponse.json();

      expect(completion.choices[0].message.content).toContain(todo);
      expect(todosBody.todos).toContain(todo);
    }, 30000);
  }

  test('ImageSearch', async () => {
    const completion = await openpluginCompletion({
      earlyAccessToken: EARLY_ACCESS_TOKEN!,
      pluginName: 'ImageSearch',
      model: 'gpt-3.5-turbo-0613',
      messages: [{ role: 'user', content: 'show me an image of a dog' }],
      temperature: 0,
    });

    expect(completion.choices[0].message.content.toLowerCase()).toContain(
      'dog'
    );
  }, 30000);

  test('experiment', async () => {
    const completion = await openpluginCompletion({
      earlyAccessToken: EARLY_ACCESS_TOKEN!,
      pluginName: 'ImageSearch',
      messages: [{ role: 'user', content: `show me an image of a dog` }],
    });
    expect(completion.choices).toBeTruthy();
  }, 30000);
});
