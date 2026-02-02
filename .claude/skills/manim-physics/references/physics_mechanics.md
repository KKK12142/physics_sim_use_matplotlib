# 역학 애니메이션 가이드

2022개정 물리학 교육과정 "힘과 에너지" 영역에 해당하는 애니메이션 패턴입니다.

## 성취기준 대응

| 성취기준 | 내용 |
|---------|------|
| [12물리01-01] | 평형과 안정성 (알짜힘=0, 돌림힘=0) |
| [12물리01-02] | 뉴턴 운동 법칙, 등가속도 운동, 교통안전 |
| [12물리01-03] | 작용-반작용, 운동량 보존 |
| [12물리01-04] | 일-에너지 정리, 역학적 에너지 보존 |
| [12물리01-05] | 열과 에너지 전환 |
| [12물리01-06] | 열기관 효율, 영구기관 불가능 |

---

## 평형과 안정성

### 힘의 평형 조건

```python
from manim import *

class ForceEquilibrium(Scene):
    """[12물리01-01] 힘의 평형 - 알짜힘이 0인 상태"""
    def construct(self):
        # 물체
        box = Square(side_length=1, fill_color=BLUE, fill_opacity=0.5)
        
        # 힘 벡터들
        f1 = Arrow(box.get_center(), box.get_center() + RIGHT * 2, 
                   color=RED, buff=0)
        f2 = Arrow(box.get_center(), box.get_center() + LEFT * 2,
                   color=GREEN, buff=0)
        
        f1_label = MathTex(r"\vec{F}_1").next_to(f1, UP)
        f2_label = MathTex(r"\vec{F}_2").next_to(f2, UP)
        
        # 평형 조건
        equilibrium_eq = MathTex(
            r"\sum \vec{F} = \vec{F}_1 + \vec{F}_2 = 0"
        ).to_corner(UR)
        
        self.play(Create(box))
        self.play(Create(f1), Write(f1_label))
        self.play(Create(f2), Write(f2_label))
        self.play(Write(equilibrium_eq))
        
        # 알짜힘 = 0 강조
        result = MathTex(r"\Rightarrow \text{정지 상태 유지}").next_to(equilibrium_eq, DOWN)
        self.play(Write(result))
        self.wait(2)
```

### 돌림힘과 회전 평형

```python
class TorqueEquilibrium(Scene):
    """[12물리01-01] 돌림힘의 평형"""
    def construct(self):
        # 시소 (lever)
        pivot = Dot(color=WHITE, radius=0.1)
        beam = Line(LEFT * 4, RIGHT * 4, stroke_width=6)
        
        # 지렛대 받침점
        triangle = Triangle(fill_color=GRAY, fill_opacity=1)
        triangle.scale(0.4).rotate(PI).next_to(pivot, DOWN, buff=0)
        
        # 양쪽 물체
        m1 = Square(side_length=0.6, fill_color=RED, fill_opacity=0.8)
        m2 = Square(side_length=0.8, fill_color=BLUE, fill_opacity=0.8)
        
        r1 = 2  # 왼쪽 거리
        r2 = 3  # 오른쪽 거리
        
        m1.move_to(LEFT * r1 + DOWN * 0.5)
        m2.move_to(RIGHT * r2 + DOWN * 0.5)
        
        # 힘 벡터 (중력)
        w1 = Arrow(m1.get_center(), m1.get_center() + DOWN * 1.5, 
                   color=YELLOW, buff=0)
        w2 = Arrow(m2.get_center(), m2.get_center() + DOWN * 1.2,
                   color=YELLOW, buff=0)
        
        # 돌림힘 수식
        torque_eq = MathTex(
            r"\tau = r \times F"
        ).to_corner(UL)
        
        equilibrium = MathTex(
            r"\tau_1 = \tau_2 \Rightarrow m_1 g r_1 = m_2 g r_2"
        ).to_corner(UR)
        
        self.play(Create(beam), Create(pivot), Create(triangle))
        self.play(Create(m1), Create(m2))
        self.play(Create(w1), Create(w2))
        self.play(Write(torque_eq), Write(equilibrium))
        self.wait(2)
```

---

## 뉴턴 운동 법칙

### 뉴턴 제1법칙 (관성)

```python
class NewtonsFirstLaw(Scene):
    """[12물리01-02] 관성의 법칙"""
    def construct(self):
        title = Text("뉴턴 제1법칙: 관성의 법칙", font_size=36).to_edge(UP)
        
        # 정지한 물체
        box1 = Square(side_length=1, fill_color=BLUE, fill_opacity=0.5)
        box1.shift(LEFT * 4)
        label1 = Text("정지 상태", font_size=20).next_to(box1, DOWN)
        
        # 등속 운동 물체
        box2 = Square(side_length=1, fill_color=GREEN, fill_opacity=0.5)
        box2.shift(LEFT * 4 + DOWN * 2)
        velocity = Arrow(box2.get_right(), box2.get_right() + RIGHT * 1.5,
                        color=RED, buff=0)
        label2 = Text("등속 운동", font_size=20).next_to(box2, DOWN)
        
        # 법칙 설명
        law = MathTex(
            r"\sum \vec{F} = 0 \Rightarrow \vec{v} = \text{const}"
        ).to_corner(UR)
        
        self.play(Write(title))
        self.play(Create(box1), Write(label1))
        self.wait()
        
        # 정지 상태 유지
        self.play(Indicate(box1))
        self.wait()
        
        # 등속 운동
        self.play(Create(box2), Create(velocity), Write(label2))
        self.play(
            box2.animate.shift(RIGHT * 6),
            velocity.animate.shift(RIGHT * 6),
            run_time=3,
            rate_func=linear
        )
        
        self.play(Write(law))
        self.wait(2)
```

### 뉴턴 제2법칙 (가속도)

```python
class NewtonsSecondLaw(Scene):
    """[12물리01-02] F = ma와 등가속도 운동"""
    def construct(self):
        title = Text("뉴턴 제2법칙", font_size=36).to_edge(UP)
        
        # 물체
        box = Square(side_length=1, fill_color=BLUE, fill_opacity=0.5)
        box.shift(LEFT * 4)
        
        # 힘 벡터
        force = Arrow(box.get_left() + LEFT * 0.5, box.get_left(),
                     color=RED, buff=0, stroke_width=6)
        f_label = MathTex(r"\vec{F}").next_to(force, UP)
        
        # 가속도 벡터
        accel = Arrow(box.get_right(), box.get_right() + RIGHT * 1,
                     color=ORANGE, buff=0)
        a_label = MathTex(r"\vec{a}").next_to(accel, UP)
        
        # 핵심 수식
        equation = MathTex(r"\vec{F} = m\vec{a}").to_corner(UR)
        equation_expanded = MathTex(
            r"\vec{a} = \frac{\vec{F}}{m}"
        ).next_to(equation, DOWN)
        
        self.play(Write(title))
        self.play(Create(box))
        self.play(Create(force), Write(f_label))
        self.play(Create(accel), Write(a_label))
        self.play(Write(equation))
        
        # 물체 가속 (등가속도 운동)
        self.play(
            box.animate.shift(RIGHT * 6),
            force.animate.shift(RIGHT * 6),
            accel.animate.shift(RIGHT * 6),
            f_label.animate.shift(RIGHT * 6),
            a_label.animate.shift(RIGHT * 6),
            run_time=2,
            rate_func=rate_functions.ease_in_quad  # 가속 느낌
        )
        
        self.play(Write(equation_expanded))
        self.wait(2)
```

### v-t, x-t 그래프

```python
class MotionGraphs(Scene):
    """[12물리01-02] 등가속도 운동의 그래프 분석"""
    def construct(self):
        # v-t 그래프
        vt_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 10, 2],
            x_length=5, y_length=3,
            axis_config={"include_tip": True}
        ).shift(LEFT * 3.5 + UP * 1)
        
        vt_labels = vt_axes.get_axis_labels(x_label="t", y_label="v")
        
        # v = v0 + at (초기속도 2, 가속도 1.5)
        v_graph = vt_axes.plot(lambda t: 2 + 1.5 * t, x_range=[0, 5], color=BLUE)
        
        # x-t 그래프  
        xt_axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 25, 5],
            x_length=5, y_length=3,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 3.5 + UP * 1)
        
        xt_labels = xt_axes.get_axis_labels(x_label="t", y_label="x")
        
        # x = v0*t + 0.5*a*t^2
        x_graph = xt_axes.plot(lambda t: 2*t + 0.5*1.5*t**2, x_range=[0, 5], color=GREEN)
        
        # 수식
        v_eq = MathTex(r"v = v_0 + at").next_to(vt_axes, DOWN)
        x_eq = MathTex(r"x = v_0 t + \frac{1}{2}at^2").next_to(xt_axes, DOWN)
        
        # v-t 그래프에서 면적 = 변위
        area = vt_axes.get_area(v_graph, x_range=[0, 3], color=YELLOW, opacity=0.3)
        area_label = MathTex(r"\int v \, dt = x").move_to(area)
        
        self.play(Create(vt_axes), Create(xt_axes))
        self.play(Write(vt_labels), Write(xt_labels))
        self.play(Create(v_graph), Create(x_graph))
        self.play(Write(v_eq), Write(x_eq))
        
        self.play(FadeIn(area), Write(area_label))
        self.wait(2)
```

---

## 운동량과 충돌

### 운동량 보존 법칙

```python
class MomentumConservation(Scene):
    """[12물리01-03] 일차원 충돌에서 운동량 보존"""
    def construct(self):
        title = Text("운동량 보존 법칙", font_size=36).to_edge(UP)
        
        # 충돌 전
        before_label = Text("충돌 전", font_size=24).shift(UP * 2 + LEFT * 5)
        
        ball1_before = Circle(radius=0.4, fill_color=RED, fill_opacity=0.8)
        ball2_before = Circle(radius=0.5, fill_color=BLUE, fill_opacity=0.8)
        
        ball1_before.move_to(LEFT * 4 + UP * 1)
        ball2_before.move_to(RIGHT * 1 + UP * 1)
        
        v1 = Arrow(ball1_before.get_right(), ball1_before.get_right() + RIGHT * 2,
                  color=GREEN, buff=0)
        v2 = Arrow(ball2_before.get_left() + LEFT * 0.5, ball2_before.get_left(),
                  color=GREEN, buff=0)
        
        # 충돌 후
        after_label = Text("충돌 후", font_size=24).shift(DOWN * 1.5 + LEFT * 5)
        
        ball1_after = Circle(radius=0.4, fill_color=RED, fill_opacity=0.8)
        ball2_after = Circle(radius=0.5, fill_color=BLUE, fill_opacity=0.8)
        
        ball1_after.move_to(LEFT * 2 + DOWN * 2)
        ball2_after.move_to(RIGHT * 2 + DOWN * 2)
        
        v1_after = Arrow(ball1_after.get_right(), ball1_after.get_right() + RIGHT * 0.8,
                        color=GREEN, buff=0)
        v2_after = Arrow(ball2_after.get_right(), ball2_after.get_right() + RIGHT * 1.5,
                        color=GREEN, buff=0)
        
        # 운동량 보존 수식
        momentum_eq = MathTex(
            r"m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'"
        ).to_corner(DR)
        
        total_p = MathTex(r"\vec{p}_{total} = \text{const}").to_corner(UR)
        
        self.play(Write(title))
        self.play(Write(before_label))
        self.play(Create(ball1_before), Create(ball2_before))
        self.play(Create(v1), Create(v2))
        
        self.wait()
        
        # 충돌 애니메이션
        self.play(
            ball1_before.animate.shift(RIGHT * 2.5),
            v1.animate.shift(RIGHT * 2.5),
            ball2_before.animate.shift(LEFT * 0.5),
            v2.animate.shift(LEFT * 0.5),
            run_time=1
        )
        
        # 충돌 후 결과
        self.play(Write(after_label))
        self.play(
            Create(ball1_after), Create(ball2_after),
            Create(v1_after), Create(v2_after)
        )
        
        self.play(Write(momentum_eq), Write(total_p))
        self.wait(2)
```

---

## 일과 에너지

### 일-에너지 정리

```python
class WorkEnergyTheorem(Scene):
    """[12물리01-04] 일-에너지 정리"""
    def construct(self):
        title = Text("일-에너지 정리", font_size=36).to_edge(UP)
        
        # 수평면 위 물체
        ground = Line(LEFT * 6, RIGHT * 6, color=GRAY).shift(DOWN * 2)
        box = Square(side_length=0.8, fill_color=BLUE, fill_opacity=0.7)
        box.next_to(ground, UP, buff=0).shift(LEFT * 4)
        
        # 힘 벡터
        force = Arrow(box.get_left() + LEFT * 0.3, box.get_left(),
                     color=RED, buff=0, stroke_width=5)
        f_label = MathTex(r"F").next_to(force, UP)
        
        # 변위 화살표
        displacement = Arrow(LEFT * 4, RIGHT * 2, color=GREEN,
                            buff=0, stroke_width=3).shift(DOWN * 1)
        d_label = MathTex(r"d").next_to(displacement, DOWN)
        
        # 일의 정의
        work_def = MathTex(r"W = Fd\cos\theta").to_corner(UL)
        
        # 일-에너지 정리
        theorem = MathTex(
            r"W_{net} = \Delta KE = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2"
        ).to_corner(UR)
        
        self.play(Write(title))
        self.play(Create(ground), Create(box))
        self.play(Create(force), Write(f_label))
        self.play(Create(displacement), Write(d_label))
        
        # 물체 이동
        self.play(
            box.animate.shift(RIGHT * 6),
            force.animate.shift(RIGHT * 6),
            f_label.animate.shift(RIGHT * 6),
            run_time=2
        )
        
        self.play(Write(work_def))
        self.play(Write(theorem))
        self.wait(2)
```

### 역학적 에너지 보존 (진자)

```python
class PendulumEnergy(Scene):
    """[12물리01-04] 진자의 역학적 에너지 보존"""
    def construct(self):
        title = Text("역학적 에너지 보존", font_size=36).to_edge(UP)
        
        # 진자 고정점
        pivot = Dot(ORIGIN + UP * 2, color=WHITE)
        
        # 여러 위치의 진자
        positions = [
            (-60 * DEGREES, "최고점", BLUE),
            (-30 * DEGREES, "중간", GREEN),
            (0, "최저점", RED),
            (30 * DEGREES, "중간", GREEN),
            (60 * DEGREES, "최고점", BLUE)
        ]
        
        length = 2.5
        pendulums = VGroup()
        energy_labels = VGroup()
        
        for angle, label, color in positions:
            # 추 위치 계산
            x = length * np.sin(angle)
            y = 2 - length * np.cos(angle)
            
            string = Line(pivot.get_center(), [x, y, 0], color=GRAY)
            bob = Circle(radius=0.2, fill_color=color, fill_opacity=0.8)
            bob.move_to([x, y, 0])
            
            pendulums.add(VGroup(string, bob))
        
        # 에너지 막대 그래프
        pe_bar = Rectangle(width=0.5, height=2, fill_color=BLUE, fill_opacity=0.8)
        ke_bar = Rectangle(width=0.5, height=0.1, fill_color=RED, fill_opacity=0.8)
        
        pe_bar.shift(RIGHT * 4 + DOWN * 0.5)
        ke_bar.next_to(pe_bar, RIGHT, buff=0.3).align_to(pe_bar, DOWN)
        
        pe_label = Text("PE", font_size=20).next_to(pe_bar, UP)
        ke_label = Text("KE", font_size=20).next_to(ke_bar, UP)
        
        # 에너지 보존 수식
        energy_eq = MathTex(
            r"E = KE + PE = \frac{1}{2}mv^2 + mgh = \text{const}"
        ).shift(DOWN * 3)
        
        self.play(Write(title))
        self.play(Create(pivot))
        
        # 순차적으로 진자 위치 표시
        for i, pendulum in enumerate(pendulums):
            self.play(Create(pendulum), run_time=0.5)
        
        self.play(
            Create(pe_bar), Create(ke_bar),
            Write(pe_label), Write(ke_label)
        )
        
        # 최저점에서 에너지 변환 애니메이션
        self.play(
            pe_bar.animate.stretch(0.05, dim=1, about_edge=DOWN),
            ke_bar.animate.stretch(20, dim=1, about_edge=DOWN),
            run_time=2
        )
        
        self.play(Write(energy_eq))
        self.wait(2)
```

---

## 열과 에너지 전환

### 열역학 제1법칙

```python
class FirstLawThermodynamics(Scene):
    """[12물리01-05] 에너지 보존과 열 전환"""
    def construct(self):
        title = Text("열역학 제1법칙", font_size=36).to_edge(UP)
        
        # 시스템 (기체가 든 실린더)
        cylinder = Rectangle(width=2, height=3, stroke_color=WHITE)
        piston = Rectangle(width=1.8, height=0.2, fill_color=GRAY, fill_opacity=1)
        piston.move_to(cylinder.get_top() + DOWN * 0.5)
        
        gas_region = Rectangle(width=1.8, height=2, fill_color=BLUE, fill_opacity=0.3)
        gas_region.move_to(cylinder.get_center() + DOWN * 0.4)
        
        system = VGroup(cylinder, gas_region, piston)
        system.shift(LEFT * 3)
        
        # 에너지 흐름 화살표
        q_arrow = Arrow(system.get_left() + LEFT * 2, system.get_left() + LEFT * 0.3,
                       color=RED, buff=0)
        q_label = MathTex(r"Q", color=RED).next_to(q_arrow, UP)
        
        w_arrow = Arrow(system.get_top() + UP * 0.3, system.get_top() + UP * 1.5,
                       color=GREEN, buff=0)
        w_label = MathTex(r"W", color=GREEN).next_to(w_arrow, RIGHT)
        
        # 에너지 보존 수식
        law = MathTex(
            r"\Delta U = Q - W"
        ).to_corner(UR)
        
        explanation = VGroup(
            MathTex(r"Q: \text{열 (시스템에 들어온)}"),
            MathTex(r"W: \text{일 (시스템이 한)}"),
            MathTex(r"\Delta U: \text{내부 에너지 변화}")
        ).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3)
        
        self.play(Write(title))
        self.play(Create(system))
        self.play(Create(q_arrow), Write(q_label))
        self.play(Create(w_arrow), Write(w_label))
        self.play(Write(law))
        self.play(Write(explanation))
        
        # 피스톤 팽창 애니메이션
        self.play(
            piston.animate.shift(UP * 0.5),
            gas_region.animate.stretch(1.3, dim=1, about_edge=DOWN),
            run_time=2
        )
        self.wait(2)
```

---

## 유틸리티 함수

```python
def create_force_vector(start, direction, magnitude, label, color=RED):
    """힘 벡터 생성"""
    end = start + direction * magnitude
    arrow = Arrow(start, end, color=color, buff=0, stroke_width=4)
    text = MathTex(label, color=color).next_to(arrow.get_end(), direction, buff=0.1)
    return VGroup(arrow, text)

def create_velocity_vector(obj, direction, magnitude, label):
    """속도 벡터 생성"""
    return create_force_vector(obj.get_center(), direction, magnitude, label, color=BLUE)

def create_energy_bar(height, color, label, position):
    """에너지 막대 그래프 생성"""
    bar = Rectangle(width=0.8, height=height, fill_color=color, fill_opacity=0.8)
    bar.move_to(position)
    text = Text(label, font_size=20).next_to(bar, UP)
    return VGroup(bar, text)

def create_coordinate_axes(x_range, y_range, x_label, y_label, position=ORIGIN):
    """좌표축 생성"""
    axes = Axes(
        x_range=x_range, y_range=y_range,
        axis_config={"include_tip": True}
    ).shift(position)
    labels = axes.get_axis_labels(x_label=x_label, y_label=y_label)
    return VGroup(axes, labels)
```

## 참고 자료

- [Manim Axes 문서](https://docs.manim.community/en/stable/reference/manim.mobject.graphing.coordinate_systems.Axes.html)
- [NumberPlane 사용법](https://docs.manim.community/en/stable/reference/manim.mobject.graphing.coordinate_systems.NumberPlane.html)
