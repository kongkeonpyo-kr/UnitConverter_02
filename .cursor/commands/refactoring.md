# REFACTOR — SRP·OCP·코드 스멜 기반 리팩토링

UnitConverter_02 **REFACTOR 단계** 전용 커맨드.  
**외부 동작(출력·오류 메시지·exit code)은 유지**하고, 구조·역할·확장성만 개선한다.

---

## 필수 선언

응답 **첫 줄**에 반드시 기재:

```
Phase: REFACTOR | Layer: {entity|control|boundary|src} | Track: {Logic|UI|Both} | NFR: {SRP|OCP|스멜}
```

| Track | Layer | 대상 경로 | Golden Master |
|-------|-------|-----------|---------------|
| **Logic** | entity, control, `src/converter.py`, `src/formatter.py` | Domain·변환·포맷 | Domain TC 위주 |
| **UI** | boundary, `src/cli.py`, `src/parser.py`, `src/validator.py` | 파싱·검증·CLI | **필수** — `tests/GoldenMaster/` |
| **Both** | orchestration (`cli.run` wiring) | Logic+UI 연결 | Golden + Boundary + Domain |

- PRD NFR-01(OCP), NFR-02(SRP), NFR-03(테스트 가능성): `PRD/unit-converter-prd.md` §3.4
- ECB 목표 구조: `.cursor/rules/.cursorrules`, `review-ecb` 커맨드

---

## REFACTOR 전제 (Gate)

1. **GREEN 유지** — 대상 Req의 TC가 이미 PASSED 상태.
2. **Golden Master baseline** — `golden_master/expected/*.txt` 존재 시 리팩토 전후 diff 검사.
3. **범위 최소화** — 한 PR/한 커밋 = 하나의 스멜 또는 하나의 NFR 축(SRP **또는** OCP).
4. **동작 변경 금지** — 의도적 UX/PRD 변경은 REFACTOR가 아니라 GREEN+PRD 갱신.

```bash
# Gate: 전체 회귀
python -m pytest tests/ -v

# Gate: Golden Master (cli.run stdout)
python -m pytest tests/GoldenMaster/test_golden_master.py -v
```

**REFACTOR 성공 기준:** pytest **전부 PASSED** + Golden Master **diff 없음** (의도적 변경 시만 `generate_golden_master.py` 재실행).

---

## SRP — 단일 책임 (NFR-02)

### 모듈별 단일 책임 (SSOT)

| 모듈 | 유일한 책임 | 하면 안 되는 일 |
|------|-------------|-----------------|
| `parser.py` | `unit:value` **구문 분리** + trim | 형식/음수/미지 단위 **검증**, 변환, print |
| `validator.py` | 입력 **검증** + `ValidationError` | 변환, 출력 포맷, Registry 확장 로직 |
| `entity/registry.py` | 단위 등록·조회·**비율 SSOT** | I/O, 메시지 문자열, round 규칙 |
| `converter.py` | meter 허브 **변환** | 입력 검증, print, JSON/CSV 포맷 |
| `formatter.py` | **출력 문자열** 생성 (FR-03 round half up) | stdin, exit code, 검증 |
| `cli.py` | **오케스트레이션** + I/O (`input`/`print`) | 검증 규칙·비율·반올림 **중복 구현** |

### SRP 위반 신호 (스멜 → 리팩토 방향)

| 스멜 | 감지 | 리팩토 방향 |
|------|------|-------------|
| **Divergent Change** | 한 파일만 자주 여러 이유로 수정 (예: `cli.py`에 검증+포맷+변환) | 책임별 모듈로 **Extract Function / Move Method** |
| **Shotgun Surgery** | 기능 하나 바꿀 때 3+ 파일 동시 수정 | 공통 로직 **한 모듈로 Consolidate** |
| **Feature Envy** | A가 B의 데이터를 더 많이 씀 (예: boundary가 비율 상수 직접 참조) | 메서드를 **데이터 쪽(entity)** 으로 이동 |
| **God Function** | `run()`/`main()` 30줄+ 분기·print·검증 혼재 | **Extract Function**, `cli`는 wiring만 |

### SRP 체크리스트 (리팩토 전후)

- [ ] `cli.run()`이 `validate_input()` → `parse_input()` → `Converter` → `formatter` **순서로만** 호출하는가?
- [ ] 오류 메시지 문자열이 **validator 한 곳**(또는 PRD 명시 상수)에만 있는가?
- [ ] `3.28084`, `1.09361` 등 Magic Number가 **`entity/constants.py` 또는 Registry** 외에 없는가?
- [ ] Domain 테스트가 `input`/`print` 없이 실행되는가? (NFR-03)

---

## OCP — 개방-폐쇄 (NFR-01)

### 확장 축 vs 수정 축

| 확장 (열림) | 수정 없이 가능해야 함 | 수정 (닫힘) |
|-------------|----------------------|-------------|
| **새 단위** (`inch`, `cubit`) | Registry(또는 `config/units.json`) 등록만 | `Converter`/`cli`의 `if unit == "meter"` 분기 |
| **새 출력 포맷** (json/csv) | Formatter 또는 `--format` 전략 추가 | `Converter` 변환 로직 |
| **새 검증 규칙** | Validator 함수/규칙 추가 | Registry 비율 테이블 |

### OCP 위반 신호

| 스멜 | 감지 | 리팩토 방향 |
|------|------|-------------|
| **Switch / if-elif on unit** | `if unit == "feet":` / `elif unit == "yard":` | **Registry lookup** + 데이터 기반 변환 |
| **Magic Constant 산재** | 동일 비율이 2+ 파일 | **Registry SSOT** 로 Merge |
| **Modified every release** | 단위 추가마다 `converter.py`·`cli.py` 동시 패치 | 확장점을 Registry·config로 **Replace Conditional with Polymorphism**(테이블) |

### OCP 수용 테스트 (수동·RED 후)

```python
# TC-NFR-01 방향: Converter/Formatter 코드 비수정 + Registry만 확장
registry = UnitRegistry({**UnitRegistry.default()._units, "inch": 39.3701})
converter = Converter(registry)
# inch 변환 가능 — Converter 소스 diff 없음
```

---

## 코드 스멜 카탈로그 & 자동 감지

리팩토 **시작 전** 아래 검색을 실행하고, 히트를 **스멜 후보 표**에 기록한다.

### 1. 구조·SOLID 스멜

| ID | 스멜 | 설명 | 검색 (rg) | 심각도 |
|----|------|------|-----------|--------|
| S01 | **Duplicate Validation** | validator와 cli에 동일 검증 | `rg "Invalid format|Unknown unit|Negative values" src/` | **HIGH** |
| S02 | **Bypass Validator** | cli가 validator 없이 직접 검증 | `rg "has_unit|split\\(\":\"" src/cli.py` + `validate_input` 부재 | **HIGH** |
| S03 | **Bypass Formatter** | cli가 f-string으로 변환 출력 | `rg "print\\(f\"\\{.*\\}.*feet" src/cli.py` | **MED** |
| S04 | **Switch on Unit** | 단위명 분기 | `rg "if unit ==|elif unit ==" src/` | **HIGH** |
| S05 | **Magic Number** | 비율 하드코딩 | `rg "3\\.28084|1\\.09361" src/ --glob '!**/constants.py'` | **HIGH** |
| S06 | **I/O in Domain** | entity/converter에서 print/input | `rg "print\\(|input\\(" src/entity/ src/converter.py` | **HIGH** |
| S07 | **Layer Leak** | parser/validator가 변환 수행 | `rg "Converter|to_base|format_conversions" src/parser.py src/validator.py` | **MED** |
| S08 | **Registry Bypass** | 단위 목록 하드코딩 | `rg '\"meter\".*\"feet\".*\"yard\"' src/ --glob '!**/registry.py'` | **MED** |
| S09 | **Long Method** | 25줄+ 단일 함수 | 수동: `run`, `validate_input`, `convert` 줄 수 | **LOW** |
| S10 | **Primitive Obsession** | `(unit, value)` 튜플 남발 | `rg "tuple\\[str, float\\]" src/` (ParsedInput 미사용 경로) | **LOW** |
| S11 | **Speculative Generality** | 미사용 추상·인터페이스 | 미참조 class/protocol | **LOW** |
| S12 | **Dead Code** | re-export shim·미사용 import | `rg "^from src\\." src/ --glob '*.py'` + 사용처 없음 | **LOW** |

### 2. 본 프로젝트 알려진 부채 (2026-06 REFACTORING 기준)

| 위치 | 스멜 ID | 내용 | 목표 상태 |
|------|---------|------|-----------|
| `src/cli.py` | S01,S02,S03 | 검증·출력을 validator/formatter 없이 inline | `validate_input` + `format_conversions` 위임 |
| `src/parser.py` | S07(경미) | `resolve_unit`으로 Registry 조회 — 파싱 vs 정규화 경계 | 정규화를 validator/registry helper로 **Move** 검토 |
| `UnitConverter.py` | S12 | 레거시 진입점 | `cli.main` thin wrapper만 유지 |

### 3. 일괄 스캔 스크립트 (리팩토 전)

```bash
# 프로젝트 루트에서
rg "3\.28084|1\.09361" src/ --glob '!**/constants.py'
rg "if unit ==|elif unit ==" src/
rg "print\(|input\(" src/entity/ src/converter.py
rg "Invalid format|Unknown unit" src/ --glob '*.py'
rg "validate_input" src/cli.py || echo "SMELL: cli bypasses validator"
rg "format_conversions|formatter" src/cli.py || echo "SMELL: cli bypasses formatter"
python -m pytest tests/ -q --tb=no
python -m pytest tests/GoldenMaster/ -q --tb=no
```

---

## REFACTOR 절차 (Extract → Move → Wire)

1. **스멜 스캔** — 위 표 + rg 실행, **1개 스멜** 선택.
2. **안전망 확인** — `tests/` + Golden Master GREEN.
3. **작은 단계 리팩토** (Fowler 우선순)
   - **Extract Function** — 긴 `run()` 분해
   - **Move Function** — 검증→validator, 포맷→formatter, 비율→registry
   - **Replace Conditional with Lookup** — unit if-elif → Registry
   - **Remove Duplication** — 메시지·split 로직 단일화
4. **회귀 실행**

```bash
python -m pytest tests/Boundary/test_cli.py tests/Domain/test_converter.py -v
python -m pytest tests/GoldenMaster/test_golden_master.py -v
```

5. **Golden diff 발생 시**
   - **비의도** → 롤백 후 단계 축소
   - **의도**(PRD 변경) → `python scripts/generate_golden_master.py` + Report·PRD 갱신

6. **보고** — 아래 템플릿.

---

## 리팩토 패턴 Quick Reference

| 패턴 | When | UnitConverter 예 |
|------|------|------------------|
| Extract Function | 한 함수가 2+ 일을 함 | `cli.run` → `_run_validated_conversion()` |
| Move Method | Feature Envy | `resolve_unit` → Registry only; parser는 thin |
| Replace Conditional | unit switch | `if feet/yard` → `registry.to_base()` |
| Introduce Parameter Object | `(unit, value)` 반복 | `ParsedInput` 일관 사용 |
| Replace Magic Number | 상수 산재 | `entity/constants.py` |
| Facade | cli 단순화 | `cli.run` = parse→validate→convert→format→print |

---

## 보고 템플릿

| 항목 | 내용 |
|------|------|
| **Phase** | REFACTOR |
| **NFR** | SRP / OCP / 스멜 ID (S01~S12) |
| **스멜 요약** | 1문장 |
| **변경 파일** | `src/...` (테스트 diff 없음 원칙) |
| **회귀** | `pytest tests/` N passed; Golden Master OK / regenerated |
| **잔여 스멜** | 다음 REFACTOR 후보 1~2개 |

### 스멜 스캔 결과 표 (선택)

| ID | 파일:줄 | 스멜 | 조치 | 상태 |
|----|---------|------|------|------|
| S02 | `src/cli.py:11-26` | Bypass Validator | `validate_input` 연동 | ✅/⬜ |

---

## 금지

- **RED/GREEN 건너뛰기** — 실패 TC를 REFACTOR로 고치지 말 것 (요구 변경은 PRD+RED 먼저).
- **assert 완화·Golden expected 수동 편집** (스크립트 재생성 없이).
- **Behavior change 혼입** — FR 메시지·반올림·단위 정책 변경은 REFACTOR 범위 밖.
- **Logic Track Domain Mock** 도입.
- **과잉 추상화** — Strategy/Factory 남발 (YAGNI; Registry 테이블로 충분).
- Skill 파일 생성 (본 커맨드는 commands 전용).

---

## 관련 커맨드·문서

| 리소스 | 용도 |
|--------|------|
| `.cursor/commands/tdd-red.md` | 실패 TC 추가 |
| `.cursor/commands/review-ecb.md` | ECB import·Layer read-only 리뷰 |
| `PRD/unit-converter-prd.md` §3.4 | NFR-01~03 |
| `scripts/generate_golden_master.py` | Golden baseline 재생성 |
| `Report/14_REFACTORING_*` | Golden Master 워크플로 |
