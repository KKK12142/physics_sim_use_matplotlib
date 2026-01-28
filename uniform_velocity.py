from manim import *
import numpy as np

class UniformMotion(Scene):
    def construct(self):
        # === Title ===
        title = Text("등속 운동", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # === 1. 상단 영역: 1차원 수평선 (위치 트랙) ===
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        # 눈금 표시 (0 ~ 20)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(21):
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 20)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)

            if i % 5 == 0:
                label = Text(str(i), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        position_label = Text("위치 (m)", font_size=20, color=WHITE)
        position_label.next_to(track, RIGHT, buff=0.3)

        self.play(Create(track), run_time=0.5)
        self.play(Create(tick_marks), Write(tick_labels), Write(position_label), run_time=1)
        self.wait(0.3)

        # === 2. 하단 영역: s-t 그래프 ===
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 20, 5],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [5, 10, 15, 20]},
        )
        axes.to_corner(DR, buff=0.8)

        x_label = Text("t (s)", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = Text("s (m)", font_size=20).next_to(axes.y_axis, UP, buff=0.2)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1)
        self.wait(0.3)

        # === 3. 물체 생성 ===
        obj_size = 0.4
        obj = Square(side_length=obj_size, color=YELLOW, fill_opacity=0.8)
        obj_start_x = track_start[0]
        obj.move_to([obj_start_x, track.get_center()[1] + obj_size/2 + 0.1, 0])

        self.play(FadeIn(obj))
        self.wait(0.3)

        # === 4. 운동 파라미터 ===
        total_time = 4  # 총 시간 (초)
        total_distance = 20  # 총 거리 (m)
        velocity = 5  # 속도 = 5 m/s
        time_interval = 1  # 시간 간격

        # 속도 정보 표시
        velocity_text = Tex(r"$v = 5$ m/s", font_size=32, color=YELLOW)
        velocity_text.to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        self.play(Write(velocity_text))

        # 시간 간격 표시
        interval_text = Tex(r"$\Delta t = 1$ s", font_size=28, color=TEAL)
        interval_text.next_to(velocity_text, DOWN, buff=0.2)
        self.play(Write(interval_text))
        self.wait(0.3)

        # === 5. 시작점 설정 ===
        # 시작 잔상 (t=0)
        afterimage_base = Square(side_length=obj_size, color=YELLOW, fill_opacity=0.1, stroke_width=2)
        afterimage_base.move_to(obj.get_center())
        afterimage_0 = DashedVMobject(afterimage_base, num_dashes=12, dashed_ratio=0.5)
        self.play(FadeIn(afterimage_0), run_time=0.3)

        # 그래프 시작점
        dot_0 = Dot(axes.c2p(0, 0), color=RED, radius=0.08)
        self.play(FadeIn(dot_0), run_time=0.3)

        # === 6. 등속 운동 애니메이션 (연속적) ===
        # ValueTracker로 시간 추적
        time_tracker = ValueTracker(0)

        # 물체 위치 업데이터
        def update_obj(m):
            t = time_tracker.get_value()
            s = velocity * t
            x_ratio = s / total_distance
            new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
            m.move_to([new_x, track.get_center()[1] + obj_size/2 + 0.1, 0])

        obj.add_updater(update_obj)

        # 저장용 리스트
        afterimages = VGroup(afterimage_0)
        graph_dots = VGroup(dot_0)
        graph_lines = VGroup()
        bars = VGroup()

        # 각 시간 간격마다 애니메이션
        for i in range(1, total_time + 1):
            t_prev = i - 1
            t_curr = i
            s_prev = velocity * t_prev
            s_curr = velocity * t_curr

            # 물체 연속 이동 (1초 동안)
            self.play(
                time_tracker.animate.set_value(t_curr),
                run_time=1,
                rate_func=linear
            )

            # 잔상 생성
            x_ratio = s_curr / total_distance
            new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
            new_pos = [new_x, track.get_center()[1] + obj_size/2 + 0.1, 0]

            afterimage_base = Square(side_length=obj_size, color=YELLOW, fill_opacity=0.1, stroke_width=2)
            afterimage_base.move_to(new_pos)
            afterimage = DashedVMobject(afterimage_base, num_dashes=12, dashed_ratio=0.5)
            afterimages.add(afterimage)
            self.play(FadeIn(afterimage), run_time=0.2)

            # 새로운 5m 막대 추가 (누적 방식)
            # 이전 막대 위에 새 막대 쌓기
            bar_unit_height = axes.c2p(0, 5)[1] - axes.c2p(0, 0)[1]
            new_bar = Rectangle(
                width=0.4,
                height=bar_unit_height,
                color=BLUE,
                fill_opacity=0.6,
                stroke_width=2,
                stroke_color=WHITE
            )
            bar_x = axes.c2p(t_curr, 0)[0]
            # 이전 높이 위에 쌓기
            base_y = axes.c2p(0, s_prev)[1]
            new_bar.move_to([bar_x, base_y + bar_unit_height/2, 0])

            # "+5m" 텍스트
            plus_text = Text("+5", font_size=14, color=WHITE)
            plus_text.move_to(new_bar.get_center())

            self.play(FadeIn(new_bar), FadeIn(plus_text), run_time=0.3)
            bars.add(VGroup(new_bar, plus_text))

            # 그래프 점 추가
            new_dot = Dot(axes.c2p(t_curr, s_curr), color=RED, radius=0.08)
            self.play(FadeIn(new_dot), run_time=0.2)
            graph_dots.add(new_dot)

            # 선 연결
            prev_dot = graph_dots[-2]
            line = Line(prev_dot.get_center(), new_dot.get_center(), color=RED, stroke_width=2)
            graph_lines.add(line)
            self.play(Create(line), run_time=0.2)

        obj.remove_updater(update_obj)
        self.wait(0.5)

        # === 7. 1차 함수 그래프 강조 ===
        graph_line = axes.plot(lambda x: velocity * x, x_range=[0, 4], color=RED, stroke_width=3)
        self.play(Create(graph_line), run_time=1)

        # 수식 표시
        equation = MathTex(r"s = vt = 5t", font_size=32, color=RED)
        equation.next_to(axes, UP, buff=0.3)
        equation_bg = SurroundingRectangle(equation, color=WHITE, fill_color=BLACK, fill_opacity=0.8, buff=0.15)
        self.play(FadeIn(equation_bg), Write(equation))
        self.wait(0.5)

        # === 8. 등속 운동 특징 강조 ===
        conclusion = VGroup(
            Text("* 등속 운동: 속도가 일정", font_size=22, color=WHITE),
            Text("* s-t 그래프: 직선 (기울기 = 속도)", font_size=22, color=WHITE),
            MathTex(r"v = \frac{\Delta s}{\Delta t} = const.", font_size=26, color=YELLOW),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        # s-t 그래프 왼쪽에 배치
        conclusion.next_to(axes, LEFT, buff=0.4)

        conclusion_bg = SurroundingRectangle(conclusion, color=WHITE, fill_color=BLACK, fill_opacity=0.85, buff=0.15)

        self.play(FadeIn(conclusion_bg), Write(conclusion), run_time=2)

        self.wait(3)


class UniformMotionSimple(Scene):
    """간단 버전"""
    def construct(self):
        # 제목
        title = Text("등속 운동", font_size=44).to_edge(UP)
        self.play(Write(title))

        # 수평 트랙
        track = NumberLine(
            x_range=[0, 20, 5],
            length=10,
            include_numbers=True,
            font_size=24
        ).shift(UP * 1.5)

        self.play(Create(track))

        # s-t 그래프
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 20, 5],
            x_length=4,
            y_length=2.5,
            axis_config={"include_tip": True},
        ).to_corner(DR, buff=0.8)

        x_label = Text("t", font_size=18).next_to(axes.x_axis, RIGHT)
        y_label = Text("s", font_size=18).next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # 물체
        obj = Dot(track.n2p(0), color=YELLOW, radius=0.2)
        self.play(FadeIn(obj))

        # 등속 운동 애니메이션 with ValueTracker
        time_tracker = ValueTracker(0)
        velocity = 5  # m/s

        # 물체 위치 업데이트
        obj.add_updater(lambda m: m.move_to(track.n2p(velocity * time_tracker.get_value())))

        # 그래프 선
        graph = always_redraw(
            lambda: axes.plot(
                lambda x: velocity * x,
                x_range=[0, time_tracker.get_value()],
                color=RED,
                stroke_width=3
            )
        )
        self.add(graph)

        # 연속 이동 + 잔상
        for t in range(1, 5):
            self.play(time_tracker.animate.set_value(t), run_time=1, rate_func=linear)
            afterimage = Dot(track.n2p(velocity * t), color=YELLOW, radius=0.15, fill_opacity=0.3)
            self.add(afterimage)

        # 수식
        eq = MathTex(r"s = 5t", color=RED, font_size=32).next_to(axes, LEFT, buff=0.5)
        self.play(Write(eq))

        self.wait(2)
