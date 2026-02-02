# 광학 및 현대물리 애니메이션 가이드

2022개정 물리학 교육과정 "빛과 물질" 영역에 해당하는 애니메이션 패턴입니다.

## 성취기준 대응

| 성취기준 | 내용 |
|---------|------|
| [12물리03-01] | 빛의 중첩과 간섭, 파동성 |
| [12물리03-02] | 굴절과 볼록렌즈, 광선 추적 |
| [12물리03-03] | 빛과 물질의 이중성 |
| [12물리03-04] | 에너지 준위와 스펙트럼 |
| [12물리03-05] | 에너지띠와 반도체 (p-n 접합) |
| [12물리03-06] | 광속 불변과 특수 상대성 이론 |

---

## 파동의 중첩과 간섭

### 두 파동의 중첩

```python
from manim import *
import numpy as np

class WaveSuperposition(Scene):
    """[12물리03-01] 파동의 중첩 원리"""
    def construct(self):
        title = Text("파동의 중첩", font_size=36).to_edge(UP)
        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=3
        ).shift(DOWN * 0.5)
        
        # 파동 1
        wave1 = axes.plot(
            lambda x: np.sin(2 * x),
            x_range=[0, 10],
            color=BLUE
        )
        label1 = MathTex("y_1 = A\\sin(kx)", color=BLUE).to_corner(UL)
        
        # 파동 2
        wave2 = axes.plot(
            lambda x: np.sin(2 * x + PI/3),
            x_range=[0, 10],
            color=RED
        )
        label2 = MathTex("y_2 = A\\sin(kx + \\phi)", color=RED).next_to(label1, DOWN)
        
        # 합성파
        wave_sum = axes.plot(
            lambda x: np.sin(2 * x) + np.sin(2 * x + PI/3),
            x_range=[0, 10],
            color=GREEN,
            stroke_width=4
        )
        label_sum = MathTex("y = y_1 + y_2", color=GREEN).next_to(label2, DOWN)
        
        # 중첩 원리
        principle = MathTex(
            r"y_{total} = y_1 + y_2"
        ).to_corner(DR)
        
        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(wave1), Write(label1))
        self.wait(0.5)
        self.play(Create(wave2), Write(label2))
        self.wait(0.5)
        self.play(Create(wave_sum), Write(label_sum))
        self.play(Write(principle))
        self.wait(2)
```

### 이중 슬릿 간섭

```python
class DoubleSlitInterference(Scene):
    """[12물리03-01] 영의 이중 슬릿 실험"""
    def construct(self):
        title = Text("이중 슬릿 간섭", font_size=36).to_edge(UP)
        
        # 광원
        light_source = Dot(LEFT * 6, color=YELLOW, radius=0.2)
        light_label = Text("광원", font_size=20).next_to(light_source, DOWN)
        
        # 슬릿 장벽
        barrier = VGroup(
            Line(UP * 3, UP * 0.4, stroke_width=6, color=GRAY),
            Line(UP * 0.2, DOWN * 0.2, stroke_width=6, color=GRAY),
            Line(DOWN * 0.4, DOWN * 3, stroke_width=6, color=GRAY)
        ).shift(LEFT * 2)
        
        slit1_pos = LEFT * 2 + UP * 0.3
        slit2_pos = LEFT * 2 + DOWN * 0.3
        
        # 스크린
        screen = Line(UP * 2.5, DOWN * 2.5, stroke_width=4, color=WHITE)
        screen.shift(RIGHT * 4)
        
        # 파동 (동심원)
        def animate_waves():
            waves1 = VGroup()
            waves2 = VGroup()
            for r in np.arange(0.5, 6, 0.5):
                c1 = Circle(radius=r, stroke_width=1, stroke_opacity=0.5, color=BLUE)
                c1.move_to(slit1_pos)
                c2 = Circle(radius=r, stroke_width=1, stroke_opacity=0.5, color=BLUE)
                c2.move_to(slit2_pos)
                waves1.add(c1)
                waves2.add(c2)
            return waves1, waves2
        
        waves1, waves2 = animate_waves()
        
        # 간섭 무늬 (밝은 점들)
        interference_pattern = VGroup()
        d = 0.6  # 슬릿 간격
        L = 6    # 슬릿-스크린 거리
        wavelength = 0.5
        
        for m in range(-4, 5):
            y = m * wavelength * L / d * 0.3  # 스케일 조정
            if abs(y) < 2.5:
                brightness = 1.0 if m % 1 == 0 else 0.3
                dot = Dot(RIGHT * 4 + UP * y, color=YELLOW, radius=0.08)
                dot.set_opacity(brightness)
                interference_pattern.add(dot)
        
        # 보강 간섭 조건
        constructive = MathTex(
            r"d\sin\theta = m\lambda \quad (m = 0, \pm1, \pm2, ...)"
        ).scale(0.7).to_corner(UR)
        
        bright_label = Text("보강 간섭 (밝음)", font_size=20, color=YELLOW).next_to(constructive, DOWN)
        
        self.play(Write(title))
        self.play(Create(light_source), Write(light_label))
        self.play(Create(barrier))
        self.play(Create(screen))
        self.play(Create(waves1), Create(waves2), run_time=2)
        self.play(Create(interference_pattern))
        self.play(Write(constructive), Write(bright_label))
        self.wait(2)
```

---

## 굴절과 렌즈

### 스넬의 법칙

```python
class SnellsLaw(Scene):
    """[12물리03-02] 빛의 굴절"""
    def construct(self):
        title = Text("스넬의 법칙", font_size=36).to_edge(UP)
        
        # 경계면
        boundary = Line(LEFT * 4, RIGHT * 4, color=WHITE, stroke_width=2)
        
        # 매질 표시
        medium1 = Rectangle(width=8, height=2.5, fill_color=BLUE, fill_opacity=0.2)
        medium1.shift(UP * 1.25)
        medium2 = Rectangle(width=8, height=2.5, fill_color=BLUE, fill_opacity=0.5)
        medium2.shift(DOWN * 1.25)
        
        n1_label = MathTex("n_1").shift(LEFT * 3 + UP * 2)
        n2_label = MathTex("n_2 > n_1").shift(LEFT * 3 + DOWN * 2)
        
        # 법선
        normal = DashedLine(UP * 2.5, DOWN * 2.5, color=GRAY)
        normal_label = Text("법선", font_size=16).next_to(normal, RIGHT, buff=0.1).shift(UP * 2)
        
        # 입사광선
        incident = Arrow(
            UP * 2 + LEFT * 2, ORIGIN,
            color=YELLOW, buff=0, stroke_width=4
        )
        
        # 굴절광선 (n2 > n1이면 법선 쪽으로 꺾임)
        refracted = Arrow(
            ORIGIN, DOWN * 2 + RIGHT * 1,
            color=YELLOW, buff=0, stroke_width=4
        )
        
        # 각도 표시
        theta1_arc = Arc(radius=0.5, start_angle=PI/2, angle=-PI/4, color=RED)
        theta1_label = MathTex(r"\theta_1", color=RED).shift(UP * 0.8 + LEFT * 0.3)
        
        theta2_arc = Arc(radius=0.5, start_angle=-PI/2, angle=PI/6, color=GREEN)
        theta2_label = MathTex(r"\theta_2", color=GREEN).shift(DOWN * 0.8 + RIGHT * 0.3)
        
        # 스넬의 법칙 수식
        snell_eq = MathTex(
            r"n_1 \sin\theta_1 = n_2 \sin\theta_2"
        ).to_corner(UR)
        
        self.play(Write(title))
        self.play(FadeIn(medium1), FadeIn(medium2))
        self.play(Create(boundary))
        self.play(Write(n1_label), Write(n2_label))
        self.play(Create(normal), Write(normal_label))
        self.play(Create(incident))
        self.play(Create(refracted))
        self.play(Create(theta1_arc), Write(theta1_label))
        self.play(Create(theta2_arc), Write(theta2_label))
        self.play(Write(snell_eq))
        self.wait(2)
```

### 볼록렌즈의 상 형성

```python
class ConvexLensImage(Scene):
    """[12물리03-02] 볼록렌즈에 의한 상 형성"""
    def construct(self):
        title = Text("볼록렌즈의 광선 추적", font_size=36).to_edge(UP)
        
        # 광축
        optical_axis = Line(LEFT * 6, RIGHT * 6, color=GRAY, stroke_width=1)
        
        # 렌즈 (볼록)
        lens = Ellipse(width=0.3, height=3, color=BLUE, stroke_width=3)
        
        # 초점 (양쪽)
        f = 2  # 초점 거리
        f1 = Dot(LEFT * f, color=RED, radius=0.08)
        f2 = Dot(RIGHT * f, color=RED, radius=0.08)
        f1_label = MathTex("F", color=RED, font_size=24).next_to(f1, DOWN)
        f2_label = MathTex("F'", color=RED, font_size=24).next_to(f2, DOWN)
        
        # 물체 (화살표)
        object_dist = 3.5
        object_height = 1.2
        obj = Arrow(
            LEFT * object_dist, LEFT * object_dist + UP * object_height,
            color=GREEN, buff=0, stroke_width=4
        )
        obj_label = Text("물체", font_size=16).next_to(obj, UP)
        
        # 광선 추적
        # 1. 광축에 평행하게 입사 → 반대쪽 초점 통과
        ray1_in = Line(obj.get_end(), ORIGIN + UP * object_height, color=YELLOW)
        ray1_out = Line(ORIGIN + UP * object_height, RIGHT * 5 + DOWN * 1, color=YELLOW)
        
        # 2. 렌즈 중심 통과 → 직진
        ray2 = Line(obj.get_end(), RIGHT * 5 + DOWN * 0.5, color=ORANGE)
        
        # 3. 초점 통과 → 광축에 평행하게 나감
        ray3_in = Line(obj.get_end(), LEFT * f + UP * 0.5, color=RED)
        ray3_out = Line(LEFT * f + UP * 0.5, ORIGIN + UP * 0.5, color=RED)
        ray3_out2 = Line(ORIGIN + UP * 0.5, RIGHT * 5 + UP * 0.5, color=RED)
        
        # 상 (실상, 도립)
        image_dist = 2.5  # 1/f = 1/do + 1/di
        image_height = -0.9
        image = Arrow(
            RIGHT * image_dist, RIGHT * image_dist + DOWN * abs(image_height),
            color=PURPLE, buff=0, stroke_width=4
        )
        image_label = Text("상 (실상)", font_size=16).next_to(image, DOWN)
        
        # 렌즈 공식
        lens_eq = MathTex(
            r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}"
        ).to_corner(DR)
        
        self.play(Write(title))
        self.play(Create(optical_axis))
        self.play(Create(lens))
        self.play(Create(f1), Create(f2), Write(f1_label), Write(f2_label))
        self.play(Create(obj), Write(obj_label))
        
        # 광선 추적 애니메이션
        self.play(Create(ray1_in))
        self.play(Create(ray1_out))
        self.play(Create(ray2))
        self.play(Create(ray3_in))
        self.play(Create(ray3_out), Create(ray3_out2))
        
        self.play(Create(image), Write(image_label))
        self.play(Write(lens_eq))
        self.wait(2)
```

---

## 빛과 물질의 이중성

### 광전 효과

```python
class PhotoelectricEffect(Scene):
    """[12물리03-03] 광전 효과"""
    def construct(self):
        title = Text("광전 효과", font_size=36).to_edge(UP)
        
        # 금속판
        metal = Rectangle(width=4, height=0.5, fill_color=GRAY, fill_opacity=0.8)
        metal.shift(DOWN * 1)
        metal_label = Text("금속판", font_size=20).next_to(metal, DOWN)
        
        # 입사 광자
        photon = VGroup(
            Line(UP * 2 + LEFT * 1, metal.get_top() + LEFT * 0.5, color=YELLOW, stroke_width=3),
            MathTex(r"h\nu", color=YELLOW).shift(UP * 1.5 + LEFT * 1.5)
        )
        
        # 방출된 전자
        electron = Dot(color=BLUE, radius=0.1)
        electron.move_to(metal.get_top() + UP * 0.2)
        e_label = MathTex("e^-", color=BLUE, font_size=24).next_to(electron, RIGHT)
        
        # 운동 에너지 화살표
        ke_arrow = Arrow(
            metal.get_top() + UP * 0.3,
            metal.get_top() + UP * 1.8,
            color=RED, buff=0
        )
        ke_label = MathTex("KE", color=RED).next_to(ke_arrow, RIGHT)
        
        # 아인슈타인 광전 효과 방정식
        equation = MathTex(
            r"h\nu = W + KE_{max}"
        ).to_corner(UR)
        
        explanation = VGroup(
            MathTex(r"h\nu: \text{광자 에너지}"),
            MathTex(r"W: \text{일함수}"),
            MathTex(r"KE_{max}: \text{최대 운동 에너지}")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(equation, DOWN)
        
        # 문턱 진동수
        threshold = MathTex(
            r"\nu_0 = \frac{W}{h} \quad (\text{문턱 진동수})"
        ).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(metal), Write(metal_label))
        self.play(Create(photon))
        
        # 광자 흡수 후 전자 방출
        self.play(
            FadeOut(photon),
            Create(electron), Write(e_label)
        )
        self.play(
            electron.animate.shift(UP * 1.5),
            Create(ke_arrow), Write(ke_label)
        )
        
        self.play(Write(equation))
        self.play(Write(explanation))
        self.play(Write(threshold))
        self.wait(2)
```

### 드브로이 물질파

```python
class DeBroglieWave(Scene):
    """[12물리03-03] 물질의 파동성"""
    def construct(self):
        title = Text("드브로이 물질파", font_size=36).to_edge(UP)
        
        # 전자
        electron = Dot(color=BLUE, radius=0.15).shift(LEFT * 4)
        e_label = MathTex("e^-", color=BLUE).next_to(electron, UP)
        
        # 운동량 화살표
        momentum = Arrow(
            electron.get_right(),
            electron.get_right() + RIGHT * 1.5,
            color=RED, buff=0
        )
        p_label = MathTex(r"\vec{p}", color=RED).next_to(momentum, UP)
        
        # 물질파 (사인파)
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-1, 1, 0.5],
            x_length=6,
            y_length=2,
            tips=False
        ).shift(RIGHT * 1)
        
        wave = axes.plot(
            lambda x: np.sin(2 * PI * x / 1.5),  # 파장 1.5
            x_range=[0, 8],
            color=YELLOW
        )
        
        # 파장 표시
        wavelength_arrow = DoubleArrow(
            axes.c2p(0.75, -1.3), axes.c2p(2.25, -1.3),
            color=GREEN, buff=0
        )
        lambda_label = MathTex(r"\lambda", color=GREEN).next_to(wavelength_arrow, DOWN)
        
        # 드브로이 관계식
        de_broglie = MathTex(
            r"\lambda = \frac{h}{p} = \frac{h}{mv}"
        ).to_corner(UR)
        
        # 전자 현미경 응용
        application = VGroup(
            Text("응용: 전자 현미경", font_size=24),
            MathTex(r"\lambda_{electron} \ll \lambda_{visible}"),
            Text("더 높은 분해능", font_size=20)
        ).arrange(DOWN).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(electron), Write(e_label))
        self.play(Create(momentum), Write(p_label))
        self.play(Create(axes))
        self.play(Create(wave))
        self.play(Create(wavelength_arrow), Write(lambda_label))
        self.play(Write(de_broglie))
        self.play(Write(application))
        self.wait(2)
```

---

## 원자 구조와 에너지 준위

### 보어 원자 모형

```python
class BohrModel(Scene):
    """[12물리03-04] 보어의 수소 원자 모형"""
    def construct(self):
        title = Text("보어의 수소 원자 모형", font_size=36).to_edge(UP)
        
        # 핵
        nucleus = Dot(color=RED, radius=0.2)
        n_label = MathTex("+", color=WHITE).scale(0.8)
        
        # 전자 궤도 (양자화)
        orbits = VGroup()
        n_labels = VGroup()
        for n in [1, 2, 3, 4]:
            r = 0.5 + 0.5 * n
            orbit = Circle(radius=r, color=BLUE, stroke_width=1)
            label = MathTex(f"n={n}", font_size=20).move_to(orbit.get_right() + RIGHT * 0.3)
            orbits.add(orbit)
            n_labels.add(label)
        
        # 전자
        electron = Dot(color=YELLOW, radius=0.1)
        electron.move_to(orbits[0].point_at_angle(0))
        
        # 에너지 준위
        energy_levels = VGroup()
        level_labels = VGroup()
        for n in [1, 2, 3, 4]:
            E = -13.6 / n**2
            y = (E + 13.6) / 13.6 * 3 - 2  # 스케일 조정
            level = Line(LEFT * 1, RIGHT * 1, color=WHITE).shift(RIGHT * 4 + UP * y)
            label = MathTex(f"n={n}", font_size=20).next_to(level, LEFT)
            energy = MathTex(f"{E:.1f} eV", font_size=16).next_to(level, RIGHT)
            energy_levels.add(level)
            level_labels.add(VGroup(label, energy))
        
        # 광자 방출 (전이)
        transition_arrow = Arrow(
            energy_levels[2].get_center(),
            energy_levels[0].get_center(),
            color=YELLOW, buff=0.1
        )
        photon_label = MathTex(r"h\nu", color=YELLOW).next_to(transition_arrow, RIGHT)
        
        # 에너지 양자화 수식
        energy_eq = MathTex(
            r"E_n = -\frac{13.6}{n^2} \text{ eV}"
        ).to_corner(UL)
        
        self.play(Write(title))
        self.play(Create(nucleus), Write(n_label))
        self.play(Create(orbits))
        self.play(Write(n_labels))
        self.play(Create(electron))
        
        # 전자 궤도 운동
        self.play(
            MoveAlongPath(electron, orbits[0]),
            run_time=2
        )
        
        # 에너지 준위 다이어그램
        self.play(Create(energy_levels), Write(level_labels))
        self.play(Create(transition_arrow), Write(photon_label))
        self.play(Write(energy_eq))
        self.wait(2)
```

### 수소 스펙트럼

```python
class HydrogenSpectrum(Scene):
    """[12물리03-04] 수소 원자의 선스펙트럼"""
    def construct(self):
        title = Text("수소 원자의 선스펙트럼", font_size=36).to_edge(UP)
        
        # 스펙트럼 배경 (가시광선 범위)
        spectrum_bg = Rectangle(width=8, height=1.5, fill_color=BLACK, fill_opacity=1)
        spectrum_bg.shift(DOWN * 0.5)
        
        # 발머 계열 (가시광선)
        # 656nm (빨강), 486nm (청록), 434nm (파랑), 410nm (보라)
        wavelengths = [(656, RED), (486, TEAL), (434, BLUE), (410, PURPLE)]
        
        spectral_lines = VGroup()
        for wl, color in wavelengths:
            x = (wl - 400) / (700 - 400) * 8 - 4
            line = Line(UP * 0.6 + RIGHT * x, DOWN * 0.6 + RIGHT * x,
                       color=color, stroke_width=4)
            label = MathTex(f"{wl}", font_size=16).next_to(line, UP)
            spectral_lines.add(VGroup(line, label))
        
        spectral_lines.shift(DOWN * 0.5)
        
        # 에너지 전이 다이어그램
        levels = VGroup()
        for n in [2, 3, 4, 5, 6]:
            y = 2 - 1/n**2 * 4
            level = Line(LEFT * 0.8, RIGHT * 0.8, color=WHITE)
            level.shift(LEFT * 5 + UP * y)
            label = MathTex(f"n={n}", font_size=16).next_to(level, LEFT)
            levels.add(VGroup(level, label))
        
        # 전이 화살표 (n=3,4,5,6 → n=2, 발머 계열)
        transitions = VGroup()
        colors = [RED, TEAL, BLUE, PURPLE]
        for i, (start_n, color) in enumerate(zip([3, 4, 5, 6], colors)):
            start_y = 2 - 1/start_n**2 * 4
            end_y = 2 - 1/4 * 4  # n=2
            arrow = Arrow(
                LEFT * 5 + UP * start_y,
                LEFT * 5 + UP * end_y,
                color=color, buff=0.15
            )
            transitions.add(arrow)
        
        # 발머 계열 수식
        balmer = MathTex(
            r"\frac{1}{\lambda} = R_H\left(\frac{1}{2^2} - \frac{1}{n^2}\right)"
        ).scale(0.8).to_corner(DR)
        
        series_label = Text("발머 계열 (n=2로 전이)", font_size=20).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(spectrum_bg))
        self.play(Create(spectral_lines), run_time=2)
        self.play(Create(levels))
        self.play(Create(transitions))
        self.play(Write(balmer))
        self.play(Write(series_label))
        self.wait(2)
```

---

## 반도체와 에너지띠

### 에너지띠 구조

```python
class EnergyBands(Scene):
    """[12물리03-05] 고체의 에너지띠 구조"""
    def construct(self):
        title = Text("에너지띠 구조", font_size=36).to_edge(UP)
        
        # 도체
        conductor = VGroup(
            Rectangle(width=1.5, height=1.5, fill_color=BLUE, fill_opacity=0.6),
            Rectangle(width=1.5, height=1, fill_color=BLUE, fill_opacity=0.3).shift(UP * 1.25),
            Text("도체", font_size=20)
        )
        conductor[0].shift(DOWN * 0.5)
        conductor[1].shift(DOWN * 0.5)
        conductor[2].shift(DOWN * 1.8)
        conductor.shift(LEFT * 4)
        
        # 반도체
        semiconductor = VGroup(
            Rectangle(width=1.5, height=1.2, fill_color=GREEN, fill_opacity=0.6),
            Rectangle(width=1.5, height=0.3, fill_color=WHITE, fill_opacity=0),  # 작은 갭
            Rectangle(width=1.5, height=1, fill_color=GREEN, fill_opacity=0.3),
            Text("반도체", font_size=20)
        )
        semiconductor[0].shift(DOWN * 0.6)
        semiconductor[2].shift(UP * 1)
        semiconductor[3].shift(DOWN * 1.8)
        
        # 부도체
        insulator = VGroup(
            Rectangle(width=1.5, height=1.2, fill_color=RED, fill_opacity=0.6),
            Rectangle(width=1.5, height=1, fill_color=RED, fill_opacity=0.3).shift(UP * 2),
            Text("부도체", font_size=20)
        )
        insulator[0].shift(DOWN * 0.5)
        insulator[1].shift(DOWN * 0.5)
        insulator[2].shift(DOWN * 1.8)
        insulator.shift(RIGHT * 4)
        
        # 띠 라벨
        valence_label = Text("가전자띠", font_size=16, color=BLUE)
        conduction_label = Text("전도띠", font_size=16, color=BLUE)
        gap_label = Text("띠틈", font_size=14, color=YELLOW)
        
        # 에너지축
        energy_axis = Arrow(LEFT * 6 + DOWN * 2, LEFT * 6 + UP * 2, 
                           color=WHITE, buff=0)
        e_label = MathTex("E").next_to(energy_axis, UP)
        
        self.play(Write(title))
        self.play(Create(energy_axis), Write(e_label))
        self.play(Create(conductor))
        self.play(Create(semiconductor))
        self.play(Create(insulator))
        self.wait(2)
```

### p-n 접합 다이오드

```python
class PNJunction(Scene):
    """[12물리03-05] p-n 접합 다이오드"""
    def construct(self):
        title = Text("p-n 접합 다이오드", font_size=36).to_edge(UP)
        
        # p형 반도체
        p_type = Rectangle(width=3, height=2, fill_color=RED, fill_opacity=0.3)
        p_type.shift(LEFT * 1.5)
        p_label = Text("p형", font_size=24).move_to(p_type)
        
        # n형 반도체
        n_type = Rectangle(width=3, height=2, fill_color=BLUE, fill_opacity=0.3)
        n_type.shift(RIGHT * 1.5)
        n_label = Text("n형", font_size=24).move_to(n_type)
        
        # 공핍층
        depletion = Rectangle(width=0.8, height=2, fill_color=WHITE, fill_opacity=0.5)
        depletion_label = Text("공핍층", font_size=16).next_to(depletion, UP)
        
        # 정공 (p형)
        holes = VGroup(*[
            Circle(radius=0.1, color=RED, fill_opacity=0.8).move_to(
                LEFT * (2 + i * 0.4) + UP * (0.6 - j * 0.4)
            )
            for i in range(3) for j in range(3)
        ])
        plus_signs = VGroup(*[
            MathTex("+", font_size=16, color=WHITE).move_to(hole)
            for hole in holes
        ])
        
        # 전자 (n형)
        electrons = VGroup(*[
            Circle(radius=0.1, color=BLUE, fill_opacity=0.8).move_to(
                RIGHT * (2 + i * 0.4) + UP * (0.6 - j * 0.4)
            )
            for i in range(3) for j in range(3)
        ])
        minus_signs = VGroup(*[
            MathTex("-", font_size=16, color=WHITE).move_to(electron)
            for electron in electrons
        ])
        
        # 순방향 바이어스
        forward_bias = VGroup(
            Text("순방향 바이어스", font_size=20),
            Arrow(LEFT * 2, RIGHT * 2, color=GREEN),
            Text("전류 흐름 O", font_size=16, color=GREEN)
        ).arrange(DOWN).to_corner(DL)
        
        # 역방향 바이어스
        reverse_bias = VGroup(
            Text("역방향 바이어스", font_size=20),
            Arrow(RIGHT * 2, LEFT * 2, color=RED),
            Text("전류 흐름 X", font_size=16, color=RED)
        ).arrange(DOWN).to_corner(DR)
        
        self.play(Write(title))
        self.play(Create(p_type), Create(n_type))
        self.play(Write(p_label), Write(n_label))
        self.play(Create(depletion), Write(depletion_label))
        self.play(Create(holes), Write(plus_signs))
        self.play(Create(electrons), Write(minus_signs))
        self.play(Write(forward_bias))
        self.play(Write(reverse_bias))
        self.wait(2)
```

---

## 특수 상대성 이론

### 시간 지연

```python
class TimeDilation(Scene):
    """[12물리03-06] 특수 상대성 이론 - 시간 지연"""
    def construct(self):
        title = Text("시간 지연", font_size=36).to_edge(UP)
        
        # 정지 관찰자의 시계
        rest_clock = VGroup(
            Circle(radius=0.8, color=WHITE),
            Line(ORIGIN, UP * 0.6, color=WHITE, stroke_width=4),
            Text("정지 관찰자", font_size=20)
        )
        rest_clock[2].next_to(rest_clock[0], DOWN)
        rest_clock.shift(LEFT * 3)
        
        # 운동 관찰자의 시계 (우주선)
        moving_clock = VGroup(
            Circle(radius=0.8, color=YELLOW),
            Line(ORIGIN, UP * 0.6, color=YELLOW, stroke_width=4),
            Text("운동 관찰자", font_size=20)
        )
        moving_clock[2].next_to(moving_clock[0], DOWN)
        moving_clock.shift(RIGHT * 3)
        
        # 속도 표시
        velocity = MathTex(r"v \approx c").next_to(moving_clock, UP, buff=0.5)
        v_arrow = Arrow(RIGHT * 2, RIGHT * 4, color=BLUE, buff=0)
        
        # 시간 지연 수식
        dilation_eq = MathTex(
            r"\Delta t = \gamma \Delta t_0 = \frac{\Delta t_0}{\sqrt{1 - \frac{v^2}{c^2}}}"
        ).scale(0.8).to_corner(UR)
        
        # 로렌츠 인자
        gamma = MathTex(r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}} > 1").next_to(dilation_eq, DOWN)
        
        # 결론
        conclusion = Text("운동하는 시계는 느리게 간다", font_size=24, color=YELLOW).to_corner(DL)
        
        self.play(Write(title))
        self.play(Create(rest_clock))
        self.play(Create(moving_clock), Create(v_arrow), Write(velocity))
        
        # 시간 경과 애니메이션 (정지 시계는 빠르게, 운동 시계는 느리게)
        self.play(
            Rotate(rest_clock[1], angle=-2*PI, about_point=rest_clock[0].get_center()),
            Rotate(moving_clock[1], angle=-PI, about_point=moving_clock[0].get_center()),
            run_time=3
        )
        
        self.play(Write(dilation_eq))
        self.play(Write(gamma))
        self.play(Write(conclusion))
        self.wait(2)
```

---

## 유틸리티 함수

```python
def create_wave(axes, wavelength, amplitude=1, phase=0, color=BLUE):
    """사인파 생성"""
    k = 2 * PI / wavelength
    return axes.plot(
        lambda x: amplitude * np.sin(k * x + phase),
        color=color
    )

def create_energy_level(y_pos, width=2, color=WHITE, n_label=None):
    """에너지 준위선 생성"""
    level = Line(LEFT * width/2, RIGHT * width/2, color=color)
    level.shift(UP * y_pos)
    if n_label:
        label = MathTex(n_label, font_size=20).next_to(level, LEFT)
        return VGroup(level, label)
    return level

def create_photon_arrow(start, end, color=YELLOW, label=r"h\nu"):
    """광자 화살표 생성"""
    arrow = Arrow(start, end, color=color, buff=0)
    text = MathTex(label, color=color).next_to(arrow, RIGHT, buff=0.1)
    return VGroup(arrow, text)

def create_lens(height=3, width=0.4, lens_type="convex"):
    """렌즈 생성"""
    if lens_type == "convex":
        return Ellipse(width=width, height=height, color=BLUE, stroke_width=3)
    else:  # concave
        # 오목렌즈는 더 복잡한 형태가 필요
        pass
```

## 참고 자료

- [Manim 파동 예제](https://docs.manim.community/en/stable/examples.html)
- [광학 시뮬레이션](https://phet.colorado.edu/en/simulations/filter?subjects=physics&type=html)
- [양자역학 시각화](https://www.falstad.com/qm1d/)
