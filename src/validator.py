from src.entity.registry import UnitRegistry

_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


class ValidationError(ValueError):
    """입력 검증 실패 (FR-06~12)."""


def validate_input(input_str: str) -> None:
    """unit:value 형식·숫자·음수·단위 검증 (FR-06~09)."""
    if ":" not in input_str:
        raise ValidationError(_FORMAT_ERROR)

    unit_str, value_str = input_str.split(":", 1)
    try:
        value = float(value_str.strip())
    except ValueError:
        raise ValidationError(f"Invalid number: {value_str.strip()}") from None

    if value < 0:
        raise ValidationError(f"Negative values are not allowed: {value}")

    unit = unit_str.strip()
    if not UnitRegistry.default().has_unit(unit):
        raise ValidationError(f"Unknown unit: {unit}")


__all__ = ["ValidationError", "validate_input"]
