todo_plugin = {
    "prompt": "add 'buy milk' to my todo list",
    "messages": [
        {
            "role": "user",
            "content": "add 'buy milk' to my todo list"
        }
    ],
    "plugin_headers": {
        "Authorization": "Bearer secret"
    },
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
    ],
    "manifest": {
        "schema_version": "v1",
        "name_for_human": "TODO List MODIFIED",
        "name_for_model": "todo",
        "description_for_human": "Manage your TODO list. You can add, remove and view your TODOs.",
        "description_for_model": "Plugin for managing a TODO list, you can add, remove and view your TODOs.",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "http://localhost:3333/openapi.yaml"
        },
        "logo_url": "http://localhost:3333/logo.png",
        "contact_email": "contact@example.com",
        "legal_info_url": "http://www.example.com/legal"
    }
}

chat_completion_of_random_function = {
    "role": "assistant",
    "content": None,
    "function_call": {
        "name": "imRandom",
        "arguments": "{\n  \"todo\": \"buy milk\"\n}"
    }
}
