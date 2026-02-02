from manim import *
import numpy as np


class DisplacementVsDistance(Scene):
    # ── 폰트 크기 ──
    FONT_TITLE = 80
    FONT_SUBTITLE = 28
    FONT_LABEL = 24

    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_straight_line()
        self.clear_screen()
        self.phase2_curved_path()
        self.clear_screen()
        self.phase3_comparison()
        self.clear_screen()
        self.outro()

    # ═══════════ Utilities ═══════════

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # ═══════════ Phase 0: Intro ═══════════

    def intro(self):
        title = Text("변위와 이동거리", font_size=self.FONT_TITLE, color=WHITE)
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)

    # ═══════════ Phase 1: 직선 이동 ═══════════

    def phase1_straight_line(self):
        # ── 1. 제목 ──
        subtitle = Text("직선 이동", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        self.play(Write(subtitle))

        # ── 2. 두 점 ──
        POINT_A = LEFT * 4 + DOWN * 0.5
        POINT_B = RIGHT * 4 + DOWN * 0.5

        dot_a = Dot(POINT_A, color=BLUE, radius=0.15)
        dot_b = Dot(POINT_B, color=RED, radius=0.15)
        label_a = Text("A", font_size=self.FONT_LABEL, color=BLUE).next_to(dot_a, DOWN)
        label_b = Text("B", font_size=self.FONT_LABEL, color=RED).next_to(dot_b, DOWN)

        self.play(Create(dot_a), Write(label_a), Create(dot_b), Write(label_b), run_time=1)
        self.wait(0.3)

        # ── 3. 직선 경로를 따라 점 이동 ──
        straight_path = Line(POINT_A, POINT_B, color=ORANGE, stroke_width=5)
        moving_dot = Dot(POINT_A, color=YELLOW, radius=0.15)
        trace = TracedPath(moving_dot.get_center, stroke_color=ORANGE, stroke_width=3, stroke_opacity=0.6)
        self.add(trace)

        self.play(MoveAlongPath(moving_dot, straight_path), run_time=2)
        self.wait(0.3)

        # ── 4. 변위와 이동거리 동시 표시 ──
        displacement_arrow = Arrow(
            POINT_A, POINT_B, color=GREEN, buff=0,
            stroke_width=6, max_tip_length_to_length_ratio=0.08,
        )
        straight_length = np.linalg.norm(np.array(POINT_B) - np.array(POINT_A))

        disp_label = VGroup(
            Text("변위", font_size=self.FONT_LABEL, color=GREEN),
            MathTex(f"= {straight_length:.1f}", font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.1).next_to(displacement_arrow, UP, buff=0.3)

        dist_label = VGroup(
            Text("이동거리", font_size=self.FONT_LABEL, color=ORANGE),
            MathTex(f"= {straight_length:.1f}", font_size=28, color=ORANGE),
        ).arrange(RIGHT, buff=0.1).next_to(displacement_arrow, DOWN * 2, buff=0.3)

        self.play(GrowArrow(displacement_arrow), run_time=1)
        self.play(Write(disp_label), Write(dist_label))
        self.wait(0.5)

        # ── 5. 결론 자막 ──
        conclusion = Text("직선 이동 → 변위 = 이동거리", font_size=self.FONT_SUBTITLE, color=YELLOW)
        conclusion.to_edge(DOWN, buff=0.5)
        conclusion_bg = SurroundingRectangle(conclusion, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(conclusion_bg), Write(conclusion))
        self.wait(1.5)

    # ═══════════ Phase 2: 곡선 이동 ═══════════

    def phase2_curved_path(self):
        # ── 1. 제목 ──
        subtitle = Text("곡선 이동", font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.to_edge(UL)
        self.play(Write(subtitle))

        # ── 2. 두 점 ──
        POINT_A = LEFT * 4 + DOWN * 0.5
        POINT_B = RIGHT * 4 + DOWN * 0.5

        dot_a = Dot(POINT_A, color=BLUE, radius=0.15)
        dot_b = Dot(POINT_B, color=RED, radius=0.15)
        label_a = Text("A", font_size=self.FONT_LABEL, color=BLUE).next_to(dot_a, DOWN)
        label_b = Text("B", font_size=self.FONT_LABEL, color=RED).next_to(dot_b, DOWN)

        self.play(Create(dot_a), Write(label_a), Create(dot_b), Write(label_b), run_time=1)
        self.wait(0.3)

        # ── 3. 곡선 경로 생성 ──
        curved_path = VMobject(color=ORANGE, stroke_width=5)
        path_points = [
            POINT_A,
            POINT_A + RIGHT * 1.5 + UP * 2,
            POINT_A + RIGHT * 3 + DOWN * 0.5,
            POINT_A + RIGHT * 4.5 + UP * 1.5,
            POINT_A + RIGHT * 6 + UP * 2.5,
            POINT_B + LEFT * 1 + UP * 1,
            POINT_B,
        ]
        curved_path.set_points_smoothly(path_points)

        # ── 4. 곡선 따라 점 이동 (MoveAlongPath) ──
        moving_dot = Dot(POINT_A, color=YELLOW, radius=0.15)
        self.add(moving_dot)
        self.play(
            Create(curved_path),
            MoveAlongPath(moving_dot, curved_path),
            run_time=2.5,
        )
        self.wait(0.3)

        # ── 5. 이동거리 라벨 (곡선 최고점 위) ──
        curved_length = curved_path.get_arc_length()
        distance_label = VGroup(
            Text("이동거리", font_size=self.FONT_LABEL, color=ORANGE),
            MathTex(f"= {curved_length:.1f}", font_size=28, color=ORANGE),
        ).arrange(RIGHT, buff=0.1)
        distance_label.next_to(curved_path, UP + RIGHT, buff=0.3)

        self.play(Write(distance_label))

        # ── 6. 변위 화살표 ──
        displacement_arrow = Arrow(
            POINT_A, POINT_B, color=GREEN, buff=0,
            stroke_width=6, max_tip_length_to_length_ratio=0.08,
        )
        straight_length = np.linalg.norm(np.array(POINT_B) - np.array(POINT_A))

        displacement_label = VGroup(
            Text("변위", font_size=self.FONT_LABEL, color=GREEN),
            MathTex(f"= {straight_length:.1f}", font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        displacement_label.next_to(displacement_arrow, DOWN, buff=0.3)

        self.play(GrowArrow(displacement_arrow), run_time=1)
        self.play(Write(displacement_label))
        self.wait(0.5)

        # ── 7. 수치 비교 박스 ──
        comparison_text = VGroup(
            VGroup(
                Text("이동거리", font_size=20, color=ORANGE),
                MathTex(f"s = {curved_length:.1f}", font_size=28, color=ORANGE),
            ).arrange(DOWN, buff=0.1),
            MathTex(r">", font_size=36, color=YELLOW),
            VGroup(
                Text("변위", font_size=20, color=GREEN),
                MathTex(f"|d| = {straight_length:.1f}", font_size=28, color=GREEN),
            ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.5)
        comparison_text.to_edge(DOWN, buff=0.5)
        comparison_bg = SurroundingRectangle(comparison_text, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.2)

        self.play(FadeIn(comparison_bg), Write(comparison_text))
        self.wait(1.5)

    # ═══════════ Phase 3: 비교 요약 ═══════════

    def phase3_comparison(self):
        # ── 1. 왼쪽: 직선 케이스 ──
        LEFT_CENTER = LEFT * 3.5

        straight_a = Dot(LEFT_CENTER + LEFT * 1.5, color=BLUE, radius=0.1)
        straight_b = Dot(LEFT_CENTER + RIGHT * 1.5, color=RED, radius=0.1)
        straight_arrow = Arrow(
            straight_a.get_center(), straight_b.get_center(),
            color=GREEN, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.12,
        )
        straight_path = Line(
            straight_a.get_center(), straight_b.get_center(),
            color=ORANGE, stroke_width=3,
        ).shift(UP * 0.15)

        straight_group = VGroup(straight_a, straight_b, straight_arrow, straight_path)
        straight_title = Text("직선 이동", font_size=22, color=WHITE)
        straight_title.next_to(straight_group, UP, buff=0.4)

        straight_eq = VGroup(
            Text("변위 = 이동거리", font_size=18, color=YELLOW),
        ).next_to(straight_group, DOWN, buff=0.4)

        left_all = VGroup(straight_title, straight_group, straight_eq)

        # ── 2. 오른쪽: 곡선 케이스 ──
        RIGHT_CENTER = RIGHT * 3.5

        curved_a = Dot(RIGHT_CENTER + LEFT * 1.5, color=BLUE, radius=0.1)
        curved_b = Dot(RIGHT_CENTER + RIGHT * 1.5, color=RED, radius=0.1)
        curved_arrow = Arrow(
            curved_a.get_center(), curved_b.get_center(),
            color=GREEN, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.12,
        )
        curved_path = VMobject(color=ORANGE, stroke_width=3)
        curved_path.set_points_smoothly([
            curved_a.get_center(),
            RIGHT_CENTER + LEFT * 0.5 + UP * 1.2,
            RIGHT_CENTER + RIGHT * 0.5 + UP * 0.5,
            curved_b.get_center(),
        ])

        curved_group = VGroup(curved_a, curved_b, curved_arrow, curved_path)
        curved_title = Text("곡선 이동", font_size=22, color=WHITE)
        curved_title.next_to(curved_group, UP, buff=0.4)

        curved_eq = VGroup(
            Text("이동거리 > 변위", font_size=18, color=YELLOW),
        ).next_to(curved_group, DOWN, buff=0.4)

        right_all = VGroup(curved_title, curved_group, curved_eq)

        # ── 3. 표시 ──
        self.play(
            FadeIn(left_all), FadeIn(right_all),
            run_time=1.5,
        )
        self.wait(1)

        # ── 4. 중앙 구분선 ──
        divider = DashedLine(UP * 2.5, DOWN * 2.5, color=GRAY, stroke_width=2)
        self.play(Create(divider), run_time=0.5)

        # ── 5. 부등식 강조 ──
        inequality = MathTex(
            r"\text{이동거리} \geq |\text{변위}|",
            font_size=36, color=YELLOW,
            tex_template=TexTemplateLibrary.ctex,
        )
        # 한글이 MathTex에서 문제가 될 수 있으므로 Text+MathTex 조합으로 변경
        inequality = VGroup(
            Text("이동거리", font_size=28, color=ORANGE),
            MathTex(r"\geq", font_size=36, color=YELLOW),
            Text("|변위|", font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.2)
        inequality.to_edge(DOWN, buff=0.8)
        inequality_bg = SurroundingRectangle(inequality, color=YELLOW, fill_color=BLACK, fill_opacity=0.9, buff=0.2)

        self.play(FadeIn(inequality_bg), Write(inequality))
        self.wait(2)

    # ═══════════ Phase 4: Outro ═══════════

    def outro(self):
        summary = VGroup(
            Text("* 변위: 시작점 → 끝점 직선 (벡터)", font_size=22, color=GREEN),
            Text("* 이동거리: 실제 이동 경로 길이 (스칼라)", font_size=22, color=ORANGE),
            Text("* 이동거리 >= |변위| (등호: 직선 이동일 때만)", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        summary_bg = SurroundingRectangle(
            summary, color=WHITE, fill_color=BLACK, fill_opacity=0.9, buff=0.3,
        )
        self.play(FadeIn(summary_bg), Write(summary), run_time=2)
        self.wait(2)
