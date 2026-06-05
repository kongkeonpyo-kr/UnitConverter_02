"""
tests/test_converter.py — Track B (Domain) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- Track  : B (Domain)
- §3.2   : FR-02 전 단위 변환 출력
- §8.2   : TC-FR-02 전 단위 출력
- Test File : tests/test_converter.py
"""

import pytest

# ---------------------------------------------------------------------------
# Req ID  : FR-02
# Track   : B (Domain)
# Test ID : TC-FR-02
# P       : P0
# Given   : meter 2.5, 기본 Registry
# Then    : feet·yard 변환 결과 반환, meter 제외
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-02")
def test_tc_fr_02_convert_all_units_excluding_source():
    """TC-FR-02: 전 단위 출력 — FR-02 (Track B)"""
    from src.converter import Converter
    from src.registry import UnitRegistry

    # Given
    registry = UnitRegistry.default()
    converter = Converter(registry)
    source_unit = "meter"
    value = 2.5

    # When
    results = converter.convert(source_unit, value)

    # Then — 소스 단위(meter) 제외, feet·yard 포함
    target_units = {r.unit for r in results}
    assert "meter" not in target_units
    assert "feet" in target_units
    assert "yard" in target_units

    feet = next(r for r in results if r.unit == "feet")
    yard = next(r for r in results if r.unit == "yard")
    assert abs(feet.value - (2.5 * 3.28084)) < 1e-4
    assert abs(yard.value - (2.5 * 1.09361)) < 1e-4
