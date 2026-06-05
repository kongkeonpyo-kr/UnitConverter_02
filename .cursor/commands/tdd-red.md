# TDD RED — 실패 테스트 먼저

UnitConverter_02 Dual-Track TDD **RED 단계** 전용 커맨드.  
구현(`src/`, `entity/`, `control/`, `boundary/`)은 작성하지 않고, **실패하는 테스트만** 추가한다.

---

## 필수 선언

응답 **첫 줄**에 반드시 기재:

```
Phase: RED | Layer: {entity|control|boundary} | Track: {Logic|UI}
```

| Track | Layer | Test ID | 파일명 | Mock |
|-------|-------|---------|--------|------|
| **Logic** | entity, control | `D-*` | `tests/test_d_*.py` | Domain Mock **금지** |
| **UI** | boundary | `U-*` | `tests/test_u_*.py` | stdin/stdout·CLI Mock **허용** |

- PRD `FR/NFR/EXT` → Test ID(`TC-FR-01` 등) 매핑은 `PRD/unit-converter-prd.md` §8 참조.
- Dual-Track naming(`D-*`/`U-*`)과 PRD Track(A/B) 대응:
  - PRD Track A (Boundary) → **UI Track** → `U-*`
  - PRD Track B (Domain) → **Logic Track** → `D-*`

---

## 절차

1. **ID 확인**
   - 대상 Req ID(FR/NFR/EXT)와 Test ID(`TC-*`)를 PRD §8에서 확인.
   - Track(Logic/UI)·Layer(entity/control/boundary) 결정.
   - 신규 TC면 `D-` 또는 `U-` ID 부여(기존 `TC-FR-*`와 주석으로 연결).

2. **AAA 테스트 작성** (`tests/`만)
   - **Arrange:** PRD Given — 입력·Registry·기본 조건.
   - **Act:** 아직 없는 구현 모듈 호출( import는 테스트 함수 내부 ).
   - **Assert:** PRD Then — 기대값·오류·exit code. **완화 금지.**
   - 파일 상단 docstring: Req ID, Test ID, Track, Layer, PRD § 참조.

3. **pytest FAIL 확인**
   - `ModuleNotFoundError` 또는 `AssertionError`로 **FAILED** 상태여야 RED 완료.
   - `skip` / `xfail` / `pass` 로 우회 **금지**.

---

## pytest 예시 (bash)

```bash
# Logic Track (Domain)
python -m pytest tests/test_d_converter.py::test_d_fr02_all_units_excluding_source -v

# UI Track (Boundary)
python -m pytest tests/test_u_cli.py::test_u_fr01_parse_meter_2_5 -v

# RED 단계 전체 tests/ (실패 예상)
python -m pytest tests/ -v
```

**RED 성공 기준:** 대상 TC가 **FAILED** (not PASSED, not SKIPPED).

---

## 보고

RED 단계 종료 시 아래 형식으로 보고:

| 항목 | 내용 |
|------|------|
| **테스트 ID** | `D-*` 또는 `U-*` (+ PRD `TC-*` / Req ID) |
| **FAIL 요약** | pytest 출력 1~2줄 (예: `ModuleNotFoundError: No module named 'entity'`) |
| **변경 파일** | `tests/` 하위만 (예: `tests/test_d_converter.py`) |

---

## 금지

- `src/`, `entity/`, `control/`, `boundary/` **수정·생성** (GREEN까지 보류)
- **Logic Track**에서 Converter·Registry·변환 로직 **Domain Mock** (`MagicMock`, `patch` on domain)
- **assert 완화** (허용 오차 임의 확대, 조건 삭제, `>=`로 변경 등)
- **`pytest.skip`**, **`pytest.mark.xfail`**, 빈 `pass` 로 통과 처리
- 요청 범위 밖 FR/TC 일괄 추가
- Skill 파일 생성 (본 커맨드는 commands 전용)
