from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float
