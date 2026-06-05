from src.constants import BASE_UNIT, FEET_PER_METER, YARD_PER_METER


class UnitRegistry:
    """기준 단위(meter) 대비 비율 등록·조회."""

    def __init__(self, units: dict[str, float]) -> None:
        self._units = dict(units)

    @classmethod
    def default(cls) -> "UnitRegistry":
        return cls(
            {
                BASE_UNIT: 1.0,
                "feet": FEET_PER_METER,
                "yard": YARD_PER_METER,
            }
        )

    def units(self) -> list[str]:
        return list(self._units.keys())

    def has_unit(self, unit: str) -> bool:
        return unit in self._units

    def to_base(self, unit: str, value: float) -> float:
        if unit not in self._units:
            raise ValueError(f"Unknown unit: {unit}")
        if unit == BASE_UNIT:
            return value
        return value / self._units[unit]

    def from_base(self, unit: str, meter_value: float) -> float:
        if unit not in self._units:
            raise ValueError(f"Unknown unit: {unit}")
        return meter_value * self._units[unit]
