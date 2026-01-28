from manim import *
import numpy as np

class UniformMotion(Scene):
    def construct(self):
        # === Title ===
        title = Text("등속 운동", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.75)

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

        position_label = Text("(m)", font_size=20, color=WHITE)
        position_label.next_to(track, RIGHT, buff=0.3)

        self.play(Create(track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), Write(position_label), run_time=1.5)
        self.wait(0.45)

        # === 2. 하단 영역(좌): v-t 그래프 ===
        axes_vt = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [5]},
        )
        axes_vt.to_corner(DL, buff=0.8)

        x_label_vt = Text("t (s)", font_size=20).next_to(axes_vt.x_axis, RIGHT, buff=0.2)
        y_label_vt = Text("v (m/s)", font_size=20).next_to(axes_vt.y_axis, UP, buff=0.2)

        self.play(Create(axes_vt), Write(x_label_vt), Write(y_label_vt), run_time=1.5)
        self.wait(0.45)

        # === 3. 하단 영역(우): s-t 그래프 ===
        axes_st = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 20, 5],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [5, 10, 15, 20]},
        )
        axes_st.to_corner(DR, buff=0.8)

        x_label_st = Text("t (s)", font_size=20).next_to(axes_st.x_axis, RIGHT, buff=0.2)
        y_label_st = Text("s (m)", font_size=20).next_to(axes_st.y_axis, UP, buff=0.2)

        self.play(Create(axes_st), Write(x_label_st), Write(y_label_st), run_time=1.5)
        self.wait(0.45)

        # === 4. 물체 생성 ===
        obj_size = 0.4
        obj = Square(side_length=obj_size, color=YELLOW, fill_opacity=0.8)
        obj_start_x = track_start[0]
        obj.move_to([obj_start_x, track.get_center()[1] + obj_size/2 + 0.1, 0])

        self.play(FadeIn(obj), run_time=0.75)
        self.wait(0.45)

        ghost_group = VGroup()
        self.add(ghost_group)

        # === 5. 운동 파라미터 및 물체 애니메이션 ===
        total_time = 4
        total_distance = 20
        v = 5  # 속도 5 m/s (일정)

        # 물체 옆에 속도 라벨 (물체와 함께 이동)
        velocity_label = always_redraw(lambda: MathTex(
            "v = 5\\,\\text{m/s}",
            font_size=20,
            color=YELLOW
        ).next_to(obj, UP, buff=0.1))
        self.add(velocity_label)

        time_tracker = ValueTracker(0)
        time_tracker.last_int_t = 0

        ghost_x_coords = [obj.get_center()[0]]

        def update_obj(m):
            t = time_tracker.get_value()
            s = v * t
            x_ratio = s / total_distance
            new_x = track_start[0] + (
                track_end[0] - track_start[0]
            ) * x_ratio
            m.move_to([new_x, track.get_center()[1] + obj_size/2 + 0.1, 0])
            current_int_t = int(t)

            if current_int_t > time_tracker.last_int_t:
                current_center = m.get_center()

                # 내부가 채워진 잔상 생성
                ghost_base = Square(side_length=obj_size, color=YELLOW, fill_opacity=0.3, stroke_width=0)
                ghost_base.move_to(current_center)

                ghost_group.add(ghost_base)
                ghost_x_coords.append(current_center[0])

                time_tracker.last_int_t = current_int_t

        obj.add_updater(update_obj)
        self.play(
            time_tracker.animate.set_value(total_time),
            run_time=6,
            rate_func=linear
        )
        obj.remove_updater(update_obj)
        self.wait(0.45)

        # === 6. 이동거리 표시 및 s-t 그래프로 옮기기 ===
        prev_s_val = 0

        for i in range(1, len(ghost_x_coords)):
            x_prev = ghost_x_coords[i-1]
            x_curr = ghost_x_coords[i]

            # 트랙 위에 초록색 선 그리기
            track_y = track.get_center()[1] - 0.2

            interval_line = Line(
                [x_prev, track_y, 0],
                [x_curr, track_y, 0],
                color=GREEN,
                stroke_width=4
            )
            self.play(Create(interval_line), run_time=0.75)

            # 그래프 옮기기 위한 좌표 계산
            curr_t = i
            curr_s_val = v * curr_t

            # 그래프 상의 목표 위치 계산
            graph_x = axes_st.c2p(curr_t, 0)[0]
            graph_y_bottom = axes_st.c2p(0, prev_s_val)[1]
            graph_y_top = axes_st.c2p(0, curr_s_val)[1]

            vertical_line = Line(
                [graph_x, graph_y_bottom, 0],
                [graph_x, graph_y_top, 0],
                color=GREEN,
                stroke_width=6
            )

            self.play(Transform(interval_line, vertical_line), run_time=0.9)

            # 수평 대시 라인 (y축에서 점까지)
            h_dash = DashedLine(
                axes_st.c2p(0, curr_s_val),
                axes_st.c2p(curr_t, curr_s_val),
                color=GRAY,
                stroke_width=1.5
            )
            # 수직 대시 라인 (x축에서 점까지)
            v_dash = DashedLine(
                axes_st.c2p(curr_t, 0),
                axes_st.c2p(curr_t, curr_s_val),
                color=GRAY,
                stroke_width=1.5
            )
            new_dot = Dot(axes_st.c2p(curr_t, curr_s_val), color=RED, radius=0.08)
            self.play(Create(h_dash), Create(v_dash), FadeIn(new_dot), run_time=0.45)
            self.play(FadeOut(interval_line), run_time=0.3)

            prev_s_val = curr_s_val

        # === 7. s-t 그래프 직선 그리기 ===
        st_graph = axes_st.plot(lambda t: v * t, x_range=[0, 4], color=RED, stroke_width=3)
        self.play(Create(st_graph), run_time=1.5)

        self.wait(0.75)

        # === 8. s-t 그래프의 기울기 = 속도 시각화 + v-t 점 찍기 ===
        connection_text = Text("s-t 그래프의 기울기 = 속도 (일정)", font_size=24, color=YELLOW)
        connection_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(connection_text), run_time=0.75)

        # 기울기 삼각형 표시 (예: t=1~2 구간)
        t1, t2 = 1, 2
        s1, s2 = v * t1, v * t2

        # 삼각형 점들
        p1 = axes_st.c2p(t1, s1)
        p2 = axes_st.c2p(t2, s1)
        p3 = axes_st.c2p(t2, s2)

        # 삼각형 선
        delta_t_line = Line(p1, p2, color=BLUE, stroke_width=3)
        delta_s_line = Line(p2, p3, color=ORANGE, stroke_width=3)

        delta_t_label = MathTex(r"\Delta t = 1\,\text{s}", font_size=20, color=BLUE).next_to(delta_t_line, DOWN, buff=0.1)
        delta_s_label = MathTex(r"\Delta s = 5\,\text{m}", font_size=20, color=ORANGE).next_to(delta_s_line, RIGHT, buff=0.1)

        self.play(Create(delta_t_line), Create(delta_s_line), run_time=0.75)
        self.play(Write(delta_t_label), Write(delta_s_label), run_time=0.75)

        # 기울기 = 속도
        slope_text = MathTex(r"v = \frac{\Delta s}{\Delta t} = \frac{5\,\text{m}}{1\,\text{s}} = 5\,\text{m/s}", font_size=24, color=ORANGE)
        slope_text.next_to(axes_st, UP, buff=0.3)
        self.play(Write(slope_text), run_time=0.75)

        self.wait(0.75)

        # v-t 그래프에 점 찍기 (기울기 값을 이동)
        slope_dot = Dot(axes_st.c2p(1.5, 7.5), color=ORANGE, radius=0.1)
        self.add(slope_dot)

        # 각 초에 v-t 그래프에 점 찍기
        vt_dots = []
        for t in range(0, 5):
            # v-t 그래프 위 대시 라인
            v_dash_vt = DashedLine(
                axes_vt.c2p(t, 0),
                axes_vt.c2p(t, v),
                color=GRAY,
                stroke_width=1.5
            )
            vt_dot = Dot(axes_vt.c2p(t, v), color=RED, radius=0.08)
            self.play(Create(v_dash_vt), FadeIn(vt_dot), run_time=0.45)
            vt_dots.append(vt_dot)

        # v-t 그래프에 수평선 그리기
        vt_graph = axes_vt.plot(lambda t: v, x_range=[0, 4], color=BLUE, stroke_width=3)
        self.play(Create(vt_graph), run_time=1.5)

        # v = 5 라벨
        v_label = MathTex("v = 5\\,\\text{m/s}", font_size=24, color=BLUE).next_to(axes_vt, UP, buff=0.3)
        self.play(Write(v_label), run_time=0.75)

        self.wait(0.75)

        # 정리
        self.play(
            FadeOut(delta_t_line), FadeOut(delta_s_line),
            FadeOut(delta_t_label), FadeOut(delta_s_label),
            FadeOut(slope_text), FadeOut(slope_dot),
            FadeOut(connection_text), FadeOut(v_label),
            run_time=0.75
        )

        # === 9. v-t 그래프 적분 면적 = 이동거리 시각화 ===
        area_text = Text("v-t 그래프 아래 면적 = 이동거리 s", font_size=24, color=YELLOW)
        area_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(area_text), run_time=0.75)

        # 시간 트래커 (적분용)
        t_integral = ValueTracker(0.01)

        # 동적 면적 (직사각형)
        def get_area():
            t_val = t_integral.get_value()
            if t_val < 0.01:
                return VGroup()
            area = axes_vt.get_area(
                vt_graph,
                x_range=[0, t_val],
                color=BLUE,
                opacity=0.4
            )
            return area

        area_fill = always_redraw(get_area)

        # 동적 면적 값 표시
        def get_area_value():
            t_val = t_integral.get_value()
            s_val = v * t_val
            return MathTex(
                f"S = {s_val:.1f}\\,\\text{{m}}",
                font_size=24,
                color=BLUE
            ).next_to(axes_vt, UP, buff=0.3)

        area_value_text = always_redraw(get_area_value)

        # 동적 점 (s-t 그래프 위) - 면적과 연동
        moving_dot_st_area = always_redraw(lambda: Dot(
            axes_st.c2p(t_integral.get_value(), v * t_integral.get_value()),
            color=BLUE,
            radius=0.1
        ))

        self.add(area_fill)
        self.play(FadeIn(area_value_text), FadeIn(moving_dot_st_area), run_time=0.75)

        # 1초마다 멈추면서 면적 값 표시
        s_values = [5, 10, 15, 20]  # 각 초의 누적 이동거리

        area_center_label = None

        for t in range(1, 5):
            self.play(t_integral.animate.set_value(t), run_time=1.5, rate_func=linear)

            # 면적 중앙 위치 계산
            center_t = t / 2
            center_v = v / 2

            new_label = MathTex(
                f"{s_values[t-1]}\\,\\text{{m}}",
                font_size=32,
                color=WHITE
            ).move_to(axes_vt.c2p(center_t, center_v))

            if area_center_label is None:
                self.play(FadeIn(new_label), run_time=0.45)
            else:
                self.play(Transform(area_center_label, new_label), run_time=0.45)

            area_center_label = new_label if area_center_label is None else area_center_label

            self.wait(0.75)

        self.wait(3)
