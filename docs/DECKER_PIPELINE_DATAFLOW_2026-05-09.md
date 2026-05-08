# Decker — 4 트랙 × 5 레이어 통합 데이터 흐름 (2026-05-09)

> **단일 정본**: 원천 데이터 → 엔진 평가 → 통합 시그널 → 채널 → 자동주문.
> v1 엔진트리거 / v2 파이프라인 / v3 게임이론 / KRX 4 트랙의 **공유 인프라 vs 분기점** 명확화.
>
> 작성: 2026-05-09 · 버전 v1.0 · 진입 사유: matched_rule_id audit 중 mtf_signal_assembler vs assemble_final_signal 두 assembler 발견 + v2/v3/KRX path 분리 정리 필요

---

## §0. TL;DR (30초)

```
공유 (자산 무관):    L0 candle/ohlcv 적재 + L1 decker_engine.facade.evaluate
분기 시작:           judgment_signals INSERT (source 컬럼으로 트랙 분리)

4 트랙:
  v1 엔진트리거    judgment_signals 그 자체 + trigger_performance (PnL 추적)
  v2 파이프라인    + mtf_signal_assembler → consumer_signal_snapshot → Telegram/Web/AutoOrder
  v3 게임이론      ← judgment_signals + trigger_performance (read only) → game_signal
  KRX             별도 cron + KRXConsumerSignalBuilder → asset_class='krx'

발견한 갭 (5/9 audit):
  WP-6 P1-G1-01 (assemble_final_signal + matched_rule_id) 가 admin 디버그만 wire.
  v2/KRX production push 에는 matched_rule_id 0% NULL.
  fix = evaluate_to_push_payload 단일 파일에 try_assemble 호출 추가 (30-60min).
```

---

## §1. 5 레이어 (자산 무관 인프라)

```
L0 적재          외부 API → DB 영구 저장 (pure I/O)
L1 평가          decker_engine.facade.evaluate (FSM state + push 변환)
L2 조립          판단 시그널 → 통합 시그널 (소비자 단위)
L3 채널          시그널 → Telegram / Web / Slack 배포
L4 주문          시그널 → ExecutionRouter → 거래소 API
```

각 레이어 책임:

| 레이어 | 책임 단일성 | 모듈 |
|---|---|---|
| L0 | 외부 API → DB. 엔진 호출 X | `candle_data_scheduler` (crypto) · `krx_ohlcv_scheduler` (KRX) |
| L1 | DB candle → engine evaluate → judgment_signals INSERT | `engine_live_l1_push_scheduler` (crypto) · `krx_daily_scheduler` (KRX) |
| L2 | judgment_signals → consumer_signal_snapshot (asset_class 별) | `consumer_signal_builder` · `krx_consumer_signal_builder` |
| L3 | consumer_signal_snapshot → 채널 dispatch | `good_signal_notifier` · `krx_telegram_channel` (dry-run) |
| L4 | consumer_signal_snapshot → 자동주문 | `auto_order_signal_processor` · `KRXAutoOrderProcessor` (미구현) |

---

## §2. 4 트랙 비교 매트릭스

| 트랙 | source / asset_class | 엔진 호출 | L2 빌더 | L3 채널 | L4 주문 | 특이점 |
|---|---|---|---|---|---|---|
| **v1 엔진트리거** | `engine:live_l1` (legacy 단일 시그널) | ✅ | — | direct push | — | judgment_signals 자체 = 시그널. L2 통합 X |
| **v2 파이프라인** | `engine:live_l1` + asset_class=`crypto` | ✅ | ✅ `consumer_signal_builder` (4h 주기, MTF 통합) | `good_signal_notifier` (Telegram/Web) | `auto_order_signal_processor` | **MTF 통합 + size_factor + qty 계약** |
| **v3 게임이론** | game_signal table 별도 (judgment_signals + trigger_performance read only) | — (v2 결과 read) | `DisplacementGameClassifier` (30min cron) | v3 Telegram 별도 | v3 AutoOrder 별도 | REVERSAL/REANCHOR 분류 + P1~P4 tier · 보호구역 X |
| **KRX** | `krx:daily` + asset_class=`krx` | ✅ | ✅ `krx_consumer_signal_builder` (16:35 KST cron) | `krx_telegram_channel` (dry-run) | `KRXAutoOrderProcessor` (Phase E 미구현) | 1d only · MTF 미사용 · KIS API 의존 향후 |

### 보호구역 (CLAUDE.md ⛔ 정합)

```
v2 NEVER TOUCH (v3/신규 코드 절대 삽입 금지):
  engine_live_l1_push_scheduler.py
  good_signal_notifier.py
  consumer_signal_builder.py

v3 단독 소유:
  displacement_game_classifier.py → game_signal table

KRX 별도 시스템 (§10):
  4 격리 컬럼 (source='krx:daily', symbol='*.KRX',
              asset_class='krx', game_mode='krx')
```

---

## §3. 데이터 흐름도 — 4 트랙 ASCII

```
┌──────────────────────────────────────────────────────────────────┐
│                         L0 적재 (자산별)                          │
│ Crypto: Binance WebSocket → candle_data                          │
│ KRX:    pykrx daily → krx_ohlcv_daily                            │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│              L1 평가 — decker_engine.facade.evaluate             │
│  candles → engine_result {state_snapshot, engine_flags, trace}   │
│  (자산 무관, 동일 엔진 사용)                                      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│      L1.5 push 변환 — evaluate_to_push_payload                   │
│  engine_result → push body (engine_* 컬럼)                       │
│  ⚠️ matched_rule_id wire 누락 (이게 5/9 audit 발견)              │
└────────────────────────┬─────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│          L1.6 판단 시그널 적재 — judgment_signal_push_insert      │
│  judgment_signals INSERT  ← 단일 진실 (모든 트랙 공유)            │
│   · source='engine:live_l1' (crypto)                             │
│   · source='krx:daily'      (KRX)                                │
│  Per-row engine_* 51 columns + entry/target/stop                 │
└────────┬─────────────────────────────────┬──────────────────────┘
         │ Crypto                          │ KRX
         ▼                                 ▼
   ┌─────────────────────────┐    ┌──────────────────────────┐
   │   v2 파이프라인         │    │   KRX 파이프라인          │
   │ ──────────────────────  │    │ ────────────────────────  │
   │ 4h 발화 시:              │    │ 16:35 KST cron:          │
   │  ↓ mtf_signal_assembler │    │  ↓ KRXConsumerSignalBldr │
   │   30m+1h+4h cache 통합   │    │   judgment_signals       │
   │   → MTFAction            │    │   + krx_context.compute  │
   │   (ENTER/WAIT/SKIP)     │    │  ↓ consumer_signal_snap  │
   │  ↓                       │    │    asset_class='krx'     │
   │ consumer_signal_builder  │    │    krx_* 7 columns       │
   │  ↓ MTF API /mtf-signal/* │    └──────────┬───────────────┘
   │  + trigger_performance  │               │
   │  → consumer_signal_snap │               │
   │    asset_class='crypto' │               │
   └─────────┬───────────────┘               │
             │                               │
             ▼                               ▼
   ┌─────────────────────────────────────────────────────────┐
   │       L3 채널 (asset_class 분기)                         │
   │ Crypto:  good_signal_notifier (Telegram + Web)           │
   │ KRX:     krx_telegram_channel (dry-run)                 │
   └─────────┬───────────────────────────────┬───────────────┘
             │                               │
             ▼                               ▼
   ┌─────────────────────────┐    ┌──────────────────────────┐
   │      L4 자동주문         │    │      L4 자동주문 (KRX)    │
   │ auto_order_signal_proc  │    │ KRXAutoOrderProcessor    │
   │ → ExecutionRouter        │    │ → KISExecutor            │
   │ → Binance / Bitget       │    │ ❌ Phase E (미구현)       │
   └─────────────────────────┘    └──────────────────────────┘

         (별도 트랙 — judgment_signals read only)
   ┌─────────────────────────────────────────────────────────┐
   │   v3 게임이론 (read v2/KRX, 별도 INSERT)                 │
   │ ────────────────────────────────────────────────────     │
   │ 30min cron: DisplacementGameClassifier                   │
   │   ← trigger_performance + judgment_signals JSONB         │
   │   → game_signal INSERT (P1~P4 tier · REVERSAL/REANCHOR)  │
   │ 5min cron:  GameSignalPerformanceTracker                 │
   │   → game_signal UPDATE (exit_ts/exit_price)              │
   └─────────────────────────────────────────────────────────┘
```

---

## §4. 두 Assembler 의 정확한 위치 (5/9 audit 발견)

### A. `mtf_signal_assembler.assemble()` — v2 production 정본 ✅

```
정본 위치:  services/decker-engine/src/decker_engine/contract/mtf_signal_assembler.py
호출처:     engine_live_l1_push_scheduler.py:609 (4h push 직전)
입력:       dict[tf, ClassificationResult] (1w/1d/8h/4h/1h/30m/15m)
출력:       MTFAction(decision: ENTER/WAIT/SKIP, size_factor 0.0~1.0,
                      reason_chain, signal_quality_by_tf)
정본 spec:  SIGNAL_ASSEMBLY_TIER1_SPEC §2.1.1
운영:       ✅ v2 production 활성. 4h+ 시그널의 통합 MTF 결정.
```

**역할**: TF 역할 분리 (STRUCTURE/JUDGMENT/ENTRY) 후 ENTER/WAIT/SKIP + size_factor 산출. 사용자가 묻는 "통합 MTF 시그널" = **이것**.

### B. `assemble_final_signal()` — WP-6 신규 spec ⚠️

```
정본 위치:  services/decker-engine/src/decker_engine/signal_assembly/assembler.py
호출처:     services/engine_core/final_signal_assembler_utils.py:try_assemble
            ← engine_label_operation_bridge.py:194 (admin endpoint only)
            ← admin_label_chart.py / admin_final_signal.py
입력:       L3InputRow list (Tier 별 후보)
출력:       FinalSignal {tier, strength, matched_rule_id, active_target_2_id, sources}
정본 spec:  WP-6 P1-G1-01 (docs/WP6_TRIGGER_SPEC_LINKAGE_WORK_PLAN.md)
운영:       ⚠️ admin 디버그까지만 wire. production push 호출 0건.
```

**역할**: Tier 분류 (T1/T2/T3) + rules.yaml rules[] 매칭으로 `matched_rule_id` 부여. "Why? 추적" 약속의 데이터 소스. **A 와 다른 목적의 신규 layer**.

### 두 assembler 의 관계 — 현재 + 의도

```
현재 (5/9 기준):
  mtf_signal_assembler  →  v2 ENTER/WAIT/SKIP + size_factor (운영)
  assemble_final_signal →  Tier + matched_rule_id (admin only)
  두 출력은 별도 path 로 흐름 — 서로 cross-reference 없음

WP-6 의도 (추측):
  assemble_final_signal 이 Tier 별 final 결정의 새 권위가 될 예정
  matched_rule_id 가 모든 시그널에 부여 = "Why?" 추적 100%
  but production wire 미완 = WP-6 끝 증거 (5/9 audit 결과 stale)
```

---

## §5. matched_rule_id 갭 — 진단 + fix 경로

### 5.1 갭 증거 (production DB)

```sql
SELECT source, COUNT(*) total, COUNT(*) FILTER (WHERE engine_matched_rule_id IS NOT NULL) filled
FROM judgment_signals WHERE source IN ('engine:live_l1','krx:daily') GROUP BY 1;

→ engine:live_l1   1593   0   (crypto v2 NULL 100%)
→ krx:daily         951   0   (KRX     NULL 100%)
```

### 5.2 wire 위치 — 단일 fix point

```python
# src/decker/api/app/services/engine_core/evaluate_to_push_payload.py
# engine_evaluate_to_signal_push_payload() 내부, push body 빌드 후

from app.services.engine_core.final_signal_assembler_utils import (
    try_assemble_rule_id_and_target_2_id,
)

rule_id, target_2_id = try_assemble_rule_id_and_target_2_id(
    tf=timeframe,
    evaluate_out=engine_result,
    signal_state=push,
)
if rule_id:
    push["engine_matched_rule_id"] = rule_id
if target_2_id:
    push["engine_active_target_2_id"] = target_2_id
```

**효과**: evaluate_to_push_payload 가 single source → crypto v2 + KRX 동시 wire.
**시간**: 30-60min (코드 + 단위테스트 + 회귀 검증).
**리스크**: assembler 가 None 반환 시 NULL 유지 (현 동작과 동일) → 회귀 0.

### 5.3 검증 SQL (post-fix)

```sql
-- 24h 후 측정
SELECT source, COUNT(*) total,
       COUNT(*) FILTER (WHERE engine_matched_rule_id IS NOT NULL) filled,
       ROUND(100.0 * COUNT(*) FILTER (WHERE engine_matched_rule_id IS NOT NULL) / COUNT(*), 1) AS pct
FROM judgment_signals
WHERE source IN ('engine:live_l1','krx:daily')
  AND generated_at >= NOW() - INTERVAL '24 hours'
GROUP BY 1;

KPI: pct ≥ 80% (T3 GO MAIN 시그널은 100%, T1 WATCH 일부는 None 정상)
```

---

## §6. 트랙별 시그널 정의 (사용자 검수용)

### v1 엔진트리거 (단일 시그널)
```
judgment_signals 1 row = 1 시그널
  · source='engine:live_l1', symbol, timeframe, generated_at
  · entry/target/stop + direction
  · engine_action_gate (GO/WATCH/HOLD) + engine_c_state (FSM)
  · trigger_performance JOIN → PnL 추적
  · matched_rule_id ❌ (5/9 fix 대상)
```

### v2 파이프라인 (통합 시그널)
```
consumer_signal_snapshot 1 row = MTF 통합 시그널 1 건
  · symbol + 4h 기준 + asset_class='crypto'
  · final_decision (ENTER/WAIT/SKIP) ← mtf_signal_assembler
  · final_size_factor (0.0~1.0) → qty 계약
  · entry_price / target_t1 / target_t2 / stop_price (← trigger_performance)
  · scenario_category / scenario_label (12 카테고리)
  · trigger_kind / trigger_kind_gate (preassembly_snapshot 추출)
  · current_pnl_pct / status (open/closed)
```

### v3 게임이론 (게임 분류 시그널)
```
game_signal 1 row = 게임이론 분류 1 건
  · symbol + timeframe + trigger_performance_id
  · game_outcome: GAME_LOSE_REV (반전) | GAME_WIN_SAME (연속)
  · n_tests (BA test count)
  · signal_tier P1~P4 (P1=MTF+REVERSAL+GO 강력)
  · confidence 0~100 (compute_confidence 공식)
  · target / stop / mtf_score
  · exit_ts / exit_price (5min tracker UPDATE)
```

### KRX (한국주식 시그널)
```
consumer_signal_snapshot WHERE asset_class='krx' = KRX 시그널
  · symbol='*.KRX' + timeframe='1d'
  · 4 액션 매핑 (ADD/HOLD/REDUCE/EXIT) ← endpoint _portfolio_action()
  · entry/target/stop (judgment_signals 직접)
  · krx_daily_limit_proximity / lock_state
  · krx_foreign_streak (외인 = NULL until KIS API)
  · krx_dart_recency_days (160 종목만 채움)
  · krx_kospi200_rs_pct
```

---

## §7. KRX 가 v2 파이프라인을 사용하지 않는 이유

```
설계 결정:
  KRX 는 1d 단일 timeframe 운영 → MTF 통합 무의미
  → mtf_signal_assembler 호출 X
  → consumer_signal_builder 가 아닌 별도 KRXConsumerSignalBuilder
  → asset_class='krx' 격리 컬럼

이점:
  · v2 보호구역 4 파일 변경 0 (CLAUDE.md ⛔ 정합)
  · KRX 1d 만 처리 → 빌더 로직 단순
  · krx_context 7 컬럼 별도 enrich

비용:
  · MTF 정합 못 받음 (1d only — KRX 시장 특성상 무관)
  · qty 계약 (compute_qty) 가 KRX 측 별도 정의 필요 (Phase E)
```

---

## §8. 시급 정합 작업 (5/9 audit 발견 → 본선)

| # | 작업 | 시간 | 효과 | 영향 트랙 |
|---|---|---|---|---|
| **A3** ✅ | `evaluate_to_push_payload` 에 try_assemble wire | 5/9 land | matched_rule_id 0% → 80%+ (다음 cron 부터) | v1 + v2 + KRX 동시 |
| **A4** ✅ | KRXDailyScheduler 5/8 미발화 root — _loop catch-up 영구 가드 | 5/9 land | deploy 시점 cron 사이클 깨짐 영구 fix · 7 tests PASS | KRX |
| **A2** | KRX Telegram cutover (사용자 ENV) | 5min | dry → live | KRX L3 |
| **B-doc** | MAIN_TRACK_STATUS_WP6_TO_WP8 정합 (WP-6 production wire 5/9 완료 명시) | 15min | 내부 doc 정직 | (doc) |

---

## §9. 정합 검증 매트릭스 (5/9 land 후)

| 약속 (랜딩/스펙) | 실제 (DB/code) | 정합 |
|---|---|---|
| v2 통합 MTF 시그널 | mtf_signal_assembler ✅ 운영 | ✅ |
| Why? matched_rule_id 추적 | 0/2544 NULL | ❌ A3 wire 후 ✅ |
| v3 게임이론 별도 트랙 | game_signal table ✅ 운영 | ✅ |
| KRX 4 액션 매핑 | _portfolio_action() ✅ wired | ✅ |
| KRX MTF 통합 | 1d only — 미적용 (의도) | 🟡 설계 결정 |
| KRX 외인 컨텍스트 | krx_investor_flow_daily 0 rows | ❌ KIS Phase F |
| 보호구역 격리 | grep 검증 ✅ | ✅ |

---

## §10. 정본 인덱스 (관련 doc)

| doc | 역할 | 관계 |
|---|---|---|
| `DECKER_PLATFORM_ALIGNMENT_AND_DATAFLOW.md` | 전체 정렬 (큰그림) | 본 doc 의 상위 |
| `KRX_DATAFLOW_SPEC.md` | KRX L0~L4 단일 트랙 | 본 doc §6 KRX 행 확장 |
| `KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md` | KRX 베타 비즈니스 | 본 doc §7 KRX 사유 보강 |
| `SIGNAL_ASSEMBLY_TIER1_SPEC` | mtf_signal_assembler 정본 | §4.A |
| `WP6_TRIGGER_SPEC_LINKAGE_WORK_PLAN.md` | assemble_final_signal 정본 | §4.B |
| `MAIN_TRACK_STATUS_WP6_TO_WP8.md` | WP-6 진행 표시 | §8 B-doc 정합 대상 |
| `CLAUDE.md` ⛔ v2 보호구역 | 보호 정책 | §2 표 정합 |

---

## §11. 다음 세션 진입 protocol

```
1. 본 doc §0 TL;DR + §3 ASCII flow + §8 시급 작업 5분 정독
2. A3 본선 진입 시:
     · evaluate_to_push_payload.py 단일 파일 수정
     · 단위테스트 + crypto+KRX 둘 다 회귀 검증 24h
3. A4 본선 진입 시:
     · Railway historical 로그 5/8 16:30 KST grep
     · KRXDailyScheduler._loop 시간 정합 + ENV 추적
4. doc 갱신 시:
     · MAIN_TRACK_STATUS_WP6_TO_WP8 §1.1 "production wire 미완" 추가
     · 본 doc §8 ✅ 마킹
```

---

**문서 버전**: v1.0 — 2026-05-09
**진입 사유**: matched_rule_id audit 중 v2 파이프라인 vs admin 두 path 발견 → 사용자 가이드로 4 트랙 정합
**소유**: Decker AI · 4 트랙 통합 정본
