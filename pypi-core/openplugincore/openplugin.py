import json
from urllib.error import HTTPError
import requests
from typing import Any, List, Dict, Union, Tuple, Callable
import os
from .types import ChatgptAssistantMessage, ChatgptFunctionMessage, PluginConfigs
from .utils.constants import openai_models_info
from .utils.prompting import estimate_tokens, tokens_to_chars, truncate_json_root
from langchain.chains.openai_functions.openapi import openapi_spec_to_openai_fn
from langchain.utilities.openapi import OpenAPISpec
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage, FunctionMessage
from langchain import LLMChain
import openai
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

plugin_configs: Dict[str, PluginConfigs] = {}


class OpenPlugin:
    def __init__(self, plugin_name: str = None, openai_api_key: str = None, root_url: str = None, verbose: bool = False):
        self.name: str = plugin_name
        self.root_url: str = root_url
        self.description: str = None
        self.manifest: Any = None
        self.functions: List[Dict[str, Any]] = None
        self.call_api_fn: Callable = None
        self.verbose: bool = verbose
        if self.name is None and self.root_url is None:
            raise ValueError("Either plugin_name or root_url must be passed in as a parameter")
        if openai_api_key is None:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key is None:
                raise ValueError("OPENAI_API_KEY not found. You can pass in the parameter openai_api_key. You can also set the environment variable OPENAI_API_KEY=<API-KEY>.")
        os.environ["OPENAI_API_KEY"] = openai_api_key
        openai.api_key = openai_api_key
        self.init(plugin_name)
        self.description: str = self.manifest["description_for_model"]

    def init(self, plugin_name: str = None) -> None:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        plugins_file_path = os.path.join(base_dir, "plugins.json")
        
        # fetch plugins from github
        try:
            plugins_url = "https://raw.githubusercontent.com/CakeCrusher/openplugin/main/migrations/plugin_store/openplugins.json"
            response = requests.get(plugins_url)
            response.raise_for_status()
            plugins = response.json()
        except Exception as e:
            raise HTTPError(f"Unable to fetch plugins from github url '{plugins_url}'")
    
        # if self.root_url has a value
        if self.root_url is None:
            try:
                self.root_url = plugins[plugin_name]
            except KeyError:
                # throw error
                raise KeyError("Plugin not found")
        self.manifest = self.fetch_manifest(self.root_url)
        self.functions, self.call_api_fn = self.openapi_to_functions_and_call_api_fn(self.manifest)

    def fetch_manifest(self, root_url: str) -> Any:
        if plugin_configs.get(self.name, {}).get("manifest", None) is not None:
            return plugin_configs[self.name]["manifest"]
        
        response = requests.get(root_url + "/.well-known/ai-plugin.json")
        response.raise_for_status()  # Raise exception if the request failed
        manifest = response.json()
        if not self.name:
            self.name: str = manifest["name_for_model"]
        if self.verbose:
            print(f"\"{self.name}\" manifest: ", json.dumps(manifest, indent=2))

        # add manifest to plugin_configs
        plugin_configs[self.name] = {
            **plugin_configs.get(self.name, {}),
            "manifest": manifest
        }
        return manifest
    
    def openapi_to_functions_and_call_api_fn(self, manifest: Any) -> Tuple[List[Dict[str, Any]], Callable]:
        openapi_url = manifest.get("api", {}).get("url")
        if self.verbose:
            print(f"\"{self.name}\" openapi_url: ", openapi_url)
        if openapi_url == None:
            raise ValueError("OpenAPI URL not found in manifest")
        if isinstance(openapi_url, Union[OpenAPISpec, str]):
            for conversion in (
                # each of the below specs can get stuck in a while loop
                OpenAPISpec.from_url,
                OpenAPISpec.from_file,
                OpenAPISpec.from_text,
            ):
                try:
                    openapi_url = conversion(openapi_url)  # type: ignore[arg-type]
                    break
                except Exception:  # noqa: E722
                    pass
            if isinstance(openapi_url, str):
                raise ValueError(f"Unable to parse spec from source {openapi_url}")
        openai_fns, call_api_fn = openapi_spec_to_openai_fn(openapi_url)
        if self.verbose:
            print(f"\"{self.name}\" functions: ", json.dumps(openai_fns, indent=2))
        return openai_fns, call_api_fn

    def _convert_openai_messages_to_langchain_messages(self, openai_messages: List[Any]) -> List[ChatgptAssistantMessage]:
        langchain_messages = []

        for openai_message in openai_messages:
            if openai_message["role"] == "system":
                langchain_messages.append(SystemMessage(content=openai_message["content"]))
            elif openai_message["role"] == "user":
                langchain_messages.append(HumanMessage(content=openai_message["content"]))
            elif openai_message["role"] == "function":
                langchain_messages.append(FunctionMessage(name=openai_message["name"], content=openai_message["content"]))
            elif openai_message["role"] == "assistant":
                # set veriable content to "" if it is None
                content = openai_message["content"] if openai_message["content"] is not None else ""
                langchain_messages.append(AIMessage(content=content, additional_kwargs={"function_call": openai_message["function_call"]}))
        
        return langchain_messages

    def fetch_plugin(self, messages: list[dict], truncate: Union[bool, int] = False, truncate_offset: int = 0, **chatgpt_args) -> ChatgptFunctionMessage:
        model = chatgpt_args.get("model", None)
        if model not in ["gpt-3.5-turbo-0613", "gpt-4-0613"]:
            raise ValueError("Model must be either gpt-3.5-turbo-0613 or gpt-4-0613")
        
        llm =  ChatOpenAI(
            **chatgpt_args,
        )
        llm_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_template("{query}"),
            llm_kwargs={"functions": self.functions},
            output_parser=JsonOutputFunctionsParser(args_only=False),
            output_key="function",
            verbose=self.verbose,
            # **(llm_kwargs or {}),
        )
        # if it is plugin function response
        functions_tokens = estimate_tokens(json.dumps(self.functions))

        try:
            # MESSAGES TO PROMPT
            # if there is a message with role system then pop it, iterate through all messages to find it
            system_message = ''
            for message in messages:
                if message["role"] == 'system':
                    system_message = 'system' + ": " + message['content'] + "\n"
                    messages.remove(message)
                    break
            
            # print("system_message: ", system_message)
            # Combine messages into one string
            messages_aggregate = '\n'.join([f"{message['role']}: {message['content']}" for message in messages])
            complete_messages_aggregate_tokens = estimate_tokens(system_message + messages_aggregate)
            # print("complete_messages_aggregate_tokens: ", complete_messages_aggregate_tokens)
            # print("functions_tokens: ", functions_tokens)
            messages_truncation_offset = tokens_to_chars(max(complete_messages_aggregate_tokens + functions_tokens - openai_models_info[model]["max_tokens"], 0)) 
            # print("messages_truncation_offset: ", messages_truncation_offset)
            messages_aggregate = messages_aggregate[messages_truncation_offset:]
           
            # TODO: temp fix to prevent collation of messages
            if (messages_truncation_offset > 0):
                messages_aggregate = "user/assistant: " + messages_aggregate
           
            complete_messages_aggregate = system_message + messages_aggregate
            # print("complete_messages_aggregate: ", complete_messages_aggregate)  
            # print("final length: ", estimate_tokens(complete_messages_aggregate))          

            # Replace prompt with messageAggregate
            llm_chain_out = llm_chain.run(complete_messages_aggregate)
            if self.verbose:
                print("Using plugin: " + self.name)
        except KeyError as e:
            # if error includes "function_call" then it is not a plugin function
            if "function_call" in str(e):
                raise ValueError("Not a plugin function")
            else:
                raise e
        if llm_chain_out["name"] not in [function["name"] for function in self.functions]:
            raise ValueError("Not a plugin function")

        # EDGE CASE
        def remove_empty_from_dict(input_dict):
            cleaned_dict = {}
            for k, v in input_dict.items():
                if isinstance(v, dict):
                    v = remove_empty_from_dict(v)
                if v and v != "none":  # only add to cleaned_dict if v is not empty
                    cleaned_dict[k] = v
            return cleaned_dict
        llm_chain_out["arguments"] = remove_empty_from_dict(llm_chain_out["arguments"])
        if self.verbose:
            print(f"\"{self.name}\" llm_chain_out: ", json.dumps(llm_chain_out, indent=2))

        # make the api call
        def request_chain(name,arguments):
            res = self.call_api_fn(
                name, arguments, headers=None, params=None
            )
            return res
        request_out = request_chain(**llm_chain_out)
        json_response = request_out.json()

        if truncate:
            truncate_to = truncate if not isinstance(truncate, bool) else None
            if truncate_to is None:
                token_slack = 56 + 300
                truncate_to = openai_models_info[model]['max_tokens'] - estimate_tokens(json.dumps(messages[-1])) - token_slack - truncate_offset
            json_response = truncate_json_root(json_response, truncate_to)

        if self.verbose:
            print(f"\"{self.name}\" json_response: ", json.dumps(json_response, indent=2))
        try:
            return ChatgptFunctionMessage(
                role="function",
                name=llm_chain_out["name"],
                content=json.dumps(json_response)
            )
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError(f"API call failed, API returned the following non-JSON response:\n{response.content}")