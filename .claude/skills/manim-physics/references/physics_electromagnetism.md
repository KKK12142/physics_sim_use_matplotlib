# 전자기학 애니메이션 가이드

2022개정 물리학 교육과정 "전기와 자기" 영역에 해당하는 애니메이션 패턴입니다.

## 성취기준 대응

| 성취기준 | 내용 |
|---------|------|
| [12물리02-01] | 전기장과 전위차, 전기적 상호작용 |
| [12물리02-02] | 저항의 연결과 소비 전력 |
| [12물리02-03] | 축전기와 전기 에너지 저장 |
| [12물리02-04] | 자성체의 종류와 활용 |
| [12물리02-05] | 전류의 자기 작용 (스피커, 전동기) |
| [12물리02-06] | 전자기 유도 (센서, 무선충전) |

---

## 전기장과 전위차

### 점전하의 전기장

```python
from manim import *
import numpy as np

class PointChargeField(Scene):
    """[12물리02-01] 점전하에 의한 전기장"""
    def construct(self):
        title = Text("점전하의 전기장", font_size=36).to_edge(UP)
        
        # 양전하
        charge = Dot(color=RED, radius=0.3)
        plus = MathTex("+", color=WHITE).move_to(charge)
        
        # 전기력선 (방사형)
        field_lines = VGroup()
        num_lines = 12
        for i in range(num_lines):
            angle = i * 2 * PI / num_lines
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            
            # 화살표 형태의 전기력선
            line = Arrow(
                charge.get_center() + direction * 0.4,
                charge.get_center() + direction * 2.5,
                color=YELLOW,
                buff=0,
                stroke_width=2
            )
            field_lines.add(line)
        
        # 전기장 수식
        field_eq = MathTex(
            r"E = k\frac{q}{r^2}"
        ).to_corner(UR)
        
        field_direction = Text(
            "양전하: 바깥 방향", font_size=24
        ).next_to(field_eq, DOWN)
        
        self.play(Write(title))
        self.play(Create(charge), Write(plus))
        self.play(Create(field_lines), run_time=2)
        self.play(Write(field_eq), Write(field_direction))
        self.wait(2)
```

### 전기력선과 등전위선

```python
class FieldAndEquipotential(Scene):
    """[12물리02-01] 전기력선과 등전위선의 관계"""
    def construct(self):
        title = Text("전기력선과 등전위선", font_size=36).to_edge(UP)
        
        # 양전하
        charge = Dot(color=RED, radius=0.25).shift(LEFT * 1)
        plus = MathTex("+").move_to(charge)
        
        # 등전위선 (동심원)
        equipotentials = VGroup()
        for r in [0.8, 1.3, 1.8, 2.3]:
            circle = Circle(radius=r, color=BLUE, stroke_width=2)
            circle.move_to(charge.get_center())
            equipotentials.add(circle)
        
        # 전기력선 (방사형)
        field_lines = VGroup()
        for angle in np.linspace(0, 2*PI, 8, endpoint=False):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            line = Arrow(
                charge.get_center() + direction * 0.35,
                charge.get_center() + direction * 2.5,
                color=YELLOW, buff=0, stroke_width=2
            )
            field_lines.add(line)
        
        # 범례
        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=YELLOW), 
                   Text("전기력선", font_size=20)).arrange(RIGHT),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=BLUE),
                   Text("등전위선", font_size=20)).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)
        
        # 수직 관계 설명
        perpendicular = MathTex(
            r"\vec{E} \perp \text{등전위선}"
        ).to_corner(UR)
        
        self.play(Write(title))
        self.play(Create(charge), Write(plus))
        self.play(Create(equipotentials))
        self.play(Create(field_lines))
        self.play(Write(legend), Write(perpendicular))
        self.wait(2)
```

### 두 전하 사이의 전기장

```python
class DipoleFiled(Scene):
    """[12물리02-01] 전기 쌍극자의 전기장"""
    def construct(self):
        title = Text("전기 쌍극자", font_size=36).to_edge(UP)
        
        # 양전하와 음전하
        pos_charge = Dot(color=RED, radius=0.25).shift(LEFT * 2)
        neg_charge = Dot(color=BLUE, radius=0.25).shift(RIGHT * 2)
        
        plus = MathTex("+").move_to(pos_charge)
        minus = MathTex("-").move_to(neg_charge)
        
        # 전기력선 (양전하에서 음전하로)
        def create_field_line(start_angle, end_angle, num_points=20):
            points = []
            for t in np.linspace(0, 1, num_points):
                # 간단한 쌍극자 필드라인 근사
                angle = start_angle + (end_angle - start_angle) * t
                r = 2 * (1 - 0.8 * np.cos(angle))
                x = r * np.cos(angle)
                y = r * np.sin(angle) * 0.5
                points.append([x, y, 0])
            return points
        
        field_lines = VGroup()
        angles = [30, 60, 90, 120, 150]
        for angle in angles:
            # 위쪽 선
            arc_up = ArcBetweenPoints(
                pos_charge.get_center() + UP * 0.3 + RIGHT * 0.2,
                neg_charge.get_center() + UP * 0.3 + LEFT * 0.2,
                angle=angle * DEGREES,
                color=YELLOW
            )
            # 아래쪽 선 (대칭)
            arc_down = ArcBetweenPoints(
                pos_charge.get_center() + DOWN * 0.3 + RIGHT * 0.2,
                neg_charge.get_center() + DOWN * 0.3 + LEFT * 0.2,
                angle=-angle * DEGREES,
                color=YELLOW
            )
            field_lines.add(arc_up, arc_down)
        
        # 중간 직선
        middle_line = Arrow(
            pos_charge.get_center() + RIGHT * 0.3,
            neg_charge.get_center() + LEFT * 0.3,
            color=YELLOW, buff=0
        )
        field_lines.add(middle_line)
        
        self.play(Write(title))
        self.play(Create(pos_charge), Create(neg_charge))
        self.play(Write(plus), Write(minus))
        self.play(Create(field_lines), run_time=2)
        self.wait(2)
```

---

## 전기 회로

### 저항의 직렬 연결

```python
class SeriesResistors(Scene):
    """[12물리02-02] 저항의 직렬 연결"""
    def construct(self):
        title = Text("저항의 직렬 연결", font_size=36).to_edge(UP)
        
        # 전원
        battery = VGroup(
            Line(UP * 0.3, DOWN * 0.3, stroke_width=4),
            Line(UP * 0.15, DOWN * 0.15, stroke_width=2).shift(RIGHT * 0.15)
        ).shift(LEFT * 4)
        
        # 저항 기호 (지그재그)
        def create_resistor(label):
            zigzag = VMobject()
            zigzag.set_points_as_corners([
                LEFT * 0.3, LEFT * 0.2 + UP * 0.15,
                LEFT * 0.1 + DOWN * 0.15, ORIGIN + UP * 0.15,
                RIGHT * 0.1 + DOWN * 0.15, RIGHT * 0.2 + UP * 0.15,
                RIGHT * 0.3
            ])
            zigzag.set_stroke(WHITE, 2)
            text = MathTex(label).next_to(zigzag, UP)
            return VGroup(zigzag, text)
        
        r1 = create_resistor("R_1").shift(LEFT * 1.5)
        r2 = create_resistor("R_2").shift(RIGHT * 0.5)
        r3 = create_resistor("R_3").shift(RIGHT * 2.5)
        
        # 연결선
        wires = VGroup(
            Line(battery.get_right(), r1[0].get_left()),
            Line(r1[0].get_right(), r2[0].get_left()),
            Line(r2[0].get_right(), r3[0].get_left()),
            Line(r3[0].get_right(), RIGHT * 4),
            Line(RIGHT * 4, RIGHT * 4 + DOWN * 2),
            Line(RIGHT * 4 + DOWN * 2, LEFT * 4 + DOWN * 2),
            Line(LEFT * 4 + DOWN * 2, battery.get_left() + DOWN * 0.5),
        )
        
        # 전류 화살표
        current = Arrow(LEFT * 3.5 + DOWN * 0.5, LEFT * 2.5 + DOWN * 0.5,
                       color=YELLOW, buff=0)
        i_label = MathTex("I", color=YELLOW).next_to(current, DOWN)
        
        # 수식
        eq1 = MathTex(r"R_{total} = R_1 + R_2 + R_3").to_corner(UR)
        eq2 = MathTex(r"I = \frac{V}{R_{total}}").next_to(eq1, DOWN)
        
        self.play(Write(title))
        self.play(Create(battery))
        self.play(Create(r1), Create(r2), Create(r3))
        self.play(Create(wires))
        self.play(Create(current), Write(i_label))
        self.play(Write(eq1), Write(eq2))
        
        # 전류가 같음 강조
        same_current = Text("직렬: 모든 저항에 같은 전류", font_size=24).to_corner(DL)
        self.play(Write(same_current))
        self.wait(2)
```

### 저항의 병렬 연결

```python
class ParallelResistors(Scene):
    """[12물리02-02] 저항의 병렬 연결"""
    def construct(self):
        title = Text("저항의 병렬 연결", font_size=36).to_edge(UP)
        
        # 저항 기호 생성 함수
        def create_resistor(label):
            rect = Rectangle(width=0.6, height=0.3, stroke_color=WHITE)
            text = MathTex(label, font_size=30).next_to(rect, RIGHT, buff=0.1)
            return VGroup(rect, text)
        
        # 세 개의 병렬 저항
        r1 = create_resistor("R_1").shift(UP * 1.5)
        r2 = create_resistor("R_2")
        r3 = create_resistor("R_3").shift(DOWN * 1.5)
        
        # 연결선
        left_node = Dot(LEFT * 3, color=YELLOW)
        right_node = Dot(RIGHT * 2, color=YELLOW)
        
        wires = VGroup(
            # 왼쪽 분기
            Line(left_node.get_center(), LEFT * 1 + UP * 1.5),
            Line(LEFT * 1 + UP * 1.5, r1[0].get_left()),
            Line(left_node.get_center(), LEFT * 1),
            Line(LEFT * 1, r2[0].get_left()),
            Line(left_node.get_center(), LEFT * 1 + DOWN * 1.5),
            Line(LEFT * 1 + DOWN * 1.5, r3[0].get_left()),
            # 오른쪽 합류
            Line(r1[0].get_right(), RIGHT * 1 + UP * 1.5),
            Line(RIGHT * 1 + UP * 1.5, right_node.get_center()),
            Line(r2[0].get_right(), right_node.get_center()),
            Line(r3[0].get_right(), RIGHT * 1 + DOWN * 1.5),
            Line(RIGHT * 1 + DOWN * 1.5, right_node.get_center()),
        )
        
        # 전류 분배 화살표
        i_total = Arrow(LEFT * 4.5, left_node.get_center() + LEFT * 0.5,
                       color=YELLOW, buff=0)
        i_total_label = MathTex("I", color=YELLOW).next_to(i_total, UP)
        
        i1 = Arrow(LEFT * 1.5 + UP * 1.5, r1[0].get_left() + LEFT * 0.2,
                  color=RED, buff=0, stroke_width=2)
        i2 = Arrow(LEFT * 1.5, r2[0].get_left() + LEFT * 0.2,
                  color=RED, buff=0, stroke_width=2)
        i3 = Arrow(LEFT * 1.5 + DOWN * 1.5, r3[0].get_left() + LEFT * 0.2,
                  color=RED, buff=0, stroke_width=2)
        
        # 수식
        eq1 = MathTex(
            r"\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3}"
        ).to_corner(UR).scale(0.8)
        
        eq2 = MathTex(r"I = I_1 + I_2 + I_3").next_to(eq1, DOWN)
        
        same_voltage = Text("병렬: 모든 저항에 같은 전압", font_size=24).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(left_node), Create(right_node))
        self.play(Create(r1), Create(r2), Create(r3))
        self.play(Create(wires))
        self.play(Create(i_total), Write(i_total_label))
        self.play(Create(i1), Create(i2), Create(i3))
        self.play(Write(eq1), Write(eq2))
        self.play(Write(same_voltage))
        self.wait(2)
```

---

## 축전기

### 축전기의 전기 에너지 저장

```python
class CapacitorEnergy(Scene):
    """[12물리02-03] 축전기의 에너지 저장"""
    def construct(self):
        title = Text("축전기의 에너지 저장", font_size=36).to_edge(UP)
        
        # 축전기 기호
        plate1 = Line(UP * 1, DOWN * 1, stroke_width=4).shift(LEFT * 0.15)
        plate2 = Line(UP * 1, DOWN * 1, stroke_width=4).shift(RIGHT * 0.15)
        
        capacitor = VGroup(plate1, plate2)
        
        # 전하 표시
        pos_charges = VGroup(*[
            MathTex("+", color=RED, font_size=24).move_to(plate1.get_center() + LEFT * 0.3 + UP * (0.6 - i * 0.4))
            for i in range(4)
        ])
        neg_charges = VGroup(*[
            MathTex("-", color=BLUE, font_size=24).move_to(plate2.get_center() + RIGHT * 0.3 + UP * (0.6 - i * 0.4))
            for i in range(4)
        ])
        
        # 전기장 화살표 (판 사이)
        field_arrows = VGroup(*[
            Arrow(plate1.get_center() + RIGHT * 0.2 + UP * (0.5 - i * 0.33),
                  plate2.get_center() + LEFT * 0.2 + UP * (0.5 - i * 0.33),
                  color=YELLOW, buff=0, stroke_width=2)
            for i in range(4)
        ])
        
        # 수식
        capacitance = MathTex(r"C = \frac{Q}{V}").to_corner(UR)
        energy = MathTex(r"U = \frac{1}{2}CV^2 = \frac{1}{2}QV = \frac{Q^2}{2C}").next_to(capacitance, DOWN)
        
        # 응용 예시
        applications = VGroup(
            Text("응용:", font_size=24),
            Text("• 터치스크린", font_size=20),
            Text("• 카메라 플래시", font_size=20),
            Text("• 전자기기 전원 안정화", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(capacitor))
        self.play(Write(pos_charges), Write(neg_charges))
        self.play(Create(field_arrows))
        self.play(Write(capacitance))
        self.play(Write(energy))
        self.play(Write(applications))
        self.wait(2)
```

---

## 자기장과 전류

### 직선 전류 주위의 자기장

```python
class MagneticFieldWire(Scene):
    """[12물리02-05] 직선 전류 주위의 자기장"""
    def construct(self):
        title = Text("직선 전류의 자기장", font_size=36).to_edge(UP)
        
        # 전선 (화면 수직 방향, 동심원으로 표현)
        wire = Circle(radius=0.15, fill_color=ORANGE, fill_opacity=1)
        current_symbol = MathTex(r"\odot", color=WHITE).scale(0.8)  # 화면 밖으로 나오는 전류
        
        wire_group = VGroup(wire, current_symbol)
        
        # 자기장 동심원
        b_field_circles = VGroup()
        for r in [0.6, 1.0, 1.5, 2.0]:
            circle = Circle(radius=r, color=PURPLE, stroke_width=2)
            # 방향 화살표 추가
            for angle in [0, PI/2, PI, 3*PI/2]:
                arrow_pos = circle.point_at_angle(angle)
                tangent = rotate_vector(arrow_pos, PI/2)
                small_arrow = Arrow(
                    arrow_pos - tangent * 0.15,
                    arrow_pos + tangent * 0.15,
                    color=PURPLE, buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.5
                )
                b_field_circles.add(small_arrow)
            b_field_circles.add(circle)
        
        # 오른손 법칙 설명
        rule = VGroup(
            Text("오른손 법칙:", font_size=24),
            Text("엄지 → 전류 방향", font_size=20),
            Text("나머지 손가락 → 자기장 방향", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)
        
        # 자기장 크기 수식
        b_eq = MathTex(r"B = \frac{\mu_0 I}{2\pi r}").to_corner(UR)
        
        self.play(Write(title))
        self.play(Create(wire_group))
        self.play(Create(b_field_circles), run_time=2)
        self.play(Write(b_eq))
        self.play(Write(rule))
        self.wait(2)
```

### 전류가 받는 자기력

```python
class MagneticForceOnWire(Scene):
    """[12물리02-05] 자기장 속 전류가 받는 힘"""
    def construct(self):
        title = Text("자기장 속 전류가 받는 힘", font_size=36).to_edge(UP)
        
        # 자기장 (화면 안쪽으로)
        b_field = VGroup()
        for i in range(-2, 3):
            for j in range(-1, 2):
                cross = MathTex(r"\times", color=BLUE).move_to([i * 1.5, j * 1.2, 0])
                b_field.add(cross)
        
        b_label = MathTex(r"\vec{B}", color=BLUE).to_corner(UL)
        
        # 전선
        wire = Line(LEFT * 3, RIGHT * 3, color=ORANGE, stroke_width=6)
        
        # 전류 방향
        current_arrow = Arrow(LEFT * 2, RIGHT * 2, color=YELLOW, buff=0)
        current_arrow.next_to(wire, DOWN, buff=0.3)
        i_label = MathTex("I").next_to(current_arrow, DOWN)
        
        # 힘 벡터 (위쪽)
        force = Arrow(ORIGIN, UP * 2, color=RED, buff=0, stroke_width=6)
        f_label = MathTex(r"\vec{F}", color=RED).next_to(force, RIGHT)
        
        # 로렌츠 힘 수식
        force_eq = MathTex(r"\vec{F} = I\vec{L} \times \vec{B}").to_corner(UR)
        magnitude_eq = MathTex(r"F = BIL\sin\theta").next_to(force_eq, DOWN)
        
        self.play(Write(title))
        self.play(Create(b_field), Write(b_label))
        self.play(Create(wire))
        self.play(Create(current_arrow), Write(i_label))
        self.play(Create(force), Write(f_label))
        self.play(Write(force_eq), Write(magnitude_eq))
        self.wait(2)
```

---

## 전자기 유도

### 패러데이 법칙

```python
class FaradaysLaw(Scene):
    """[12물리02-06] 전자기 유도"""
    def construct(self):
        title = Text("패러데이 전자기 유도 법칙", font_size=36).to_edge(UP)
        
        # 코일
        coil = VGroup()
        for i in range(4):
            loop = Ellipse(width=1.5, height=0.6, color=ORANGE, stroke_width=3)
            loop.shift(RIGHT * i * 0.3)
            coil.add(loop)
        coil.shift(LEFT * 0.5)
        
        # 자석
        magnet = VGroup(
            Rectangle(width=0.8, height=1.5, fill_color=RED, fill_opacity=0.8),
            Rectangle(width=0.8, height=1.5, fill_color=BLUE, fill_opacity=0.8).shift(DOWN * 1.5),
            Text("N", color=WHITE, font_size=24).shift(UP * 0.3),
            Text("S", color=WHITE, font_size=24).shift(DOWN * 1.2)
        )
        magnet.shift(LEFT * 4)
        
        # 자기력선
        field_lines = VGroup()
        for offset in [-0.3, 0, 0.3]:
            line = CurvedArrow(
                magnet.get_right() + UP * offset,
                coil.get_left() + UP * offset,
                color=PURPLE, angle=-0.3
            )
            field_lines.add(line)
        
        # 유도 기전력 수식
        emf_eq = MathTex(r"\mathcal{E} = -\frac{d\Phi_B}{dt}").to_corner(UR)
        flux_eq = MathTex(r"\Phi_B = BA\cos\theta").next_to(emf_eq, DOWN)
        
        # 전류 방향 표시
        induced_current = CurvedArrow(
            coil.get_top() + LEFT * 0.5,
            coil.get_top() + RIGHT * 0.5,
            color=YELLOW
        )
        i_label = MathTex("I_{ind}", color=YELLOW).next_to(induced_current, UP)
        
        self.play(Write(title))
        self.play(Create(coil))
        self.play(Create(magnet))
        
        # 자석을 코일쪽으로 이동
        self.play(Create(field_lines))
        self.play(
            magnet.animate.shift(RIGHT * 2),
            field_lines.animate.shift(RIGHT * 2),
            run_time=2
        )
        
        # 유도 전류 발생
        self.play(Create(induced_current), Write(i_label))
        self.play(Write(emf_eq), Write(flux_eq))
        self.wait(2)
```

### 렌츠의 법칙

```python
class LenzsLaw(Scene):
    """[12물리02-06] 렌츠의 법칙"""
    def construct(self):
        title = Text("렌츠의 법칙", font_size=36).to_edge(UP)
        
        # 코일 (상단 시점)
        coil_outer = Circle(radius=1.5, color=ORANGE, stroke_width=4)
        coil_inner = Circle(radius=1.3, color=ORANGE, stroke_width=4)
        coil = VGroup(coil_outer, coil_inner)
        
        # 자기장 증가 (아래로)
        b_increase = VGroup()
        for i in range(-1, 2):
            for j in range(-1, 2):
                arrow = Arrow(
                    [i * 0.6, j * 0.6 + 0.3, 0],
                    [i * 0.6, j * 0.6 - 0.3, 0],
                    color=BLUE, buff=0, stroke_width=2
                )
                b_increase.add(arrow)
        
        b_label = MathTex(r"\vec{B} \uparrow", color=BLUE).shift(UP * 2.5)
        
        # 유도 전류 (반시계 방향 - 위에서 볼 때)
        current_arrows = VGroup()
        for angle in [0, PI/2, PI, 3*PI/2]:
            pos = 1.4 * np.array([np.cos(angle), np.sin(angle), 0])
            tangent = np.array([-np.sin(angle), np.cos(angle), 0])
            arrow = Arrow(
                pos - tangent * 0.2, pos + tangent * 0.2,
                color=YELLOW, buff=0, stroke_width=3
            )
            current_arrows.add(arrow)
        
        # 유도 자기장 (위로 - 원래 자기장 변화 방해)
        b_induced = Arrow(
            DOWN * 0.5, UP * 0.8,
            color=GREEN, buff=0, stroke_width=4
        )
        b_ind_label = MathTex(r"\vec{B}_{ind}", color=GREEN).next_to(b_induced, RIGHT)
        
        # 렌츠 법칙 설명
        law = MathTex(
            r"\text{유도 전류의 방향: 자기선속 변화를 방해}"
        ).scale(0.7).to_corner(DR)
        
        self.play(Write(title))
        self.play(Create(coil))
        self.play(Create(b_increase), Write(b_label))
        self.play(Create(current_arrows))
        self.play(Create(b_induced), Write(b_ind_label))
        self.play(Write(law))
        self.wait(2)
```

---

## 유틸리티 함수

```python
def create_resistor_symbol(width=0.6, height=0.25):
    """저항 기호 생성"""
    return Rectangle(width=width, height=height, stroke_color=WHITE, stroke_width=2)

def create_capacitor_symbol(gap=0.1, height=0.8):
    """축전기 기호 생성"""
    left = Line(UP * height/2, DOWN * height/2).shift(LEFT * gap/2)
    right = Line(UP * height/2, DOWN * height/2).shift(RIGHT * gap/2)
    return VGroup(left, right)

def create_battery_symbol(long_height=0.6, short_height=0.3):
    """전지 기호 생성"""
    long = Line(UP * long_height/2, DOWN * long_height/2, stroke_width=4)
    short = Line(UP * short_height/2, DOWN * short_height/2, stroke_width=2).shift(RIGHT * 0.15)
    return VGroup(long, short)

def create_magnetic_field_into_page(x_range, y_range, spacing=1):
    """화면 안쪽으로 들어가는 자기장 (X 표시)"""
    crosses = VGroup()
    for x in np.arange(x_range[0], x_range[1], spacing):
        for y in np.arange(y_range[0], y_range[1], spacing):
            cross = MathTex(r"\times", color=BLUE).move_to([x, y, 0]).scale(0.8)
            crosses.add(cross)
    return crosses

def create_magnetic_field_out_of_page(x_range, y_range, spacing=1):
    """화면 바깥으로 나오는 자기장 (점 표시)"""
    dots = VGroup()
    for x in np.arange(x_range[0], x_range[1], spacing):
        for y in np.arange(y_range[0], y_range[1], spacing):
            dot = Dot([x, y, 0], color=BLUE, radius=0.08)
            circle = Circle(radius=0.12, color=BLUE, stroke_width=1).move_to([x, y, 0])
            dots.add(VGroup(dot, circle))
    return dots
```

## 참고 자료

- [Manim Vector 사용법](https://docs.manim.community/en/stable/reference/manim.mobject.geometry.line.Arrow.html)
- [전자기학 시각화 예제](https://docs.manim.community/en/stable/examples.html)
