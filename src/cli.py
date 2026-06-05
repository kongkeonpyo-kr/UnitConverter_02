import argparse
import sys

from src.converter import Converter
from src.entity.registry import UnitRegistry
from src.formatter import format_table
from src.parser import parse_input
from src.validator import ValidationError, validate_input

_PROMPT = "Insert value for converting (ex: meter:2.5): "


def run(input_str: str, output_format: str = "line") -> None:
    """입력 문자열을 검증·파싱·변환·출력한다 (I/O 없음, 테스트·재사용 가능)."""
    try:
        validate_input(input_str)
    except ValidationError as exc:
        print(exc)
        return

    parsed = parse_input(input_str)
    registry = UnitRegistry.default()

    if output_format == "table":
        print(format_table(parsed.unit, parsed.value, registry))
        return

    converter = Converter(registry)
    for result in converter.convert(parsed.unit, parsed.value):
        print(f"{parsed.value} {parsed.unit} = {result.value} {result.unit}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Unit length converter")
    parser.add_argument(
        "--format",
        choices=["line", "table", "json", "csv"],
        default="line",
        help="output format (default: line)",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="unit:value to convert (ex: meter:2.5)",
    )
    args = parser.parse_args(argv)

    input_str = args.input if args.input is not None else input(_PROMPT)
    run(input_str, output_format=args.format)


if __name__ == "__main__":
    main(sys.argv[1:])
