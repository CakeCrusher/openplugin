export let todo_plugin: any = {
  prompt: "add 'buy milk' to my todo list",
  chat_completion_of_function: {
    role: 'assistant',
    content: null,
    function_call: {
      name: 'addTodo',
      arguments: '{\n  "todo": "buy milk"\n}',
    },
  },
  llm_chain_out: {
    name: 'addTodo',
    arguments: {
      json: {
        todo: 'buy milk',
      },
    },
  },
  'request_out.json()': {
    todo: 'buy milk',
  },
  functions: [
    {
      name: 'addTodo',
      description: 'Add a todo to the list',
      parameters: {
        type: 'object',
        properties: {
          data: {
            additionalProperties: {},
            properties: {
              todo: {
                type: 'string',
                description: 'The todo item to add.',
              },
            },
            required: [],
            type: 'object',
          },
        },
        required: ['data'],
      },
    },
    {
      name: 'getTodos',
      description: 'Get the list of todos',
      parameters: {
        type: 'object',
        required: [],
        properties: {},
      },
    },
  ],
};

export let chat_completion_of_random_function: any = {
  role: 'assistant',
  content: null,
  function_call: {
    name: 'imRandom',
    arguments: '{\n  "todo": "buy milk"\n}',
  },
};
