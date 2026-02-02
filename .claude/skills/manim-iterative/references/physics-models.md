# 물리 모델

## 스프링 충돌 모델

연속적이고 물리적으로 자연스러운 충돌을 표현한다. F-t가 0에서 시작하고 0으로 끝나며, 적분이 충격량과 정확히 일치한다.

### 수학

- `u = τ/Δt` (정규화된 충돌 시간, 0→1)
- **힘**: `F(τ) = 12I/Δt · u(1-u)²` — peak at `u = 1/3`
- **속도**: `v(τ) = v₀(1 - 6u² + 8u³ - 3u⁴)` — v₀에서 0으로 감소
- **변형**: `deform(τ) = 6u² - 8u³ + 3u⁴` — 0→1 단조증가
- **최대힘**: `F_peak = 48I/(27Δt)`
- **평균힘**: `F_avg = I/Δt`

### 코드

```python
def _f_spring(self, tau, dt):
    """힘 모델: tau=0~dt 구간에서만 비영, 경계에서 정확히 0"""
    if tau <= 0 or tau >= dt:
        return 0.0
    u = tau / dt
    return 12 * self.IMPULSE / dt * u * (1 - u) ** 2

def _v_spring(self, tau, dt):
    """속도: v₀에서 0으로 연속 감소"""
    if tau <= 0:
        return self.V_IMPACT
    if tau >= dt:
        return 0.0
    u = tau / dt
    return self.V_IMPACT * (1 - 6 * u**2 + 8 * u**3 - 3 * u**4)

def _deform_frac(self, tau, dt):
    """변형 비율: 0→1 단조증가"""
    if tau <= 0:
        return 0.0
    if tau >= dt:
        return 1.0
    u = tau / dt
    return 6 * u**2 - 8 * u**3 + 3 * u**4

def _F_peak(self, dt):
    return 48 * self.IMPULSE / (27 * dt)

def _F_avg(self, dt):
    return self.IMPULSE / dt
```

### 검증 포인트
- `∫₀^Δt F(τ)dτ = I` (충격량 보존)
- `v(0) = v₀`, `v(Δt) = 0`
- `F(0) = 0`, `F(Δt) = 0`
- `deform(0) = 0`, `deform(Δt) = 1`

---

## 바닥 변형 (가우시안 프로파일)

충돌 시 바닥이 충돌 지점 중심으로 오목하게 들어가는 시각 효과.

```python
def get_deformed_floor():
    d = deform_frac(coll_tracker.get_value(), delta_t) * max_deform
    if d > 0.001:
        n = 30
        pts = []
        for i in range(n + 1):
            frac = i / n
            x = floor_left_x + frac * floor_width
            dist = (x - impact_x) / (floor_width * 0.3)
            pts.append([x, floor_top_y - d * np.exp(-dist**2), 0])
        pts.append([floor_left_x + floor_width, floor_bottom_y, 0])
        pts.append([floor_left_x, floor_bottom_y, 0])
        return Polygon(*[np.array(p) for p in pts],
                       color=floor_color, fill_opacity=0.8, stroke_width=2)
    # 변형 없으면 직사각형
    r = Rectangle(width=floor_width, height=0.3, ...)
    r.move_to([impact_x, floor_y, 0])
    return r
```

### 파라미터
- `max_deform`: 최대 변형량 (딱딱=0.08, 부드러움=0.2)
- `floor_width * 0.3`: 가우시안 폭 (작을수록 국소적)

---

## 등속/등가속도 운동학

### 등속 운동
- `s(t) = v₀ · t`
- v-t: 수평선, s-t: 직선

### 등가속도 운동
- `v(t) = v₀ + at`
- `s(t) = v₀t + ½at²`
- v-t: 직선 (기울기=a), s-t: 포물선

### 코드 패턴

```python
total_time = 5
a = 2  # 가속도
v_0 = 5  # 초기속도

time_tracker = ValueTracker(0)

def update_obj(m):
    t = time_tracker.get_value()
    s = v_0 * t + 0.5 * a * t ** 2
    x_ratio = s / total_distance
    new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
    m.move_to([new_x, y_pos, 0])

obj.add_updater(update_obj)
self.play(time_tracker.animate.set_value(total_time),
          run_time=7.5, rate_func=linear)
obj.remove_updater(update_obj)
```

---

## 충돌 운동학 (탄성/비탄성)

### 완전 탄성 충돌 (같은 질량)
- `v_A' = 0`, `v_B' = v_A`

### 탄성 충돌 (다른 질량)
- `v_A' = (m_A - m_B)/(m_A + m_B) · v_A`
- `v_B' = 2m_A/(m_A + m_B) · v_A`

### 완전 비탄성 충돌
- `v' = (m_A · v_A)/(m_A + m_B)` — 합체

### smooth_step 전환

충돌 전후의 급격한 변화를 매끄럽게 표현:

```python
def smooth_step(t, t0, width=0.15):
    return 1 / (1 + np.exp(-(t - t0) / (width / 4)))

def p_a_func(t):
    s = smooth_step(t, collision_t)
    return p_before * (1 - s) + p_after * s
```
