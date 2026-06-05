"""
tests/test_converter.py — Track B (Domain) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- Track  : B (Domain)
- §3.2   : FR-02~FR-05 (Domain 변환·반올림·파생·단위 표기)
- §8.2   : TC-FR-02, TC-FR-03, TC-FR-04, TC-FR-05
- Dual-Track : Logic (PRD Track B — Domain)
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


# ---------------------------------------------------------------------------
# Req ID  : FR-03
# Track   : Logic (PRD Track B — Domain)
# Test ID : D-FR-03 / TC-FR-03
# Layer   : entity / control
# P       : P0
# Given   : meter 2.5
# Then    : "8.2 feet", "2.7 yard" (round half up, 소수 1자리)
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-03")
@pytest.mark.track("Logic")
def test_d_fr03_round_half_up_one_decimal():
    """D-FR-03 / TC-FR-03: 소수 1자리 반올림 — FR-03 (Logic Track)"""
    # Arrange
    source_unit = "meter"
    value = 2.5
    expected_lines = ["8.2 feet", "2.7 yard"]

    # Act (GREEN: Formatter 또는 control 유스케이스 연결)
    # from control.format_usecase import format_conversions
    # lines = format_conversions(source_unit, value)

    # Assert (GREEN 시 활성화)
    # assert any("8.2 feet" in line for line in lines)
    # assert any("2.7 yard" in line for line in lines)

    pytest.fail(
        f"RED: FR-03 GREEN 미구현 — Then {expected_lines!r} (round half up)"
    )


# ---------------------------------------------------------------------------
# Req ID  : FR-04
# Track   : Logic (PRD Track B — Domain)
# Test ID : D-FR-04 / TC-FR-04
# Layer   : entity / control
# P       : P0
# Given   : feet 3.28084
# Then    : yard ≈ 1.0 (meter 경유 파생 변환)
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-04")
@pytest.mark.track("Logic")
def test_d_fr04_derived_conversion_via_meter():
    """D-FR-04 / TC-FR-04: meter 기준 파생 변환 — FR-04 (Logic Track)"""
    # Arrange
    source_unit = "feet"
    value = 3.28084
    expected_yard = 1.0
    tolerance = 1e-4

    # Act (GREEN: Converter + Registry — meter hub 경유)
    # from src.converter import Converter
    # from src.registry import UnitRegistry
    # registry = UnitRegistry.default()
    # converter = Converter(registry)
    # results = converter.convert(source_unit, value)

    # Assert (GREEN 시 활성화)
    # yard = next(r for r in results if r.unit == "yard")
    # assert abs(yard.value - expected_yard) < tolerance

    pytest.fail(
        f"RED: FR-04 GREEN 미구현 — feet:{value} → yard≈{expected_yard} (meter 경유)"
    )


# ---------------------------------------------------------------------------
# Req ID  : FR-05
# Track   : Logic (PRD Track B — Domain)
# Test ID : D-FR-05 / TC-FR-05
# Layer   : entity / control
# P       : P0
# Given   : meter 1
# Then    : 출력 단위명 feet, yard (복수형 아님)
# ---------------------------------------------------------------------------
@pytest.mark.req("FR-05")
@pytest.mark.track("Logic")
def test_d_fr05_unit_names_singular():
    """D-FR-05 / TC-FR-05: 단위 표기 (단수) — FR-05 (Logic Track)"""
    # Arrange
    source_unit = "meter"
    value = 1.0
    allowed_units = {"feet", "yard"}
    forbidden_units = {"feets", "yards", "meters"}

    # Act (GREEN: Formatter 또는 Converter 결과의 unit 필드)
    # from src.converter import Converter
    # from src.registry import UnitRegistry
    # registry = UnitRegistry.default()
    # converter = Converter(registry)
    # results = converter.convert(source_unit, value)

    # Assert (GREEN 시 활성화)
    # output_units = {r.unit for r in results}
    # assert output_units <= allowed_units
    # assert forbidden_units.isdisjoint(output_units)

    pytest.fail(
        f"RED: FR-05 GREEN 미구현 — Then 단수형 {allowed_units!r}, "
        f"복수형 금지 {forbidden_units!r}"
    )
