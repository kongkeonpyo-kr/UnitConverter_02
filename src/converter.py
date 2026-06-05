from src.entity.conversion_result import ConversionResult
from src.entity.registry import UnitRegistry


class Converter:
    """meter 기준 허브 변환 — 소스 단위는 결과에서 제외."""

    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert(self, source_unit: str, value: float) -> list[ConversionResult]:
        meter_value = self._registry.to_base(source_unit, value)
        results: list[ConversionResult] = []
        for unit in self._registry.units():
            if unit == source_unit:
                continue
            converted = self._registry.from_base(unit, meter_value)
            results.append(ConversionResult(unit=unit, value=converted))
        return results
