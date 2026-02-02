# 물리학 교수학습 자료 제작 — 프로젝트 지침

## 프로젝트 개요
Manim Community를 사용한 고등학교 물리학 교육 애니메이션 제작 프로젝트.

## 환경
- Python venv: `./venv/bin/manim` (시스템 PATH에 없음)
- 저화질 렌더링 확인: `./venv/bin/manim -ql 파일명.py 클래스명`

## 핵심 규칙

### 한글 처리
- **한글 텍스트는 반드시 `Text()`** 사용. `MathTex()`의 `\text{}` 안에 한글 넣으면 LaTeX 컴파일 에러 발생.
- 한글+수식 혼합이 필요하면 `VGroup(Text(...), MathTex(...)).arrange(RIGHT)`로 나란히 배치.
- `°` 같은 특수문자도 MathTex에서 주의. `^{\circ}` 사용하거나 Text()로 처리.

### 색상 컨벤션
| 물리량 | 색상 |
|--------|------|
| 힘 (F) | RED |
| 변위 (d) | GREEN |
| 속도 (v) | BLUE |
| 위치에너지 (PE) | BLUE |
| 운동에너지 (KE) | ORANGE |
| 총 에너지 / 결론 / 강조 | YELLOW |
| 마찰력 / 음의 일 | RED (점선) |
| 물체 A | BLUE |
| 물체 B | RED |
| 합체 물체 | PURPLE |
| 보조선 | GRAY |

### 씬 구조 패턴
```python
class ClassName(Scene):
    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_xxx()
        self.clear_screen()
        # ...
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)
```

### 애니메이션 규칙
- ValueTracker updater 사용 후 **반드시 `clear_updaters()` 호출**
- `always_redraw` 클로저에서 루프 변수 캡처 주의
- 동적 그래프 → 애니메이션 종료 후 정적 그래프로 교체

### 렌더링 전 체크리스트
- [ ] MathTex 안에 한글 없는지 확인
- [ ] v-t 그래프가 F/m 적분과 일치하는지
- [ ] 축 범위가 peak 값의 1.15~1.25배인지
- [ ] updater 해제 완료
- [ ] 인트로/아웃트로 패턴 포함

### 스프링 그리기 (`make_spring`)

3D 나선을 2D로 투영한 스프링. 양끝에 직선 앵커(`─`) 포함. 길이를 변수로 받아 `always_redraw`와 조합하면 후크의 법칙 등에서 동적으로 사용 가능.

```
─/\/\/\/\/\/─
  앵커  코일  앵커
```

```python
def make_spring(start, end, n_coils=8, coil_width=0.3, anchor_len=0.3,
                color=WHITE, stroke_width=2.5):
    """
    start, end : 스프링 양 끝점 좌표 (앵커 끝)
    n_coils    : 코일 감은 수
    coil_width : 코일 수직 진폭 (반폭)
    anchor_len : 양쪽 직선 앵커 길이 (절대값, 전체의 40% 이하로 클램핑)
    """
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    total_vec = end - start
    total_len = np.linalg.norm(total_vec)
    if total_len < 1e-6:
        return VGroup()
    direction = total_vec / total_len
    perp = np.array([-direction[1], direction[0], 0.0])

    actual_anchor = min(anchor_len, total_len * 0.4)
    coil_start = start + direction * actual_anchor
    coil_end = end - direction * actual_anchor
    coil_len = np.linalg.norm(coil_end - coil_start)

    anchor1 = Line(start, coil_start, color=color, stroke_width=stroke_width)
    anchor2 = Line(coil_end, end, color=color, stroke_width=stroke_width)

    n_points = n_coils * 16 + 1
    coil_points = []
    for i in range(n_points):
        t = i / (n_points - 1)
        along = coil_start + direction * coil_len * t
        offset = perp * coil_width * np.sin(t * n_coils * TAU)
        coil_points.append(along + offset)

    coil = VMobject(color=color, stroke_width=stroke_width)
    coil.set_points_smoothly([np.array(p) for p in coil_points])

    return VGroup(anchor1, coil, anchor2)
```

**동적 사용 예시** (ValueTracker + always_redraw):
```python
length_tracker = ValueTracker(3.0)

spring = always_redraw(lambda: make_spring(
    LEFT * 5, LEFT * 5 + RIGHT * length_tracker.get_value(),
    n_coils=10, coil_width=0.35, color=GREEN,
))

obj = always_redraw(lambda: Square(
    side_length=0.5, color=BLUE, fill_opacity=0.8,
).move_to(LEFT * 5 + RIGHT * length_tracker.get_value() + RIGHT * 0.25))

self.add(spring, obj)
self.play(length_tracker.animate.set_value(5.0), run_time=1.5)  # 늘리기
self.play(length_tracker.animate.set_value(1.5), run_time=1.5)  # 압축
```

### 코드 작성 후
- 반드시 `./venv/bin/manim -ql` 저화질 렌더링으로 에러 확인
- 에러 발생 시 수정 후 재렌더링
- 재렌더링한 영상은 확인할 필요없음 사람이 직접 영상을 확인할거임.