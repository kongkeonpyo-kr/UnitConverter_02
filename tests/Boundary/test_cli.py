"""
tests/Boundary/test_cli.py — Track A (Boundary) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- Track  : A (Boundary) → Dual-Track: UI
- §3.3   : FR-01, FR-06 ~ FR-12 입력 파싱·검증
- §3.7   : EXT-07 ~ EXT-09 출력 포맷
- §8.2   : TC-FR-01, TC-FR-06 ~ TC-FR-12
- §8.4   : TC-EXT-07 ~ TC-EXT-09
- Layer  : boundary
- Test File : tests/Boundary/test_cli.py
"""

import contextlib
import io
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
    from src.validator import ValidationError, validate_input

    with pytest.raises(ValidationError, match=re.escape(expected_msg)):
        validate_input(input_str)


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
    from src.validator import ValidationError, validate_input

    with pytest.raises(ValidationError, match=re.escape(expected_fragment)):
        validate_input(input_str)


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
    from src.parser import parse_input

    result = parse_input(input_str)

    # Assert (GREEN)
    assert result.unit == expected_unit
    assert result.value == expected_value


# ---------------------------------------------------------------------------
# Req ID  : FR-12
# Track   : UI (PRD Track A — Boundary)
# Test ID : U-FR-12 / TC-FR-12
# Layer   : boundary
# P       : P0
# Given   : Meter:2.5, METER:1, Feet:1, YARD:1
# Then    : 검증 통과, unit은 Registry 표준 키(소문자)로 정규화
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-12")
@pytest.mark.track("UI")
@pytest.mark.parametrize(
    "input_str,expected_unit",
    [
        ("Meter:2.5", "meter"),
        ("METER:2.5", "meter"),
        ("Feet:1", "feet"),
        ("YARD:1", "yard"),
    ],
)
def test_u_fr12_case_insensitive_unit_accepted(input_str, expected_unit):
    """U-FR-12 / TC-FR-12: 대소문자 무시 — FR-12 (UI Track)"""
    from src.parser import parse_input
    from src.validator import validate_input

    # Act (GREEN)
    validate_input(input_str)

    result = parse_input(input_str)
    assert result.unit == expected_unit


# ---------------------------------------------------------------------------
# Req ID  : EXT-07
# Track   : A (Boundary)
# Test ID : TC-EXT-07
# P       : P1
# Given   : --format table, meter:2.5 (fixture 비율 meter:1, feet:3, yard:1)
# Then    : unit/input/result 박스 테이블 출력
# ---------------------------------------------------------------------------
@pytest.mark.req("EXT-07")
@pytest.mark.track("UI")
def test_tc_ext_07_format_table_with_fixture_ratios():
    """TC-EXT-07: table 포맷 — fixture 비율 기준 박스 테이블 (Track A)"""
    from src.config_loader import load_unit_registry
    from src.formatter import format_table

    from pathlib import Path

    fixture_path = Path(__file__).resolve().parents[1] / "fixtures" / "units.json"
    registry = load_unit_registry(fixture_path)

    expected = "\n".join(
        [
            "┌────────┬─────────┬─────────┐",
            "│ unit   │ input   │ result  │",
            "├────────┼─────────┼─────────┤",
            "│ meter  │ 2.5     │ 2.5     │",
            "│ feet   │ 2.5     │ 7.5000  │",
            "│ yard   │ 2.5     │ 2.5000  │",
            "└────────┴─────────┴─────────┘",
        ]
    )

    assert format_table("meter", 2.5, registry) == expected


@pytest.mark.req("EXT-07")
@pytest.mark.track("UI")
def test_tc_ext_07_format_table_prd_builtin_ratios():
    """TC-EXT-07: table 포맷 — PRD §3.7 내장 비율 예시 (8.2021, 2.7340)"""
    from src.entity.constants import BASE_UNIT, FEET_PER_METER, YARD_PER_METER
    from src.entity.registry import UnitRegistry
    from src.formatter import format_table

    prd_registry = UnitRegistry(
        {
            BASE_UNIT: 1.0,
            "feet": FEET_PER_METER,
            "yard": YARD_PER_METER,
        }
    )
    expected = "\n".join(
        [
            "┌────────┬─────────┬─────────┐",
            "│ unit   │ input   │ result  │",
            "├────────┼─────────┼─────────┤",
            "│ meter  │ 2.5     │ 2.5     │",
            "│ feet   │ 2.5     │ 8.2021  │",
            "│ yard   │ 2.5     │ 2.7340  │",
            "└────────┴─────────┴─────────┘",
        ]
    )

    assert format_table("meter", 2.5, prd_registry) == expected


@pytest.mark.req("EXT-07")
@pytest.mark.track("UI")
def test_tc_ext_07_cli_run_format_table():
    """TC-EXT-07: cli.run(output_format='table') — stdout 박스 테이블"""
    from src.cli import run
    from src.formatter import format_table

    expected = format_table("meter", 2.5) + "\n"

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run("meter:2.5", output_format="table")

    assert buf.getvalue() == expected


@pytest.mark.req("EXT-07")
@pytest.mark.track("UI")
def test_tc_ext_07_main_argv_format_table():
    """TC-EXT-07: main(['meter:2.5', '--format', 'table']) — CLI 인자 연동"""
    from src.cli import main
    from src.formatter import format_table

    expected = format_table("meter", 2.5) + "\n"

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main(["meter:2.5", "--format", "table"])

    assert buf.getvalue() == expected
