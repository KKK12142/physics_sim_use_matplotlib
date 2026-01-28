from manim import *
import numpy as np

class DisplacementVsDistance(Scene):
    def construct(self):
        # === Title ===
        title = Text("변위 vs 이동거리", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # === 1. 두 점 생성 ===
        point_A = Dot(LEFT * 4, color=BLUE, radius=0.15)
        point_B = Dot(RIGHT * 4, color=RED, radius=0.15)

        label_A = Text("A", font_size=32, color=BLUE).next_to(point_A, DOWN)
        label_B = Text("B", font_size=32, color=RED).next_to(point_B, DOWN)

        self.play(
            Create(point_A), Write(label_A),
            Create(point_B), Write(label_B),
            run_time=1
        )
        self.wait(0.5)

        # === 2. 곡선 경로 생성 (이동거리) - 복잡한 곡선 ===
        self.play(FadeOut(title))
        curved_path = VMobject(color=ORANGE, stroke_width=5)
        path_points = [
            point_A.get_center(),
            point_A.get_center() + RIGHT*1.5 + UP*2,
            point_A.get_center() + RIGHT*3 + DOWN*0.5,
            point_A.get_center() + RIGHT*4.5 + UP*1.5,
            point_A.get_center() + RIGHT*6 + UP*2.5,
            point_B.get_center() + LEFT*1 + UP*1,
            point_B.get_center(),
        ]
        curved_path.set_points_smoothly(path_points)

        # 이동거리 레이블
        distance_label = Text("실제 이동한 거리 = 이동거리 (Distance)", font_size=24, color=ORANGE, )
        distance_label.next_to(curved_path, UP, buff=0.3)

        self.play(Write(distance_label))

        # === 3. 곡선 경로 따라 점 이동 ===
        moving_dot = Dot(color=YELLOW, radius=0.15) 
        moving_dot.move_to(curved_path.get_start())
        self.add(moving_dot)

        moving_dot.add_updater(lambda m: m.move_to(curved_path.get_end()))
        self.play(Create(curved_path), run_time=2.5)
        moving_dot.clear_updaters()

        self.wait(0.5)

        # === 4. 변위 화살표 생성 (벡터) ===
        displacement_arrow = Arrow(
            point_A.get_center(),
            point_B.get_center(),
            color=GREEN,
            stroke_width=6,
            buff=0,
            max_tip_length_to_length_ratio=0.08
        )

        # 변위 레이블
        displacement_label = Text("위치 변화량 = 변위 (Displacement)", font_size=24, color=GREEN)
        displacement_label.next_to(displacement_arrow, DOWN, buff=0.4)

        # 변위 화살표 표시
        self.play(GrowArrow(displacement_arrow), run_time=1.5)
        self.play(Write(displacement_label))
        self.wait(0.5)

        # === 5. 거리 계산 및 표시 ===

        # 직선 거리 계산
        straight_length = np.linalg.norm(
            np.array(point_B.get_center()) - np.array(point_A.get_center())
        )

        # 곡선 길이 계산 (근사)
        curved_length = curved_path.get_arc_length()

        # 정보 박스
        displacement_info = VGroup(
            Text("변위:", font_size=24, color=GREEN),
            Text(f"|d| = {straight_length:.1f}", font_size=28, color=GREEN),
            Text("(직선거리)", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        distance_info = VGroup(
            Text("이동거리:", font_size=24, color=ORANGE),
            Text(f"s = {curved_length:.1f}", font_size=28, color=ORANGE),
            Text("(경로 길이)", font_size=18, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        info_box = VGroup(displacement_info, distance_info).arrange(RIGHT, buff=1.5)
        info_box.to_edge(DOWN, buff=0.7)

        # 박스 배경
        box_bg = SurroundingRectangle(info_box, color=WHITE, fill_color=BLACK, fill_opacity=0.8, buff=0.3)

        self.play(
            FadeIn(box_bg),
            Write(displacement_info),
            Write(distance_info),
            run_time=2
        )
        self.wait(1)

        # === 6. 부등호 강조 ===

        inequality = Text("이동거리 >= 변위", font_size=36, color=YELLOW)
        inequality.next_to(box_bg, UP, buff=0.3)

        self.play(Write(inequality))
        self.wait(0.5)

        # === 7. 핵심 메시지 ===

        # 기존 요소 페이드 아웃
        self.play(
            FadeOut(box_bg),
            FadeOut(displacement_info),
            FadeOut(distance_info),
            FadeOut(inequality),
            FadeOut(moving_dot),
        )

        key_message = VGroup(
            Text("* 변위: 시작점 -> 끝점 직선 (벡터)", font_size=22, color=GREEN),
            Text("* 이동거리: 실제 이동 경로 길이 (스칼라)", font_size=22, color=ORANGE),
            Text("* 이동거리 >= |변위| (등호: 직선 이동일 때만)", font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        key_message.to_edge(DOWN, buff=0.5)

        final_box = SurroundingRectangle(key_message, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.25)

        self.play(
            FadeIn(final_box),
            Write(key_message),
            run_time=2
        )

        self.wait(3)


class DisplacementVsDistanceSimple(Scene):
    """간단 버전 - 핵심만"""
    def construct(self):
        # 제목
        title = Text("변위 vs 이동거리", font_size=44).to_edge(UP)
        self.play(Write(title))

        # 두 점
        A = LEFT * 4 + DOWN * 0.5
        B = RIGHT * 4 + DOWN * 0.5

        dot_A = Dot(A, color=BLUE, radius=0.2)
        dot_B = Dot(B, color=RED, radius=0.2)
        text_A = Text("시작", font_size=20, color=BLUE).next_to(dot_A, DOWN)
        text_B = Text("끝", font_size=20, color=RED).next_to(dot_B, DOWN)

        self.play(Create(dot_A), Create(dot_B), Write(text_A), Write(text_B))
        self.wait(0.5)

        # 변위 (직선 화살표)
        displacement = Arrow(A, B, color=GREEN, buff=0, stroke_width=6)
        disp_label = Text("변위 = 8.0", font_size=28, color=GREEN).next_to(displacement, DOWN, buff=0.3)

        self.play(GrowArrow(displacement), run_time=1.5)
        self.play(Write(disp_label))
        self.wait(0.5)

        # 곡선 경로
        path_points = [A, A + RIGHT*2 + UP*2.5, A + RIGHT*5 + UP*1, A + RIGHT*6 + UP*3, B + UP*1, B]
        curved = VMobject(color=ORANGE, stroke_width=5)
        curved.set_points_smoothly(path_points)

        curve_length = curved.get_arc_length()
        curve_label = Text(f"이동거리 = {curve_length:.1f}", font_size=28, color=ORANGE)
        curve_label.next_to(curved, UP, buff=0.2)

        self.play(Create(curved), run_time=2)
        self.play(Write(curve_label))
        self.wait(0.5)

        # 물체 이동
        obj = Dot(A, color=YELLOW, radius=0.25)
        trace = TracedPath(obj.get_center, stroke_color=YELLOW, stroke_width=2, stroke_opacity=0.5)
        self.add(trace)

        self.play(MoveAlongPath(obj, curved), run_time=3)
        self.wait(0.5)

        # 결론
        conclusion = VGroup(
            Text(f"이동거리 ({curve_length:.1f}) > 변위 (8.0)", font_size=30, color=YELLOW),
        )
        conclusion.to_edge(DOWN, buff=0.8)
        bg = SurroundingRectangle(conclusion, color=WHITE, fill_color=BLACK, fill_opacity=0.9, buff=0.2)

        self.play(FadeIn(bg), Write(conclusion))
        self.wait(2)
