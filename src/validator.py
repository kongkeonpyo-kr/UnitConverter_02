_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"


class ValidationError(ValueError):
    """입력 검증 실패 (FR-06~12)."""


def validate_input(input_str: str) -> None:
    """unit:value 형식·숫자 검증 (FR-06, FR-07)."""
    if ":" not in input_str:
        raise ValidationError(_FORMAT_ERROR)

    _, value_str = input_str.split(":", 1)
    try:
        float(value_str.strip())
    except ValueError:
        raise ValidationError(f"Invalid number: {value_str.strip()}") from None


__all__ = ["ValidationError", "validate_input"]
