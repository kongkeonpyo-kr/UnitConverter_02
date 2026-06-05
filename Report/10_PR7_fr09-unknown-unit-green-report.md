# 10 — PR7 Boundary FR-09 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 10 (PR7) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `a29eb8f` — FR-08 음수 거부 + TC-FR-08 GREEN (PR7 3차) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-09 (미지 단위 거부) |
| PR | PR7 — U-FR-09 / TC-FR-09 GREEN (4차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-09 GREEN** 작업의 `git status` 변경분을 기록한다.

- `src/validator.py` 미등록 단위 검증(`UnitRegistry.has_unit`) 확장 내역을 문서화한다.
- `tests/Boundary/test_cli.py` FR-09 TC 활성화를 기록한다.
- `README.md` ToDo 갱신(FR-09·9/12 GREEN) 범위를 정리한다.
- FR-10~12 RED 유지 및 PR7 후속 작업 진입점을 제공한다.

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
  Report/10_PR7_fr09-unknown-unit-green-report.md
  boundary/                                  (__pycache__ 잔존만)
  src/__pycache__/formatter.cpython-314.pyc  (커밋 제외 권장)
  src/__pycache__/validator.cpython-314.pyc  (커밋 제외 권장)
  src/entity/__pycache__/
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트·문서)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **수정** | `src/validator.py` | +8 | −2 |
| **수정** | `tests/Boundary/test_cli.py` | +4 | −5 |
| **수정** | `README.md` | (FR-09·9/12 반영) | — |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-09 GREEN — `validator.py` 1건 + Boundary TC 1건 + `README.md` ToDo 갱신. **첫 entity 의존** (`UnitRegistry`).

---

## 3. 변경 파일 상세

### 3.1 수정 — `src/validator.py` (FR-09)

FR-08 음수 검사 이후 **등록 단위 확인** 추가.

```python
from src.entity.registry import UnitRegistry

unit = unit_str.strip()
if not UnitRegistry.default().has_unit(unit):
    raise ValidationError(f"Unknown unit: {unit}")
```

| Given | Then |
|-------|------|
| `"cubit:1"` | `ValidationError`: `Unknown unit: cubit` |

**설계 메모**

- PRD §3.3 FR-09: 미등록 단위 거부, 메시지 `Unknown unit: {unit}`.
- `UnitRegistry.default()` — PR1·PR3 entity SSOT 재사용 (OCP 확장 지점).
- `unit_str.strip()` — unit 추출만 선행 (FR-11 trim은 parse 쪽, FR-10 빈 값은 후속).
- **의존 방향:** `validator` → `entity.registry` (boundary → entity, 단방향).
- FR-10~12(빈 값·trim·대소문자)는 **미구현**.

### 3.2 수정 — `tests/Boundary/test_cli.py` (U-FR-09 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-09 ...")` | `validate_input()` + `pytest.raises` |
| import | 주석 처리 | `ValidationError`, `validate_input` |
| match | `match=expected_msg` (주석) | `match=re.escape(expected_msg)` |

```python
with pytest.raises(ValidationError, match=re.escape("Unknown unit: cubit")):
    validate_input("cubit:1")
```

### 3.3 수정 — `README.md` (ToDo 갱신)

| 섹션 | 변경 요약 |
|------|-----------|
| 헤더 | PR7 (Validator FR-06~**09** GREEN) |
| 전체 GREEN | 8/12 → **9/12** |
| PR7 마일스톤 | `a29eb8f` — FR-06~**09**, FR-10~12 잔여 |
| Boundary FR-09 | GREEN ✅ |
| TC 결과·실행 예시 | **9 passed**, 4 failed / FR-09 TC 명령 추가 |
| `validator.py` | 🟡 (FR-06~**09**) |

---

## 4. 아키텍처 — PR7 FR-09 이후 Boundary 흐름

```
validate_input(input_str)
    │
    ├─ FR-06  ":" 없음           →  ValidationError (format)
    ├─ FR-07  float() 실패       →  ValidationError (invalid number)
    ├─ FR-08  value < 0          →  ValidationError (negative)
    ├─ FR-09  !has_unit(unit)    →  ValidationError (unknown unit)  ← 4차
    └─ (추후 FR-10~12)

src/validator.py  ──→  src/entity/registry.py  (UnitRegistry.has_unit)
```

| Layer | 모듈 | FR | PR7 진행 |
|-------|------|-----|----------|
| Boundary | `src/validator.py` | FR-06~09 | **✅** |
| Entity | `src/entity/registry.py` | SSOT, NFR-01 | ✅ (재사용) |
| Boundary | `src/validator.py` | FR-10~12 | ⬜ |

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-09 단건

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr09_unknown_unit -v
# 1 passed
```

### 5.2 Boundary — Validator (FR-06~09)

```bash
python -m pytest tests/Boundary/test_cli.py -k "fr06 or fr07 or fr08 or fr09" -v
# 4 passed (U-FR-06~09)
```

### 5.3 Boundary — `tests/Boundary/test_cli.py` 전체

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-01 | FR-01 | **PASS** |
| U-FR-06 ~ U-FR-09 | FR-06~09 | **PASS** |
| U-FR-10 | FR-10 | FAIL (RED) ×2 |
| U-FR-11 | FR-11 | FAIL (RED) |
| U-FR-12 | FR-12 | FAIL (RED) |

```bash
python -m pytest tests/Boundary/test_cli.py -v
# 5 passed, 4 failed
```

### 5.4 Domain — 회귀 없음

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 ~ D-FR-05 | FR-02~05 | **PASS** (4건) |

### 5.5 전체 합계

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **5** (FR-01, FR-06~09) | 4 (RED) |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **9** | **4** |

> Report 09 대비: **+1 PASS** (FR-09). FR-06~08 회귀 없음.

---

## 6. README ToDo 대비 진행 (FR-09 반영)

### P0 FR — Boundary (Track A)

| Req ID | GREEN (Report 09) | GREEN (Report 10) |
|--------|:-----------------:|:-----------------:|
| FR-06~08 | ✅ | ✅ |
| **FR-09** | ⬜ | **✅ PR7 4차** |
| FR-10~12 | ⬜ | ⬜ |

### P0 FR 전체

| 시점 | GREEN |
|------|:-----:|
| Report 09 (FR-08) | 8/12 |
| **Report 10 (FR-09)** | **9/12** |

---

## 7. PR7 진행 비교 (3차 vs 4차)

| 차수 | 커밋 | FR | `validator.py` 추가 |
|------|------|-----|----------------------|
| 3차 | `a29eb8f` | FR-08 음수 거부 | `value < 0` 검사 |
| **4차** | (미커밋) | **FR-09 미지 단위** | **`UnitRegistry.has_unit`** |

---

## 8. 커밋 권장 사항 (PR7 FR-09)

### 8.1 포함 권장

```
src/validator.py
tests/Boundary/test_cli.py
README.md
Report/10_PR7_fr09-unknown-unit-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-09 미지 단위 검증을 validator에 추가하고 Boundary TC-FR-09 GREEN 및 README ToDo를 갱신합니다.
```

### 8.4 PR7 (4차) 제안 제목

```
PR7: Boundary FR-09 GREEN (validator — unknown unit rejected)
```

---

## 9. 다음 단계 (PR7 후속)

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | 빈 unit/value 검증 | FR-10 |
| 2 | FR-11 TC 활성화 | FR-11 (`parse_input` strip) |
| 3 | 대소문자 거부 | FR-12 (`Meter` → Unknown unit) |
| 4 | `cli.py` → `validator` 연동 | FR-06~12 |
| 5 | README ToDo FR-10~12 GREEN 컬럼 갱신 | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 09 (PR7 3차) | [Report/09_PR7_fr08-negative-validation-green-report.md](./09_PR7_fr08-negative-validation-green-report.md) |
| Validator | [src/validator.py](../src/validator.py) |
| UnitRegistry | [src/entity/registry.py](../src/entity/registry.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
