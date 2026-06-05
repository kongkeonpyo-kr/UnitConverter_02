from src.converter import Converter
from src.parser import parse_input
from src.registry import UnitRegistry

_PROMPT = "Insert value for converting (ex: meter:2.5): "
_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


def run(input_str: str) -> None:
    """입력 문자열을 파싱·변환·출력한다 (I/O 없음, 테스트·재사용 가능)."""
    if ":" not in input_str:
        print(_FORMAT_ERROR)
        return

    _, value_str = input_str.split(":", 1)

    try:
        parsed = parse_input(input_str)
    except ValueError:
        print(f"Invalid number: {value_str.strip()}")
        return

    registry = UnitRegistry.default()
    if not registry.has_unit(parsed.unit):
        print(f"Unknown unit: {parsed.unit}")
        return

    converter = Converter(registry)
    for result in converter.convert(parsed.unit, parsed.value):
        print(f"{parsed.value} {parsed.unit} = {result.value} {result.unit}")


def main() -> None:
    input_str = input(_PROMPT)
    run(input_str)
