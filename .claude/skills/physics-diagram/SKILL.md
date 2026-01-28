---
name: physics-diagram
description: 물리학 역학 다이어그램 및 자유물체도(FBD) 생성. matplotlib 기반 클래스로 바닥, 경사면, 테이블 위 물체 배치, 도르래 시스템, 힘 벡터, 좌표축, 수식 박스를 그림. 사용 시점 - 물리 문제 일러스트, 자유물체도, 경사면 힘 분해, 도르래 시스템, 용수철 연결 다이어그램을 그리거나 이미지를 재현할 때.
---

# Physics Diagram (물리학 다이어그램)

`scripts/utils.py`를 사용하여 물리학 역학 다이어그램을 제작합니다.

## Quick Start

```python
from utils import *
import matplotlib.pyplot as plt

setup_style('AppleGothic')  # Mac: AppleGothic, Windows: Malgun Gothic, Linux: NanumGothic
fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, xlim=(-1, 10), ylim=(-1, 6))

ground = Ground(ax, y=0, xlim=(-1, 10))
box = Box(ax, size=(1.5, 1), on=ground, t=0.5, label='m', color='lightblue')
arrow(ax, box.center, box.center + (0, -1.5), RED, label=r'$m\vec{g}$')

plt.savefig('output.svg', format='svg', bbox_inches='tight')
```

## Instructions

### Step 1: 요구사항 파악

이미지/텍스트에서 확인할 것:
- 표면 종류 (Ground, Incline, Table, Ceiling, Wall)
- 물체 개수와 위치 관계
- 연결 요소 (Pulley, Rope, Spring)
- 힘 벡터 필요 여부
- 라벨과 수치

**부족한 정보는 반드시 질문!**

### Step 2: 코드 작성 순서

1. **표면 먼저** → 2. **물체 배치** (`on=`) → 3. **도르래** → 4. **로프/용수철** → 5. **힘 벡터** → 6. **라벨**

### Step 3: SVG로 저장

```python
plt.savefig('output.svg', format='svg', bbox_inches='tight')
```

## 클래스 요약

### 표면 (on 파라미터 지원)

| 클래스 | 설명 | 주요 파라미터 |
|--------|------|--------------|
| `Ground` | 바닥 + 빗금 | `y`, `xlim` |
| `Incline` | 경사면 | `origin`, `width`, `height`, `direction` |
| `Table` | 테이블 | `x`, `y`, `width`, `height` |
| `Ceiling` | 천장 | `y`, `xlim` |
| `Wall` | 벽 | `x`, `ylim`, `side` |

**경사면 direction**:
- `'-'`: ／ 모양 (왼쪽 높음) → 도르래 `t=0`
- `'+'`: ＼ 모양 (오른쪽 높음) → 도르래 `t=1`

### 물체

| 클래스 | 주요 파라미터 |
|--------|--------------|
| `Box` | `size=(w,h)`, `on`, `t`, `label`, `color` |
| `Circle` | `radius`, `on`, `t`, `label` |
| `MassPoint` | `x`, `y` |

**속성**: `center`, `top`, `bottom`, `left`, `right`, `surface_normal`, `surface_tangent`

### 연결 요소

```python
# 도르래
pulley = Pulley(ax, on=incline, t=0, for_obj=box)

# 로프
Rope(ax, box.right, pulley.left)

# 용수철
Spring(ax, obj1=box1, obj2=box2)
```

### 힘 벡터

```python
arrow(ax, start, end, color, label='F')

# 색상: RED, BLUE, GREEN, ORANGE, PURPLE, GRAY, BROWN
```

## 도르래 연결 규칙 (중요!)

### 경사면/테이블 끝 도르래

```python
pulley = Pulley(ax, on=incline, t=0, for_obj=box)

# direction='-' → t=0, box.left ↔ pulley.right
# direction='+' → t=1, box.right ↔ pulley.left
```

### 바닥 도르래 (수직 정렬)

```python
target_x = hanging_box.center.x - pulley_radius
t = ground.get_t_for_x(target_x)
pulley = Pulley(ax, on=ground, t=t, radius=pulley_radius)

Rope(ax, floor_box.right, pulley.bottom)  # 바닥 물체
Rope(ax, pulley.right, hanging_box.bottom)  # 매달린 물체 (수직!)
```

## 힘 분해 (경사면)

```python
# 중력
arrow(ax, box.center, box.center + (0, -mg), RED, label=r'$m\vec{g}$')

# 수직항력 (표면 법선)
N = box.surface_normal * (mg * np.cos(incline.angle_rad))
arrow(ax, box.center, box.center + N, BLUE, label=r'$\vec{N}$')

# 장력 (표면 접선, 음수=경사면 위쪽)
T = box.surface_tangent * (-tension_mag)
arrow(ax, box.center, box.center + T, PURPLE, label=r'$\vec{T}$')
```

## 예시

전체 예시는 [references/examples.md](references/examples.md) 참조.

### 경사면 + 도르래

```python
incline = Incline(ax, origin=(0, 0), width=6, height=3, direction='-')
box = Box(ax, size=(1, 0.6), on=incline, t=0.5, label=r'$m_1$')

pulley = Pulley(ax, on=incline, t=0, for_obj=box)
hanging = Box(ax, x=pulley.bottom.x, y=0.5, size=(0.5, 0.8), label=r'$m_2$')

Rope(ax, box.left, pulley.right)
Rope(ax, pulley.bottom, hanging.top)
```

### 천장 도르래 + 판 + 추

```python
ceiling = Ceiling(ax, y=7, xlim=(0, 9))
pulley_L = Pulley(ax, on=ceiling, t=0.3, radius=0.35)
pulley_R = Pulley(ax, on=ceiling, t=0.8, radius=0.35)

plate = Box(ax, x=pulley_L.center.x, y=3.5, size=(2.5, 0.25), label='판')
boxA = Box(ax, size=(0.6, 0.5), on=plate, t=0.25, label='A')

Rope(ax, plate.top, pulley_L.bottom)
Rope(ax, pulley_L.right, pulley_R.left, horizontal=True)
```

## 체크리스트

- [ ] 물체가 올바른 표면 위에 배치됨 (`on=`)
- [ ] 도르래 연결점이 direction 규칙에 맞음
- [ ] 로프가 자연스럽게 연결됨
- [ ] 힘 벡터 방향이 물리적으로 올바름
- [ ] 라벨이 겹치지 않음
- [ ] SVG로 저장됨
