# 07 — PR6 Boundary FR-06 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 07 (PR6) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `1b83ce0` — FR-03 Formatter + Domain FR-03~05 GREEN (PR5) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-06 (형식 검증) |
| PR | PR6 — U-FR-06 / TC-FR-06 GREEN (1차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-06 GREEN** 작업의 `git status` 변경분을 기록한다.

- `src/validator.py` 신규 추가 (`:` 구분자 필수 검증) 내역을 문서화한다.
- `tests/Boundary/test_cli.py` FR-06 TC 활성화 및 `re.escape` 보정을 기록한다.
- FR-07~12는 RED 유지 범위를 명확히 하고, PR6 후속 작업 진입점을 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   src/__pycache__/__init__.cpython-314.pyc   (커밋 제외 권장)
  modified:   src/__pycache__/converter.cpython-314.pyc  (커밋 제외 권장)
  modified:   src/__pycache__/registry.cpython-314.pyc   (커밋 제외 권장)
  modified:   tests/Boundary/test_cli.py

Untracked files:
  src/validator.py                           (신규 — FR-06)
  src/__pycache__/validator.cpython-314.pyc  (커밋 제외 권장)
  src/__pycache__/formatter.cpython-314.pyc  (커밋 제외 권장)
  src/entity/__pycache__/
  boundary/                                  (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트만)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **신규** | `src/validator.py` | +14 | — |
| **수정** | `tests/Boundary/test_cli.py` | +5 | −4 |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-06 GREEN에 필요한 **소스 1건 + 테스트 1건**만 변경. `cli.py`·`parser.py`는 미수정.

---

## 3. 변경 파일 상세

### 3.1 신규 — `src/validator.py` (FR-06)

| 심볼 | 역할 | FR |
|------|------|-----|
| `ValidationError` | 입력 검증 실패 예외 (`ValueError` 상속) | FR-06~12 공통 |
| `validate_input(input_str)` | `:` 없으면 형식 오류 raise | **FR-06** |

```python
_FORMAT_ERROR = "Invalid format. Use unit:value (ex: meter:2.5)"

def validate_input(input_str: str) -> None:
    if ":" not in input_str:
        raise ValidationError(_FORMAT_ERROR)
```

| Given | Then |
|-------|------|
| `"meter"` (콜론 없음) | `ValidationError`: `Invalid format. Use unit:value (ex: meter:2.5)` |

**설계 메모**

- PRD §3.3 FR-06 메시지와 `src/cli.py`의 `_FORMAT_ERROR` 상수와 **동일 문구** 유지.
- FR-06 범위만 구현 — 숫자·음수·미지 단위·빈 값·trim·대소문자는 FR-07~12 후속.

### 3.2 수정 — `tests/Boundary/test_cli.py` (U-FR-06 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-06 GREEN 미구현 ...")` | `validate_input()` + `pytest.raises` |
| import | 주석 처리 | `ValidationError`, `validate_input` from `src.validator` |
| match | `match=expected_msg` (주석) | `match=re.escape(expected_msg)` |

**`re.escape` 보정 이유**

- `pytest.raises(..., match=...)`는 **정규식** 매칭.
- PRD 오류 메시지 `(ex: meter:2.5)`의 괄호가 regex 그룹으로 해석되어, 메시지가 일치해도 **AssertionError** 발생.
- `re.escape(expected_msg)`로 리터럴 매칭 보장.

```python
import re

with pytest.raises(ValidationError, match=re.escape(expected_msg)):
    validate_input("meter")
```

---

## 4. 아키텍처 — PR6 FR-06 이후 Boundary 흐름

```
tests/Boundary/test_cli.py
       │
       ├── FR-01  →  src/parser.py          parse_input()
       └── FR-06  →  src/validator.py       validate_input()   ← PR6 (1차)
                              │
                    (추후 FR-07~12 확장)
                              │
                    src/cli.py  run()        ":" 검사 (print, return)
```

| Layer | 모듈 | FR | PR |
|-------|------|-----|-----|
| Boundary | `src/parser.py` | FR-01, FR-11(strip) | PR1 |
| Boundary | **`src/validator.py`** | **FR-06** (1차) | **PR6** |
| Boundary | `src/cli.py` | I/O, 레거시 `:` 검사 | PR1 |
| Domain | `src/converter.py`, `src/formatter.py` | FR-02~05 | PR1·PR5 |

**의존 방향:** `validator` → `entity` import 없음 (FR-06은 문자열만 검사).

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-06 단건

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr06_invalid_format_missing_colon -v
# 1 passed
```

### 5.2 Boundary — `tests/Boundary/test_cli.py` 전체

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-01 | FR-01 | **PASS** |
| U-FR-06 | FR-06 | **PASS** ← PR6 |
| U-FR-07 | FR-07 | FAIL (RED) |
| U-FR-08 | FR-08 | FAIL (RED) |
| U-FR-09 | FR-09 | FAIL (RED) |
| U-FR-10 | FR-10 | FAIL (RED) ×2 |
| U-FR-11 | FR-11 | FAIL (RED) |
| U-FR-12 | FR-12 | FAIL (RED) |

```bash
python -m pytest tests/Boundary/test_cli.py -v
# 2 passed, 7 failed
```

### 5.3 Domain — 회귀 없음

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 ~ D-FR-05 | FR-02~05 | **PASS** (4건) |

### 5.4 전체 합계

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **2** (FR-01, FR-06) | 7 (RED) |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **6** | **7** |

> PR5 대비: **+1 PASS** (FR-06). Domain 4건 회귀 없음.

---

## 6. README ToDo 대비 진행 (PR6 FR-06 반영)

### P0 FR — Boundary (Track A)

| Req ID | RED | GREEN (PR5 후) | GREEN (PR6 FR-06 후) |
|--------|:---:|:--------------:|:--------------------:|
| FR-01 | ✅ | ✅ PR1 | ✅ |
| FR-06 | ✅ | ⬜ | **✅ PR6** |
| FR-07~12 | ✅ | ⬜ | ⬜ |

### P0 FR — Domain (Track B) — 미변경

| Req ID | GREEN |
|--------|:-----:|
| FR-02~05 | ✅ PR1·PR5 |

**P0 FR 전체 GREEN:** **6/12** (FR-01, FR-02~06)

---

## 7. PR6 vs PR5 비교

| PR | 범위 | src 신규 | Boundary GREEN |
|----|------|----------|----------------|
| PR5 | FR-03~05 Domain | `formatter.py` | FR-01만 |
| **PR6 (1차)** | **FR-06 형식 검증** | **`validator.py`** | **FR-01, FR-06** |

---

## 8. 커밋 권장 사항 (PR6 FR-06)

### 8.1 포함 권장

```
src/validator.py
tests/Boundary/test_cli.py
Report/07_PR6_fr06-format-validation-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-06 형식 검증(validator) 추가 및 Boundary TC-FR-06 GREEN을 완료합니다.
```

### 8.4 PR6 (1차) 제안 제목

```
PR6: Boundary FR-06 GREEN (validator — colon required)
```

---

## 9. 다음 단계 (PR6 후속)

| 순서 | 작업 | FR | 비고 |
|------|------|-----|------|
| 1 | `validate_input` 숫자 검증 | FR-07 | `Invalid number: abc` |
| 2 | 음수 거부 | FR-08 | `Negative values are not allowed` |
| 3 | 미지 단위 + `UnitRegistry.has_unit` | FR-09, FR-12 | case-sensitive |
| 4 | 빈 unit/value | FR-10 | `Unit and value must not be empty` |
| 5 | FR-11 TC 활성화 | FR-11 | `parse_input` strip 이미 구현 |
| 6 | `cli.py` → `validator` 연동 | FR-06~12 | `print`/`return` → raise 처리 |
| 7 | FR-07~12 TC `re.escape` 일괄 적용 | — | FR-06과 동일 패턴 |
| 8 | README ToDo GREEN 컬럼 갱신 | — | FR-06 ✅ |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 06 (PR5) | [Report/06_PR5_domain-fr03-fr05-green-report.md](./06_PR5_domain-fr03-fr05-green-report.md) |
| Validator | [src/validator.py](../src/validator.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
| CLI (레거시 `:` 검사) | [src/cli.py](../src/cli.py) |
