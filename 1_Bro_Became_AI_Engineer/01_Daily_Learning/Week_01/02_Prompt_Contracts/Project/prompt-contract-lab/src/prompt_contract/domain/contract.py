from dataclasses import dataclass


@dataclass(frozen=True)
class PromptContract:
    role: str
    objective: str
    instructions: list[str]
    input_template: str
    output_template: str
    version: str