from manim import *
import numpy as np

class UniformAccelerationMotion(Scene):
    def construct(self):
        # === Title ===
        title = Text("등가속도 운동", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.75)

        # === 1. 상단 영역: 1차원 수평선 (위치 트랙) ===
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        # 눈금 표시 (0 ~ 50)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(51):
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 50)
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
            x_range=[0, 5, 1],
            y_range=[0, 16, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [5, 7, 9, 11, 13, 15]},
        )
        axes_vt.to_corner(DL, buff=0.8)

        x_label_vt = Text("t (s)", font_size=20).next_to(axes_vt.x_axis, RIGHT, buff=0.2)
        y_label_vt = Text("v (m/s)", font_size=20).next_to(axes_vt.y_axis, UP, buff=0.2)

        self.play(Create(axes_vt), Write(x_label_vt), Write(y_label_vt), run_time=1.5)
        self.wait(0.45)

        # === 3. 하단 영역(우): s-t 그래프 ===
        axes_st = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 50, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [6, 14, 24, 36, 50]}
        )
        axes_st.to_corner(DR, buff=0.8)

        x_label_st = Text("t (s)", font_size=20).next_to(axes_st.x_axis, RIGHT, buff=0.2)
        y_label_st = Text("s (m)", font_size=20).next_to(axes_st.y_axis, UP, buff=0.2)

        self.play(Create(axes_st), Write(x_label_st), Write(y_label_st), run_time=1.5)
        self.wait(0.45)

        # === 4. 물체 생성 ===
        obj_size = 0.4
        obj = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        obj_start_x = track_start[0]
        obj.move_to([obj_start_x, track.get_center()[1] + obj_size/2 + 0.1, 0])

        self.play(FadeIn(obj), run_time=0.75)
        self.wait(0.45)

        ghost_group = VGroup()
        self.add(ghost_group)

        # === 5. 운동 파라미터 및 물체 애니메이션 ===
        total_time = 5
        total_distance = 50
        a = 2  # 가속도 2 m/s^2
        v_0 = 5  # 초기속도 5 m/s

        # 물체 옆에 속도 라벨 (물체와 함께 이동, 동적으로 변함)
        time_tracker = ValueTracker(0)

        velocity_label = always_redraw(lambda: MathTex(
            f"v = {v_0 + a * time_tracker.get_value():.1f}\\,\\text{{m/s}}",
            font_size=20,
            color=BLUE
        ).next_to(obj, UP, buff=0.1))
        self.add(velocity_label)

        time_tracker.last_int_t = 0

        ghost_x_coords = [obj.get_center()[0]]

        def update_obj(m):
            t = time_tracker.get_value()
            s = v_0 * t + 0.5 * a * t ** 2
            v = v_0 + a * t
            x_ratio = s / total_distance
            new_x = track_start[0] + (
                track_end[0] - track_start[0]
            ) * x_ratio
            m.move_to([new_x, track.get_center()[1] + obj_size/2 + 0.1, 0])
            current_int_t = int(t)

            if current_int_t > time_tracker.last_int_t:
                current_center = m.get_center()

                # 내부가 채워진 잔상 생성
                ghost_base = Square(side_length=obj_size, color=BLUE, fill_opacity=0.3, stroke_width=0)
                ghost_base.move_to(current_center)

                ghost_group.add(ghost_base)
                ghost_x_coords.append(current_center[0])

                time_tracker.last_int_t = current_int_t

        obj.add_updater(update_obj)
        self.play(
            time_tracker.animate.set_value(total_time),
            run_time=7.5,
            rate_func=linear
        )
        obj.remove_updater(update_obj)
        self.wait(0.45)

        # === 6. 이동거리 표시 및 그래프로 옮기기 ===
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
            curr_s_val = v_0 * curr_t + 0.5 * a * curr_t ** 2

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

        # === 7. 동적 접선으로 "s-t 기울기 = 속도" 시각화 + v-t 점 찍기 ===
        # s-t 곡선 그리기
        st_curve = axes_st.plot(lambda t: v_0 * t + 0.5 * a * t**2, x_range=[0, 5], color=GREEN, stroke_width=3)
        self.play(Create(st_curve), run_time=1.5)

        # 초기속도 (t=0, v=5) 점 + 대시 라인
        v_dash_vt_0 = DashedLine(
            axes_vt.c2p(0, 0),
            axes_vt.c2p(0, v_0),
            color=GRAY,
            stroke_width=1.5
        )
        initial_v_dot = Dot(axes_vt.c2p(0, v_0), color=RED, radius=0.08)
        initial_v_label = MathTex("v_0 = 5\\,\\text{m/s}", font_size=20, color=WHITE).next_to(initial_v_dot, UR, buff=0.1)

        self.play(Create(v_dash_vt_0), FadeIn(initial_v_dot), Write(initial_v_label), run_time=0.75)

        # 연결 개념 텍스트
        connection_text = Text("s-t 그래프의 접선 기울기 = 속도", font_size=24, color=YELLOW)
        connection_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(connection_text), run_time=0.75)

        # 시간 트래커
        t_tracker = ValueTracker(0.5)

        # 동적 점 (s-t 그래프 위)
        moving_dot_st = always_redraw(lambda: Dot(
            axes_st.c2p(t_tracker.get_value(), v_0 * t_tracker.get_value() + 0.5 * a * t_tracker.get_value()**2),
            color=YELLOW,
            radius=0.1
        ))

        # 동적 접선 (접선의 기울기 = 속도)
        def get_tangent_line():
            t_val = t_tracker.get_value()
            s_val = v_0 * t_val + 0.5 * a * t_val**2
            slope = v_0 + a * t_val  # ds/dt = v = v_0 + at

            # 접선 길이 조절
            dt = 0.8
            t1, t2 = t_val - dt, t_val + dt
            s1 = s_val + slope * (-dt)
            s2 = s_val + slope * dt

            return Line(
                axes_st.c2p(t1, s1),
                axes_st.c2p(t2, s2),
                color=ORANGE,
                stroke_width=4
            )

        tangent_line = always_redraw(get_tangent_line)

        # 기울기 값 표시
        slope_text = always_redraw(lambda: MathTex(
            f"v = {v_0 + a * t_tracker.get_value():.0f}\\,\\text{{m/s}}",
            font_size=28,
            color=ORANGE
        ).next_to(axes_st, UP, buff=0.3))

        self.play(
            FadeIn(moving_dot_st),
            FadeIn(tangent_line),
            FadeIn(slope_text),
            run_time=0.75
        )

        # v-t 그래프에 찍을 점들 저장
        vt_dots = []

        # 1초씩 이동하며 점 찍기
        for t in range(1, 6):
            # t까지 애니메이션
            self.play(t_tracker.animate.set_value(t), run_time=1.5, rate_func=linear)
            self.wait(0.45)

            # 현재 속도 값
            v_val = v_0 + a * t

            # s-t 접선 위치에서 점 생성
            slope_dot = Dot(axes_st.c2p(t, v_0 * t + 0.5 * a * t**2), color=ORANGE, radius=0.1)
            self.add(slope_dot)

            # 점이 s-t → v-t로 이동하는 애니메이션
            self.play(slope_dot.animate.move_to(axes_vt.c2p(t, v_val)), run_time=1.2)

            # 빨간 점으로 변환
            vt_target = Dot(axes_vt.c2p(t, v_val), color=RED, radius=0.08)
            self.play(Transform(slope_dot, vt_target), run_time=0.45)

            vt_dots.append(slope_dot)
            self.wait(0.45)

        # 동적 요소 정리
        self.play(
            FadeOut(moving_dot_st),
            FadeOut(tangent_line),
            FadeOut(slope_text),
            FadeOut(connection_text),
            run_time=0.75
        )

        # v-t 그래프에 직선 그리기
        vt_graph = axes_vt.plot(lambda t: v_0 + a * t, x_range=[0, 5], color=BLUE, stroke_width=3)
        self.play(Create(vt_graph), run_time=1.5)

        self.wait(0.75)

        # === 8. v-t 그래프 적분 면적 = 이동거리 시각화 ===
        # 새 설명 텍스트
        area_text = Text("v-t 그래프 아래 면적 = 이동거리 s", font_size=24, color=YELLOW)
        area_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(area_text), run_time=0.75)

        # 시간 트래커 (적분용)
        t_integral = ValueTracker(0.01)

        # 동적 면적 (사다리꼴)
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
            s_val = v_0 * t_val + 0.5 * a * t_val**2
            return MathTex(
                f"S = {s_val:.1f}\\,\\text{{m}}",
                font_size=24,
                color=BLUE
            ).next_to(axes_vt, UP, buff=0.3)

        area_value_text = always_redraw(get_area_value)

        # 동적 점 (s-t 그래프 위) - 면적과 연동
        moving_dot_st_area = always_redraw(lambda: Dot(
            axes_st.c2p(t_integral.get_value(), v_0 * t_integral.get_value() + 0.5 * a * t_integral.get_value()**2),
            color=BLUE,
            radius=0.1
        ))

        self.add(area_fill)
        self.play(FadeIn(area_value_text), FadeIn(moving_dot_st_area), run_time=0.75)

        # 1초마다 멈추면서 면적 값 표시 (하나의 숫자가 업데이트)
        s_values = [6, 14, 24, 36, 50]  # 각 초의 누적 이동거리

        area_center_label = None

        for t in range(1, 6):
            # t-1 → t 까지 애니메이션
            self.play(t_integral.animate.set_value(t), run_time=1.5, rate_func=linear)

            # 면적 중앙 위치 계산
            center_t = t / 2
            center_v = (v_0 + (v_0 + a * t)) / 2  # 평균 속도

            # 새 레이블 생성
            new_label = MathTex(
                f"{s_values[t-1]}\\,\\text{{m}}",
                font_size=32,
                color=WHITE
            ).move_to(axes_vt.c2p(center_t, center_v / 2))

            if area_center_label is None:
                self.play(FadeIn(new_label), run_time=0.45)
            else:
                self.play(Transform(area_center_label, new_label), run_time=0.45)

            area_center_label = new_label if area_center_label is None else area_center_label

            self.wait(0.75)

        self.wait(3)
