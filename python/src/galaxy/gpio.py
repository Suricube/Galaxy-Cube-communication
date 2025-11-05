import json

def reset_all_cmd():
    return json.dumps({
                "command": "function_component",
                "parameters": {
                    "actor_name": "galaxy_gpio",
                    "function_name": "execute_json_command",
                    "function_parameters": "reset_all",
                },
            })

def wait_for_cmd():
    return json.dumps({"command": "wait_for", "parameters": 1})  # 10ms

def stop_trigger_cmd():
    return json.dumps({
                "command": "function_component",
                "parameters": {
                    "actor_name": "galaxy_gpio",
                    "function_name": "execute_json_command",
                    "function_parameters": "stop",
                },
            })

def start_trigger_cmd():
    return json.dumps({
                "command": "function_component",
                "parameters": {
                    "actor_name": "galaxy_gpio",
                    "function_name": "execute_json_command",
                    "function_parameters": "start",
                },
            })
