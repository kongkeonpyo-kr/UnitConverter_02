# 11 — PR7 Boundary FR-10 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 11 (PR7) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `6611cb1` — FR-09 미지 단위 + TC-FR-09 GREEN (PR7 4차) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-10 (빈 unit/value) |
| PR | PR7 — U-FR-10 / TC-FR-10 GREEN (5차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-10 GREEN** 작업의 `git status` 변경분을 기록한다.

- `src/validator.py` 빈 unit/value 검증 확장 내역을 문서화한다.
- `tests/Boundary/test_cli.py` FR-10 TC 활성화(parametrize 2건)를 기록한다.
- `README.md` ToDo 갱신(FR-10·10/12 GREEN) 범위를 정리한다.
- FR-11~12 RED 유지 및 PR7 후속 작업 진입점을 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   README.md
  modified:   src/__pycache__/*.pyc              (커밋 제외 권장)
  modified:   src/validator.py
  modified:   tests/Boundary/test_cli.py

Untracked files:
  Report/11_PR7_fr10-empty-unit-value-green-report.md
  boundary/                                  (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트·문서)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **수정** | `src/validator.py` | +6 | −2 |
| **수정** | `tests/Boundary/test_cli.py` | +4 | −8 |
| **수정** | `README.md` | (FR-10·10/12 반영) | — |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-10 GREEN — `validator.py` 1건 + Boundary TC 1건(parametrize ×2) + `README.md` ToDo 갱신.

---

## 3. 변경 파일 상세

### 3.1 수정 — `src/validator.py` (FR-10)

`split` 직후 **`float()` 이전**에 빈 unit/value 검사 추가.

```python
_EMPTY_ERROR = "Invalid format. Unit and value must not be empty"

unit = unit_str.strip()
if not unit or not value_str.strip():
    raise ValidationError(_EMPTY_ERROR)
```

| Given | Then |
|-------|------|
| `":2.5"` | `ValidationError`: `Invalid format. Unit and value must not be empty` |
| `"meter:"` | 동일 (빈 value) |

**설계 메모**

- PRD §3.3 FR-10 메시지와 일치.
- `float()` **전** 검사 — `"meter:"`가 FR-07(`Invalid number:`)로 오분류되지 않도록 함.
- 검증 순서: FR-06(`:`) → FR-10(빈 값) → FR-07(숫자) → FR-08(음수) → FR-09(단위).
- FR-11(trim)·FR-12(대소문자)는 **미구현**.

### 3.2 수정 — `tests/Boundary/test_cli.py` (U-FR-10 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-10 ...")` ×2 | `validate_input()` + `pytest.raises` |
| parametrize | `":2.5"`, `"meter:"` | 동일 |
| match | 주석 | `re.escape("Unit and value must not be empty")` |

### 3.3 수정 — `README.md` (ToDo 갱신)

| 섹션 | 변경 요약 |
|------|-----------|
| 헤더 | PR7 (Validator FR-06~**10** GREEN) |
| 전체 GREEN | 9/12 → **10/12** |
| PR7 마일스톤 | `6611cb1` — FR-06~**10**, FR-11~12 잔여 |
| Boundary FR-10 | GREEN ✅ |
| TC 결과·실행 예시 | **11 passed**, 2 failed / FR-10 TC 명령 추가 |
| `validator.py` | 🟡 (FR-06~**10**) |

---

## 4. 아키텍처 — PR7 FR-10 이후 검증 순서

```
validate_input(input_str)
    ├─ FR-06   ":" 없음
    ├─ FR-10   unit 또는 value 빈 문자열     ← 5차 (float 이전)
    ├─ FR-07   float() 실패
    ├─ FR-08   value < 0
    └─ FR-09   !has_unit(unit)
```

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-10 (parametrize)

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr10_empty_unit_or_value -v
# 2 passed (:2.5, meter:)
```

### 5.2 Boundary — `tests/Boundary/test_cli.py` 전체

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-01 | FR-01 | **PASS** |
| U-FR-06 ~ U-FR-10 | FR-06~10 | **PASS** |
| U-FR-11 | FR-11 | FAIL (RED) |
| U-FR-12 | FR-12 | FAIL (RED) |

```bash
python -m pytest tests/Boundary/test_cli.py -v
# 7 passed, 2 failed
```

### 5.3 Domain — 회귀 없음

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 ~ D-FR-05 | FR-02~05 | **PASS** (4건) |

### 5.4 전체 합계

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **7** (FR-01, FR-06~10) | 2 (RED) |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **11** | **2** |

> Report 10 대비: **+2 PASS** (FR-10 parametrize). FR-06~09 회귀 없음.

---

## 6. README ToDo 대비 진행 (FR-10 반영)

### P0 FR — Boundary (Track A)

| Req ID | GREEN (Report 10) | GREEN (Report 11) |
|--------|:-----------------:|:-----------------:|
| FR-06~09 | ✅ | ✅ |
| **FR-10** | ⬜ | **✅ PR7 5차** |
| FR-11~12 | ⬜ | ⬜ |

### P0 FR 전체

| 시점 | GREEN |
|------|:-----:|
| Report 10 (FR-09) | 9/12 |
| **Report 11 (FR-10)** | **10/12** |

---

## 7. PR7 진행 비교 (4차 vs 5차)

| 차수 | 커밋 | FR | `validator.py` 추가 |
|------|------|-----|----------------------|
| 4차 | `6611cb1` | FR-09 미지 단위 | `UnitRegistry.has_unit` |
| **5차** | (미커밋) | **FR-10 빈 unit/value** | **`_EMPTY_ERROR` 검사 (float 이전)** |

---

## 8. 커밋 권장 사항 (PR7 FR-10)

### 8.1 포함 권장

```
src/validator.py
tests/Boundary/test_cli.py
README.md
Report/11_PR7_fr10-empty-unit-value-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-10 빈 unit/value 검증을 validator에 추가하고 Boundary TC-FR-10 GREEN 및 README ToDo를 갱신합니다.
```

### 8.4 PR7 (5차) 제안 제목

```
PR7: Boundary FR-10 GREEN (validator — empty unit or value)
```

---

## 9. 다음 단계 (PR7 후속)

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | FR-11 TC 활성화 | FR-11 (`parse_input` strip 이미 구현) |
| 2 | 대소문자 거부 | FR-12 (`Meter` → Unknown unit) |
| 3 | `cli.py` → `validator` 연동 | FR-06~12 |
| 4 | README ToDo FR-11~12 GREEN 컬럼 갱신 | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 10 (PR7 4차) | [Report/10_PR7_fr09-unknown-unit-green-report.md](./10_PR7_fr09-unknown-unit-green-report.md) |
| Validator | [src/validator.py](../src/validator.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
