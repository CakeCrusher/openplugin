todo_plugin = {
    "prompt": "add 'buy milk' to my todo list",
    "messages": [
        {
            "role": "user",
            "content": "add 'buy milk' to my todo list"
        }
    ],
    "chat_completion_of_function": {
        "role": "assistant",
        "content": None,
        "function_call": {
            "name": "addTodo",
            "arguments": "{\n  \"todo\": \"buy milk\"\n}"
        }
    },
    "llm_chain_out": {
        "name": "addTodo",
        "arguments": {
            "json": {
                "todo": "buy milk"
            }
        }
    },
    "request_out.json()": {
        "todo": "buy milk"
    },
    "functions": [
        {
            "name": "addTodo",
            "description": "Add a todo to the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "json": {
                        "properties": {
                            "todo": {
                                "type": "string",
                                "description": "The todo item to add."
                            }
                        },
                        "type": "object"
                    }
                }
            }
        },
        {
            "name": "getTodos",
            "description": "Get the list of todos",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    ]
}

chat_completion_of_random_function = {
    "role": "assistant",
    "content": None,
    "function_call": {
        "name": "imRandom",
        "arguments": "{\n  \"todo\": \"buy milk\"\n}"
    }
}
