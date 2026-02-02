# 한글 텍스트 및 교육과정 표준

## 텍스트 규칙

- **한글 텍스트**: `Text()` 사용 (Manim의 기본 폰트가 한글을 지원)
- **수식**: `MathTex()` 사용 (LaTeX 렌더링)
- **혼합**: 한글과 수식을 같은 줄에 넣을 때는 `VGroup`으로 나란히 배치

```python
# 한글 텍스트
title = Text("충격량과 운동량", font_size=80, color=WHITE)

# 수식
eq = MathTex(r"I = F \times \Delta t", font_size=72)

# 혼합 (한글 + 수식)
mixed = VGroup(
    MathTex(r"v_0 = 4\text{m/s}", font_size=36, color=WHITE),
    Text(" 로 마찰 구간을 지나는 상황", font_size=24, color=WHITE),
).arrange(RIGHT, buff=0.2)
```

### MathTex 내 한글
`\text{}` 안에 한글을 넣으면 렌더링이 안 될 수 있다. 단위(`kg`, `m/s`, `N·s`)는 영문 `\text{}`로, 한글 설명은 별도 `Text()`로 분리한다.

```python
# 좋은 예
MathTex(r"= 19.6 \text{ kg·m/s}", font_size=36)

# 한글 설명은 Text로 분리
Text("평균힘", font_size=16, color=ORANGE)
```

---

## 인트로 패턴

```python
def intro(self):
    title = Text("충격량과 운동량 II", font_size=80, color=WHITE)
    box = SurroundingRectangle(title, color=YELLOW, buff=0.4,
                                corner_radius=0.15, stroke_width=4)
    title.move_to(ORIGIN)
    self.play(Write(title), run_time=1.0)
    self.play(Write(box), run_time=1.0)
    self.wait(0.5)
```

### 변형: 수식 + 부제

```python
def intro(self):
    eq = MathTex(r"\vec{p}", "=", "m", r"\vec{v}", font_size=96, color=WHITE)
    eq.move_to(ORIGIN)
    self.play(Write(eq), run_time=2.0)
    self.wait(0.5)

    box = SurroundingRectangle(eq, color=YELLOW, buff=0.4,
                                corner_radius=0.15, stroke_width=4)
    self.play(Create(box), run_time=0.75)

    title = Text("운동량 보존 법칙", font_size=44, color=YELLOW)
    title.next_to(box, DOWN, buff=0.6)
    self.play(Write(title), run_time=1.0)

    subtitle = Text("외력이 없으면 총 운동량은 변하지 않는다", font_size=28, color=WHITE)
    subtitle.next_to(title, DOWN, buff=0.5)
    self.play(Write(subtitle), run_time=1.0)
    self.wait(1.5)
```

---

## 아웃트로 패턴

### 패턴 A: 핵심 메시지 → FadeOut → 제목 재등장

```python
def outro(self):
    msg = Text(
        "같은 충격량(운동량변화량)이어도\n물체에 작용하는 평균힘의 크기가 달라질 수 있다.",
        font_size=40, color=WHITE, line_spacing=1.5,
    ).move_to(ORIGIN)
    self.play(Write(msg), run_time=2)
    self.wait(2)
    self.play(FadeOut(msg), run_time=1)
    self.wait(0.5)

    title = Text("충격량과 운동량 II", font_size=80, color=WHITE).move_to(ORIGIN)
    box = SurroundingRectangle(title, color=YELLOW, buff=0.4,
                                corner_radius=0.15, stroke_width=4)
    self.play(Write(title), run_time=1.0)
    self.play(Create(box), run_time=0.8)
    self.wait(2)
```

### 패턴 B: 핵심 공식 + 요약 포인트

```python
def outro(self):
    final_eq = MathTex("m_1", "v_1", "+", "m_2", "v_2", "=",
                        "m_1", "v_1'", "+", "m_2", "v_2'",
                        font_size=64, color=WHITE)
    final_eq.move_to(ORIGIN)
    final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4,
                                      corner_radius=0.15, stroke_width=4)
    subtitle = Text("운동량 보존 법칙", font_size=40, color=YELLOW)
    subtitle.next_to(final_box, DOWN, buff=0.5)

    self.play(Write(final_eq), run_time=1.5)
    self.play(Create(final_box), run_time=0.75)
    self.play(Write(subtitle), run_time=1.0)
    self.wait(1.0)

    points = VGroup(
        Text("• 운동량 = 질량 × 속도 (벡터량)", font_size=24, color=WHITE),
        Text("• 외력이 없으면 총 운동량 보존", font_size=24, color=WHITE),
        Text("• 충돌 종류와 무관하게 항상 성립", font_size=24, color=WHITE),
    )
    points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    points.next_to(subtitle, DOWN, buff=0.5)
    self.play(FadeIn(points), run_time=1.0)
    self.wait(3)
```

### 패턴 C: 다음 차시 예고

```python
next_title = Text("다음 시간", font_size=36, color=GRAY).shift(UP * 0.5)
next_q = Text("에어백은 어떻게 우리를 보호할까?", font_size=32, color=YELLOW)
next_q.next_to(next_title, DOWN, buff=0.4)
next_hint = MathTex(r"\Delta t \uparrow \;\Rightarrow\; F \downarrow",
                    font_size=40, color=WHITE)
next_hint.next_to(next_q, DOWN, buff=0.4)
```

---

## 결론/강조 오버레이

화면 위에 반투명 배경 + 핵심 수식:

```python
conclusion = MathTex(r"I = |\Delta p| = 8 \text{ N·s}",
                     font_size=64, color=YELLOW).move_to(ORIGIN)
bg_rect = BackgroundRectangle(conclusion, color=BLACK, fill_opacity=0.85, buff=0.3)
self.play(FadeIn(bg_rect), Write(conclusion))
self.wait(2)
```

---

## 자주 쓰는 물리 용어 한글 표기

| 물리량 | 한글 | 영문 표기 (수식 내) |
|--------|------|---------------------|
| 운동량 | 운동량 | `p`, `\vec{p}` |
| 충격량 | 충격량 | `I` |
| 힘 | 힘 | `F`, `\vec{F}` |
| 속도 | 속도 | `v`, `\vec{v}` |
| 가속도 | 가속도 | `a` |
| 질량 | 질량 | `m` |
| 시간 | 시간 | `t`, `\Delta t` |
| 변위 | 변위 | `s`, `\Delta s` |
| 운동에너지 | 운동에너지 | `KE`, `E_k` |
| 평균힘 | 평균힘 | `\bar{F}` |
| 마찰구간 | 마찰구간 | — |
| 힘 작용 구간 | 힘 작용 구간 | — |
| 등속 운동 | 등속 운동 | — |
| 등가속도 운동 | 등가속도 운동 | — |

---

## 교육과정 표준 참조

고등학교 물리학I 성취기준 코드를 참고하여 교육 목표를 명시할 수 있다:

- `[12물리01-02]` 뉴턴 운동 법칙
- `[12물리01-03]` 운동량과 충격량
- `[12물리01-04]` 운동량 보존 법칙

---

## 폰트 크기 가이드

| 용도 | font_size |
|------|-----------|
| 메인 제목 | 48~80 |
| 부제/실험명 | 28~36 |
| 축 라벨 | 14~20 |
| 물체 내 텍스트 | 16~18 |
| 수식 (메인) | 36~72 |
| 수식 (보조/계산) | 22~28 |
| 결론 강조 수식 | 56~96 |
| 요약 포인트 | 24 |
