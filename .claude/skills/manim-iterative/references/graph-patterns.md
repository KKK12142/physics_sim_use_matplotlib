# 그래프 패턴

## 이중 축 설정 (v-t 위, F-t 아래)

```python
graph_cx = -0.8
t_graph_end = t_coll_end + 0.3
ft_y_max = F_peak * 1.2  # peak × 1.2 여유
ft_y_step = max(round(ft_y_max / 4, -1), 10)

vt_axes = Axes(
    x_range=[0, t_graph_end, 0.5], y_range=[0, 12, 2],
    x_length=3.5, y_length=2.2,
    axis_config={"include_tip": False, "font_size": 20},
    x_axis_config={"numbers_to_include": [0.5, 1.0]},
    y_axis_config={"numbers_to_include": [V_IMPACT]},  # 핵심 물리값만
).move_to([graph_cx, 1.5, 0])

ft_axes = Axes(
    x_range=[0, t_graph_end, 0.5], y_range=[0, ft_y_max, ft_y_step],
    x_length=3.5, y_length=2.2,
    axis_config={"include_tip": False, "font_size": 20},
    x_axis_config={"numbers_to_include": [0.5, 1.0]},
    y_axis_config={"numbers_to_include": [round(F_peak)]},
).move_to([graph_cx, -1.8, 0])
```

### 축 라벨

```python
vt_xl = Text("t (s)", font_size=14).next_to(vt_axes.x_axis, RIGHT, buff=0.1)
vt_yl = Text("v (m/s)", font_size=14).next_to(vt_axes.y_axis, UP, buff=0.1)
```

---

## 좌하/우하 배치 (충격량과운동량.py, 등가속도운동.py)

```python
ft_axes = Axes(...).to_corner(DL, buff=0.8)
vt_axes = Axes(...).to_corner(DR, buff=0.8)
```

---

## 충돌 종료 커스텀 틱

표준 눈금에 없는 충돌 종료 시각을 수동으로 추가:

```python
te_tick = Line(
    axes.c2p(t_coll_end, 0) + UP * 0.08,
    axes.c2p(t_coll_end, 0) + DOWN * 0.08,
    color=WHITE, stroke_width=2
)
te_num = MathTex(rf"{t_coll_end:.1f}", font_size=16, color=WHITE)
te_num.next_to(axes.c2p(t_coll_end, 0), DOWN, buff=0.15)
```

---

## 점선 참조선 (y축→점, x축→점)

특정 좌표값을 축에서 점까지 연결하는 보조선:

```python
# 수평 점선 (y축 → 점)
h_dash = DashedLine(
    axes.c2p(0, y_val), axes.c2p(x_val, y_val),
    color=GRAY, stroke_width=1.5, dash_length=0.08
)
# 수직 점선 (x축 → 점)
v_dash = DashedLine(
    axes.c2p(x_val, 0), axes.c2p(x_val, y_val),
    color=GRAY, stroke_width=1.5, dash_length=0.08
)
dot = Dot(axes.c2p(x_val, y_val), color=RED, radius=0.06)

self.play(Create(h_dash), Create(v_dash), FadeIn(dot), run_time=0.5)
```

---

## F-t 면적 (충격량)

### axes.get_area() — plot 객체 전달

**중요**: `get_area()`에는 함수가 아닌 **plot으로 생성한 곡선 객체**를 전달해야 한다.

```python
# 먼저 곡선 객체 생성
ft_pulse = ft_axes.plot(
    lambda t: f_spring(t - t0, delta_t),
    x_range=[t0, t_coll_end, 0.002], color=RED, stroke_width=3
)

# 곡선 객체를 전달하여 면적 생성
area_ft = ft_axes.get_area(ft_pulse, x_range=[t0, t_coll_end],
                            color=RED, opacity=0.3)
self.play(FadeIn(area_ft))
```

### Polygon으로 직접 면적 (직사각형 등)

```python
area = Polygon(
    axes.c2p(t_start, 0), axes.c2p(t_start, F_val),
    axes.c2p(t_end, F_val), axes.c2p(t_end, 0),
    color=RED, fill_opacity=0.4, stroke_width=1,
)
```

---

## 평균힘 수평선 + 라벨

```python
avg_line = DashedLine(
    ft_axes.c2p(0, F_avg), ft_axes.c2p(t_coll_end, F_avg),
    color=ORANGE, stroke_width=2.5, dash_length=0.1
)
avg_txt = Text("평균힘", font_size=16, color=ORANGE)
avg_txt.next_to(ft_axes.c2p(0, F_avg), LEFT, buff=0.15)
avg_val = MathTex(rf"\bar{{F}} = {F_avg:.0f}" + r"\text{ N}",
                  font_size=18, color=ORANGE)
avg_val.next_to(avg_line, UP, buff=0.08)

# 평균힘 직사각형 영역 (반투명)
avg_rect = Polygon(
    ft_axes.c2p(t0, 0), ft_axes.c2p(t0, F_avg),
    ft_axes.c2p(t_coll_end, F_avg), ft_axes.c2p(t_coll_end, 0),
    color=ORANGE, fill_opacity=0.15, stroke_width=1.5, stroke_color=ORANGE,
)
```

---

## 비교 오버레이 (두 실험 동일 축)

```python
comp_axes = Axes(
    x_range=[0, 0.55, 0.1],
    y_range=[0, F_peak_A * 1.15, 50],
    x_length=5.5, y_length=4.5,
    axis_config={"include_tip": False, "font_size": 16, "include_numbers": False},
).move_to([2.5, 0, 0])

# 두 곡선을 같은 축에 그리기
curve_a = comp_axes.plot(lambda t: f_spring(t, dt_a),
                         x_range=[0, dt_a, 0.001], color=RED, stroke_width=3)
curve_b = comp_axes.plot(lambda t: f_spring(t, dt_b),
                         x_range=[0, dt_b, 0.001], color=TEAL, stroke_width=3)

# 곡선 라벨
cl_a = Text("A", font_size=20, color=RED).next_to(curve_a.get_top(), UR, buff=0.1)
cl_b = Text("B", font_size=20, color=TEAL).next_to(curve_b.get_right(), RIGHT, buff=0.1)
```

### 같은 충격량 강조

```python
area_a = comp_axes.get_area(curve_a, x_range=[0, dt_a], color=RED, opacity=0.35)
area_b = comp_axes.get_area(curve_b, x_range=[0, dt_b], color=TEAL, opacity=0.35)

same_grp = VGroup(
    MathTex(r"S_A", color=RED), MathTex(r"=", color=YELLOW),
    MathTex(r"S_B", color=TEAL), MathTex(r"= 19.6 \text{ N·s}", color=YELLOW),
).arrange(RIGHT, buff=0.15)
```

---

## 차이 화살표 (힘 배수, 시간 배수)

```python
# 수직 차이 (힘)
f_arrow = DoubleArrow(
    [mid_x, axes.c2p(0, F_avg_b)[1], 0],
    [mid_x, axes.c2p(0, F_avg_a)[1], 0],
    color=YELLOW, buff=0, stroke_width=3, tip_length=0.15,
)
f_diff = Text("힘 4배", font_size=16, color=YELLOW).next_to(f_arrow, RIGHT, buff=0.1)

# 수평 차이 (시간)
t_arrow = DoubleArrow(
    [axes.c2p(dt_a, 0)[0], bot_y, 0],
    [axes.c2p(dt_b, 0)[0], bot_y, 0],
    color=YELLOW, buff=0, stroke_width=3, tip_length=0.15,
)
t_diff = Text("시간 4배", font_size=16, color=YELLOW).next_to(t_arrow, DOWN, buff=0.1)
```

---

## 동적 면적 (v-t 적분 시각화)

```python
t_integral = ValueTracker(0.01)

def get_area():
    t_val = t_integral.get_value()
    if t_val < 0.01:
        return VGroup()
    return axes_vt.get_area(vt_graph, x_range=[0, t_val], color=BLUE, opacity=0.4)

area_fill = always_redraw(get_area)
self.add(area_fill)

# 1초마다 면적 값 표시
self.play(t_integral.animate.set_value(t), run_time=1.5, rate_func=linear)
```
