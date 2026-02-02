from manim import *
import numpy as np


class UniformAccelerationMotion(Scene):
    # ── 물리 상수 ──
    ACCEL = 2
    V_INIT = 5
    TOTAL_TIME = 5
    TOTAL_DIST = 50

    # ── 폰트 크기 ──
    FONT_TITLE = 80
    FONT_SUBTITLE = 28
    FONT_LABEL = 20
    FONT_AXIS_LABEL = 16
    FONT_AXIS_NUM = 20
    FONT_CALC = 36
    FONT_CALC_RESULT = 40

    def construct(self):
        self.intro()
        self.clear_screen()
        self.setup_scene()
        self.animate_motion()
        self.show_displacement()
        self.tangent_to_vt()
        self.area_to_displacement()
        self.clear_screen()
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # ═══════════ Phase 1: 인트로 ═══════════
    def intro(self):
        eq = MathTex("v", "=", "v_0", "+", "a", "t", font_size=self.FONT_TITLE, color=WHITE)
        eq.move_to(ORIGIN)
        self.play(Write(eq), run_time=1.5)
        self.wait(0.5)

        box = SurroundingRectangle(eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        title = Text("등가속도 운동", font_size=44, color=YELLOW)
        title.next_to(box, DOWN, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(1.0)

    # ═══════════ Phase 2: 씬 구성 ═══════════
    def setup_scene(self):
        # ── 1. 타이틀 ──
        self.scene_title = Text("등가속도 운동", font_size=48, color=WHITE)
        self.scene_title.to_edge(UP)
        self.play(Write(self.scene_title))
        self.wait(0.75)

        # ── 2. 트랙 (0~50 m) ──
        TRACK_START = LEFT * 6
        TRACK_END = RIGHT * 6
        self.track_start = TRACK_START
        self.track_end = TRACK_END

        self.track = Line(TRACK_START, TRACK_END, color=WHITE, stroke_width=3)
        self.track.shift(UP * 1.5)

        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(51):
            x_pos = TRACK_START[0] + (TRACK_END[0] - TRACK_START[0]) * (i / 50)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, self.track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 5 == 0:
                label = Text(str(i), font_size=self.FONT_AXIS_LABEL, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        position_label = Text("(m)", font_size=self.FONT_LABEL, color=WHITE)
        position_label.next_to(self.track, RIGHT, buff=0.3)

        self.play(Create(self.track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), Write(position_label), run_time=1.5)
        self.wait(0.45)

        # ── 3. v-t 그래프 (좌하단) ──
        self.axes_vt = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 16, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [5, 7, 9, 11, 13, 15]},
        )
        self.axes_vt.to_corner(DL, buff=0.8)

        x_label_vt = Text("t (s)", font_size=self.FONT_LABEL).next_to(self.axes_vt.x_axis, RIGHT, buff=0.2)
        y_label_vt = Text("v (m/s)", font_size=self.FONT_LABEL).next_to(self.axes_vt.y_axis, UP, buff=0.2)

        self.play(Create(self.axes_vt), Write(x_label_vt), Write(y_label_vt), run_time=1.5)
        self.wait(0.45)

        # ── 4. s-t 그래프 (우하단) ──
        self.axes_st = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 50, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "tip_length": 0.15},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [6, 14, 24, 36, 50]}
        )
        self.axes_st.to_corner(DR, buff=0.8)

        x_label_st = Text("t (s)", font_size=self.FONT_LABEL).next_to(self.axes_st.x_axis, RIGHT, buff=0.2)
        y_label_st = Text("s (m)", font_size=self.FONT_LABEL).next_to(self.axes_st.y_axis, UP, buff=0.2)

        self.play(Create(self.axes_st), Write(x_label_st), Write(y_label_st), run_time=1.5)
        self.wait(0.45)

    # ═══════════ Phase 3: 물체 이동 ═══════════
    def animate_motion(self):
        OBJ_SIZE = 0.4
        ball = Square(side_length=OBJ_SIZE, color=BLUE, fill_opacity=0.8)
        ball_start_x = self.track_start[0]
        ball.move_to([ball_start_x, self.track.get_center()[1] + OBJ_SIZE / 2 + 0.1, 0])

        self.play(FadeIn(ball), run_time=0.75)
        self.wait(0.45)

        self.ghost_group = VGroup()
        self.add(self.ghost_group)

        # ── 1. 속도 라벨 ──
        time_tracker = ValueTracker(0)

        velocity_label = always_redraw(lambda: MathTex(
            f"v = {self.V_INIT + self.ACCEL * time_tracker.get_value():.1f}\\,\\text{{m/s}}",
            font_size=self.FONT_LABEL,
            color=BLUE
        ).next_to(ball, UP, buff=0.1))
        self.add(velocity_label)

        time_tracker.last_int_t = 0

        self.ghost_x_coords = [ball.get_center()[0]]

        # ── 2. 이동 updater ──
        track = self.track
        track_start = self.track_start
        track_end = self.track_end
        v_init = self.V_INIT
        accel = self.ACCEL
        total_dist = self.TOTAL_DIST
        ghost_group = self.ghost_group
        ghost_x_coords = self.ghost_x_coords

        def update_ball(m):
            t = time_tracker.get_value()
            s = v_init * t + 0.5 * accel * t ** 2
            x_ratio = s / total_dist
            new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
            m.move_to([new_x, track.get_center()[1] + OBJ_SIZE / 2 + 0.1, 0])
            current_int_t = int(t)

            if current_int_t > time_tracker.last_int_t:
                current_center = m.get_center()
                ghost_base = Square(side_length=OBJ_SIZE, color=BLUE, fill_opacity=0.3, stroke_width=0)
                ghost_base.move_to(current_center)
                ghost_group.add(ghost_base)
                ghost_x_coords.append(current_center[0])
                time_tracker.last_int_t = current_int_t

        ball.add_updater(update_ball)
        self.play(
            time_tracker.animate.set_value(self.TOTAL_TIME),
            run_time=7.5,
            rate_func=linear
        )
        ball.remove_updater(update_ball)
        self.wait(0.45)

    # ═══════════ Phase 4: 이동거리 표시 ═══════════
    def show_displacement(self):
        prev_s_val = 0

        for i in range(1, len(self.ghost_x_coords)):
            x_prev = self.ghost_x_coords[i - 1]
            x_curr = self.ghost_x_coords[i]

            # ── 트랙 위에 초록색 선 ──
            track_y = self.track.get_center()[1] - 0.2

            interval_line = Line(
                [x_prev, track_y, 0],
                [x_curr, track_y, 0],
                color=GREEN,
                stroke_width=4
            )
            self.play(Create(interval_line), run_time=0.75)

            # ── 그래프 옮기기 ──
            curr_t = i
            curr_s_val = self.V_INIT * curr_t + 0.5 * self.ACCEL * curr_t ** 2

            graph_x = self.axes_st.c2p(curr_t, 0)[0]
            graph_y_bottom = self.axes_st.c2p(0, prev_s_val)[1]
            graph_y_top = self.axes_st.c2p(0, curr_s_val)[1]

            vertical_line = Line(
                [graph_x, graph_y_bottom, 0],
                [graph_x, graph_y_top, 0],
                color=GREEN,
                stroke_width=6
            )

            self.play(Transform(interval_line, vertical_line), run_time=0.9)

            # ── 대시 라인 + 점 ──
            h_dash = DashedLine(
                self.axes_st.c2p(0, curr_s_val),
                self.axes_st.c2p(curr_t, curr_s_val),
                color=GRAY, stroke_width=1.5
            )
            v_dash = DashedLine(
                self.axes_st.c2p(curr_t, 0),
                self.axes_st.c2p(curr_t, curr_s_val),
                color=GRAY, stroke_width=1.5
            )
            new_dot = Dot(self.axes_st.c2p(curr_t, curr_s_val), color=RED, radius=0.08)
            self.play(Create(h_dash), Create(v_dash), FadeIn(new_dot), run_time=0.45)
            self.play(FadeOut(interval_line), run_time=0.3)

            prev_s_val = curr_s_val

    # ═══════════ Phase 5: 접선 기울기 → v-t 점 ═══════════
    def tangent_to_vt(self):
        v_init = self.V_INIT
        accel = self.ACCEL

        # ── 1. s-t 곡선 ──
        self.st_curve = self.axes_st.plot(
            lambda t: v_init * t + 0.5 * accel * t ** 2,
            x_range=[0, 5], color=GREEN, stroke_width=3
        )
        self.play(Create(self.st_curve), run_time=1.5)

        # ── 2. 초기속도 점 ──
        v_dash_vt_0 = DashedLine(
            self.axes_vt.c2p(0, 0),
            self.axes_vt.c2p(0, v_init),
            color=GRAY, stroke_width=1.5
        )
        initial_v_dot = Dot(self.axes_vt.c2p(0, v_init), color=RED, radius=0.08)
        initial_v_label = MathTex(
            "v_0 = 5\\,\\text{m/s}", font_size=self.FONT_LABEL, color=WHITE
        ).next_to(initial_v_dot, UR, buff=0.1)

        self.play(Create(v_dash_vt_0), FadeIn(initial_v_dot), Write(initial_v_label), run_time=0.75)

        # ── 3. 연결 텍스트 ──
        connection_text = Text("s-t 그래프의 접선 기울기 = 속도", font_size=24, color=YELLOW)
        connection_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(connection_text), run_time=0.75)

        # ── 4. 동적 접선 ──
        t_tracker = ValueTracker(0.5)

        moving_dot_st = always_redraw(lambda: Dot(
            self.axes_st.c2p(
                t_tracker.get_value(),
                v_init * t_tracker.get_value() + 0.5 * accel * t_tracker.get_value() ** 2
            ),
            color=YELLOW, radius=0.1
        ))

        axes_st = self.axes_st

        def get_tangent_line():
            t_val = t_tracker.get_value()
            s_val = v_init * t_val + 0.5 * accel * t_val ** 2
            slope = v_init + accel * t_val

            dt = 0.8
            t1, t2 = t_val - dt, t_val + dt
            s1 = s_val + slope * (-dt)
            s2 = s_val + slope * dt

            return Line(
                axes_st.c2p(t1, s1),
                axes_st.c2p(t2, s2),
                color=ORANGE, stroke_width=4
            )

        tangent_line = always_redraw(get_tangent_line)

        slope_text = always_redraw(lambda: MathTex(
            f"v = {v_init + accel * t_tracker.get_value():.0f}\\,\\text{{m/s}}",
            font_size=self.FONT_SUBTITLE,
            color=ORANGE
        ).next_to(axes_st, UP, buff=0.3))

        self.play(
            FadeIn(moving_dot_st),
            FadeIn(tangent_line),
            FadeIn(slope_text),
            run_time=0.75
        )

        # ── 5. 1초씩 이동하며 점 찍기 ──
        vt_dots = []

        for t in range(1, 6):
            self.play(t_tracker.animate.set_value(t), run_time=1.5, rate_func=linear)
            self.wait(0.45)

            v_val = v_init + accel * t

            slope_dot = Dot(
                axes_st.c2p(t, v_init * t + 0.5 * accel * t ** 2),
                color=ORANGE, radius=0.1
            )
            self.add(slope_dot)

            self.play(slope_dot.animate.move_to(self.axes_vt.c2p(t, v_val)), run_time=1.2)

            vt_target = Dot(self.axes_vt.c2p(t, v_val), color=RED, radius=0.08)
            self.play(Transform(slope_dot, vt_target), run_time=0.45)

            vt_dots.append(slope_dot)
            self.wait(0.45)

        # ── 6. 정리 ──
        self.play(
            FadeOut(moving_dot_st),
            FadeOut(tangent_line),
            FadeOut(slope_text),
            FadeOut(connection_text),
            run_time=0.75
        )

        # ── 7. v-t 직선 ──
        self.vt_graph = self.axes_vt.plot(
            lambda t: v_init + accel * t,
            x_range=[0, 5], color=BLUE, stroke_width=3
        )
        self.play(Create(self.vt_graph), run_time=1.5)
        self.wait(0.75)

    # ═══════════ Phase 6: v-t 면적 = 변위 ═══════════
    def area_to_displacement(self):
        v_init = self.V_INIT
        accel = self.ACCEL
        vt_graph = self.vt_graph
        axes_vt = self.axes_vt
        axes_st = self.axes_st

        # ── 1. 설명 텍스트 ──
        area_text = Text("v-t 그래프 아래 면적 = 변위 s", font_size=24, color=YELLOW)
        area_text.to_edge(UP).shift(DOWN * 0.8)
        self.play(Write(area_text), run_time=0.75)

        # ── 2. 동적 면적 ──
        t_integral = ValueTracker(0.01)

        def get_area():
            t_val = t_integral.get_value()
            if t_val < 0.01:
                return VGroup()
            area = axes_vt.get_area(
                vt_graph,
                x_range=[0, t_val],
                color=BLUE, opacity=0.4
            )
            return area

        area_fill = always_redraw(get_area)

        # ── 3. 면적 값 표시 ──
        def get_area_value():
            t_val = t_integral.get_value()
            s_val = v_init * t_val + 0.5 * accel * t_val ** 2
            return MathTex(
                f"S = {s_val:.1f}\\,\\text{{m}}",
                font_size=24,
                color=BLUE
            ).next_to(axes_vt, UP, buff=0.3)

        area_value_text = always_redraw(get_area_value)

        # ── 4. s-t 연동 점 ──
        moving_dot_st_area = always_redraw(lambda: Dot(
            axes_st.c2p(
                t_integral.get_value(),
                v_init * t_integral.get_value() + 0.5 * accel * t_integral.get_value() ** 2
            ),
            color=BLUE, radius=0.1
        ))

        self.add(area_fill)
        self.play(FadeIn(area_value_text), FadeIn(moving_dot_st_area), run_time=0.75)

        # ── 5. 1초마다 면적 값 표시 ──
        s_values = [6, 14, 24, 36, 50]
        area_center_label = None

        for t in range(1, 6):
            self.play(t_integral.animate.set_value(t), run_time=1.5, rate_func=linear)

            center_t = t / 2
            center_v = (v_init + (v_init + accel * t)) / 2

            new_label = MathTex(
                f"{s_values[t - 1]}\\,\\text{{m}}",
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

    # ═══════════ Phase 7: 아웃트로 ═══════════
    def outro(self):
        # ── 1. 핵심 공식 ──
        eq1 = MathTex("v", "=", "v_0", "+", "a", "t", font_size=48, color=WHITE)
        eq2 = MathTex("s", "=", "v_0", "t", "+", "\\frac{1}{2}", "a", "t^2", font_size=48, color=WHITE)
        eq3_left = Text("v-t 면적", font_size=self.FONT_SUBTITLE, color=WHITE)
        eq3_right = Text("= 변위", font_size=self.FONT_SUBTITLE, color=WHITE)
        eq3 = VGroup(eq3_left, eq3_right).arrange(RIGHT, buff=0.2)

        formulas = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.5)
        formulas.move_to(UP * 0.5)

        for eq in formulas:
            self.play(Write(eq), run_time=0.8)
            self.wait(0.3)

        # ── 2. 타이틀 + 박스 ──
        title = Text("등가속도 운동", font_size=44, color=YELLOW)
        title.next_to(formulas, DOWN, buff=0.8)
        box = SurroundingRectangle(
            VGroup(formulas, title), color=YELLOW, buff=0.4,
            corner_radius=0.15, stroke_width=4
        )

        self.play(Write(title), run_time=1.0)
        self.play(Create(box), run_time=0.75)
        self.wait(3)
