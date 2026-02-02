# 물리 애니메이션 공통 패턴

물리학 교육용 Manim 애니메이션에서 자주 사용되는 공통 패턴과 유틸리티입니다.

## 색상 규칙

물리량에 따른 일관된 색상 체계를 사용하면 학습자의 이해를 돕습니다.

```python
from manim import *

# 역학 관련 색상
FORCE_COLOR = RED           # 힘
VELOCITY_COLOR = BLUE       # 속도
ACCELERATION_COLOR = ORANGE # 가속도
DISPLACEMENT_COLOR = GREEN  # 변위
MOMENTUM_COLOR = PURPLE     # 운동량

# 에너지 관련 색상
KINETIC_ENERGY_COLOR = ORANGE   # 운동 에너지
POTENTIAL_ENERGY_COLOR = BLUE   # 위치 에너지
TOTAL_ENERGY_COLOR = GREEN      # 총 에너지
HEAT_COLOR = RED_E              # 열

# 전자기 관련 색상
POSITIVE_CHARGE_COLOR = RED     # 양전하
NEGATIVE_CHARGE_COLOR = BLUE    # 음전하
ELECTRIC_FIELD_COLOR = YELLOW   # 전기장
MAGNETIC_FIELD_COLOR = PURPLE   # 자기장
CURRENT_COLOR = ORANGE          # 전류

# 광학 관련 색상
LIGHT_COLOR = YELLOW        # 빛
INCIDENT_COLOR = YELLOW     # 입사광
REFLECTED_COLOR = GREEN     # 반사광
REFRACTED_COLOR = BLUE      # 굴절광
```

---

## 벡터 생성 유틸리티

### 물리량 벡터

```python
class PhysicsVector:
    """물리량 벡터 생성 클래스"""
    
    @staticmethod
    def force(start, direction, magnitude, label=r"\vec{F}", color=RED):
        """힘 벡터 생성"""
        end = start + direction * magnitude
        arrow = Arrow(start, end, color=color, buff=0, stroke_width=4)
        text = MathTex(label, color=color).next_to(arrow.get_end(), direction, buff=0.1)
        return VGroup(arrow, text)
    
    @staticmethod
    def velocity(center, direction, magnitude, label=r"\vec{v}", color=BLUE):
        """속도 벡터 생성"""
        start = center
        end = center + direction * magnitude
        arrow = Arrow(start, end, color=color, buff=0, stroke_width=3)
        text = MathTex(label, color=color).next_to(arrow.get_end(), direction, buff=0.1)
        return VGroup(arrow, text)
    
    @staticmethod
    def acceleration(center, direction, magnitude, label=r"\vec{a}", color=ORANGE):
        """가속도 벡터 생성"""
        start = center
        end = center + direction * magnitude
        arrow = Arrow(start, end, color=color, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        text = MathTex(label, color=color).next_to(arrow.get_end(), direction, buff=0.1)
        return VGroup(arrow, text)
    
    @staticmethod
    def decompose(start, vector, angle, labels=(r"F_x", r"F_y"), colors=(RED, GREEN)):
        """벡터 성분 분해"""
        magnitude = np.linalg.norm(vector)
        
        # x 성분
        x_comp = np.array([vector[0], 0, 0])
        x_arrow = Arrow(start, start + x_comp, color=colors[0], buff=0, stroke_width=3)
        x_label = MathTex(labels[0], color=colors[0]).next_to(x_arrow, DOWN, buff=0.1)
        
        # y 성분
        y_comp = np.array([0, vector[1], 0])
        y_arrow = Arrow(start + x_comp, start + vector, color=colors[1], buff=0, stroke_width=3)
        y_label = MathTex(labels[1], color=colors[1]).next_to(y_arrow, RIGHT, buff=0.1)
        
        return VGroup(x_arrow, x_label, y_arrow, y_label)
```

---

## 좌표계 및 그래프

### 물리량 그래프

```python
class PhysicsGraph:
    """물리량 그래프 생성 클래스"""
    
    @staticmethod
    def motion_graph(x_label, y_label, x_range, y_range, position=ORIGIN):
        """운동 그래프 (v-t, x-t, a-t)"""
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"include_tip": True}
        )
        labels = axes.get_axis_labels(x_label=x_label, y_label=y_label)
        return VGroup(axes, labels).shift(position)
    
    @staticmethod
    def energy_diagram(energies, labels, colors, position=ORIGIN):
        """에너지 막대 그래프"""
        bars = VGroup()
        max_energy = max(energies)
        bar_width = 0.8
        
        for i, (energy, label, color) in enumerate(zip(energies, labels, colors)):
            height = (energy / max_energy) * 3  # 최대 높이 3
            bar = Rectangle(
                width=bar_width,
                height=height,
                fill_color=color,
                fill_opacity=0.7
            )
            bar.move_to(position + RIGHT * i * 1.5)
            bar.align_to(position + DOWN * 1.5, DOWN)
            
            text = Text(label, font_size=20).next_to(bar, UP)
            value = MathTex(f"{energy}", font_size=24).move_to(bar)
            
            bars.add(VGroup(bar, text, value))
        
        return bars
```

---

## 물체 및 장치

### 기본 물체

```python
class PhysicsObjects:
    """물리 실험에서 사용되는 물체"""
    
    @staticmethod
    def box(side_length=1, color=BLUE, opacity=0.5, label=None):
        """상자 (질점 대용)"""
        box = Square(side_length=side_length, fill_color=color, fill_opacity=opacity)
        if label:
            text = MathTex(label).move_to(box)
            return VGroup(box, text)
        return box
    
    @staticmethod
    def ball(radius=0.3, color=RED, opacity=0.8):
        """공"""
        return Circle(radius=radius, fill_color=color, fill_opacity=opacity)
    
    @staticmethod
    def incline(base_length=4, height=2, color=GRAY, opacity=0.5):
        """경사면"""
        return Polygon(
            ORIGIN,
            RIGHT * base_length,
            RIGHT * base_length + UP * height,
            fill_color=color,
            fill_opacity=opacity
        )
    
    @staticmethod
    def spring(start, end, coils=8, amplitude=0.3, color=WHITE):
        """용수철"""
        direction = end - start
        length = np.linalg.norm(direction)
        unit = direction / length
        normal = np.array([-unit[1], unit[0], 0])
        
        points = [start]
        for i in range(coils * 2):
            t = (i + 1) / (coils * 2 + 1)
            pos = start + direction * t
            offset = amplitude * normal * ((-1) ** i)
            points.append(pos + offset)
        points.append(end)
        
        spring = VMobject()
        spring.set_points_as_corners(points)
        spring.set_stroke(color, width=2)
        return spring
    
    @staticmethod
    def pulley(center, radius=0.3, color=GRAY):
        """도르래"""
        outer = Circle(radius=radius, color=color, fill_opacity=0.5)
        inner = Circle(radius=radius/3, color=WHITE, fill_opacity=1)
        pulley = VGroup(outer, inner)
        pulley.move_to(center)
        return pulley
```

### 전기 회로 부품

```python
class CircuitComponents:
    """전기 회로 부품"""
    
    @staticmethod
    def resistor(position=ORIGIN, label="R"):
        """저항"""
        rect = Rectangle(width=0.6, height=0.25, stroke_color=WHITE, stroke_width=2)
        text = MathTex(label, font_size=20).next_to(rect, UP, buff=0.1)
        return VGroup(rect, text).move_to(position)
    
    @staticmethod
    def capacitor(position=ORIGIN, label="C"):
        """축전기"""
        left = Line(UP * 0.3, DOWN * 0.3, stroke_width=3)
        right = Line(UP * 0.3, DOWN * 0.3, stroke_width=3).shift(RIGHT * 0.15)
        text = MathTex(label, font_size=20).next_to(VGroup(left, right), UP, buff=0.1)
        return VGroup(left, right, text).move_to(position)
    
    @staticmethod
    def battery(position=ORIGIN, label="V"):
        """전지"""
        long_line = Line(UP * 0.4, DOWN * 0.4, stroke_width=4)
        short_line = Line(UP * 0.2, DOWN * 0.2, stroke_width=2).shift(RIGHT * 0.15)
        plus = MathTex("+", font_size=16).next_to(long_line, LEFT, buff=0.05)
        text = MathTex(label, font_size=20).next_to(VGroup(long_line, short_line), UP, buff=0.1)
        return VGroup(long_line, short_line, plus, text).move_to(position)
    
    @staticmethod
    def wire(start, end, color=WHITE):
        """도선"""
        return Line(start, end, color=color, stroke_width=2)
```

---

## 애니메이션 패턴

### 물체 운동

```python
class MotionPatterns:
    """물체 운동 애니메이션 패턴"""
    
    @staticmethod
    def uniform_motion(obj, direction, distance, run_time=2):
        """등속 운동"""
        return obj.animate.shift(direction * distance), {"run_time": run_time, "rate_func": linear}
    
    @staticmethod
    def accelerated_motion(obj, direction, distance, run_time=2):
        """가속 운동"""
        return obj.animate.shift(direction * distance), {"run_time": run_time, "rate_func": rate_functions.ease_in_quad}
    
    @staticmethod
    def decelerated_motion(obj, direction, distance, run_time=2):
        """감속 운동"""
        return obj.animate.shift(direction * distance), {"run_time": run_time, "rate_func": rate_functions.ease_out_quad}
    
    @staticmethod
    def projectile_path(start, v0, angle, g=10, num_points=50):
        """포물선 운동 경로"""
        vx = v0 * np.cos(angle)
        vy = v0 * np.sin(angle)
        
        # 비행 시간
        t_flight = 2 * vy / g
        
        points = []
        for t in np.linspace(0, t_flight, num_points):
            x = start[0] + vx * t
            y = start[1] + vy * t - 0.5 * g * t**2
            points.append([x, y, 0])
        
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in points])
        path.set_stroke(YELLOW, width=2)
        return path
```

### 파동 애니메이션

```python
class WavePatterns:
    """파동 애니메이션 패턴"""
    
    @staticmethod
    def traveling_wave(axes, wavelength, amplitude, speed, t):
        """진행파 함수"""
        k = 2 * PI / wavelength
        omega = speed * k
        return axes.plot(
            lambda x: amplitude * np.sin(k * x - omega * t),
            color=BLUE
        )
    
    @staticmethod
    def standing_wave(axes, wavelength, amplitude, t):
        """정상파 함수"""
        k = 2 * PI / wavelength
        omega = 2 * PI  # 임의의 각진동수
        return axes.plot(
            lambda x: 2 * amplitude * np.sin(k * x) * np.cos(omega * t),
            color=YELLOW
        )
    
    @staticmethod
    def circular_wave(center, max_radius, num_circles=5):
        """원형 파동 (동심원)"""
        waves = VGroup()
        for i in range(num_circles):
            r = max_radius * (i + 1) / num_circles
            opacity = 1 - i / num_circles
            circle = Circle(radius=r, stroke_width=2, stroke_opacity=opacity, color=BLUE)
            circle.move_to(center)
            waves.add(circle)
        return waves
```

---

## 수식 표시 패턴

### 단계별 유도

```python
class EquationDerivation:
    """수식 유도 애니메이션"""
    
    @staticmethod
    def step_by_step(equations, position=ORIGIN, alignment=DOWN):
        """단계별 수식 표시"""
        eq_group = VGroup()
        for i, eq in enumerate(equations):
            tex = MathTex(eq)
            if i == 0:
                tex.move_to(position)
            else:
                tex.next_to(eq_group[-1], alignment, buff=0.5)
            eq_group.add(tex)
        return eq_group
    
    @staticmethod
    def highlight_term(equation, term_index, color=YELLOW):
        """특정 항 강조"""
        box = SurroundingRectangle(equation[term_index], color=color, buff=0.1)
        return box
    
    @staticmethod
    def transform_step(scene, eq1, eq2, run_time=1):
        """수식 변환 애니메이션"""
        scene.play(TransformMatchingShapes(eq1, eq2), run_time=run_time)
```

---

## 장면 구성 템플릿

### 기본 물리 실험 장면

```python
class PhysicsExperimentTemplate(Scene):
    """물리 실험 장면 템플릿"""
    
    def setup_experiment(self, title):
        """실험 셋업"""
        title_text = Text(title, font_size=36).to_edge(UP)
        self.play(Write(title_text))
        return title_text
    
    def add_coordinate_system(self, x_range, y_range, position=ORIGIN):
        """좌표계 추가"""
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={"include_tip": True}
        ).shift(position)
        self.play(Create(axes))
        return axes
    
    def add_legend(self, items, position=DR):
        """범례 추가"""
        legend = VGroup()
        for color, label in items:
            dot = Dot(color=color)
            text = Text(label, font_size=16)
            item = VGroup(dot, text).arrange(RIGHT, buff=0.2)
            legend.add(item)
        legend.arrange(DOWN, aligned_edge=LEFT).to_corner(position)
        self.play(Write(legend))
        return legend
    
    def show_equation(self, equation, position=UR):
        """수식 표시"""
        eq = MathTex(equation).to_corner(position)
        self.play(Write(eq))
        return eq
    
    def conclude(self, message):
        """결론 표시"""
        conclusion = Text(message, font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(conclusion))
        return conclusion
```

### 사용 예시

```python
class FreeFallExperiment(PhysicsExperimentTemplate):
    """자유 낙하 실험"""
    def construct(self):
        # 1. 실험 셋업
        self.setup_experiment("자유 낙하 운동")
        
        # 2. 좌표계
        axes = self.add_coordinate_system(
            x_range=[0, 3, 1],
            y_range=[0, 50, 10],
            position=LEFT * 3
        )
        
        # 3. 물체 생성
        ball = PhysicsObjects.ball(radius=0.2, color=RED)
        ball.move_to(LEFT * 3 + UP * 2)
        self.play(Create(ball))
        
        # 4. 운동 수식
        self.show_equation(r"y = \frac{1}{2}gt^2")
        
        # 5. 애니메이션
        anim, kwargs = MotionPatterns.accelerated_motion(ball, DOWN, 4)
        self.play(anim, **kwargs)
        
        # 6. 결론
        self.conclude("가속도 g = 9.8 m/s²")
        self.wait(2)
```

---

## 참고 사항

### 성취기준 docstring 형식

모든 Scene 클래스에 성취기준을 명시합니다:

```python
class MyScene(Scene):
    """[12물리XX-XX] 성취기준 내용 요약"""
    def construct(self):
        pass
```

### 권장 run_time 값

| 애니메이션 유형 | 권장 시간 |
|----------------|----------|
| 간단한 생성 | 0.5 ~ 1초 |
| 변환/이동 | 1 ~ 2초 |
| 복잡한 과정 | 2 ~ 3초 |
| 데이터 플롯 | 2 ~ 4초 |

### 화면 구성 권장사항

- **제목**: `to_edge(UP)`
- **수식**: `to_corner(UR)` 또는 `to_corner(UL)`
- **범례**: `to_corner(DR)` 또는 `to_corner(DL)`
- **결론/설명**: `to_edge(DOWN)`
- **메인 콘텐츠**: 중앙 영역
