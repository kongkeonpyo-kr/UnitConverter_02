# 09 — PR7 Boundary FR-08 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 09 (PR7) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `d787bee` — FR-07 숫자 검증 + TC-FR-07 GREEN (PR7 2차) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-08 (음수 거부) |
| PR | PR7 — U-FR-08 / TC-FR-08 GREEN (3차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-08 GREEN** 작업의 `git status` 변경분을 기록한다.

- `src/validator.py` 음수 거부(`value < 0`) 확장 내역을 문서화한다.
- `tests/Boundary/test_cli.py` FR-08 TC 활성화를 기록한다.
- `README.md` ToDo 갱신(FR-08·8/12 GREEN) 범위를 정리한다.
- FR-09~12 RED 유지 및 PR7 후속 작업 진입점을 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   README.md
  modified:   src/__pycache__/__init__.cpython-314.pyc   (커밋 제외 권장)
  modified:   src/__pycache__/converter.cpython-314.pyc  (커밋 제외 권장)
  modified:   src/__pycache__/registry.cpython-314.pyc   (커밋 제외 권장)
  modified:   src/validator.py
  modified:   tests/Boundary/test_cli.py

Untracked files:
  Report/09_PR7_fr08-negative-validation-green-report.md
  boundary/                                  (__pycache__ 잔존만)
  src/__pycache__/formatter.cpython-314.pyc  (커밋 제외 권장)
  src/__pycache__/validator.cpython-314.pyc  (커밋 제외 권장)
  src/entity/__pycache__/
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트·문서)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **수정** | `src/validator.py` | +5 | −2 |
| **수정** | `tests/Boundary/test_cli.py` | +4 | −8 |
| **수정** | `README.md` | (FR-08·8/12 반영) | — |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-08 GREEN — `validator.py` 1건 + Boundary TC 1건 + `README.md` ToDo 갱신.

---

## 3. 변경 파일 상세

### 3.1 수정 — `src/validator.py` (FR-08)

FR-07 `float()` 변환 성공 후 **음수 검사** 추가.

```python
value = float(value_str.strip())
# ...
if value < 0:
    raise ValidationError(f"Negative values are not allowed: {value}")
```

| Given | Then |
|-------|------|
| `"meter:-1"` | `ValidationError`: `Negative values are not allowed: -1.0` |

**설계 메모**

- PRD §3.3 FR-08: `value < 0` 거부, 메시지 `Negative values are not allowed: {value}`.
- TC는 `match=re.escape("Negative values are not allowed")` — 메시지 **부분 일치**로 검증.
- `value == 0` 은 허용 (`< 0` 조건만 거부).
- FR-09~12(미지 단위·빈 값·trim·대소문자)는 **미구현**.

### 3.2 수정 — `tests/Boundary/test_cli.py` (U-FR-08 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-08 ...")` | `validate_input()` + `pytest.raises` |
| import | 주석 처리 | `ValidationError`, `validate_input` |
| match | `match=expected_fragment` (주석) | `match=re.escape(expected_fragment)` |

```python
with pytest.raises(ValidationError, match=re.escape("Negative values are not allowed")):
    validate_input("meter:-1")
```

### 3.3 수정 — `README.md` (ToDo 갱신)

| 섹션 | 변경 요약 |
|------|-----------|
| 헤더 | PR7 (Validator FR-06~**08** GREEN) |
| 전체 GREEN | 7/12 → **8/12** |
| PR7 마일스톤 | `d787bee` — FR-06~**08**, FR-09~12 잔여 |
| Boundary FR-08 | GREEN ✅ |
| TC 결과·실행 예시 | **8 passed**, 5 failed / FR-08 TC 명령 추가 |
| `validator.py` | 🟡 (FR-06~**08**) |

---

## 4. 아키텍처 — PR7 FR-08 이후 Boundary 흐름

```
validate_input(input_str)
    │
    ├─ FR-06  ":" 없음           →  ValidationError (format)
    ├─ FR-07  float() 실패       →  ValidationError (invalid number)
    ├─ FR-08  value < 0          →  ValidationError (negative)     ← 3차
    └─ (추후 FR-09~12)
```

| Layer | 모듈 | FR | PR7 진행 |
|-------|------|-----|----------|
| Boundary | `src/validator.py` | FR-06~08 | **✅** |
| Boundary | `src/validator.py` | FR-09~12 | ⬜ |

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-08 단건

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr08_negative_value_rejected -v
# 1 passed
```

### 5.2 Boundary — Validator (FR-06~08)

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr06_invalid_format_missing_colon \
                 tests/Boundary/test_cli.py::test_u_fr07_invalid_number \
                 tests/Boundary/test_cli.py::test_u_fr08_negative_value_rejected -v
# 3 passed
```

### 5.3 Boundary — `tests/Boundary/test_cli.py` 전체

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-01 | FR-01 | **PASS** |
| U-FR-06 | FR-06 | **PASS** |
| U-FR-07 | FR-07 | **PASS** |
| U-FR-08 | FR-08 | **PASS** ← PR7 3차 |
| U-FR-09 ~ U-FR-12 | FR-09~12 | FAIL (RED) |

```bash
python -m pytest tests/Boundary/test_cli.py -v
# 4 passed, 5 failed
```

### 5.4 Domain — 회귀 없음

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 ~ D-FR-05 | FR-02~05 | **PASS** (4건) |

### 5.5 전체 합계

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **4** (FR-01, FR-06~08) | 5 (RED) |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **8** | **5** |

> Report 08 대비: **+1 PASS** (FR-08). FR-06·07 회귀 없음.

---

## 6. README ToDo 대비 진행 (FR-08 반영)

### P0 FR — Boundary (Track A)

| Req ID | GREEN (Report 08) | GREEN (Report 09) |
|--------|:-----------------:|:-----------------:|
| FR-06~07 | ✅ | ✅ |
| **FR-08** | ⬜ | **✅ PR7 3차** |
| FR-09~12 | ⬜ | ⬜ |

### P0 FR 전체

| 시점 | GREEN |
|------|:-----:|
| Report 08 (FR-07) | 7/12 |
| **Report 09 (FR-08)** | **8/12** |

---

## 7. PR7 진행 비교 (2차 vs 3차)

| 차수 | 커밋 | FR | `validator.py` 추가 |
|------|------|-----|----------------------|
| 2차 | `d787bee` | FR-07 숫자 검증 | `float()` 검사 |
| **3차** | (미커밋) | **FR-08 음수 거부** | **`value < 0` 검사** |

---

## 8. 커밋 권장 사항 (PR7 FR-08)

### 8.1 포함 권장

```
src/validator.py
tests/Boundary/test_cli.py
README.md
Report/09_PR7_fr08-negative-validation-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-08 음수 거부를 validator에 추가하고 Boundary TC-FR-08 GREEN 및 README ToDo를 갱신합니다.
```

### 8.4 PR7 (3차) 제안 제목

```
PR7: Boundary FR-08 GREEN (validator — negative value rejected)
```

---

## 9. 다음 단계 (PR7 후속)

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | 미지 단위 + `UnitRegistry.has_unit` | FR-09, FR-12 |
| 2 | 빈 unit/value | FR-10 |
| 3 | FR-11 TC 활성화 | FR-11 (`parse_input` strip) |
| 4 | `cli.py` → `validator` 연동 | FR-06~12 |
| 5 | README ToDo FR-09~12 GREEN 컬럼 갱신 | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 08 (PR7 2차) | [Report/08_PR7_fr07-number-validation-green-report.md](./08_PR7_fr07-number-validation-green-report.md) |
| Validator | [src/validator.py](../src/validator.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
