# 애니메이션 레시피

## 자유낙하

`ease_in_quad`로 가속 효과 + ValueTracker로 속도 라벨 동시 업데이트:

```python
fall_dist = obj_start_y - obj_land_y
v_tracker = ValueTracker(0)

v_label = always_redraw(lambda: MathTex(
    rf"v = {v_tracker.get_value():.1f}", font_size=20, color=GREEN,
).next_to(ball, RIGHT, buff=0.15))

# v-t, F-t 곡선도 동시 생성
vt_fall = vt_axes.plot(lambda t: G * t, x_range=[0, T_FALL], color=GREEN, stroke_width=3)
ft_fall = ft_axes.plot(lambda t: 0, x_range=[0, T_FALL], color=WHITE, stroke_width=3)

self.play(
    ball.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_dist),
    ball_label.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_dist),
    v_tracker.animate.set_value(V_IMPACT),
    Create(vt_fall), Create(ft_fall),
    run_time=2, rate_func=linear,
)
```

### 주의
- `ball.animate`에 개별 `rate_func`를 지정하고, 전체 `self.play`에는 `rate_func=linear` 사용
- 이렇게 하면 공은 가속하며 떨어지고, ValueTracker는 선형으로 증가

---

## 충돌 (always_redraw 바닥 변형 + 공 위치 updater)

```python
coll_tracker = ValueTracker(0)

# 바닥: always_redraw로 매 프레임 재생성
def_floor = always_redraw(get_deformed_floor)  # physics-models.md 참고

# 공 위치: add_updater
def upd_ball(b):
    d = deform_frac(coll_tracker.get_value(), delta_t) * max_deform
    b.move_to([obj_x, obj_land_y - d, 0])

ball.add_updater(upd_ball)

# 바닥 교체
self.play(FadeOut(floor_rect), FadeIn(def_floor), run_time=0.1)

# 충돌 진행 + 그래프 동시 그리기
self.play(
    coll_tracker.animate.set_value(delta_t),
    p_tracker.animate.set_value(0),
    Create(vt_coll), Create(ft_pulse),
    run_time=1.0, rate_func=linear,
)

# ── 후처리 (필수!) ──
ball.clear_updaters()
ball.move_to([obj_x, obj_land_y - max_deform, 0])  # 최종 위치 고정
```

---

## Growing Curve (실시간 확장되는 곡선)

`always_redraw`로 ValueTracker 값까지만 그린 곡선을 매 프레임 재생성:

```python
ct = ValueTracker(0)

def mk_growing_curve():
    te = min(ct.get_value(), dt)
    if te < 0.003:
        return VGroup()  # 너무 짧으면 빈 그룹
    return axes.plot(lambda s: f_spring(s, dt),
                     x_range=[0, te, 0.002], color=RED, stroke_width=3)

gc = always_redraw(mk_growing_curve)
self.add(gc)  # add로 추가 (FadeIn 아님!)

self.play(ct.animate.set_value(dt), run_time=2.5, rate_func=linear)

# ── 후처리: 정적 곡선으로 교체 ──
self.remove(gc)
static_curve = axes.plot(lambda s: f_spring(s, dt),
                         x_range=[0, dt, 0.001], color=RED, stroke_width=3)
self.add(static_curve)
```

### 핵심 포인트
- `self.add(gc)` 사용 (FadeIn/Create 아님)
- 후처리에서 `self.remove(gc)` → 정적 곡선 `self.add(static_curve)`
- x_range 하한 체크 (`te < 0.003`이면 빈 VGroup 반환)

---

## ValueTracker + updater 기반 시뮬레이션 (운동량보존.py)

```python
time_tracker = ValueTracker(0)

def pos_a(t):
    if t <= collision_t:
        return start_a_x + v_a * scale_v * t
    return start_a_x + v_a * scale_v * collision_t + v_a_after * scale_v * (t - collision_t)

box_a.add_updater(lambda m: m.move_to([pos_a(time_tracker.get_value()), y_a, 0]))
label_a.add_updater(lambda m: m.move_to(box_a))
mass_a.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))

# 동적 속도 화살표
vel_arrow_dyn = always_redraw(lambda: Arrow(
    start=box_a.get_right(), end=box_a.get_right() + RIGHT * 0.8,
    color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
) if time_tracker.get_value() < collision_t else VMobject())

# p-t growing curve
pt_line_a = always_redraw(lambda: axes_pt.plot(
    p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
    color=BLUE, stroke_width=3
) if time_tracker.get_value() > 0.01 else VMobject())

self.add(vel_arrow_dyn, pt_line_a)

# 애니메이션 실행
self.play(time_tracker.animate.set_value(collision_t),
          run_time=collision_t * 0.8, rate_func=linear)

# 충돌 이펙트
self.play(Flash(box_a.get_right(), color=YELLOW, flash_radius=0.5))

# 충돌 후
self.play(time_tracker.animate.set_value(sim_total),
          run_time=(sim_total - collision_t) * 0.8, rate_func=linear)

# ── 후처리 ──
box_a.clear_updaters()
box_b.clear_updaters()
label_a.clear_updaters()
mass_a.clear_updaters()
self.remove(vel_arrow_dyn, pt_line_a)

# 정적 그래프로 교체
final_pt_a = axes_pt.plot(p_a_func, x_range=[0, sim_total], color=BLUE, stroke_width=3)
self.add(final_pt_a)
```

---

## 순차 수식 표시

```python
calc_grp = VGroup(
    MathTex(r"p = mv", font_size=36, color=WHITE),
    MathTex(r"= 2 \times 9.8", font_size=36, color=WHITE),
    MathTex(r"= 19.6 \text{ kg·m/s}", font_size=36, color=YELLOW),
).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([calc_x, 2.5, 0])

for line in calc_grp:
    self.play(Write(line), run_time=0.5)

# 결과 강조
rbox = SurroundingRectangle(calc_grp[-1], color=YELLOW, buff=0.15,
                             corner_radius=0.1, stroke_width=2)
self.play(Create(rbox))
```

---

## 수식 변환 (TransformMatchingTex)

```python
from manim import TransformMatchingTex

eq1 = MathTex("F", "=", "m", "a", font_size=80)
self.play(Write(eq1))

eq2 = MathTex("F", "=", "m", r"\times", r"\frac{\Delta v}{\Delta t}", font_size=80)
self.play(TransformMatchingTex(eq1, eq2))

# 부분 강조
self.play(Indicate(eq2[2], color=RED))
```

---

## 잔상(Ghost) 효과

시간 간격마다 반투명 복사본을 남겨 궤적을 시각화:

```python
ghost_group = VGroup()
self.add(ghost_group)

time_tracker.last_int_t = 0

def update_obj(m):
    t = time_tracker.get_value()
    # ... 위치 계산 ...
    current_int_t = int(t)
    if current_int_t > time_tracker.last_int_t:
        ghost = Square(side_length=obj_size, color=BLUE,
                       fill_opacity=0.3, stroke_width=0)
        ghost.move_to(m.get_center())
        ghost_group.add(ghost)
        time_tracker.last_int_t = current_int_t

obj.add_updater(update_obj)
```

---

## 비탄성 충돌 합체 처리

```python
# 충돌 후 B를 A 옆에 붙이기
box_b.clear_updaters()
self.play(box_b.animate.next_to(box_a, RIGHT, buff=0), run_time=0.3)

# 합체 질량 라벨
merged_label = MathTex("2\\,\\text{kg}", font_size=18, color=PURPLE)
merged_label.add_updater(lambda m: m.next_to(VGroup(box_a, box_b), UP, buff=0.1))

# 합체 속도 화살표
merged_vel = always_redraw(lambda: Arrow(
    start=box_b.get_right(), end=box_b.get_right() + RIGHT * 0.4,
    color=PURPLE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
))

# B가 A를 따라가도록
box_b.add_updater(lambda m: m.next_to(box_a, RIGHT, buff=0))
```

---

## 후처리 체크리스트

모든 동적 애니메이션 후 반드시 수행:

1. `obj.clear_updaters()` — 모든 관련 객체
2. 위치 고정: `obj.move_to([final_x, final_y, 0])`
3. `self.remove(dynamic_obj)` — always_redraw 객체 제거
4. `self.add(static_obj)` — 정적 교체 객체 추가
5. `FadeOut(labels)` — 동적 라벨 제거
