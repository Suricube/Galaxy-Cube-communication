from typing import Literal

def set_pulse_forwarder(
    output_pin: str = "pulse_0",
    input_signal_generator_type: Literal["asg", "dsg"] = "asg",
    input_signal_generator_index: int = 0,
) -> dict:
    return {
        "command": "function_component",
        "parameters": [
            {
                "actor_name": output_pin,
                "function_name": "execute_json_command",
                "function_parameters": {
                    "set_settings": {
                        "select_signal_generator": {
                            input_signal_generator_type: input_signal_generator_index
                        },
                        "select_pulse_type": "pulse_at_section",
                        "pulse_divider_value": 0,
                        "pulse_delayer": 0,
                        "pulse_width": 2000,  # 8ns * 1000 = 8us
                        "flags": 0,
                    }
                },
            }
        ],
    }
