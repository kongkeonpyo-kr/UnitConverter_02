"""
tests/test_cli.py — Track A (Boundary) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- Track  : A (Boundary)
- §3.3   : FR-01 입력 파싱
- §8.2   : TC-FR-01 meter:2.5 파싱
- Test File : tests/test_cli.py
"""

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
def test_tc_fr_01_parse_meter_2_5():
    """TC-FR-01: meter:2.5 파싱 — FR-01 입력 파싱 (Track A)"""
    from src.parser import parse_input

    # Given
    input_str = "meter:2.5"

    # When
    result = parse_input(input_str)

    # Then
    assert result.unit == "meter"
    assert result.value == 2.5
