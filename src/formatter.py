from decimal import ROUND_HALF_UP, Decimal

from src.converter import Converter
from src.entity.registry import UnitRegistry


def round_half_up(value: float, decimals: int = 1) -> str:
    """소수 N자리 round half up — FR-03."""
    quantizer = Decimal(10) ** -decimals
    return str(Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP))


def format_conversions(source_unit: str, value: float) -> list[str]:
    """변환 결과를 '8.2 feet' 형식 문자열 목록으로 반환 — FR-03."""
    registry = UnitRegistry.default()
    converter = Converter(registry)
    results = converter.convert(source_unit, value)
    return [f"{round_half_up(r.value)} {r.unit}" for r in results]
