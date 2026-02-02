from manim import *
import numpy as np

class VectorAddition(Scene):
    def construct(self):
        # === Title ===
        title = Text("벡터의 합", font_size=48, color=WHITE)
        title.to_edge(UL)
        self.play(Write(title))
        self.wait(0.5)

        # 좌표계 생성
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"include_tip": True, "tip_length": 0.2},
        ).set_color(GRAY)
        self.play(Create(axes), run_time=1)

        # === 1. 수직인 두 벡터 a, b 생성 ===
        origin = axes.c2p(0, 0)

        # 벡터 a (x축 방향)
        vec_a_end = axes.c2p(3, 0)
        vec_a = Arrow(origin, vec_a_end, color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_a = MathTex(r"\vec{a}", color=RED, font_size=36).next_to(vec_a, DOWN, buff=0.2)

        # 벡터 b (y축 방향)
        vec_b_end = axes.c2p(0, 2)
        vec_b = Arrow(origin, vec_b_end, color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_b = MathTex(r"\vec{b}", color=BLUE, font_size=36).next_to(vec_b, LEFT, buff=0.2)

        self.play(GrowArrow(vec_a), Write(label_a), run_time=1)
        self.play(GrowArrow(vec_b), Write(label_b), run_time=1)
        self.wait(0.5)

        # 직각 표시
        right_angle = RightAngle(
            Line(origin, vec_a_end),
            Line(origin, vec_b_end),
            color=YELLOW,
            stroke_width=3,
            length=0.3
        )
        self.play(Create(right_angle))
        self.wait(0.3)

        # === 2. 벡터 합 a + b ===
        # b를 a의 끝점으로 이동 (평행이동)
        vec_b_shifted = Arrow(vec_a_end, axes.c2p(3, 2), color=BLUE, buff=0, stroke_width=6,
                              max_tip_length_to_length_ratio=0.15).set_opacity(0.6)
        vec_b_shifted_dashed = DashedVMobject(vec_b_shifted, num_dashes=10)

        self.play(
            Create(vec_b_shifted_dashed),
            run_time=1
        )

        # 합벡터 a + b
        vec_sum_end = axes.c2p(3, 2)
        vec_sum = Arrow(origin, vec_sum_end, color=GREEN, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        label_sum = MathTex(r"\vec{a} + \vec{b}", color=GREEN, font_size=36).next_to(vec_sum.get_center(), UP + LEFT, buff=0.2)

        self.play(GrowArrow(vec_sum), run_time=1.5)
        self.play(Write(label_sum))
        self.wait(1)

        # === 3. 페이드 아웃 ===
        self.play(
            FadeOut(vec_a), FadeOut(label_a),
            FadeOut(vec_b), FadeOut(label_b),
            FadeOut(vec_b_shifted_dashed),
            FadeOut(vec_sum), FadeOut(label_sum),
            FadeOut(right_angle),
            run_time=1
        )
        self.wait(0.5)

        # === 4. 새로운 벡터 a, b (다른 각도) ===
        # 벡터 a2 (30도 방향)
        angle_a2 = 30 * DEGREES
        vec_a2_end = axes.c2p(3 * np.cos(angle_a2), 3 * np.sin(angle_a2))
        vec_a2 = Arrow(origin, vec_a2_end, color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_a2 = MathTex(r"\vec{a}", color=RED, font_size=36).next_to(vec_a2.get_center(), DOWN, buff=0.15)

        # 벡터 b2 (120도 방향)
        angle_b2 = 120 * DEGREES
        vec_b2_end = axes.c2p(2 * np.cos(angle_b2), 2 * np.sin(angle_b2))
        vec_b2 = Arrow(origin, vec_b2_end, color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_b2 = MathTex(r"\vec{b}", color=BLUE, font_size=36).next_to(vec_b2.get_center(), UP + LEFT, buff=0.15)

        self.play(GrowArrow(vec_a2), Write(label_a2), run_time=1)
        self.play(GrowArrow(vec_b2), Write(label_b2), run_time=1)
        self.wait(0.5)

        # === 5. 벡터 합 (평행사변형 법칙) ===
        # b를 a의 끝점으로 이동
        vec_b2_shifted_end = np.array(vec_a2_end) + np.array(vec_b2_end) - np.array(origin)
        vec_b2_shifted = Arrow(vec_a2_end, vec_b2_shifted_end, color=BLUE, buff=0, stroke_width=6,
                               max_tip_length_to_length_ratio=0.15).set_opacity(0.6)
        vec_b2_shifted_dashed = DashedVMobject(vec_b2_shifted, num_dashes=10)

        # a를 b의 끝점으로 이동
        vec_a2_shifted_end = np.array(vec_b2_end) + np.array(vec_a2_end) - np.array(origin)
        vec_a2_shifted = Arrow(vec_b2_end, vec_a2_shifted_end, color=RED, buff=0, stroke_width=6,
                               max_tip_length_to_length_ratio=0.15).set_opacity(0.6)
        vec_a2_shifted_dashed = DashedVMobject(vec_a2_shifted, num_dashes=10)

        self.play(
            Create(vec_b2_shifted_dashed),
            Create(vec_a2_shifted_dashed),
            run_time=1
        )

        # 합벡터
        sum_x = 3 * np.cos(angle_a2) + 2 * np.cos(angle_b2)
        sum_y = 3 * np.sin(angle_a2) + 2 * np.sin(angle_b2)
        vec_sum2_end = axes.c2p(sum_x, sum_y)
        vec_sum2 = Arrow(origin, vec_sum2_end, color=GREEN, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        label_sum2 = MathTex(r"\vec{a} + \vec{b}", color=GREEN, font_size=36).next_to(vec_sum2.get_center(), RIGHT, buff=0.2)

        self.play(GrowArrow(vec_sum2), run_time=1.5)
        self.play(Write(label_sum2))
        self.wait(1)

        # === 6. 페이드 아웃 ===
        self.play(
            FadeOut(vec_a2), FadeOut(label_a2),
            FadeOut(vec_b2), FadeOut(label_b2),
            FadeOut(vec_b2_shifted_dashed),
            FadeOut(vec_a2_shifted_dashed),
            FadeOut(vec_sum2), FadeOut(label_sum2),
            FadeOut(title),
            run_time=1
        )
        self.wait(0.5)

        # === 7. 대각선 벡터 성분 분해 (첫 번째 예시) ===
        subtitle = Text("벡터의 성분 분해", font_size=48, color=WHITE)
        subtitle.to_edge(UL)
        self.play(Write(subtitle))

        # 수식 영역 (4사분면, y축에 가깝게)
        formula_area = VGroup()
        formula_area.to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=1.5)

        # --- 첫 번째 벡터 분해 ---
        # 1. 대각선 벡터 v 그리기
        angle_diag = 50 * DEGREES
        diag_length = 3.0
        vx_val = diag_length * np.cos(angle_diag)
        vy_val = diag_length * np.sin(angle_diag)
        vec_diag_end = axes.c2p(vx_val, vy_val)

        vec_v = Arrow(origin, vec_diag_end, color=PURPLE, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        label_v = MathTex(r"\vec{v}", color=PURPLE, font_size=40).next_to(vec_v.get_center(), UP + LEFT, buff=0.2)

        self.play(GrowArrow(vec_v), Write(label_v), run_time=1.5)
        self.wait(0.5)

        # 각도 표시
        angle_arc = Arc(radius=0.6, start_angle=0, angle=angle_diag, color=ORANGE, stroke_width=3)
        angle_arc.move_arc_center_to(origin)
        angle_label = MathTex(r"\theta", color=ORANGE, font_size=28).move_to(origin + RIGHT*0.9 + UP*0.3)
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(0.3)

        # 2. v벡터 복제 → x축으로 투영 → vx 벡터로 변환
        vec_v_copy_x = vec_v.copy().set_color(RED)
        self.play(Create(vec_v_copy_x), run_time=0.5)

        # 투영선 (점선)
        proj_line_x = DashedLine(vec_diag_end, axes.c2p(vx_val, 0), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_x), run_time=0.5)

        # vx 벡터로 변환
        vec_vx = Arrow(origin, axes.c2p(vx_val, 0), color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_vx = MathTex(r"v_x = |\vec{v}|\cdot\cos\theta", color=RED, font_size=32).next_to(vec_vx, DOWN, buff=0.15)

        self.play(Transform(vec_v_copy_x, vec_vx), run_time=1)
        self.play(Write(label_vx))

        # 수식 vx = v cos theta
        formula_vx = MathTex(r"v_x = |\vec{v}| \cos\theta", color=RED, font_size=28)
        formula_vx.to_corner(DR, buff=1.5).shift(UP*1.5)
        formula_vx_bg = SurroundingRectangle(formula_vx, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(formula_vx_bg), Write(formula_vx))
        self.wait(0.5)

        # 3. v벡터 복제 → y축으로 투영 → vy 벡터로 변환
        vec_v_copy_y = vec_v.copy().set_color(BLUE)
        self.play(Create(vec_v_copy_y), run_time=0.5)

        # 투영선 (점선)
        proj_line_y = DashedLine(vec_diag_end, axes.c2p(0, vy_val), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_y), run_time=0.5)

        # vy 벡터로 변환
        vec_vy = Arrow(origin, axes.c2p(0, vy_val), color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_vy = MathTex(r"v_y = |\vec{v}|\cdot\sin\theta", color=BLUE, font_size=32).next_to(vec_vy, LEFT, buff=0.15)

        self.play(Transform(vec_v_copy_y, vec_vy), run_time=1)
        self.play(Write(label_vy))

        # 수식 vy = v sin theta
        formula_vy = MathTex(r"v_y = |\vec{v}| \sin\theta", color=BLUE, font_size=28)
        formula_vy.next_to(formula_vx_bg, DOWN, buff=0.2)
        formula_vy_bg = SurroundingRectangle(formula_vy, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(formula_vy_bg), Write(formula_vy))
        self.wait(1)

        # 최종 수식
        final_formula = MathTex(r"\vec{v} = v_x \hat{i} + v_y \hat{j}", color=PURPLE, font_size=28)
        final_formula.next_to(formula_vy_bg, DOWN, buff=0.2)
        final_formula_bg = SurroundingRectangle(final_formula, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(final_formula_bg), Write(final_formula))
        self.wait(1.5)

        # 첫 번째 예시 페이드 아웃
        self.play(
            FadeOut(vec_v), FadeOut(label_v),
            FadeOut(vec_v_copy_x), FadeOut(label_vx),
            FadeOut(vec_v_copy_y), FadeOut(label_vy),
            FadeOut(proj_line_x), FadeOut(proj_line_y),
            FadeOut(angle_arc), FadeOut(angle_label),
            FadeOut(formula_vx), FadeOut(formula_vx_bg),
            FadeOut(formula_vy), FadeOut(formula_vy_bg),
            FadeOut(final_formula), FadeOut(final_formula_bg),
            run_time=1
        )
        self.wait(0.5)

        # === 8. 두 번째 벡터 분해 (다른 각도) ===
        # 1. 대각선 벡터 v2 그리기 (30도 방향)
        angle_diag2 = 210 * DEGREES
        diag_length2 = 3.5
        vx_val2 = diag_length2 * np.cos(angle_diag2)
        vy_val2 = diag_length2 * np.sin(angle_diag2)
        vec_diag_end2 = axes.c2p(vx_val2, vy_val2)

        vec_v2 = Arrow(origin, vec_diag_end2, color=PURPLE, buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.12)
        label_v2 = MathTex(r"\vec{v}", color=PURPLE, font_size=40).next_to(vec_v2.get_center(), UP, buff=0.2)

        self.play(GrowArrow(vec_v2), Write(label_v2), run_time=1.5)
        self.wait(0.5)

        # 각도 표시
        angle_arc2 = Arc(
            radius=0.8, 
            start_angle=PI, 
            angle=PI/6, 
            color=ORANGE, 
            stroke_width=3,
            arc_center=origin  # 생성할 때 중심 지정
        )
        angle_label2 = MathTex(r"\theta = 30°", color=ORANGE, font_size=24)
        angle_label2.next_to(angle_arc2, LEFT, buff=0.15)

        self.play(FadeIn(angle_arc2), Write(angle_label2))
        self.wait(0.3)

        # 2. v벡터 복제 → x축으로 투영
        vec_v2_copy_x = vec_v2.copy().set_color(RED)
        self.play(Create(vec_v2_copy_x), run_time=0.5)

        proj_line_x2 = DashedLine(vec_diag_end2, axes.c2p(vx_val2, 0), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_x2), run_time=0.5)

        vec_vx2 = Arrow(origin, axes.c2p(vx_val2, 0), color=RED, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_vx2 = MathTex(r"v_x = |\vec{v}| \cos 30°", color=RED, font_size=32).next_to(vec_vx2, UP, buff=0.15)

        self.play(Transform(vec_v2_copy_x, vec_vx2), run_time=1)
        self.play(Write(label_vx2))

        formula_vx2 = MathTex(r"v_x = |\vec{v}| \cos 30° \approx 0.87|\vec{v}|", color=RED, font_size=26)
        formula_vx2.to_corner(DR, buff=1.5).shift(UP*1.5)
        formula_vx2_bg = SurroundingRectangle(formula_vx2, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(formula_vx2_bg), Write(formula_vx2))
        self.wait(0.5)

        # 3. v벡터 복제 → y축으로 투영
        vec_v2_copy_y = vec_v2.copy().set_color(BLUE)
        self.play(Create(vec_v2_copy_y), run_time=0.5)

        proj_line_y2 = DashedLine(vec_diag_end2, axes.c2p(0, vy_val2), color=GRAY, stroke_width=2)
        self.play(Create(proj_line_y2), run_time=0.5)

        vec_vy2 = Arrow(origin, axes.c2p(0, vy_val2), color=BLUE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        label_vy2 = MathTex(r"v_y = |\vec{v}| \sin 30°", color=BLUE, font_size=32).next_to(vec_vy2, RIGHT, buff=0.15)

        self.play(Transform(vec_v2_copy_y, vec_vy2), run_time=1)
        self.play(Write(label_vy2))

        formula_vy2 = MathTex(r"v_y = |\vec{v}| \sin 30° = 0.5|\vec{v}|", color=BLUE, font_size=26)
        formula_vy2.next_to(formula_vx2_bg, DOWN, buff=0.2)
        formula_vy2_bg = SurroundingRectangle(formula_vy2, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(formula_vy2_bg), Write(formula_vy2))
        self.wait(1)

        # 피타고라스 정리 강조
        pythagoras = MathTex(r"|\vec{v}| = \sqrt{v_x^2 + v_y^2}", color=YELLOW, font_size=30)
        pythagoras.next_to(formula_vy2_bg, DOWN, buff=0.3)
        pythagoras_bg = SurroundingRectangle(pythagoras, color=YELLOW, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(pythagoras_bg), Write(pythagoras))

        self.wait(3)
