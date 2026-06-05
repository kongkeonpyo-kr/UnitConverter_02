from src.converter import Converter
from src.entity.registry import UnitRegistry
from src.parser import parse_input
from src.validator import ValidationError, validate_input

_PROMPT = "Insert value for converting (ex: meter:2.5): "


def run(input_str: str) -> None:
    """입력 문자열을 검증·파싱·변환·출력한다 (I/O 없음, 테스트·재사용 가능)."""
    try:
        validate_input(input_str)
    except ValidationError as exc:
        print(exc)
        return

    parsed = parse_input(input_str)
    registry = UnitRegistry.default()
    converter = Converter(registry)
    for result in converter.convert(parsed.unit, parsed.value):
        print(f"{parsed.value} {parsed.unit} = {result.value} {result.unit}")


def main() -> None:
    input_str = input(_PROMPT)
    run(input_str)
