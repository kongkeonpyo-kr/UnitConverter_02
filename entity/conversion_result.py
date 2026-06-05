from dataclasses import dataclass


@dataclass(frozen=True)
class ConversionResult:
    unit: str
    value: float
