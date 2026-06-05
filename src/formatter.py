from decimal import ROUND_HALF_UP, Decimal

from src.converter import Converter
from src.entity.registry import UnitRegistry


def round_half_up(value: float, decimals: int = 1) -> str:
    """소수 N자리 round half up — FR-03."""
    quantizer = Decimal(10) ** -decimals
    return str(Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP))


def _format_table_input(value: float) -> str:
    """테이블 input 열 — 최대 4자리 round half up, 불필요한 0 제거."""
    quantized = Decimal(str(value)).quantize(
        Decimal("0.0001"), rounding=ROUND_HALF_UP
    )
    return format(quantized.normalize(), "f")


def _format_table_result(value: float, *, is_source: bool) -> str:
    """테이블 result 열 — 소스 단위는 input과 동일, 그 외 4자리 고정."""
    if is_source:
        return _format_table_input(value)
    return round_half_up(value, decimals=4)


_TABLE_MIN_COL_WIDTHS = (8, 9, 9)


def _render_box_table(headers: list[str], rows: list[list[str]]) -> str:
    """박스 드로잉 문자로 표 형식 문자열을 만든다."""
    columns = list(zip(*([headers] + rows)))
    widths = [
        max(min_width, max(len(cell) for cell in col) + 2)
        for min_width, col in zip(_TABLE_MIN_COL_WIDTHS, columns)
    ]

    def _border(left: str, mid: str, right: str, fill: str) -> str:
        segments = [fill * width for width in widths]
        return left + mid.join(segments) + right

    def _row(cells: list[str]) -> str:
        padded = [f" {cell.ljust(width - 2)} " for cell, width in zip(cells, widths)]
        return "│" + "│".join(padded) + "│"

    lines = [
        _border("┌", "┬", "┐", "─"),
        _row(headers),
        _border("├", "┼", "┤", "─"),
        *[_row(row) for row in rows],
        _border("└", "┴", "┘", "─"),
    ]
    return "\n".join(lines)


def format_conversions(source_unit: str, value: float) -> list[str]:
    """변환 결과를 '8.2 feet' 형식 문자열 목록으로 반환 — FR-03."""
    registry = UnitRegistry.default()
    converter = Converter(registry)
    results = converter.convert(source_unit, value)
    return [f"{round_half_up(r.value)} {r.unit}" for r in results]


def format_table(
    source_unit: str,
    value: float,
    registry: UnitRegistry | None = None,
) -> str:
    """EXT-07 — unit / input / result 박스 테이블."""
    registry = registry or UnitRegistry.default()
    meter_value = registry.to_base(source_unit, value)
    input_str = _format_table_input(value)

    rows: list[list[str]] = []
    for unit in registry.units():
        is_source = unit == source_unit
        if is_source:
            result_str = input_str
        else:
            converted = registry.from_base(unit, meter_value)
            result_str = _format_table_result(converted, is_source=False)
        rows.append([unit, input_str, result_str])

    return _render_box_table(["unit", "input", "result"], rows)
