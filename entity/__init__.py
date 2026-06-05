"""순수 도메인 — 단위·비율·변환 결과 (I/O 없음)."""

from entity.conversion_result import ConversionResult
from entity.constants import BASE_UNIT, FEET_PER_METER, YARD_PER_METER
from entity.registry import UnitRegistry

__all__ = [
    "BASE_UNIT",
    "ConversionResult",
    "FEET_PER_METER",
    "UnitRegistry",
    "YARD_PER_METER",
]
