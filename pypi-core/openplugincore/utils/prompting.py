# C:\Projects\OpenPlugin\openplugin\pypi-core\openplugincore\utils\prompting.py

import json
import random
import re
from typing import Any, List, Union


def estimate_tokens(s: str) -> int:
    return len(s) // 2

def tokens_to_chars(tokens: int) -> int:
    return tokens * 2


def truncate_string(s: str, truncate_by: int) -> str:
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    parts = re.split(url_pattern, s)
    if len(parts) > 1 and url_pattern.search(parts[-1]) is None:
        # If the last part is not a URL, truncate it
        parts[-1] = parts[-1][:-truncate_by]
    elif len(parts) > 2:
        # If the last part is a URL, truncate the part before it
        parts[-2] = parts[-2][:-truncate_by]
    else:
        # If there's only one part and it's not a URL, truncate it
        parts[0] = parts[0][:-truncate_by]
    return ''.join(parts)


def truncate_array(arr: List[Any], truncate_by: int) -> List[Any]:
    random_index = random.randint(0, len(arr) - 1)
    del arr[random_index]
    return arr


def handle_array(arr: List[Any], truncate_by: int) -> List[Any]:
    reduced_array = []
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for item in arr:
        if isinstance(item, dict) and estimate_tokens(json.dumps(item)) > 20:
            reduced_array.append(truncate_json(item, truncate_by))
        elif isinstance(item, str) and estimate_tokens(item) > 10 and (url_pattern.search(item) is None or (item.replace(url_pattern.search(item), '') != '')):
            reduced_array.append(truncate_string(item, truncate_by))
        else:
            reduced_array.append(item)

    if json.dumps(reduced_array) == json.dumps(arr):
        return truncate_array(arr, truncate_by)
    else:
        return reduced_array



def truncate_json(json_obj: Any, truncate_by: int) -> Any:
    if isinstance(json_obj, str):
        # print("truncating string")
        return truncate_string(json_obj, truncate_by)
    elif isinstance(json_obj, list):
        # print("truncating array")
        return handle_array(json_obj, truncate_by)
    elif isinstance(json_obj, dict):
        # print("truncating object")
        has_deleted_misc = False
        for key in list(json_obj.keys()):
            # print("key: " + key)
            if not json_obj[key] or (isinstance(json_obj[key], dict) and len(json_obj[key]) == 0):
                # print("deleting key: " + key)
                del json_obj[key]
            elif not has_deleted_misc and\
            (not isinstance(json_obj[key], str) or (isinstance(json_obj[key], str) and len(json_obj[key]) == 0)) and\
            (not isinstance(json_obj[key], list) or (isinstance(json_obj[key], list) and len(json_obj[key]) == 0)) and\
            not isinstance(json_obj[key], dict):
                # print("deleting key: " + key)
                has_deleted_misc = True
                del json_obj[key]
            else:
                json_obj[key] = truncate_json(json_obj[key], truncate_by)
        if len(json_obj) == 0:
            # print("empty object")
            return None
        return json_obj
    else:
        # print("finishing")
        return json_obj


def truncate_json_root(json_obj: Any, truncate_to: int, verbose: bool = False) -> Any:
    if verbose:
        print('original json token count: ' +
              str(estimate_tokens(json.dumps(json_obj))))
    truncate_by = 1
    prev_json = None
    while estimate_tokens(json.dumps(json_obj)) > truncate_to:
        prev_json = json.dumps(json_obj)
        json_obj = truncate_json(json_obj, truncate_by)
        if json.dumps(json_obj) == prev_json:
            return json_obj
    if verbose:
        print('final json token count: ' +
              str(estimate_tokens(json.dumps(json_obj))))
    return json_obj
