# ECB Review — 아키텍처·계약 위반 검사

UnitConverter_02 **ECB + Dual-Track 계약** 리뷰 전용 커맨드.  
**코드 수정 금지** — 위반 항목만 표로 보고한다.

---

## 필수 선언

응답 **첫 줄**에 반드시 기재:

```
Phase: REVIEW | Scope: ECB·계약 | Action: read-only
```

---

## 리뷰 범위

| 포함 | 제외 |
|------|------|
| ECB import 방향 위반 | 스타일·네이밍 취향 |
| Layer 계약 위반 (역할 침범) | 성능·미세 최적화 |
| Logic Track Domain Mock 위반 | UI Track Mock (허용) |
| MagicConstant SSOT 위반 (entity 산재) | 기능 요구(PR D) 충족 여부 전체 감사 |

대상 경로: `entity/`, `control/`, `boundary/`, `tests/` (및 레거시 `src/` 존재 시)

---

## ECB 계약 (기준)

```
boundary ──→ control ──→ entity
                ↑            ↑
           entity만      외부 Layer import 금지
```

| Layer | 허용 import | 금지 |
|-------|-------------|------|
| **entity** | stdlib, 동일 entity 패키지 | `boundary`, `control`, I/O |
| **control** | `entity` | `boundary`, I/O 직접 호출 |
| **boundary** | `control`, `entity`(얇은 DTO만) | entity 우회·도메인 규칙 중복 |

---

## 절차

1. **import 스캔** — `entity/`, `control/`, `boundary/` 각 파일의 import 문 수집.
2. **방향 검증** — 허용 그래프 대비 역방향·횡단 import 표기.
3. **테스트 스캔** — `tests/test_d_*.py`(Logic)에서 `MagicMock`/`patch`/`Mock` on domain 여부.
4. **위반 표 작성** — 아래 템플릿만 출력. 위반 0건이면 「위반 없음」1행.

---

## 위반 보고 템플릿 (표)

### 1. Import 방향 위반

| # | 파일 | Layer | 위반 import | 계약 | 심각도 |
|---|------|-------|-------------|------|--------|
| 1 | `entity/foo.py` | entity | `from boundary.cli import ...` | entity → boundary 금지 | **HIGH** |
| 2 | `control/usecase.py` | control | `from boundary.parser import ...` | control → boundary 금지 | **HIGH** |
| 3 | `boundary/cli.py` | boundary | (없음) | — | — |

**심각도:** HIGH = 빌드/아키텍처 붕괴, MED = 계약 경계 흐림, LOW = 권장 위반(역할 중복 징후).

### 2. Layer 계약 위반 (역할 침범)

| # | 파일 | Layer | 내용 | 계약 |
|---|------|-------|------|------|
| 1 | `boundary/parser.py` | boundary | 변환 비율 `3.28084` 하드코딩 | boundary에 도메인 규칙 중복 금지 |
| 2 | `entity/converter.py` | entity | `print()` 호출 | entity I/O 금지 |

### 3. Logic Track — Domain Mock 위반

| # | 테스트 파일 | Track | Mock 대상 | 사용 API | 계약 |
|---|-------------|-------|-----------|----------|------|
| 1 | `tests/test_d_converter.py` | Logic | `Converter.convert` | `@patch` | Logic Track Domain Mock 금지 |
| 2 | `tests/test_u_cli.py` | UI | `stdin` | `monkeypatch` | **허용** — 보고 제외 |

**Logic Track 대상:** `test_d_*.py`, `test_converter.py`(레거시), `@pytest.mark` Logic/D-*  
**Domain Mock 예:** Converter, Registry, Unit, 변환 비율 provider를 Mock/patch/stub

---

## 검색 힌트 (리뷰어용, 수정 아님)

```bash
# entity 역방향 import 후보
rg "^from (boundary|control)" entity/
rg "^import (boundary|control)" entity/

# control → boundary
rg "^from boundary" control/

# Logic Track Domain Mock 후보
rg "Mock|patch|MagicMock" tests/test_d_*.py tests/test_converter.py
```

---

## 보고 형식

| 항목 | 내용 |
|------|------|
| **스캔 범위** | 검사한 디렉터리·파일 수 |
| **위반 건수** | Import / Layer / Domain Mock 각 N건 |
| **표** | 위 템플릿 3종 (해당 없으면 「해당 없음」) |
| **권고** | 수정 방향 1줄씩 (코드 패치 **금지**) |

---

## 금지

- 소스·테스트 **코드 수정** (리뷰 커맨드는 read-only)
- 위반 외 리팩터·기능 제안 장문
- UI Track Mock을 위반으로 기록
- Skill 파일 생성
