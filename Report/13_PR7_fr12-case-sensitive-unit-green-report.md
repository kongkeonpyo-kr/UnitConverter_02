# 13 — PR7 Boundary FR-12 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 13 (PR7) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `359e161` — FR-11 trim TC-FR-11 GREEN (PR7 6차) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-12 (대소문자 거부) |
| PR | PR7 — U-FR-12 / TC-FR-12 GREEN (7차·**PR7 완료**) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-12 GREEN** 작업의 `git status` 변경분을 기록한다.

- FR-12 TC 활성화(기존 FR-09 `has_unit` case-sensitive 활용) 범위를 문서화한다.
- **`src/` 로직 변경 없음** — docstring 1줄 + TC 활성화만으로 GREEN 처리한 최소 범위를 명확히 한다.
- `README.md` ToDo 갱신(**P0 FR 12/12 GREEN**)을 정리한다.
- PR7 Boundary Validator **전체 완료** 스냅샷 및 PR8(NFR) 진입점을 제공한다.

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
  Report/13_PR7_fr12-case-sensitive-unit-green-report.md
  boundary/                                  (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트·문서)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **수정** | `tests/Boundary/test_cli.py` | +4 | −5 |
| **수정** | `src/validator.py` | +1 | −1 (docstring) |
| **수정** | `README.md` | (12/12·PR7 ✅ 반영) | — |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-12는 **TC 활성화 + docstring**만. `UnitRegistry.has_unit("Meter")` → False는 FR-09에서 이미 동작.

---

## 3. 변경 파일 상세

### 3.1 변경 없음(로직) — FR-09 + FR-12 case-sensitive

FR-09 구현이 FR-12를 **포함**:

```python
unit = unit_str.strip()
if not UnitRegistry.default().has_unit(unit):
    raise ValidationError(f"Unknown unit: {unit}")
```

| Given | Then |
|-------|------|
| `"Meter:2.5"` | `ValidationError`: `Unknown unit: Meter` |

**설계 메모**

- `UnitRegistry` 키는 `"meter"`, `"feet"`, `"yard"` — **대소문자 구분**.
- `"Meter"` ≠ `"meter"` → FR-12 Then 충족.
- FR-09(`cubit`)와 FR-12(`Meter`) 동일 코드 경로.

### 3.2 수정 — `src/validator.py` (docstring)

```python
"""unit:value 형식·숫자·음수·단위 검증 (FR-06~12)."""
```

### 3.3 수정 — `tests/Boundary/test_cli.py` (U-FR-12 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-12 ...")` | `validate_input()` + `pytest.raises` |
| match | 주석 | `re.escape("Unknown unit: Meter")` |

### 3.4 수정 — `README.md` (ToDo 갱신)

| 섹션 | 변경 요약 |
|------|-----------|
| 헤더 | P0 FR **12/12 GREEN** |
| PR7 마일스톤 | **✅ 완료** (FR-06~12) |
| Boundary FR-12 | GREEN ✅ |
| `src/validator.py` | **✅** (FR-06~12) |
| TC 결과 | **13 passed** (전체 GREEN) |

---

## 4. PR7 Boundary FR 전체 완료

| FR | 모듈 | PR7 차수 | 비고 |
|----|------|----------|------|
| FR-06 | `validator` | 1차 | `:` 필수 |
| FR-07 | `validator` | 2차 | 숫자 검증 |
| FR-08 | `validator` | 3차 | 음수 거부 |
| FR-09 | `validator` + Registry | 4차 | 미지 단위 |
| FR-10 | `validator` | 5차 | 빈 unit/value |
| FR-11 | `parser` (TC만) | 6차 | strip |
| **FR-12** | **validator (TC만)** | **7차** | **case-sensitive** |

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-12 단건

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr12_case_sensitive_unit_rejected -v
# 1 passed
```

### 5.2 전체

```bash
python -m pytest tests/ -v
# 13 passed
```

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **9** | 0 |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **13** | **0** |

> Report 12 대비: **+1 PASS** (FR-12). **P0 FR 12/12 GREEN 달성**.

---

## 6. README ToDo 대비 진행

| 시점 | P0 FR GREEN |
|------|:-----------:|
| Report 12 (FR-11) | 11/12 |
| **Report 13 (FR-12)** | **12/12** |

**Domain Track:** FR-02~05 ✅ (PR1·PR5)  
**Boundary Track:** FR-01, FR-06~12 ✅ (PR1·PR7)

---

## 7. PR7 vs PR8

| PR | 범위 | P0 FR GREEN | 상태 |
|----|------|:-----------:|:----:|
| **PR7** | Boundary FR-06~12 + FR-11 | 12/12 (FR 전체) | **✅** |
| **PR8** | NFR P0 TC + 구현 | 0/8 | ⬜ |

---

## 8. 커밋 권장 사항 (PR7 FR-12 · PR7 완료)

### 8.1 포함 권장

```
tests/Boundary/test_cli.py
src/validator.py
README.md
Report/13_PR7_fr12-case-sensitive-unit-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-12 대소문자 거부 TC-FR-12 GREEN을 활성화하고 P0 FR 12/12 GREEN 및 README ToDo를 갱신합니다.
```

### 8.4 PR7 (7차·완료) 제안 제목

```
PR7: Boundary FR-12 GREEN — P0 FR 12/12 complete (Validator track)
```

---

## 9. 다음 단계 (PR8)

| 순서 | 작업 | 비고 |
|------|------|------|
| 1 | `cli.py` → `validator` 연동 | 출력·exit code |
| 2 | NFR P0 TC 작성·GREEN | PR8 |
| 3 | EXT P1 | PR9 |
| 4 | README NFR·EXT GREEN 컬럼 갱신 | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 12 (PR7 6차) | [Report/12_PR7_fr11-whitespace-trim-green-report.md](./12_PR7_fr11-whitespace-trim-green-report.md) |
| Validator | [src/validator.py](../src/validator.py) |
| UnitRegistry | [src/entity/registry.py](../src/entity/registry.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
