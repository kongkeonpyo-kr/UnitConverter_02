from src.parsed_input import ParsedInput


def parse_input(input_str: str) -> ParsedInput:
    """unit:value 문자열을 unit·value로 분리 (FR-01)."""
    unit, value_str = input_str.split(":", 1)
    return ParsedInput(
        unit=unit.strip(),
        value=float(value_str.strip()),
    )


__all__ = ["ParsedInput", "parse_input"]
