"""
tests/Boundary/test_cli.py — Track A (Boundary) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- Track  : A (Boundary) → Dual-Track: UI
- §3.3   : FR-01, FR-06 ~ FR-12 입력 파싱·검증
- §8.2   : TC-FR-01, TC-FR-06 ~ TC-FR-12
- Layer  : boundary
- Test File : tests/Boundary/test_cli.py
"""

import re

import pytest

# ---------------------------------------------------------------------------
# Req ID  : FR-01
# Track   : A (Boundary)
# Test ID : TC-FR-01
# P       : P0
# Given   : 유효 문자열 "meter:2.5"
# Then    : unit="meter", value=2.5
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-01")
@pytest.mark.track("UI")
def test_tc_fr_01_parse_meter_2_5():
    """TC-FR-01: meter:2.5 파싱 — FR-01 입력 파싱 (Track A)"""
    from src.parsed_input import ParsedInput
    from src.parser import parse_input

    # Given
    input_str = "meter:2.5"

    # When
    result = parse_input(input_str)

    # Then
    assert isinstance(result, ParsedInput)
    assert result.unit == "meter"
    assert result.value == 2.5


# ---------------------------------------------------------------------------
# Req ID  : FR-06
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-06 / TC-FR-06
# Layer   : boundary
# P       : P0
# Given   : "meter" (콜론 없음)
# Then    : 형식 오류 메시지 또는 exit 1
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-06")
@pytest.mark.track("UI")
def test_u_fr06_invalid_format_missing_colon():
    """U-FR-06 / TC-FR-06: 잘못된 형식 — FR-06 (UI Track)"""
    input_str = "meter"
    expected_msg = "Invalid format. Use unit:value (ex: meter:2.5)"

    # Act (GREEN)
    from src.validator import ValidationError, validate_input

    with pytest.raises(ValidationError, match=re.escape(expected_msg)):
        validate_input(input_str)


# ---------------------------------------------------------------------------
# Req ID  : FR-07
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-07 / TC-FR-07
# Layer   : boundary
# P       : P0
# Given   : meter:abc
# Then    : Invalid number: abc
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-07")
@pytest.mark.track("UI")
def test_u_fr07_invalid_number():
    """U-FR-07 / TC-FR-07: 잘못된 숫자 — FR-07 (UI Track)"""
    input_str = "meter:abc"
    expected_msg = "Invalid number: abc"

    # Act (GREEN)
    from src.validator import ValidationError, validate_input

    with pytest.raises(ValidationError, match=re.escape(expected_msg)):
        validate_input(input_str)


# ---------------------------------------------------------------------------
# Req ID  : FR-08
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-08 / TC-FR-08
# Layer   : boundary
# P       : P0
# Given   : meter:-1
# Then    : Negative values are not allowed, 거부
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-08")
@pytest.mark.track("UI")
def test_u_fr08_negative_value_rejected():
    """U-FR-08 / TC-FR-08: 음수 거부 — FR-08 (UI Track)"""
    input_str = "meter:-1"
    expected_fragment = "Negative values are not allowed"

    # Act (GREEN)
    from src.validator import ValidationError, validate_input

    with pytest.raises(ValidationError, match=re.escape(expected_fragment)):
        validate_input(input_str)


# ---------------------------------------------------------------------------
# Req ID  : FR-09
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-09 / TC-FR-09
# Layer   : boundary
# P       : P0
# Given   : cubit:1 (미등록)
# Then    : Unknown unit: cubit
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-09")
@pytest.mark.track("UI")
def test_u_fr09_unknown_unit():
    """U-FR-09 / TC-FR-09: 미지 단위 — FR-09 (UI Track)"""
    input_str = "cubit:1"
    expected_msg = "Unknown unit: cubit"

    # Act (GREEN)
    # from src.validator import validate_input
    # with pytest.raises(ValidationError, match=expected_msg):
    #     validate_input(input_str)

    pytest.fail(f"RED: FR-09 GREEN 미구현 — Given {input_str!r}, Then {expected_msg!r}")


# ---------------------------------------------------------------------------
# Req ID  : FR-10
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-10 / TC-FR-10
# Layer   : boundary
# P       : P0
# Given   : ":2.5" 또는 "meter:"
# Then    : empty format 오류
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-10")
@pytest.mark.track("UI")
@pytest.mark.parametrize("input_str", [":2.5", "meter:"])
def test_u_fr10_empty_unit_or_value(input_str):
    """U-FR-10 / TC-FR-10: 빈 unit/value — FR-10 (UI Track)"""
    expected_fragment = "Unit and value must not be empty"

    # Act (GREEN)
    # from src.validator import validate_input
    # with pytest.raises(ValidationError, match=expected_fragment):
    #     validate_input(input_str)

    pytest.fail(
        f"RED: FR-10 GREEN 미구현 — Given {input_str!r}, "
        f"Then {expected_fragment!r}"
    )


# ---------------------------------------------------------------------------
# Req ID  : FR-11
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-11 / TC-FR-11
# Layer   : boundary
# P       : P0
# Given   : " meter : 2.5 "
# Then    : unit="meter", value=2.5
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-11")
@pytest.mark.track("UI")
def test_u_fr11_whitespace_trim():
    """U-FR-11 / TC-FR-11: 공백 trim — FR-11 (UI Track)"""
    input_str = " meter : 2.5 "
    expected_unit = "meter"
    expected_value = 2.5

    # Act (GREEN)
    # from src.parser import parse_input
    # result = parse_input(input_str)

    # Assert (GREEN 시 활성화)
    # assert result.unit == expected_unit
    # assert result.value == expected_value

    pytest.fail(
        f"RED: FR-11 GREEN 미구현 — Given {input_str!r}, "
        f"Then unit={expected_unit!r}, value={expected_value}"
    )


# ---------------------------------------------------------------------------
# Req ID  : FR-12
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-12 / TC-FR-12
# Layer   : boundary
# P       : P0
# Given   : Meter:2.5
# Then    : Unknown unit: Meter
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-12")
@pytest.mark.track("UI")
def test_u_fr12_case_sensitive_unit_rejected():
    """U-FR-12 / TC-FR-12: 대소문자 거부 — FR-12 (UI Track)"""
    input_str = "Meter:2.5"
    expected_msg = "Unknown unit: Meter"

    # Act (GREEN)
    # from src.validator import validate_input
    # with pytest.raises(ValidationError, match=expected_msg):
    #     validate_input(input_str)

    pytest.fail(f"RED: FR-12 GREEN 미구현 — Given {input_str!r}, Then {expected_msg!r}")
