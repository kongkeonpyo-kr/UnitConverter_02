
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### ToDo — TDD 진행 현황 (PRD v1.2 기준)

> 상세 요구·추적표: [PRD/unit-converter-prd.md](PRD/unit-converter-prd.md) §8  
> 브랜치: `GREEN` | PR7 (Validator FR-06~08 GREEN)

#### 완료 기준

| Phase | 완료 기준 |
|-------|-----------|
| **RED** | PRD Req ID별 TC 1:1 작성, `pytest` 수집 가능, **의도적 실패** (`pytest.fail` 또는 import/assert 실패) |
| **GREEN** | 해당 TC **PASS**, 최소 구현으로 요구사항 충족 (assert 완화·skip 금지) |

#### 전체 진행 요약

| Phase | P0 FR (12) | NFR (8) | EXT (9) | 비고 |
|-------|------------|---------|---------|------|
| **RED** | ✅ 12/12 | ⬜ 0/8 | ⬜ 0/9 | P0 FR RED 전체 완료 |
| **GREEN** | ✅ 8/12 | ⬜ 0/8 | ⬜ 0/9 | PR7 (FR-01~08) |

#### GREEN PR 마일스톤

| PR | 커밋 | 범위 | 상태 |
|----|------|------|------|
| **PR1** | `521a4f4` | 레거시 `UnitConverter.py` → `src/` 분리, FR-01·FR-02 GREEN | ✅ |
| **PR2** | `c4fbfd8` | 루트 `entity/` 삭제 | ✅ |
| **PR3** | `f78949a` | `src/entity/` SSOT, re-export shim, import 정리 | ✅ |
| **PR4** | — | FR-04 TC GREEN (Domain, Report 05) | ✅ |
| **PR5** | `1b83ce0` | FR-03 Formatter + FR-03~05 Domain GREEN | ✅ |
| **PR7** | `d787bee` | FR-06~08 Validator (형식·숫자·음수), FR-09~12 잔여 | 🟡 |
| **PR8** | — | NFR P0 TC + 구현 | ⬜ |
| **PR9** | — | EXT P1 (설정·동적등록·출력포맷) | ⬜ |

---

#### P0 — FR (기능 요구) ToDo

**Track A — Boundary** (`tests/Boundary/test_cli.py`)

| Req ID | Test ID | 요구 | RED | GREEN | PR |
|--------|---------|------|:---:|:-----:|-----|
| FR-01 | TC-FR-01 | 입력 파싱 (`meter:2.5`) | ✅ | ✅ | PR1 |
| FR-06 | TC-FR-06 | 형식 검증 (`:` 필수) | ✅ | ✅ | PR7 |
| FR-07 | TC-FR-07 | 숫자 검증 | ✅ | ✅ | PR7 |
| FR-08 | TC-FR-08 | 음수 거부 | ✅ | ✅ | PR7 |
| FR-09 | TC-FR-09 | 미지 단위 거부 | ✅ | ⬜ | PR7 |
| FR-10 | TC-FR-10 | 빈 unit/value | ✅ | ⬜ | PR7 |
| FR-11 | TC-FR-11 | 공백 trim | ✅ | ⬜ | PR7 |
| FR-12 | TC-FR-12 | 대소문자 거부 | ✅ | ⬜ | PR7 |

**Track B — Domain** (`tests/Domain/test_converter.py`)

| Req ID | Test ID | 요구 | RED | GREEN | PR |
|--------|---------|------|:---:|:-----:|-----|
| FR-02 | TC-FR-02 | 전 단위 변환 (소스 제외) | ✅ | ✅ | PR1 |
| FR-03 | TC-FR-03 | 소수 1자리 반올림 (round half up) | ✅ | ✅ | PR5 |
| FR-04 | TC-FR-04 | meter 기준 파생 변환 | ✅ | ✅ | PR5 |
| FR-05 | TC-FR-05 | 단위 표기 (단수형) | ✅ | ✅ | PR5 |

---

#### P0 — NFR (비기능·아키텍처) ToDo

| Req ID | Test ID | 요구 | RED | GREEN | PR | Test File |
|--------|---------|------|:---:|:-----:|-----|-----------|
| NFR-01 | TC-NFR-01 | OCP (Registry 확장) | ⬜ | ⬜ | PR8 | `tests/test_registry.py` |
| NFR-02 | TC-NFR-02 | SRP (모듈 분리) | ⬜ | 🟡 | PR3 | `tests/test_structure.py` |
| NFR-03 | TC-NFR-03 | 테스트 가능성 (I/O 분리) | ⬜ | 🟡 | PR1 | `tests/Domain/test_converter.py` |
| NFR-04 | TC-NFR-04 | Python 3.10+ | ⬜ | ⬜ | PR8 | `tests/test_environment.py` |
| NFR-05 | TC-NFR-05 | 의존성 최소화 | ⬜ | ⬜ | PR9 | `tests/test_environment.py` |
| NFR-06 | TC-NFR-06 | 변환 정확도 | ⬜ | 🟡 | PR1 | `tests/Domain/test_converter.py` |
| NFR-07 | TC-NFR-07 | exit code | ⬜ | ⬜ | PR7 | `tests/Boundary/test_cli.py` |
| NFR-08 | TC-NFR-08 | CLI 실행 | ⬜ | ⬜ | PR7 | `tests/Boundary/test_cli.py` |

> 🟡 = TC 미작성·RED 미완료이나 PR1~PR3 구현으로 **부분 충족** (Registry OCP 구조, Converter 단독 테스트, FR-02 정확도)

---

#### P1 — EXT (확장 요구) ToDo

| Req ID | Test ID | 요구 | RED | GREEN | PR | Test File |
|--------|---------|------|:---:|:-----:|-----|-----------|
| EXT-01 | TC-EXT-01 | 설정 파일 로드 | ⬜ | ⬜ | PR9 | `tests/test_config_loader.py` |
| EXT-02 | TC-EXT-02 | 설정 누락 기본값 | ⬜ | ⬜ | PR9 | `tests/test_config_loader.py` |
| EXT-03 | TC-EXT-03 | 설정 파싱 실패 | ⬜ | ⬜ | PR9 | `tests/test_config_loader.py` |
| EXT-04 | TC-EXT-04 | `--config` 옵션 | ⬜ | ⬜ | PR9 | `tests/test_config_loader.py` |
| EXT-05 | TC-EXT-05 | 동적 단위 등록 | ⬜ | ⬜ | PR9 | `tests/test_registry.py` |
| EXT-06 | TC-EXT-06 | 등록 후 즉시 변환 | ⬜ | ⬜ | PR9 | `tests/test_registry.py` |
| EXT-07 | TC-EXT-07 | table 포맷 출력 | ⬜ | ⬜ | PR9 | `tests/Boundary/test_cli.py` |
| EXT-08 | TC-EXT-08 | json 포맷 출력 | ⬜ | ⬜ | PR9 | `tests/Boundary/test_cli.py` |
| EXT-09 | TC-EXT-09 | csv 포맷 출력 | ⬜ | ⬜ | PR9 | `tests/Boundary/test_cli.py` |

---

#### TC 실행

```bash
# 전체
python -m pytest tests/ -v

# GREEN 통과 TC — Boundary
python -m pytest tests/Boundary/test_cli.py::test_tc_fr_01_parse_meter_2_5 -v
python -m pytest tests/Boundary/test_cli.py::test_u_fr06_invalid_format_missing_colon -v
python -m pytest tests/Boundary/test_cli.py::test_u_fr07_invalid_number -v
python -m pytest tests/Boundary/test_cli.py::test_u_fr08_negative_value_rejected -v

# GREEN 통과 TC — Domain
python -m pytest tests/Domain/test_converter.py -v
```

**현재 TC 결과:** 13 collected — **8 passed**, 5 failed (FR-09~12 RED)

---

#### 구현 현황 (`src/`)

| 모듈 | Layer | FR/NFR | PR | 상태 |
|------|-------|--------|-----|------|
| `src/parser.py` | Boundary | FR-01 | PR1 | ✅ |
| `src/parsed_input.py` | Boundary | FR-01 | PR1 | ✅ |
| `src/cli.py` | Boundary | NFR-03, NFR-08 | PR1 | 🟡 |
| `src/converter.py` | Domain | FR-02 | PR1 | ✅ |
| `src/entity/registry.py` | Entity | NFR-01 | PR1·PR3 | ✅ |
| `src/entity/constants.py` | Entity | SSOT | PR1·PR3 | ✅ |
| `src/entity/conversion_result.py` | Entity | FR-02 | PR1·PR3 | ✅ |
| `src/formatter.py` | Domain | FR-03, FR-05 | PR5 | ✅ |
| `src/validator.py` | Boundary | FR-06~12 | PR7 | 🟡 (FR-06~08) |
| `config/units.json` | — | EXT-01 | PR9 | ⬜ |

---

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
