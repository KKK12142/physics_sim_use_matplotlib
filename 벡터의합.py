from manim import *
import numpy as np


class VectorAddition(Scene):
    # ── 폰트 크기 ──
    FONT_TITLE = 80
    FONT_SUBTITLE = 28
    FONT_LABEL = 36
    FONT_FORMULA = 36
    FONT_FORMULA_SM = 30

    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_perpendicular_addition()
        self.clear_screen()
        self.phase2_angled_addition_obtuse()
        self.clear_screen()
        self.phase3_angled_addition_acute()
        self.clear_screen()
        self.phase4_decomposition_q1()
        self.clear_screen()
        self.phase5_decomposition_q3()
        self.clear_screen()
        self.phase6_decomposition_q2()
        self.clear_screen()
        self.outro()

    # ═══════════ Utilities ═══════════

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    def _make_axes(self, x_range, y_range):
        """사분면에 맞춰 축 범위를 받아 생성."""
        x_span = x_range[1] - x_range[0]
        y_span = y_range[1] - y_range[0]
        # 화면 비율 16:9 → 가로 12, 세로 7 정도로 스케일
        aspect = x_span / y_span
        if aspect > 12 / 7:
            x_length = 12
            y_length = 12 / aspect
        else:
            y_length = 7
            x_length = 7 * aspect
        axes = Axes(
            x_range=[x_range[0], x_range[1], 1],
            y_range=[y_range[0], y_range[1], 1],
            x_length=x_length,
            y_length=y_length,
            axis_config={"include_tip": True, "tip_length": 0.2},
        ).set_color(GRAY)
        return axes

    def _make_arrow(self, start, end, color, stroke_width=6):
        return Arrow(
            start, end, color=color, buff=0,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.15,
        )

    # ═══════════ Phase 0: Intro ═══════════

    def intro(self):
        title = Text("벡터의 합과 분해", font_size=self.FONT_TITLE, color=WHITE)
        formula = MathTex(r"\vec{a} + \vec{b}", font_size=48, color=YELLOW)
        VGroup(title, formula).arrange(DOWN, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(formula, shift=UP * 0.3))
        self.wait(1.5)

    # ═══════════ Phase 1: 수직 벡터 합 ═══════════

    def phase1_perpendicular_addition(self):
        # ── 1. 축과 제목 (Q1 중심) ──
        subtitle = Text("꼬리-머리 방법", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-1, 5), y_range=(-1, 4))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 벡터 a (x축), 벡터 b (y축) ──
        vec_a_end = axes.c2p(3, 0)
        vec_a = self._make_arrow(origin, vec_a_end, RED)
        label_a = MathTex(r"\vec{a}", color=RED, font_size=self.FONT_LABEL).next_to(vec_a, DOWN, buff=0.2)

        vec_b_end = axes.c2p(0, 2)
        vec_b = self._make_arrow(origin, vec_b_end, BLUE)
        label_b = MathTex(r"\vec{b}", color=BLUE, font_size=self.FONT_LABEL).next_to(vec_b, LEFT, buff=0.2)

        self.play(GrowArrow(vec_a), Write(label_a), run_time=1)
        self.play(GrowArrow(vec_b), Write(label_b), run_time=1)
        self.wait(0.5)

        # ── 3. 직각 표시 ──
        right_angle = RightAngle(
            Line(origin, vec_a_end), Line(origin, vec_b_end),
            color=YELLOW, stroke_width=3, length=0.3,
        )
        self.play(Create(right_angle))
        self.wait(0.3)

        # ── 4. b를 a 끝으로 평행이동 ──
        vec_b_shifted = self._make_arrow(vec_a_end, axes.c2p(3, 2), BLUE)
        vec_b_shifted.set_opacity(0.6)
        vec_b_shifted_dashed = DashedVMobject(vec_b_shifted, num_dashes=10)
        self.play(Create(vec_b_shifted_dashed), run_time=1)

        # ── 5. 합벡터 ──
        vec_sum_end = axes.c2p(3, 2)
        vec_sum = Arrow(
            origin, vec_sum_end, color=GREEN, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_sum = MathTex(
            r"\vec{a} + \vec{b}", color=GREEN, font_size=self.FONT_LABEL,
        ).next_to(vec_sum.get_center(), UP + LEFT, buff=0.2)

        self.play(GrowArrow(vec_sum), run_time=1.5)
        self.play(Write(label_sum))
        self.wait(0.5)

        # ── 6. 크기 수식 (큰 폰트, 박스 없이) ──
        magnitude_formula = MathTex(
            r"|\vec{a}+\vec{b}| = \sqrt{a^2 + b^2}",
            color=YELLOW, font_size=self.FONT_FORMULA,
        )
        magnitude_formula.to_edge(DOWN, buff=0.5)
        self.play(Write(magnitude_formula))
        self.wait(1.5)

    # ═══════════ Phase 2: 비스듬한 벡터 합 (둔각 사이) ═══════════

    def phase2_angled_addition_obtuse(self):
        # ── 1. 축과 제목 (Q1+Q2) ──
        subtitle = Text("평행사변형 법칙", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-3, 5), y_range=(-1, 4))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 벡터 a (30°), 벡터 b (120°) → 사잇각 90° ──
        ANGLE_A = 30 * DEGREES
        ANGLE_B = 120 * DEGREES
        LEN_A, LEN_B = 3.0, 2.0

        vec_a_end = axes.c2p(LEN_A * np.cos(ANGLE_A), LEN_A * np.sin(ANGLE_A))
        vec_a = self._make_arrow(origin, vec_a_end, RED)
        label_a = MathTex(r"\vec{a}", color=RED, font_size=self.FONT_LABEL).next_to(vec_a.get_center(), DOWN, buff=0.15)

        vec_b_end = axes.c2p(LEN_B * np.cos(ANGLE_B), LEN_B * np.sin(ANGLE_B))
        vec_b = self._make_arrow(origin, vec_b_end, BLUE)
        label_b = MathTex(r"\vec{b}", color=BLUE, font_size=self.FONT_LABEL).next_to(vec_b.get_center(), UP + LEFT, buff=0.15)

        self.play(GrowArrow(vec_a), Write(label_a), run_time=1)
        self.play(GrowArrow(vec_b), Write(label_b), run_time=1)
        self.wait(0.5)

        # ── 3. 평행이동 벡터 (점선) ──
        vec_b_shifted_end = np.array(vec_a_end) + np.array(vec_b_end) - np.array(origin)
        vec_b_shifted = self._make_arrow(vec_a_end, vec_b_shifted_end, BLUE)
        vec_b_shifted.set_opacity(0.6)
        vec_b_shifted_dashed = DashedVMobject(vec_b_shifted, num_dashes=10)

        vec_a_shifted_end = np.array(vec_b_end) + np.array(vec_a_end) - np.array(origin)
        vec_a_shifted = self._make_arrow(vec_b_end, vec_a_shifted_end, RED)
        vec_a_shifted.set_opacity(0.6)
        vec_a_shifted_dashed = DashedVMobject(vec_a_shifted, num_dashes=10)

        self.play(Create(vec_b_shifted_dashed), Create(vec_a_shifted_dashed), run_time=1)

        # ── 4. 평행사변형 하이라이트 ──
        parallelogram = Polygon(
            origin, vec_a_end, vec_b_shifted_end, vec_b_end,
            color=YELLOW, fill_color=YELLOW, fill_opacity=0.1,
            stroke_width=0,
        )
        self.play(FadeIn(parallelogram), run_time=0.5)

        # ── 5. 합벡터 ──
        sum_x = LEN_A * np.cos(ANGLE_A) + LEN_B * np.cos(ANGLE_B)
        sum_y = LEN_A * np.sin(ANGLE_A) + LEN_B * np.sin(ANGLE_B)
        vec_sum_end = axes.c2p(sum_x, sum_y)
        vec_sum = Arrow(
            origin, vec_sum_end, color=GREEN, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_sum = MathTex(
            r"\vec{a} + \vec{b}", color=GREEN, font_size=self.FONT_LABEL,
        ).next_to(vec_sum.get_center(), RIGHT, buff=0.2)

        self.play(GrowArrow(vec_sum), run_time=1.5)
        self.play(Write(label_sum))
        self.wait(1.5)

    # ═══════════ Phase 3: 비스듬한 벡터 합 (예각 사이) ═══════════

    def phase3_angled_addition_acute(self):
        # ── 1. 축과 제목 (Q1 중심) ──
        subtitle = Text("예각 사이 벡터의 합", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-1, 7), y_range=(-1, 5))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 벡터 a (20°), 벡터 b (60°) → 사잇각 40° ──
        ANGLE_A = 20 * DEGREES
        ANGLE_B = 60 * DEGREES
        LEN_A, LEN_B = 4.0, 3.0

        vec_a_end = axes.c2p(LEN_A * np.cos(ANGLE_A), LEN_A * np.sin(ANGLE_A))
        vec_a = self._make_arrow(origin, vec_a_end, RED)
        label_a = MathTex(r"\vec{a}", color=RED, font_size=self.FONT_LABEL).next_to(vec_a.get_center(), DOWN, buff=0.15)

        vec_b_end = axes.c2p(LEN_B * np.cos(ANGLE_B), LEN_B * np.sin(ANGLE_B))
        vec_b = self._make_arrow(origin, vec_b_end, BLUE)
        label_b = MathTex(r"\vec{b}", color=BLUE, font_size=self.FONT_LABEL).next_to(vec_b.get_center(), LEFT, buff=0.15)

        self.play(GrowArrow(vec_a), Write(label_a), run_time=1)
        self.play(GrowArrow(vec_b), Write(label_b), run_time=1)
        self.wait(0.5)

        # ── 3. 사잇각 표시 ──
        angle_arc = Arc(
            radius=0.8, start_angle=ANGLE_A, angle=ANGLE_B - ANGLE_A,
            color=ORANGE, stroke_width=3, arc_center=origin,
        )
        angle_label = MathTex(r"40^{\circ}", color=ORANGE, font_size=24)
        mid_angle = (ANGLE_A + ANGLE_B) / 2
        angle_label.move_to(origin + 1.15 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(0.3)

        # ── 4. 평행이동 + 평행사변형 ──
        vec_b_shifted_end = np.array(vec_a_end) + np.array(vec_b_end) - np.array(origin)
        vec_b_shifted = self._make_arrow(vec_a_end, vec_b_shifted_end, BLUE)
        vec_b_shifted.set_opacity(0.6)
        vec_b_shifted_dashed = DashedVMobject(vec_b_shifted, num_dashes=10)

        vec_a_shifted_end = np.array(vec_b_end) + np.array(vec_a_end) - np.array(origin)
        vec_a_shifted = self._make_arrow(vec_b_end, vec_a_shifted_end, RED)
        vec_a_shifted.set_opacity(0.6)
        vec_a_shifted_dashed = DashedVMobject(vec_a_shifted, num_dashes=10)

        parallelogram = Polygon(
            origin, vec_a_end, vec_b_shifted_end, vec_b_end,
            color=YELLOW, fill_color=YELLOW, fill_opacity=0.1,
            stroke_width=0,
        )

        self.play(
            Create(vec_b_shifted_dashed), Create(vec_a_shifted_dashed),
            FadeIn(parallelogram),
            run_time=1,
        )

        # ── 5. 합벡터 ──
        sum_x = LEN_A * np.cos(ANGLE_A) + LEN_B * np.cos(ANGLE_B)
        sum_y = LEN_A * np.sin(ANGLE_A) + LEN_B * np.sin(ANGLE_B)
        vec_sum_end = axes.c2p(sum_x, sum_y)
        vec_sum = Arrow(
            origin, vec_sum_end, color=GREEN, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_sum = MathTex(
            r"\vec{a} + \vec{b}", color=GREEN, font_size=self.FONT_LABEL,
        ).next_to(vec_sum.get_center(), UP + RIGHT, buff=0.2)

        self.play(GrowArrow(vec_sum), run_time=1.5)
        self.play(Write(label_sum))
        self.wait(1.5)

    # ═══════════ Phase 4: 성분 분해 (1사분면, 50°) ═══════════

    def phase4_decomposition_q1(self):
        # ── 1. 축과 제목 (Q1 확대) ──
        subtitle = Text("벡터의 성분 분해", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-1, 5), y_range=(-1, 4))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 대각선 벡터 v ──
        ANGLE_DIAG = 50 * DEGREES
        DIAG_LENGTH = 3.0
        vx_val = DIAG_LENGTH * np.cos(ANGLE_DIAG)
        vy_val = DIAG_LENGTH * np.sin(ANGLE_DIAG)
        vec_diag_end = axes.c2p(vx_val, vy_val)

        vec_v = Arrow(
            origin, vec_diag_end, color=PURPLE, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_v = MathTex(r"\vec{v}", color=PURPLE, font_size=40).next_to(vec_v.get_center(), UP + LEFT, buff=0.2)

        self.play(GrowArrow(vec_v), Write(label_v), run_time=1.5)
        self.wait(0.5)

        # ── 3. 각도 표시 ──
        angle_arc = Arc(radius=0.6, start_angle=0, angle=ANGLE_DIAG, color=ORANGE, stroke_width=3)
        angle_arc.move_arc_center_to(origin)
        angle_label = MathTex(r"\theta", color=ORANGE, font_size=self.FONT_FORMULA_SM).move_to(
            origin + 0.9 * np.array([np.cos(ANGLE_DIAG / 2), np.sin(ANGLE_DIAG / 2), 0])
        )
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(0.3)

        # ── 4. x성분 분해 ──
        vec_v_copy_x = vec_v.copy().set_color(RED)
        self.play(Create(vec_v_copy_x), run_time=0.5)

        proj_line_x = DashedLine(vec_diag_end, axes.c2p(vx_val, 0), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_x), run_time=0.5)

        vec_vx = self._make_arrow(origin, axes.c2p(vx_val, 0), RED)
        label_vx = MathTex(r"v_x", color=RED, font_size=self.FONT_FORMULA_SM).next_to(vec_vx, DOWN, buff=0.15)

        self.play(Transform(vec_v_copy_x, vec_vx), run_time=1)
        self.play(Write(label_vx))

        formula_vx = MathTex(r"v_x = |\vec{v}| \cos\theta", color=RED, font_size=self.FONT_FORMULA)
        formula_vx.to_corner(UL, buff=0.8).shift(DOWN * 1.2)
        self.play(Write(formula_vx))
        self.wait(0.5)

        # ── 5. y성분 분해 ──
        vec_v_copy_y = vec_v.copy().set_color(BLUE)
        self.play(Create(vec_v_copy_y), run_time=0.5)

        proj_line_y = DashedLine(vec_diag_end, axes.c2p(0, vy_val), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_y), run_time=0.5)

        vec_vy = self._make_arrow(origin, axes.c2p(0, vy_val), BLUE)
        label_vy = MathTex(r"v_y", color=BLUE, font_size=self.FONT_FORMULA_SM).next_to(vec_vy, LEFT, buff=0.15)

        self.play(Transform(vec_v_copy_y, vec_vy), run_time=1)
        self.play(Write(label_vy))

        formula_vy = MathTex(r"v_y = |\vec{v}| \sin\theta", color=BLUE, font_size=self.FONT_FORMULA)
        formula_vy.next_to(formula_vx, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(formula_vy))
        self.wait(0.5)

        # ── 6. 최종 수식 ──
        final_formula = MathTex(
            r"\vec{v} = v_x \hat{i} + v_y \hat{j}", color=PURPLE, font_size=self.FONT_FORMULA,
        )
        final_formula.next_to(formula_vy, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(final_formula))
        self.wait(0.5)

        pythagoras = MathTex(
            r"|\vec{v}| = \sqrt{v_x^2 + v_y^2}", color=YELLOW, font_size=self.FONT_FORMULA,
        )
        pythagoras.next_to(final_formula, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(pythagoras))
        self.wait(1.5)

    # ═══════════ Phase 5: 성분 분해 (3사분면, 210°) ═══════════

    def phase5_decomposition_q3(self):
        # ── 1. 축과 제목 (Q3 확대) ──
        subtitle = Text("성분 분해 (제3사분면)", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-5, 1), y_range=(-4, 1))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 대각선 벡터 v (210°) ──
        ANGLE_DIAG = 210 * DEGREES
        DIAG_LENGTH = 3.5
        vx_val = DIAG_LENGTH * np.cos(ANGLE_DIAG)
        vy_val = DIAG_LENGTH * np.sin(ANGLE_DIAG)
        vec_diag_end = axes.c2p(vx_val, vy_val)

        vec_v = Arrow(
            origin, vec_diag_end, color=PURPLE, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_v = MathTex(r"\vec{v}", color=PURPLE, font_size=40).next_to(vec_v.get_center(), DOWN + LEFT, buff=0.2)

        self.play(GrowArrow(vec_v), Write(label_v), run_time=1.5)
        self.wait(0.5)

        # ── 3. 각도 표시 (참조각 30°) ──
        angle_arc = Arc(
            radius=0.8, start_angle=PI, angle=PI / 6,
            color=ORANGE, stroke_width=3, arc_center=origin,
        )
        angle_label = MathTex(r"30^{\circ}", color=ORANGE, font_size=24)
        angle_label.next_to(angle_arc, LEFT, buff=0.15)

        self.play(FadeIn(angle_arc), Write(angle_label))
        self.wait(0.3)

        # ── 4. x성분 분해 ──
        vec_v_copy_x = vec_v.copy().set_color(RED)
        self.play(Create(vec_v_copy_x), run_time=0.5)

        proj_line_x = DashedLine(vec_diag_end, axes.c2p(vx_val, 0), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_x), run_time=0.5)

        vec_vx = self._make_arrow(origin, axes.c2p(vx_val, 0), RED)
        label_vx = MathTex(r"v_x", color=RED, font_size=self.FONT_FORMULA_SM).next_to(vec_vx, UP, buff=0.15)

        self.play(Transform(vec_v_copy_x, vec_vx), run_time=1)
        self.play(Write(label_vx))

        formula_vx = MathTex(
            r"v_x = -|\vec{v}| \cos 30^{\circ}", color=RED, font_size=self.FONT_FORMULA,
        )
        formula_vx.to_corner(UL, buff=0.8).shift(DOWN * 3.0)
        self.play(Write(formula_vx))
        self.wait(0.5)

        # ── 5. y성분 분해 ──
        vec_v_copy_y = vec_v.copy().set_color(BLUE)
        self.play(Create(vec_v_copy_y), run_time=0.5)

        proj_line_y = DashedLine(vec_diag_end, axes.c2p(0, vy_val), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_y), run_time=0.5)

        vec_vy = self._make_arrow(origin, axes.c2p(0, vy_val), BLUE)
        label_vy = MathTex(r"v_y", color=BLUE, font_size=self.FONT_FORMULA_SM).next_to(vec_vy, RIGHT, buff=0.15)

        self.play(Transform(vec_v_copy_y, vec_vy), run_time=1)
        self.play(Write(label_vy))

        formula_vy = MathTex(
            r"v_y = -|\vec{v}| \sin 30^{\circ}", color=BLUE, font_size=self.FONT_FORMULA,
        )
        formula_vy.next_to(formula_vx, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(formula_vy))
        self.wait(0.5)

        # ── 6. 최종 수식 ──
        final_formula = MathTex(
            r"\vec{v} = v_x \hat{i} + v_y \hat{j}", color=PURPLE, font_size=self.FONT_FORMULA,
        )
        final_formula.next_to(formula_vy, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(final_formula))
        self.wait(0.5)

        pythagoras = MathTex(
            r"|\vec{v}| = \sqrt{v_x^2 + v_y^2}", color=YELLOW, font_size=self.FONT_FORMULA,
        )
        pythagoras.next_to(final_formula, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(pythagoras))
        self.wait(1.5)

    # ═══════════ Phase 6: 성분 분해 (2사분면, 135°) ═══════════

    def phase6_decomposition_q2(self):
        # ── 1. 축과 제목 (Q2 확대) ──
        subtitle = Text("성분 분해 (제2사분면)", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        axes = self._make_axes(x_range=(-4, 1), y_range=(-1, 4))
        self.play(Write(subtitle), Create(axes), run_time=1)

        origin = axes.c2p(0, 0)

        # ── 2. 대각선 벡터 v (135°) ──
        ANGLE_DIAG = 135 * DEGREES
        DIAG_LENGTH = 3.0
        vx_val = DIAG_LENGTH * np.cos(ANGLE_DIAG)
        vy_val = DIAG_LENGTH * np.sin(ANGLE_DIAG)
        vec_diag_end = axes.c2p(vx_val, vy_val)

        vec_v = Arrow(
            origin, vec_diag_end, color=PURPLE, buff=0,
            stroke_width=8, max_tip_length_to_length_ratio=0.12,
        )
        label_v = MathTex(r"\vec{v}", color=PURPLE, font_size=40).next_to(vec_v.get_center(), UP + LEFT, buff=0.2).shift(UP * 0.4)

        self.play(GrowArrow(vec_v), Write(label_v), run_time=1.5)
        self.wait(0.5)

        # ── 3. 각도 표시 (참조각 45°) ──
        angle_arc = Arc(
            radius=0.7, start_angle=PI / 2, angle=PI / 4,
            color=ORANGE, stroke_width=3, arc_center=origin,
        )
        angle_label = MathTex(r"45^{\circ}", color=ORANGE, font_size=24)
        angle_label.move_to(origin + 1.05 * np.array([np.cos(112.5 * DEGREES), np.sin(112.5 * DEGREES), 0]))

        self.play(FadeIn(angle_arc), Write(angle_label))
        self.wait(0.3)

        # ── 4. x성분 분해 ──
        vec_v_copy_x = vec_v.copy().set_color(RED)
        self.play(Create(vec_v_copy_x), run_time=0.5)

        proj_line_x = DashedLine(vec_diag_end, axes.c2p(vx_val, 0), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_x), run_time=0.5)

        vec_vx = self._make_arrow(origin, axes.c2p(vx_val, 0), RED)
        label_vx = MathTex(r"v_x", color=RED, font_size=self.FONT_FORMULA_SM).next_to(vec_vx, DOWN, buff=0.15)

        self.play(Transform(vec_v_copy_x, vec_vx), run_time=1)
        self.play(Write(label_vx))

        formula_vx = MathTex(
            r"v_x = -|\vec{v}| \cos 45^{\circ}", color=RED, font_size=self.FONT_FORMULA,
        )
        formula_vx.to_corner(UL, buff=0.8).shift(DOWN * 1.2)
        self.play(Write(formula_vx))
        self.wait(0.5)

        # ── 5. y성분 분해 ──
        vec_v_copy_y = vec_v.copy().set_color(BLUE)
        self.play(Create(vec_v_copy_y), run_time=0.5)

        proj_line_y = DashedLine(vec_diag_end, axes.c2p(0, vy_val), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_y), run_time=0.5)

        vec_vy = self._make_arrow(origin, axes.c2p(0, vy_val), BLUE)
        label_vy = MathTex(r"v_y", color=BLUE, font_size=self.FONT_FORMULA_SM).next_to(vec_vy, RIGHT, buff=0.15)

        self.play(Transform(vec_v_copy_y, vec_vy), run_time=1)
        self.play(Write(label_vy))

        formula_vy = MathTex(
            r"v_y = |\vec{v}| \sin 45^{\circ}", color=BLUE, font_size=self.FONT_FORMULA,
        )
        formula_vy.next_to(formula_vx, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(formula_vy))
        self.wait(0.5)

        # ── 6. 최종 수식 ──
        final_formula = MathTex(
            r"\vec{v} = v_x \hat{i} + v_y \hat{j}", color=PURPLE, font_size=self.FONT_FORMULA,
        )
        final_formula.next_to(formula_vy, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(final_formula))
        self.wait(0.5)

        pythagoras = MathTex(
            r"|\vec{v}| = \sqrt{v_x^2 + v_y^2}", color=YELLOW, font_size=self.FONT_FORMULA,
        )
        pythagoras.next_to(final_formula, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(pythagoras))
        self.wait(1.5)

    # ═══════════ Phase 7: Outro ═══════════

    def outro(self):
        summary = VGroup(
            MathTex(r"\vec{a}+\vec{b} : \text{tail-to-head / parallelogram}", font_size=self.FONT_FORMULA, color=GREEN),
            MathTex(r"v_x = |\vec{v}|\cos\theta, \quad v_y = |\vec{v}|\sin\theta", font_size=self.FONT_FORMULA, color=YELLOW),
            MathTex(r"|\vec{v}| = \sqrt{v_x^2 + v_y^2}", font_size=self.FONT_FORMULA, color=PURPLE),
        ).arrange(DOWN, buff=0.4)

        summary_bg = SurroundingRectangle(
            summary, color=WHITE, fill_color=BLACK, fill_opacity=0.9, buff=0.3,
        )
        self.play(FadeIn(summary_bg), Write(summary), run_time=2)
        self.wait(2)
