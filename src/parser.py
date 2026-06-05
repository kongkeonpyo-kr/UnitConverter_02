from src.entity.registry import UnitRegistry
from src.parsed_input import ParsedInput


def parse_input(input_str: str) -> ParsedInput:
    """unit:value 문자열을 unit·value로 분리 (FR-01)."""
    unit, value_str = input_str.split(":", 1)
    unit = unit.strip()
    resolved = UnitRegistry.default().resolve_unit(unit)
    if resolved is not None:
        unit = resolved
    return ParsedInput(
        unit=unit,
        value=float(value_str.strip()),
    )


__all__ = ["ParsedInput", "parse_input"]
