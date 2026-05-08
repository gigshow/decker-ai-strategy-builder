# Decker KRX — Business Model & Roadmap (Beta)

> **단일 정본**: 베타 단계 비즈니스 모델 + 공개 로드맵.
> 마케팅 랜딩 (`/markets/krx`) · Tier 1 홈 (`/krx`) · 공개레포 README · ONBOARDING_PUBLIC 의 카피·약속은 본 문서에 정합한다.
>
> 작성: 2026-05-09 · 버전 v1.0 · 다음 갱신: 분기말 (Q2 종료 = 2026-06-30)

---

## §1. 베타 framing — "Decker for Korean Stocks (Beta)"

```
포지셔닝:    매수·매도 신호가 아닌 → 포트폴리오 4 액션 추천
             (ADD · HOLD · REDUCE · EXIT)
가격:        무료 베타 (Beta tier · 무인증 30 req/day, X-API-Key 발급 시 1k/day)
운영:        매일 16:30 KST 평가, 일봉 (1d) 기준
한계:        NOT 투자자문. 시그널 = 결정 보조 정보. 손익 = 사용자 책임.
범위:        KOSPI 948 + KOSDAQ 1,822 universe (총 2,770 종목 OHLCV 보유)
             ranking universe = 거래대금 200 ∪ 사용자 구독 ∪ 등락폭증 ∪ 거래량폭증
```

### 베타 단계 정의 (왜 베타인가)

- ✅ **결정론적 엔진**: crypto 와 동일한 FSM/state engine 재사용 — back-testable.
- ✅ **L0 적재 + L1 평가 + L2 조립**: 시그널 카드 (entry/target/stop) 까지 production live.
- 🟡 **L3 채널 (Telegram)**: dry-run 운영 중. 베타 cutover 단계.
- ❌ **L4 자동주문 (KIS)**: 외부 API 의존. Q3-Q4 로드맵.
- ❌ **외인 net-buy / 시총 정확 / 펀더멘털**: KIS Open API 인입 대기 → 4 KRX 컨텍스트 중 2 만 wired.
- ❌ **백테스트 결과 공개**: GA 시점 OR 사용자 베타 피드백 후속.

베타 = **"시그널은 정직하게 노출, 자동주문 + 펀더 데이터는 약속"** 단계.

---

## §2. 가치 제안 (4 axes)

| # | 축 | 차별점 |
|---|---|---|
| ① | **결정론적 엔진** | 같은 입력 → 같은 출력. crypto 운영 검증된 FSM 재사용. |
| ② | **4 액션 (ADD / HOLD / REDUCE / EXIT)** | "매수·매도" 이분법 X. 포지션 보유 단계별 행동. |
| ③ | **진입가 / 목표 / 손절 동시 제공** | 시그널 카드 1 개 = 거래 의사결정 3 요소 (E/T/S). |
| ④ | **한국시장 컨텍스트 통합** | DART 공시 recency · KOSPI200 RS · 가격제한 lock 상태. (외인 / 시총 = KIS 인입 후) |

### "왜 매수·매도가 아닌가" — 핵심 메시지

```
시장:  주식은 종목이 많고, 한 종목 안에서도 비중 조정이 필요.
이슈:  buy/sell 이분법 = 비중 무시 → 사용자 노이즈 손실 패턴.
응답:  ADD (불타기) / REDUCE (분할) / EXIT (청산) / HOLD (유지)
       → 포지션 단계에 맞는 정밀 추천.
```

---

## §3. 데이터 출처 (공식·공개)

| 출처 | 빈도 | 용도 | 적재 상태 |
|---|---|---|---|
| **pykrx (KRX MDC)** | Daily 16:00 KST | OHLCV (KOSPI 948 + KOSDAQ 1,822) | ✅ 844K rows |
| **DART OpenDART** | Daily | 공시 (filings) → DART recency 컨텍스트 | 🟡 3,395 rows / 160 종목 (5.8%) — 백필 진행 중 |
| **ECOS 한국은행** | Daily | 환율 (USD/KRW) · 기준금리 · KTB3Y | ✅ 2,756 rows |
| **DART 기업 induty_code** | One-shot | 종목→33 KSIC sector 매핑 | ✅ 2,656 / 2,770 (95.8%) |
| **KIS Open API** | TBD | 외인 / 시총 / 펀더멘털 | ❌ Q3-Q4 — 베타 후속 |

### 한국시장 컨텍스트 4 축 (제공 매트릭스)

| 컨텍스트 | 약속 (랜딩) | 실제 (DB 검증) |
|---|---|---|
| **가격제한 (limit lock)** | ✅ 노출 | ✅ 715/715 채움 |
| **KOSPI200 상대강도 (RS)** | ✅ 노출 | ✅ 715/715 채움 |
| **DART 공시 recency** | ✅ 노출 | 🟡 162/715 (22.7%) — DART 백필 확대 시 100% 도달 |
| **외인 연속 net-buy** | ⏳ KIS 후속 | ❌ 0 rows (`krx_investor_flow_daily`) — Q3 이전 노출 X |

---

## §4. 제공 매트릭스 (정직 공개)

### ✅ 베타 단계 제공 — 카드에 그대로 노출

| 항목 | 검증 (production DB, 2026-05-09 기준) |
|---|---|
| 시그널 발화 (judgment_signals krx:daily) | 951 rows / 394 종목 / 5/7 |
| Entry / Target / Stop 채움률 | **951/951 (100%)** |
| 4 액션 매핑 (engine state → ADD/HOLD/REDUCE/EXIT) | 결정 트리 wired ✅ — `_portfolio_action()` |
| Action gate (GO / WATCH / HOLD) | GO 333 / WATCH 159 / HOLD 459 |
| Sector 분류 (33 KSIC) | 2,656 / 2,770 (95.8%) |
| 시장 탭 (KOSPI / KOSDAQ / ALL) | live ✅ |
| 데이터 freshness 배너 (3 단계) | live ✅ |
| 텔레그램 KRX 채널 | ✅ 5/9 cutover live — 일 1회 16:30 KST 단방향 broadcast (포트폴리오 브리핑) · chat_id=623511568 (deckerclawbot 재사용) · 양방향 명령은 D3 후속 |

### 🟡 베타 단계 부분 제공

| 항목 | 현 상태 | 근본 |
|---|---|---|
| **Why? matched_rule_id 추적** | ✅ 5/9 wire land — `evaluate_to_push_payload` 단일 진입점에 `try_assemble_rule_id_and_target_2_id` 호출 추가 (commit `<A3-fix>`). 다음 cron 부터 production 적재 (T3 GO MAIN 100% / T1 WATCH 일부 None 정상). 7 단위테스트 PASS · 회귀 0. 정본: `docs/DECKER_PIPELINE_DATAFLOW_2026-05-09.md §5.2` |
| **DART recency 100%** | 162/715 (22.7%) | dart_filings 5.8% 종목만 적재 → DART API 점진 백필 |
| **5/8 (금) 시그널** | ✅ 5/9 root fix land — Railway deploy 가 16:30 KST 직전·직후 일어나면 새 process 가 next 16:30 까지 22h 대기. KRXDailyScheduler `_loop` 진입 시 catch-up 추가 (영업일 + now ≥ 16:30 KST + 오늘 시그널 0건 → 즉시 1회 실행). 7 단위테스트 PASS. 정본: `docs/DECKER_PIPELINE_DATAFLOW_2026-05-09.md §8` |

### ❌ 베타 단계 미제공 — 후속 약속

| 항목 | 후속 시점 | 의존 |
|---|---|---|
| **KIS 자동주문 (체이닝)** | Q3-Q4 (2026 7-12월) | KIS Open API 키 발급 + KISExecutor 구현 |
| **외인 net-buy / 시총 정확 / 펀더** | Q3 (2026 7-9월) | KIS Open API 인입 |
| **5-year 백테스트 공개** | GA 시점 | OHLCV 5년 backfill + 전략별 PnL 검증 |
| **OpenClaw decker-krx 스킬** | Q4 시점 (2026 10-12월) | Claude 스킬 인프라 + 권한 |

---

## §5. 로드맵 (베타 → GA)

```
NOW (5/9)
├── ✅ Tier 1 홈 + 마케팅 랜딩 live
├── ✅ KOSPI + KOSDAQ universe (2,770 종목)
├── ✅ 4 액션 (ADD/HOLD/REDUCE/EXIT) + entry/target/stop
└── 🟡 텔레그램 채널 dry → live cutover (5min)

Q2 (5-6월) — 베타 안정화
├── A3  Why? matched_rule_id wire ✅ 5/9 land (evaluate_to_push 단일 fix · 7 tests PASS)
├── A4  L1 5/8 사고 root fix ✅ 5/9 land (KRXDailyScheduler catch-up — deploy 시점 cron 사이클 영구 가드)
├── B   마케팅 카피 정합 (5y backtest / 9-layer / KIS killer 제거 → 베타 framing) ✅ 5/9 land
├── C   공개레포 README + ONBOARDING_PUBLIC KRX 섹션 land ✅ 5/9 land
├── D1  Telegram cutover ✅ 5/9 land (chat_id=623511568 reuse, ENABLE=true, DRY_RUN=false)
│        · 일 1회 16:30 KST 단방향 broadcast (포트폴리오 브리핑 — ADD/EXIT/REDUCE)
├── D2  ENV cutover — partial bar guard (shadow → live), market=ALL (사용자 5min)
├── D3  KRX 봇 양방향 명령 추가 (3-4h) — /krx (브리핑 on-demand) · /signal 005930 (종목 상세)
└── E   DART 백필 KOSPI 200 + universe 폭증 종목 → recency 50%+

Q3 (7-9월) — KIS 데이터 인입 (외인/시총/펀더)
├── F1  KIS Open API 키 발급 + 어댑터 (외인 net-buy / 시총 정확 / 펀더멘털)
├── F2  consumer_signal_snapshot 4 KRX 컨텍스트 100% 충족
└── F3  5-year backfill 단계적 (1 → 2 → 5 년)

Q4 (10-12월) — 자동주문 cutover + GA 준비
├── G1  KISExecutor (모의투자 mock 1주 → real cutover)
├── G2  KRXAutoOrderProcessor (game_mode='krx' 처리기)
├── G3  OpenClaw decker-krx 스킬 (Claude 권장 사용)
├── G4  GA 가격 정책 (FREE 30 req/day → PRO $20/mo 10k req/day)
└── G5  5-year 백테스트 결과 공개 + 마케팅 카피 정밀 보강
```

---

## §6. 가격 정책 (베타 단계)

| Tier | 단가 | quota | 액세스 | 운영 시점 |
|---|---|---|---|---|
| **무인증 데모** | 무료 | 10 req/IP/day | `/api/v1/public/demo` (BTCUSDT) | NOW |
| **BETA (KRX X-API-Key)** | 무료 | 1,000 req/day | `/api/v1/public/krx/*` | NOW (Beta) |
| **PRO** | $20/mo | 10,000 req/day | crypto + KRX 통합 + KIS 자동주문 | GA (Q4) |

**원칙**: 베타 = 무료. PRO 는 GA 시점 KIS 자동주문 + 5y 백테스트 + 외인 데이터까지 묶어서 출시. 베타 동안 PRO 가입 노출 X (오해 방지).

---

## §7. 책임 한계 (필수)

```
NOT 투자자문 (Not investment advice).
시그널 = 결정 보조 정보 (decision support information).
실제 거래 손익 = 사용자 책임 (user's own responsibility).
백테스트 결과 ≠ 미래 수익 보장.
KRX 16:30 KST 일일 평가 — 장중 실시간 평가 X.
가격 제한 (상한가/하한가) lock 시 체결 불가 — 카드에 명시.
```

---

## §8. 공개 채널 인덱스

| 채널 | 위치 | framing |
|---|---|---|
| **마케팅 랜딩** | `/markets/krx` | "Decker for Korean stocks (Beta)" — KOSPI+KOSDAQ universe / 4 액션 / DART·ECOS·pykrx |
| **Tier 1 홈** | `/krx` | "매수·매도가 아닌, 4 상태 추천" — 오늘의 액션 / WATCH / 빠른 검색 |
| **시그널 리스트** | `/krx/signals` | 사용자 로그인 후 — 게이트·액션·sector 필터 |
| **종목 상세** | `/krx/signals/[ticker]` | entry/target/stop + Why? + KRX 컨텍스트 4축 |
| **공개레포 README** | `gigshow/decker-trading-platform` | 상단 "KRX (Korean Market) — Beta" 섹션 신규 |
| **공개 온보딩** | `docs/ONBOARDING_PUBLIC.md` | "한국주식 베타 사용자" 페르소나 신규 |
| **Telegram 채널** | `t.me/deckerclawbot?start=krx` | dry-run → live cutover (chat_id 등록 완료) |
| **공개 API** | `/api/v1/public/krx/*` | X-API-Key 발급 시 사용 |

---

## §9. 정합 검증 — "약속 ↔ 실제" 매트릭스

| 채널·약속 | 실제 | 정합 |
|---|---|---|
| 마케팅 hero pill `[5-year backtest]` | 백테스트 결과 0 | ❌ 제거 (B1) |
| 마케팅 hero pill `[9-layer RULES]` | 코드·docs grep 0건 | ❌ 제거 (B1) |
| 마케팅 hero pill `[KOSPI 200 universe]` | 실 universe = KOSPI 948 + KOSDAQ 1,822 | 🟡 정정 (B1) → "KOSPI + KOSDAQ universe" |
| 마케팅 §6 `★ killer feature — KIS chaining` | KISExecutor 0 LOC | ❌ dimming + "🚧 베타 후속 로드맵" (B2) |
| 마케팅 §10 `OpenClaw decker-krx` | disabled `(준비 중)` 표시 | ✅ OK (현재 framing 정확) |
| Tier 1 hero `카드 클릭 시 Why? 추적까지` | matched_rule_id NULL | 🟡 A3 본선 wire 후 100% 충족 |
| Tier 1 카드 `4 KRX 컨텍스트` | 4 중 2 정합 (외인 + 시총 정확 = NULL) | 🟡 카드에 외인 = "—" 표시 정직 |
| Tier 1 footer `매일 16:30 KST 갱신` | 5/8 (금) 0 row 사고 | ❌ A4 진단 후 운영 사고 fix |

---

## §10. 다음 본선 진입 (Phase A·B·C 완료 후)

본 문서 v1.0 land + Phase B (마케팅 카피) + Phase C (공개레포) 완료 후:

```
Q2 잔여 본선 (분기말 6/30 까지):
  - ENV cutover 잔여 (사용자 5min) — Telegram + partial guard + market=ALL
  - DART 백필 확대 (KOSPI 200 + 폭증 종목) — recency 50%+ 도달
  - L1 5/8 사고 root fix — Railway 로그 진단 후 cron 정합

Q3 진입 시점 — KIS Open API 키 발급 직후:
  - F1 KIS 어댑터 (외인/시총/펀더) — 1-2주
  - F2 consumer_signal_snapshot 4 KRX 컨텍스트 100%
  - F3 5y backfill 단계적
```

---

## §11. 갱신 정책

본 문서는 **분기말** 갱신 (Q2 = 6/30, Q3 = 9/30, Q4 = 12/31). 분기 중 단계 land 시 §5 로드맵 ✅ 마킹만. GA 시점 (Q4 종료) 별도 v2.0 발행.

---

**문서 버전**: v1.0 — 2026-05-09
**상태**: BETA · 무료 운영 중
**소유**: Decker AI · KRX 모듈 클러스터
**정본 위치**: `docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md`
