"""순수 도메인 — 단위·비율·변환 결과 (I/O 없음)."""

from src.entity.constants import BASE_UNIT, FEET_PER_METER, YARD_PER_METER
from src.entity.conversion_result import ConversionResult
from src.entity.registry import UnitRegistry

__all__ = [
    "BASE_UNIT",
    "ConversionResult",
    "FEET_PER_METER",
    "UnitRegistry",
    "YARD_PER_METER",
]
