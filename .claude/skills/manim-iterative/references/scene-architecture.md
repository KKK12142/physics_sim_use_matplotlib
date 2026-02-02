# 씬 구조 패턴

## construct() → phase 메서드 패턴

```python
class ImpulseMomentum2(Scene):
    # ── 클래스 상수 ──
    MASS = 2
    G = 9.8
    T_FALL = 1.0
    V_IMPACT = 9.8       # = G * T_FALL
    IMPULSE = 19.6        # = MASS * V_IMPACT

    def construct(self):
        # 실험 파라미터 사전 계산
        self.exp_a = self._make_experiment(
            label="실험 A (딱딱한 바닥)", delta_t=0.1,
            max_deform=0.08, floor_color=GRAY_BROWN,
        )
        self.exp_b = self._make_experiment(
            label="실험 B (부드러운 바닥)", delta_t=0.4,
            max_deform=0.2, floor_color=TEAL,
        )

        self.intro()
        self.clear_screen()
        self.derivation()
        self.clear_screen()
        self.sim_hard_floor()
        self.clear_screen()
        self.sim_soft_floor()
        self.clear_screen()
        self.comparison()
        self.clear_screen()
        self.outro()
```

## clear_screen() 헬퍼

```python
def clear_screen(self):
    self.play(*[FadeOut(m) for m in self.mobjects])
    self.wait(0.5)
```

---

## `_make_experiment()` 딕셔너리 패턴 (핵심)

초기조건에서 실험에 필요한 모든 물리량을 **한번만** 계산하여 딕셔너리로 반환한다.
이후 시뮬레이션 코드에서는 `exp["F_peak"]` 등으로 참조만 한다.

```python
def _make_experiment(self, label, delta_t, max_deform, floor_color):
    """초기조건으로부터 실험에 필요한 모든 물리량을 한번에 계산"""
    return dict(
        label=label,
        delta_t=delta_t,
        max_deform=max_deform,
        floor_color=floor_color,
        F_peak=self._F_peak(delta_t),
        F_avg=self._F_avg(delta_t),
        t_coll_end=self.T_FALL + delta_t,
    )
```

### 장점
- 파라미터 변경 시 한 곳만 수정
- 물리적 일관성 보장 (도출량이 자동으로 갱신)
- 여러 실험 비교 시 동일한 구조로 접근

### 사용 패턴

```python
def _run_fall_sim(self, exp):
    exp_label = exp["label"]
    floor_color = exp["floor_color"]
    delta_t = exp["delta_t"]
    F_peak = exp["F_peak"]
    F_avg = exp["F_avg"]
    t_coll_end = exp["t_coll_end"]
    # ... 시뮬레이션 코드에서 직접 사용
```

---

## 레이아웃 그리드

### 시뮬레이션 + 이중 그래프 (운동량과충격량2.py)

```
┌─────────────────────────────────────────┐
│  exp_title (상단 중앙)                    │
├──────────┬──────────────┬───────────────┤
│ 물체+바닥  │  v-t 그래프    │  계산 수식     │
│ (x=-5)   │  (cx=-0.8)   │  (x=4.5)     │
│          │  y: 1.5       │  y: 2.5      │
│          ├──────────────┤              │
│          │  F-t 그래프    │              │
│          │  y: -1.8      │  y: -0.8     │
└──────────┴──────────────┴───────────────┘
```

### 트랙 + 이중 그래프 (등가속도운동.py, 충격량과운동량.py)

```
┌─────────────────────────────────────────┐
│  title (상단)                             │
├─────────────────────────────────────────┤
│  트랙 (UP * 1.5, 좌-6 ~ 우+6)            │
│  + 눈금 + 물체                            │
├──────────────────┬──────────────────────┤
│  v-t / F-t 그래프  │  s-t / 계산 영역      │
│  (DL corner)     │  (DR corner)         │
└──────────────────┴──────────────────────┘
```

### 비교 씬 (두 실험 오버레이)

```
┌──────────┬──────────────────────────────┐
│ 미니 셋업  │  오버레이 F-t 그래프            │
│  실험 A    │  (comp_axes, cx=2.5)         │
│  실험 B    │  곡선 A (RED) + 곡선 B (TEAL) │
│ (x=-5)   │  + 평균힘 점선 + 면적           │
└──────────┴──────────────────────────────┘
```

---

## 트랙 + 눈금 생성 패턴

```python
track_start = LEFT * 6
track_end = RIGHT * 6
track = Line(track_start, track_end, color=WHITE, stroke_width=3)
track.shift(UP * 1.5)

tick_marks = VGroup()
tick_labels = VGroup()
total_m = 50  # 트랙 전체 미터

for i in range(total_m + 1):
    x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / total_m)
    tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
    tick.move_to([x_pos, track.get_center()[1], 0])
    tick_marks.add(tick)
    if i % 5 == 0:
        label = Text(str(i), font_size=16, color=GRAY)
        label.next_to(tick, DOWN, buff=0.15)
        tick_labels.add(label)

# 좌표 변환 헬퍼
track_len = track_end[0] - track_start[0]
def m2x(m):
    return track_start[0] + track_len * (m / total_m)
```
