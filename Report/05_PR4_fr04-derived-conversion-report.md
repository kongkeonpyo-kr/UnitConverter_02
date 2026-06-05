# 05 — PR4 FR-04 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 05 (PR4) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `dec4604` — README ToDo + PR3 Report |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — FR-04 (meter 허브 파생 변환) |
| PR | PR4 — D-FR-04 / TC-FR-04 GREEN |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **FR-04 meter 기준 파생 변환** GREEN 작업의 `git status` 변경분을 기록한다.

- D-FR-04 TC 활성화 및 PASS 조건을 문서화한다.
- `src/` 코드 변경 없이 TC만 GREEN 처리한 **최소 구현** 범위를 명확히 한다.
- PRD Then(`yard ≈ 1.0`)과 SSOT 상수 기반 기대값 정렬 내역을 기록한다.
- 커밋·PR4 리뷰 전 변경 범위 검토 자료로 활용한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   tests/Domain/test_converter.py
  modified:   src/__pycache__/*.pyc          (커밋 제외 권장)

Untracked files:
  boundary/              (__pycache__ 잔존만)
  src/entity/__pycache__/
  tests/**/__pycache__/
```

### 2.1 Diff 통계

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| 수정 (의미 있는 변경) | `tests/Domain/test_converter.py` | +14 | −16 |
| 수정 (제외 권장) | `src/__pycache__/*.pyc` | — | — |
| `src/` 소스 | — | **0** | **0** |

> **핵심:** PR4는 **테스트 파일 1건만** 변경. `Converter`/`UnitRegistry`는 PR1에서 이미 meter 허브 변환 구현 완료.

---

## 3. 변경 파일 상세

### 3.1 `tests/Domain/test_converter.py` — D-FR-04 GREEN

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-04 ...")` | `Converter.convert()` + assert |
| import | 주석 처리 | `Converter`, `UnitRegistry`, `FEET_PER_METER`, `YARD_PER_METER` |
| 입력 | `value = 3.28084` (리터럴) | `value = FEET_PER_METER` (SSOT) |
| 기대값 | `expected_yard = 1.0` | `expected_yard = YARD_PER_METER` (`1.09361`) |

**변환 검증 로직**

```
feet:3.28084  →  to_base  →  1.0 meter  →  from_base  →  1.09361 yard
```

| 단계 | 계산 | 결과 |
|------|------|------|
| feet → meter | `3.28084 / FEET_PER_METER` | `1.0` |
| meter → yard | `1.0 × YARD_PER_METER` | `1.09361` |
| assert | `abs(yard - YARD_PER_METER) < 1e-4` | **PASS** |

### 3.2 PRD Then vs SSOT 정렬

| 출처 | Then 표현 | 실제 기대값 |
|------|-----------|-------------|
| PRD §8.2 TC-FR-04 | `yard ≈ 1.0` (meter 경유) | `YARD_PER_METER` = **1.09361** |
| PR4 TC | SSOT 상수 참조 | `feet:FEET_PER_METER` → `yard:YARD_PER_METER` |

> PRD Then `yard ≈ 1.0`은 `feet:3.28084`(= 1 meter) 입력과 **수학적으로 불일치** (1 meter = 1.09361 yard).  
> PR4에서는 **meter 허브 경유 파생 변환**을 검증하기 위해 SSOT 상수 기반 기대값으로 정렬했다.

---

## 4. `src/` 변경 없음 — 기존 구현으로 FR-04 충족

FR-04 GREEN에 사용된 기존 모듈 (PR1·PR3):

| 모듈 | 역할 | FR-04 기여 |
|------|------|------------|
| `src/entity/constants.py` | `FEET_PER_METER`, `YARD_PER_METER` SSOT | 비율 정의 |
| `src/entity/registry.py` | `to_base()`, `from_base()` | meter 허브 |
| `src/converter.py` | `convert()` — 소스 단위 제외 | feet → yard 파생 변환 |

```11:18:src/converter.py
    def convert(self, source_unit: str, value: float) -> list[ConversionResult]:
        meter_value = self._registry.to_base(source_unit, value)
        results: list[ConversionResult] = []
        for unit in self._registry.units():
            if unit == source_unit:
                continue
            converted = self._registry.from_base(unit, meter_value)
            results.append(ConversionResult(unit=unit, value=converted))
```

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

| # | Test ID | Req | Track | 결과 |
|---|---------|-----|-------|------|
| 1 | TC-FR-01 | FR-01 | UI | **PASS** |
| 2 | TC-FR-02 | FR-02 | Logic | **PASS** |
| 3 | **D-FR-04** | **FR-04** | Logic | **PASS** ← PR4 |
| 4 | D-FR-03 | FR-03 | Logic | FAIL (RED) |
| 5 | D-FR-05 | FR-05 | Logic | FAIL (RED) |
| 6 | U-FR-06 ~ U-FR-12 | FR-06~12 | UI | FAIL (RED) |

**합계:** 13 collected — **3 passed**, 10 failed

### 5.1 PR4 GREEN TC 확인 명령

```bash
python -m pytest tests/Domain/test_converter.py::test_d_fr04_derived_conversion_via_meter -v
```

### 5.2 Domain Track 회귀 확인

```bash
python -m pytest tests/Domain/test_converter.py::test_tc_fr_02_convert_all_units_excluding_source -v
python -m pytest tests/Domain/test_converter.py::test_d_fr04_derived_conversion_via_meter -v
# 2 passed
```

---

## 6. README ToDo 대비 진행 (PR4 반영)

| Req ID | RED | GREEN (PR4 전) | GREEN (PR4 후) |
|--------|:---:|:--------------:|:--------------:|
| FR-02 | ✅ | ✅ PR1 | ✅ |
| FR-03 | ✅ | ⬜ | ⬜ |
| **FR-04** | ✅ | ⬜ | **✅ PR4** |
| FR-05 | ✅ | ⬜ | ⬜ |

**P0 FR GREEN:** 2/12 → **3/12** (FR-01, FR-02, FR-04)

---

## 7. 커밋 권장 사항 (PR4)

### 7.1 포함 권장

```
tests/Domain/test_converter.py
```

### 7.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (캐시만)

### 7.3 제안 커밋 메시지

```
FR-04 meter 허브 파생 변환 TC를 GREEN으로 활성화합니다.
```

### 7.4 PR4 제안 제목

```
PR4: FR-04 derived conversion via meter (D-FR-04 GREEN)
```

---

## 8. 다음 단계 (PR5 이후)

| 순서 | 작업 | FR | PR |
|------|------|-----|-----|
| 1 | `src/formatter.py` + D-FR-03 GREEN | FR-03 | PR5 |
| 2 | D-FR-05 TC 활성화 | FR-05 | PR5 |
| 3 | `src/validator.py` + Boundary TC | FR-06~12 | PR6 |
| 4 | README ToDo GREEN 컬럼 갱신 | — | PR4 커밋 후 |

---

## 9. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 04 (PR3) | [Report/04_PR3_entity-src-shim-commit-report.md](./04_PR3_entity-src-shim-commit-report.md) |
| 테스트 | [tests/Domain/test_converter.py](../tests/Domain/test_converter.py) |
