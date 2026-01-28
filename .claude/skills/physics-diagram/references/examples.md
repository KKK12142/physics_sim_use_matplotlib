# Physics Diagram 예시 모음

## 1. 바닥 위 물체 - 자유물체도

```python
fig, ax = plt.subplots(figsize=(8, 6))
clean_ax(ax, (-1, 7), (-1, 5))

ground = Ground(ax, y=0, xlim=(-1, 7))
box = Box(ax, size=(1.5, 1), on=ground, t=0.5, label='m', color='lightblue')

arrow(ax, box.center, box.center + (0, -1.5), RED, label=r'$m\vec{g}$')
arrow(ax, box.center, box.center + (0, 1.5), BLUE, label=r'$\vec{N}$')
arrow(ax, box.center, box.center + (2, 0), GREEN, label=r'$\vec{F}$')
arrow(ax, box.center, box.center + (-1, 0), ORANGE, label=r'$\vec{f}$')
```

## 2. 경사면 위 물체 - 힘 분해

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-1, 8), (-1, 5))

incline = Incline(ax, origin=(0, 0), width=6, height=3, direction='-', color='#d4a574')
box = Box(ax, size=(1, 0.6), on=incline, t=0.5, label='m', color='lightblue')

mg = 1.5
arrow(ax, box.center, box.center + (0, -mg), RED, label=r'$m\vec{g}$')

N_mag = mg * np.cos(incline.angle_rad)
N = box.surface_normal * N_mag
arrow(ax, box.center, box.center + N, BLUE, label=r'$\vec{N}$')

f = box.surface_tangent * 0.5
arrow(ax, box.center, box.center + f, ORANGE, label=r'$\vec{f}$')

coord_axes(ax, box.bottom, length=1.2, angle=incline.angle_deg)
```

## 3. 테이블 + 양쪽 도르래 시스템

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-2, 10), (-2, 6))

table = Table(ax, x=1, y=2, width=6, height=0.3)
box = Box(ax, size=(1.2, 0.8), on=table, t=0.5, label='m', color='lightblue')

p_left = Pulley(ax, on=table, t=0, for_obj=box)
p_right = Pulley(ax, on=table, t=1, for_obj=box)

box_left = Box(ax, x=p_left.bottom.x, y=0.8, size=(0.6, 0.8), label=r'$M_1$', color='orange')
box_right = Box(ax, x=p_right.bottom.x, y=0.5, size=(0.6, 0.8), label=r'$M_2$', color='green')

Rope(ax, box.left, p_left.right)
Rope(ax, p_left.bottom, box_left.top)
Rope(ax, box.right, p_right.left)
Rope(ax, p_right.bottom, box_right.top)
```

## 4. 경사면 + 도르래 (direction='-')

왼쪽이 높은 경사면 → 도르래 `t=0`, 연결: `box.left ↔ pulley.right`

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-2, 10), (-1, 6))

incline = Incline(ax, origin=(0, 0), width=6, height=3, direction='-', color='#d4a574')
box = Box(ax, size=(1, 0.6), on=incline, t=0.5, label=r'$m_1$', color='lightblue')

pulley = Pulley(ax, on=incline, t=0, for_obj=box)
hanging = Box(ax, x=pulley.bottom.x, y=0.5, size=(0.5, 0.8), label=r'$m_2$', color='orange')

Rope(ax, box.left, pulley.right)
Rope(ax, pulley.bottom, hanging.top)

# 힘 다이어그램
mg1 = 1.2
arrow(ax, box.center, box.center + (0, -mg1), RED, label=r'$m_1\vec{g}$')
N1 = box.surface_normal * (mg1 * np.cos(incline.angle_rad))
arrow(ax, box.center, box.center + N1, BLUE, label=r'$\vec{N}$')
T1 = box.surface_tangent * (-0.8)  # 음수: 경사면 위쪽(왼쪽)
arrow(ax, box.center, box.center + T1, PURPLE, label=r'$\vec{T}$')
```

## 5. 경사면 + 도르래 (direction='+')

오른쪽이 높은 경사면 → 도르래 `t=1`, 연결: `box.right ↔ pulley.left`

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-2, 10), (-1, 6))

incline = Incline(ax, origin=(0, 0), width=6, height=3, direction='+', color='#d4a574')
box = Box(ax, size=(1, 0.6), on=incline, t=0.5, label=r'$m_1$', color='lightblue')

pulley = Pulley(ax, on=incline, t=1, for_obj=box)
hanging = Box(ax, x=pulley.bottom.x, y=0.5, size=(0.5, 0.8), label=r'$m_2$', color='orange')

Rope(ax, box.right, pulley.left)
Rope(ax, pulley.bottom, hanging.top)

T = box.surface_tangent * 0.8  # 양수: 경사면 위쪽(오른쪽)
arrow(ax, box.center, box.center + T, PURPLE, label=r'$\vec{T}$')
```

## 6. 천장에 매달린 물체

```python
fig, ax = plt.subplots(figsize=(6, 6))
clean_ax(ax, (-2, 4), (-1, 5))

ceiling = Ceiling(ax, y=4, xlim=(-1, 3))
box = Box(ax, x=1, y=2, size=(1, 0.8), label='m', color='lightblue')

Rope(ax, (1, 4), box.top)

arrow(ax, box.center, box.center + (0, -1.2), RED, label=r'$m\vec{g}$')
arrow(ax, box.center, box.center + (0, 1.2), BLUE, label=r'$\vec{T}$')
```

## 7. 원형 물체 (구르는 물체)

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-1, 8), (-1, 5))

incline = Incline(ax, origin=(0, 0), width=6, height=3, direction='-', color='#d4a574')
circle = Circle(ax, radius=0.4, on=incline, t=0.5, label='m', color='lightgreen')

arrow(ax, circle.center, circle.center + (0, -1), RED, label=r'$m\vec{g}$')
N = circle.surface_normal * 0.8
arrow(ax, circle.center, circle.center + N, BLUE, label=r'$\vec{N}$')

# 마찰력 (바닥 접점)
f = circle.surface_tangent * 0.3
arrow(ax, circle.bottom, circle.bottom + f, ORANGE, label=r'$\vec{f}$')
```

## 8. 질점에 여러 힘

```python
fig, ax = plt.subplots(figsize=(8, 8))
clean_ax(ax, (-3, 3), (-3, 3))

mass_point = MassPoint(ax, x=0, y=0)

arrow(ax, (0, 0), (2, 0), RED, label=r'$\vec{F}_1$')
arrow(ax, (0, 0), (1, 1.7), BLUE, label=r'$\vec{F}_2$')
arrow(ax, (0, 0), (-1.5, 0.8), GREEN, label=r'$\vec{F}_3$')
arrow(ax, (0, 0), (0, -1.5), ORANGE, label=r'$\vec{F}_4$')

coord_axes(ax, (-2.5, -2.5), length=1, labels=('x', 'y'))
```

## 9. 토크 방향 표시

```python
fig, ax = plt.subplots(figsize=(8, 6))
clean_ax(ax, (-1, 7), (-1, 5))

ground = Ground(ax, y=0, xlim=(-1, 7))
box = Box(ax, size=(3, 0.3), on=ground, t=0.5, color='#8B4513')

pivot = MassPoint(ax, x=3, y=0.3, size=8)

arrow(ax, (1.5, 0.3), (1.5, 1.5), RED, label=r'$\vec{F}_1$')
arrow(ax, (4.5, 0.3), (4.5, -1), BLUE, label=r'$\vec{F}_2$')

TorqueSymbol(ax, x=3, y=2, radius=0.3, direction='out', color=PURPLE)
ax.text(3.5, 2, r'$\tau$ (반시계)', fontsize=11, color=PURPLE)

TorqueSymbol(ax, x=3, y=3, radius=0.3, direction='in', color=ORANGE)
ax.text(3.5, 3, r'$\tau$ (시계)', fontsize=11, color=ORANGE)
```

## 10. 바닥 위 연결된 두 물체

```python
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-1, 10), (-1, 5))

ground = Ground(ax, y=0, xlim=(-1, 10))

boxA = Box(ax, size=(1.2, 0.8), on=ground, t=0.25, label=r'$m_1$', color='lightblue')
boxB = Box(ax, size=(1.2, 0.8), on=ground, t=0.55, label=r'$m_2$', color='orange')

Rope(ax, boxA.right, boxB.left)

arrow(ax, boxA.left, boxA.left + (-1.5, 0), GREEN, label=r'$\vec{F}$')
```

## 11. 양쪽 경사면 + 매달린 물체 (3물체)

```python
fig, ax = plt.subplots(figsize=(14, 7))
clean_ax(ax, (-2, 14), (-2, 7))

incl_left = Incline(ax, origin=(0, 0), width=5, height=3, direction='+')
incl_right = Incline(ax, origin=(7, 0), width=5, height=3, direction='-')

box_A = Box(ax, size=(0.8, 0.5), on=incl_left, t=0.5, label=r'$m_1$', color='lightblue')
box_B = Box(ax, size=(0.8, 0.5), on=incl_right, t=0.5, label=r'$m_2$', color='orange')

# + → t=1, - → t=0
pulley_left = Pulley(ax, on=incl_left, t=1, for_obj=box_A)
pulley_right = Pulley(ax, on=incl_right, t=0, for_obj=box_B)

hanging = Box(ax, x=6, y=1.5, size=(0.6, 0.8), label=r'$m_3$', color='lightgreen')

Rope(ax, box_A.right, pulley_left.left)
Rope(ax, pulley_left.bottom, hanging.top)
Rope(ax, hanging.top, pulley_right.bottom)
Rope(ax, pulley_right.right, box_B.left)
```

## 12. 천장 도르래 시스템 (판 + 추)

```python
fig, ax = plt.subplots(figsize=(10, 8))
clean_ax(ax, (-1, 10), (-1, 8))

ceiling = Ceiling(ax, y=7, xlim=(0, 9), depth=0.3)
ground = Ground(ax, y=0, xlim=(-1, 10))

pulley_left = Pulley(ax, on=ceiling, t=0.28, radius=0.35)
pulley_right = Pulley(ax, on=ceiling, t=0.78, radius=0.35)

plate = Box(ax, x=pulley_left.center.x, y=3.5, size=(2.5, 0.25), label='판', color='#d4d4d4')

boxA = Box(ax, size=(0.6, 0.5), on=plate, t=0.25, label='A', color='lightblue')
boxB = Box(ax, size=(0.6, 0.5), on=plate, t=0.75, label='B', color='lightgreen')

weight = Box(ax, x=pulley_right.bottom.x, y=2, size=(0.8, 1), label='추', color='#a0a0a0')

# p: 판 → 왼쪽 도르래
Rope(ax, plate.top, pulley_left.bottom)
# q: 바닥 → 판
Rope(ax, (plate.bottom.x, 0), plate.bottom)
# 도르래 사이
Rope(ax, pulley_left.right, pulley_right.left, horizontal=True)
# 오른쪽 도르래 → 추
Rope(ax, pulley_right.bottom, weight.top)

ax.text(plate.top.x - 0.3, (plate.top.y + pulley_left.bottom.y) / 2, 'p', fontsize=11)
ax.text(plate.bottom.x + 0.3, plate.bottom.y / 2, 'q', fontsize=11)
```

## 13. 바닥 도르래 + 경사면 시스템

`get_t_for_x()`로 수직 정렬

```python
fig, ax = plt.subplots(figsize=(14, 7))
clean_ax(ax, (-1, 14), (-3, 6))

ground = Ground(ax, y=0, xlim=(-1, 14))
boxA = Box(ax, size=(1, 0.8), on=ground, t=0.15, label='A', color='lightblue')

incline = Incline(ax, origin=(6, 0), width=6, height=3, direction='-')

temp_box = Box(ax, size=(0.8, 0.5), on=incline, t=0.6, label='', alpha=0)
pulley_incline = Pulley(ax, on=incline, t=0, for_obj=temp_box)

boxB = Box(ax, x=pulley_incline.bottom.x, y=1.9, size=(0.6, 0.8), label='B', color='orange')

# 바닥 도르래: right.x가 B.x와 일치
pulley_radius = 0.35
target_x = boxB.center.x - pulley_radius
t_pulley = ground.get_t_for_x(target_x)
pulley_ground = Pulley(ax, on=ground, t=t_pulley, radius=pulley_radius)

Rope(ax, boxA.right, pulley_ground.bottom)  # A → 바닥 도르래
Rope(ax, pulley_ground.right, boxB.bottom)  # 바닥 도르래 → B (수직!)
Rope(ax, boxB.top, pulley_incline.bottom)   # B → 경사면 도르래

boxC = Box(ax, size=(0.8, 0.5), on=incline, t=0.6, label='C', color='lightgreen')
Rope(ax, pulley_incline.right, boxC.left)
```

## 14. 용수철 연결 시스템

```python
fig, ax = plt.subplots(figsize=(14, 6))
clean_ax(ax, (-1, 14), (-1, 5))

ground = Ground(ax, y=0, xlim=(-1, 14))
plateA = Box(ax, x=6.5, y=0.5, size=(8, 0.4), label='A', color='#e0e0e0')

boxB1 = Box(ax, size=(1, 0.8), on=plateA, t=0.1, label='B', color='white')
boxB2 = Box(ax, size=(1, 0.8), on=plateA, t=0.25, label='B', color='white')
boxC = Box(ax, size=(1, 0.8), on=plateA, t=0.65, label='C', color='white')
boxD = Box(ax, size=(1, 0.8), on=plateA, t=0.8, label='D', color='white')

Spring(ax, start=(boxB2.right.x, plateA.top.y + 0.4),
       end=(boxC.left.x, plateA.top.y + 0.4), n_coils=6, amplitude=0.15)
```

## Incline 생성 방법

```python
# 방법 1: width + height
Incline(ax, origin=(0, 0), width=6, height=3, direction='-')

# 방법 2: width + angle (도)
Incline(ax, origin=(0, 0), width=6, angle=30, direction='-')

# 방법 3: height + angle (도)
Incline(ax, origin=(0, 0), height=3, angle=30, direction='-')
```

## 기타 유틸리티

```python
# 수식 박스
formula_box(ax, 6, 3, r'$F = ma$', fontsize=14)

# 각도 호
angle_arc(ax, center=(0, 0), radius=1, theta1=0, theta2=30, label=r'$\theta$')

# 좌표축
coord_axes(ax, origin=(0, 0), length=1.5, angle=0, labels=('x', 'y'))
```
