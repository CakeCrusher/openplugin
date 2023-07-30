from typing import Any, Dict, TypedDict
from enum import Enum

class AssistantRole(Enum):
    USER = "user"

class ChatgptAssistantMessage(TypedDict):
    role: AssistantRole
    content: str

class FunctionRole(Enum):
    FUNCTION = "function"

class ChatgptFunctionMessage(TypedDict):
    role: FunctionRole
    name: str
    content: str

class CallableFunction(TypedDict):
    name: str
    description: str
    parameters: Dict[str, Any]

class OTPHashValue(TypedDict):
    path: str
    method: str
    parameters: Any
    request_body: Any
OTPHash = Dict[str, OTPHashValue]

class PluginConfigs(TypedDict):
    manifest: Any
    openapi: Any