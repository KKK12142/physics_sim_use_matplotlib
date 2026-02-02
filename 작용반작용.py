from manim import *
import numpy as np


class NewtonsThirdLaw(Scene):
    def construct(self):
        self.intro()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase1_equal_mass()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase2_different_mass()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase3_examples()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase4_misconception()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.outro()

    # =========================================================
    # Intro
    # =========================================================
    def intro(self):
        eq = MathTex(r"\vec{F}_{AB}", "=", r"-\vec{F}_{BA}", font_size=80, color=WHITE)
        eq.move_to(ORIGIN)
        self.play(Write(eq), run_time=2.0)
        self.wait(0.5)

        box = SurroundingRectangle(eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        title = Text("뉴턴의 운동 제3법칙: 작용과 반작용", font_size=44, color=YELLOW)
        title.next_to(box, DOWN, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.75)

        subtitle = Text("A가 B를 밀면, B도 A를 똑같은 힘으로 밉니다", font_size=28, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 1: 실험 A — 같은 질량 (m vs m)
    # =========================================================
    def phase1_equal_mass(self):
        title = Text("실험 A: 같은 질량 (m vs m)", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track ---
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(21):
            val = i - 10
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 20)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 5 == 0:
                label = Text(str(val), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        self.play(Create(track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), run_time=0.75)

        # --- 수식 정리 영역 (하단 좌) ---
        info_origin = DOWN * 1.2 + LEFT * 4.0
        info_title = Text("수식 정리", font_size=22, color=YELLOW)
        info_title.move_to(info_origin + UP * 1.3)
        self.play(Write(info_title), run_time=0.5)

        # --- v-t graph (하단 우) ---
        axes_vt = Axes(
            x_range=[0, 2, 0.5], y_range=[-4, 4, 1],
            x_length=4.5, y_length=3.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0.5, 1.0, 1.5, 2.0]},
            y_axis_config={"numbers_to_include": [-3, -1, 1, 3]},
        )
        axes_vt.to_corner(DR, buff=0.6)
        x_lab = Text("t (s)", font_size=18).next_to(axes_vt.x_axis, RIGHT, buff=0.15)
        y_lab = Text("v (m/s)", font_size=18).next_to(axes_vt.y_axis, UP, buff=0.15)
        self.play(Create(axes_vt), Write(x_lab), Write(y_lab), run_time=0.75)
        self.wait(0.3)

        # --- 물체 배치 ---
        obj_size = 0.45
        center_y = track.get_center()[1]

        box_a = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        box_b = Square(side_length=obj_size, color=RED, fill_opacity=0.8)
        label_a = Text("A", font_size=18, color=WHITE)
        label_b = Text("B", font_size=18, color=WHITE)

        # A와 B가 접촉한 상태로 배치
        box_a.move_to([0 - obj_size / 2, center_y + obj_size / 2 + 0.1, 0])
        box_b.move_to([0 + obj_size / 2, center_y + obj_size / 2 + 0.1, 0])
        label_a.move_to(box_a)
        label_b.move_to(box_b)

        mass_a = MathTex("m", font_size=20, color=BLUE).next_to(box_a, UP, buff=0.1)
        mass_b = MathTex("m", font_size=20, color=RED).next_to(box_b, UP, buff=0.1)

        # 접촉면 표시
        contact_line = DashedLine(
            [0, center_y + obj_size + 0.15, 0],
            [0, center_y + 0.05, 0],
            color=YELLOW, stroke_width=2, dash_length=0.06
        )

        self.play(
            FadeIn(box_a), FadeIn(box_b), Write(label_a), Write(label_b),
            Write(mass_a), Write(mass_b), Create(contact_line),
            run_time=1.0
        )
        self.wait(0.3)

        # 접촉 상태의 시작 위치 기록
        start_a_x = box_a.get_center()[0]
        start_b_x = box_b.get_center()[0]

        # "서로 밀기!" 텍스트
        push_text = Text("서로 밀기!", font_size=32, color=YELLOW)
        push_text.next_to(contact_line, UP, buff=0.4)
        self.play(Write(push_text), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(push_text), FadeOut(contact_line), run_time=0.3)

        # --- 운동 시뮬레이션 ---
        accel = 3.0
        force_time = 1.0
        v_final = accel * force_time  # 3 m/s
        scale_factor = 0.5

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= force_time:
                return -0.5 * accel * t ** 2
            else:
                s1 = 0.5 * accel * force_time ** 2
                return -(s1 + v_final * (t - force_time))

        def pos_b(t):
            if t <= force_time:
                return 0.5 * accel * t ** 2
            else:
                s1 = 0.5 * accel * force_time ** 2
                return s1 + v_final * (t - force_time)

        def update_box_a(m):
            t = time_tracker.get_value()
            x = start_a_x + pos_a(t) * scale_factor
            m.move_to([x, center_y + obj_size / 2 + 0.1, 0])

        def update_box_b(m):
            t = time_tracker.get_value()
            x = start_b_x + pos_b(t) * scale_factor
            m.move_to([x, center_y + obj_size / 2 + 0.1, 0])

        label_a.add_updater(lambda m: m.move_to(box_a))
        label_b.add_updater(lambda m: m.move_to(box_b))
        mass_a.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))
        mass_b.add_updater(lambda m: m.next_to(box_b, UP, buff=0.1))

        # 힘 화살표 (가속 구간에만)
        force_arrow_a = always_redraw(lambda: Arrow(
            start=box_a.get_left(),
            end=box_a.get_left() + LEFT * 0.6,
            color=BLUE, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() <= force_time else VMobject())

        force_arrow_b = always_redraw(lambda: Arrow(
            start=box_b.get_right(),
            end=box_b.get_right() + RIGHT * 0.6,
            color=RED, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() <= force_time else VMobject())

        self.add(force_arrow_a, force_arrow_b)

        # v-t 그래프 라인
        vt_line_a = always_redraw(lambda: axes_vt.plot(
            lambda t: -(accel * t if t <= force_time else v_final),
            x_range=[0, max(time_tracker.get_value(), 0.02)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        vt_line_b = always_redraw(lambda: axes_vt.plot(
            lambda t: accel * t if t <= force_time else v_final,
            x_range=[0, max(time_tracker.get_value(), 0.02)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        self.add(vt_line_a, vt_line_b)

        box_a.add_updater(update_box_a)
        box_b.add_updater(update_box_b)

        # 수식 1: 힘 동일
        info_eq1 = MathTex(r"F_A = F_B = 3\,\text{N}", font_size=24, color=WHITE)
        info_eq1.move_to(info_origin + UP * 0.7)
        self.play(Write(info_eq1), run_time=0.5)

        self.play(time_tracker.animate.set_value(1.0), run_time=2.5, rate_func=linear)

        # 수식 2: 가속도 동일
        info_eq2 = MathTex(r"a_A = a_B = 3\,\text{m/s}^2", font_size=24, color=WHITE)
        info_eq2.move_to(info_origin + UP * 0.1)
        self.play(Write(info_eq2), run_time=0.5)

        self.play(time_tracker.animate.set_value(2.0), run_time=2.5, rate_func=linear)

        box_a.clear_updaters()
        box_b.clear_updaters()
        label_a.clear_updaters()
        label_b.clear_updaters()
        mass_a.clear_updaters()
        mass_b.clear_updaters()
        self.remove(force_arrow_a, force_arrow_b, vt_line_a, vt_line_b)

        # 최종 v-t 라인 (정적)
        final_vt_a = axes_vt.plot(
            lambda t: -(accel * t if t <= force_time else v_final),
            x_range=[0, 2], color=BLUE, stroke_width=3
        )
        final_vt_b = axes_vt.plot(
            lambda t: accel * t if t <= force_time else v_final,
            x_range=[0, 2], color=RED, stroke_width=3
        )
        vt_label_a = Text("A", font_size=16, color=BLUE).next_to(axes_vt.c2p(2, -3), LEFT, buff=0.1)
        vt_label_b = Text("B", font_size=16, color=RED).next_to(axes_vt.c2p(2, 3), LEFT, buff=0.1)
        self.add(final_vt_a, final_vt_b)
        self.play(Write(vt_label_a), Write(vt_label_b), run_time=0.5)

        # v-t 점선 보조선: t=1 수직, v=±3 수평
        dash_vert = DashedLine(
            axes_vt.c2p(1, -4), axes_vt.c2p(1, 4),
            color=GRAY, stroke_width=1.5, dash_length=0.08
        )
        dash_h_a = DashedLine(
            axes_vt.c2p(0, -3), axes_vt.c2p(1, -3),
            color=BLUE, stroke_width=1.5, dash_length=0.08, stroke_opacity=0.5
        )
        dash_h_b = DashedLine(
            axes_vt.c2p(0, 3), axes_vt.c2p(1, 3),
            color=RED, stroke_width=1.5, dash_length=0.08, stroke_opacity=0.5
        )
        t1_label = MathTex("t=1", font_size=14, color=GRAY).next_to(axes_vt.c2p(1, -4), DOWN, buff=0.1)
        va_label = MathTex("v=-3", font_size=14, color=BLUE).next_to(axes_vt.c2p(0, -3), LEFT, buff=0.1)
        vb_label = MathTex("v=3", font_size=14, color=RED).next_to(axes_vt.c2p(0, 3), LEFT, buff=0.1)

        self.play(
            Create(dash_vert), Create(dash_h_a), Create(dash_h_b),
            Write(t1_label), Write(va_label), Write(vb_label),
            run_time=0.75
        )

        # 수식 3: 결론
        info_eq3 = Text("질량이 같으면 가속도도 같다", font_size=20, color=YELLOW)
        info_eq3.move_to(info_origin + DOWN * 0.5)
        self.play(Write(info_eq3), run_time=0.75)
        self.wait(2.0)

    # =========================================================
    # Phase 2: 실험 B — 다른 질량 (m vs 3m) ★
    # =========================================================
    def phase2_different_mass(self):
        title = Text("실험 B: 다른 질량 (m vs 3m)", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track ---
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(21):
            val = i - 10
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 20)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 5 == 0:
                label = Text(str(val), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        self.play(Create(track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), run_time=0.75)

        # --- 수식 정리 영역 (하단 좌) ---
        info_origin = DOWN * 1.2 + LEFT * 4.0
        info_title = Text("수식 정리", font_size=22, color=YELLOW)
        info_title.move_to(info_origin + UP * 1.3)
        self.play(Write(info_title), run_time=0.5)

        # --- v-t graph (하단 우) ---
        axes_vt = Axes(
            x_range=[0, 2, 0.5], y_range=[-4, 2, 1],
            x_length=4.5, y_length=3.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0.5, 1.0, 1.5, 2.0]},
            y_axis_config={"numbers_to_include": [-3, -2, -1, 1]},
        )
        axes_vt.to_corner(DR, buff=0.6)
        x_lab = Text("t (s)", font_size=18).next_to(axes_vt.x_axis, RIGHT, buff=0.15)
        y_lab = Text("v (m/s)", font_size=18).next_to(axes_vt.y_axis, UP, buff=0.15)
        self.play(Create(axes_vt), Write(x_lab), Write(y_lab), run_time=0.75)
        self.wait(0.3)

        # --- 물체 배치 ---
        obj_size = 0.4
        center_y = track.get_center()[1]

        box_a = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        label_a = Text("A", font_size=16, color=WHITE)
        mass_a_label = MathTex("m", font_size=20, color=BLUE)

        box_b = VGroup(*[
            Square(side_length=obj_size, color=RED, fill_opacity=0.8)
            for _ in range(3)
        ])
        box_b.arrange(UP, buff=0)
        label_b = Text("B", font_size=16, color=WHITE)
        mass_b_label = MathTex("3m", font_size=20, color=RED)

        # A와 B가 접촉한 상태로 배치
        box_a.move_to([0 - obj_size / 2, center_y + obj_size / 2 + 0.1, 0])
        box_b.move_to([0 + obj_size / 2, center_y + box_b.get_height() / 2 + 0.1, 0])
        label_a.move_to(box_a)
        label_b.move_to(box_b)
        mass_a_label.next_to(box_a, UP, buff=0.1)
        mass_b_label.next_to(box_b, UP, buff=0.1)

        # 접촉면 표시
        contact_y_top = center_y + box_b.get_height() + 0.15
        contact_line = DashedLine(
            [0, contact_y_top, 0],
            [0, center_y + 0.05, 0],
            color=YELLOW, stroke_width=2, dash_length=0.06
        )

        self.play(
            FadeIn(box_a), FadeIn(box_b), Write(label_a), Write(label_b),
            Write(mass_a_label), Write(mass_b_label), Create(contact_line),
            run_time=1.0
        )
        self.wait(0.3)

        # 접촉 상태의 시작 위치 기록
        start_a_x = box_a.get_center()[0]
        start_b_x = box_b.get_center()[0]

        # 질문
        question = Text("가벼운 A와 무거운 B, 누가 더 큰 힘을 받을까요?", font_size=26, color=YELLOW)
        question.next_to(title, DOWN, buff=0.25)
        self.play(Write(question), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(question), run_time=0.5)

        # "서로 밀기!"
        push_text = Text("서로 밀기!", font_size=32, color=YELLOW)
        push_text.next_to(contact_line, UP, buff=0.4)
        self.play(Write(push_text), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(push_text), FadeOut(contact_line), run_time=0.3)

        # --- 운동 시뮬레이션 ---
        a_A = 3.0
        a_B = 1.0
        force_time = 1.0
        v_A = a_A * force_time  # 3
        v_B = a_B * force_time  # 1
        scale_factor = 0.5

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= force_time:
                return -0.5 * a_A * t ** 2
            else:
                s1 = 0.5 * a_A * force_time ** 2
                return -(s1 + v_A * (t - force_time))

        def pos_b(t):
            if t <= force_time:
                return 0.5 * a_B * t ** 2
            else:
                s1 = 0.5 * a_B * force_time ** 2
                return s1 + v_B * (t - force_time)

        def update_box_a(m):
            t = time_tracker.get_value()
            x = start_a_x + pos_a(t) * scale_factor
            m.move_to([x, center_y + obj_size / 2 + 0.1, 0])

        def update_box_b(m):
            t = time_tracker.get_value()
            x = start_b_x + pos_b(t) * scale_factor
            bh = m.get_height()
            m.move_to([x, center_y + bh / 2 + 0.1, 0])

        label_a.add_updater(lambda m: m.move_to(box_a))
        label_b.add_updater(lambda m: m.move_to(box_b))
        mass_a_label.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))
        mass_b_label.add_updater(lambda m: m.next_to(box_b, UP, buff=0.1))

        # 힘 화살표 (같은 길이!)
        force_arrow_a = always_redraw(lambda: Arrow(
            start=box_a.get_left(),
            end=box_a.get_left() + LEFT * 0.6,
            color=BLUE, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() <= force_time else VMobject())

        force_arrow_b = always_redraw(lambda: Arrow(
            start=box_b.get_right(),
            end=box_b.get_right() + RIGHT * 0.6,
            color=RED, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() <= force_time else VMobject())

        self.add(force_arrow_a, force_arrow_b)

        # v-t 그래프 라인
        vt_line_a = always_redraw(lambda: axes_vt.plot(
            lambda t: -(a_A * t if t <= force_time else v_A),
            x_range=[0, max(time_tracker.get_value(), 0.02)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        vt_line_b = always_redraw(lambda: axes_vt.plot(
            lambda t: a_B * t if t <= force_time else v_B,
            x_range=[0, max(time_tracker.get_value(), 0.02)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        self.add(vt_line_a, vt_line_b)

        box_a.add_updater(update_box_a)
        box_b.add_updater(update_box_b)

        # 수식 1: 힘 동일
        info_eq1 = MathTex(r"F_A = F_B = 3\,\text{N}", font_size=24, color=WHITE)
        info_eq1.move_to(info_origin + UP * 0.7)
        self.play(Write(info_eq1), run_time=0.5)

        self.play(time_tracker.animate.set_value(1.0), run_time=2.5, rate_func=linear)

        # 수식 2: 가속도 다름
        info_eq2a = MathTex(r"a_A = \frac{F}{m} = 3\,\text{m/s}^2", font_size=22, color=BLUE)
        info_eq2a.move_to(info_origin + UP * 0.1)
        info_eq2b = MathTex(r"a_B = \frac{F}{3m} = 1\,\text{m/s}^2", font_size=22, color=RED)
        info_eq2b.move_to(info_origin + DOWN * 0.4)
        self.play(Write(info_eq2a), run_time=0.5)
        self.play(Write(info_eq2b), run_time=0.5)

        self.play(time_tracker.animate.set_value(2.0), run_time=2.5, rate_func=linear)

        box_a.clear_updaters()
        box_b.clear_updaters()
        label_a.clear_updaters()
        label_b.clear_updaters()
        mass_a_label.clear_updaters()
        mass_b_label.clear_updaters()
        self.remove(force_arrow_a, force_arrow_b, vt_line_a, vt_line_b)

        # 최종 정적 그래프
        final_vt_a = axes_vt.plot(
            lambda t: -(a_A * t if t <= force_time else v_A),
            x_range=[0, 2], color=BLUE, stroke_width=3
        )
        final_vt_b = axes_vt.plot(
            lambda t: a_B * t if t <= force_time else v_B,
            x_range=[0, 2], color=RED, stroke_width=3
        )
        vt_label_a = Text("A (a=3)", font_size=14, color=BLUE).next_to(axes_vt.c2p(2, -3), LEFT, buff=0.1)
        vt_label_b = Text("B (a=1)", font_size=14, color=RED).next_to(axes_vt.c2p(2, 1), LEFT, buff=0.1)
        self.add(final_vt_a, final_vt_b)
        self.play(Write(vt_label_a), Write(vt_label_b), run_time=0.5)

        # v-t 점선 보조선: t=1 수직, v=-3 / v=+1 수평
        dash_vert = DashedLine(
            axes_vt.c2p(1, -4), axes_vt.c2p(1, 2),
            color=GRAY, stroke_width=1.5, dash_length=0.08
        )
        dash_h_a = DashedLine(
            axes_vt.c2p(0, -3), axes_vt.c2p(1, -3),
            color=BLUE, stroke_width=1.5, dash_length=0.08, stroke_opacity=0.5
        )
        dash_h_b = DashedLine(
            axes_vt.c2p(0, 1), axes_vt.c2p(1, 1),
            color=RED, stroke_width=1.5, dash_length=0.08, stroke_opacity=0.5
        )
        t1_label = MathTex("t=1", font_size=14, color=GRAY).next_to(axes_vt.c2p(1, -4), DOWN, buff=0.1)
        va_label = MathTex("v=-3", font_size=14, color=BLUE).next_to(axes_vt.c2p(0, -3), LEFT, buff=0.1)
        vb_label = MathTex("v=1", font_size=14, color=RED).next_to(axes_vt.c2p(0, 1), LEFT, buff=0.1)

        self.play(
            Create(dash_vert), Create(dash_h_a), Create(dash_h_b),
            Write(t1_label), Write(va_label), Write(vb_label),
            run_time=0.75
        )
        self.wait(0.5)

        # 반전: 힘은 같다!
        surprise = Text("힘의 크기는 동일!", font_size=28, color=YELLOW)
        surprise.next_to(track, DOWN, buff=0.3)
        self.play(Write(surprise), run_time=0.75)
        self.wait(1.0)

        # 수식 3: 결론
        info_eq3 = Text("힘은 같지만 가속도는 다르다!", font_size=20, color=YELLOW)
        info_eq3.move_to(info_origin + DOWN * 1.0)
        self.play(FadeOut(surprise), Write(info_eq3), run_time=0.75)
        self.wait(2.0)

    # =========================================================
    # Phase 3: 일상 속 작용-반작용 예시
    # =========================================================
    def phase3_examples(self):
        title = Text("일상 속 작용과 반작용", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- 예시 1: 벽을 미는 사람 (왼쪽 절반) ----
        ex1_title = Text("예시 1: 벽 밀기", font_size=24, color=YELLOW)
        ex1_title.move_to(UP * 2.2 + LEFT * 3.5)
        self.play(Write(ex1_title), run_time=0.5)

        # 벽
        wall = Rectangle(width=0.4, height=2.5, color=GRAY, fill_opacity=0.6)
        wall.move_to(LEFT * 2 + DOWN * 0.2)

        # 사람 (원 + 몸체)
        person_head = Circle(radius=0.25, color=BLUE, fill_opacity=0.8)
        person_body = Line(ORIGIN, DOWN * 0.8, color=BLUE, stroke_width=4)
        person_arms = Line(LEFT * 0.4, RIGHT * 0.4, color=BLUE, stroke_width=4)
        person_legs = VGroup(
            Line(ORIGIN, DL * 0.5, color=BLUE, stroke_width=4),
            Line(ORIGIN, DR * 0.5, color=BLUE, stroke_width=4),
        )
        person_body.next_to(person_head, DOWN, buff=0)
        person_arms.move_to(person_body.get_start() + DOWN * 0.2)
        person_legs[0].move_to(person_body.get_end(), aligned_edge=UP)
        person_legs[1].move_to(person_body.get_end(), aligned_edge=UP)
        person = VGroup(person_head, person_body, person_arms, person_legs)
        person.move_to(LEFT * 4 + DOWN * 0.2)

        wall_label = Text("벽", font_size=20, color=GRAY).next_to(wall, UP, buff=0.1)
        person_label = Text("사람", font_size=20, color=BLUE).next_to(person, UP, buff=0.1)

        self.play(FadeIn(wall), FadeIn(person), Write(wall_label), Write(person_label), run_time=0.75)

        # 사람이 벽에 접근
        self.play(person.animate.shift(RIGHT * 1.3), person_label.animate.shift(RIGHT * 1.3), run_time=0.75)

        # 힘 화살표
        f_person_wall = Arrow(
            start=wall.get_left() + LEFT * 0.1,
            end=wall.get_left() + RIGHT * 0.8,
            color=RED, buff=0, stroke_width=5
        )
        f_wall_person = Arrow(
            start=wall.get_left() + LEFT * 0.1,
            end=wall.get_left() + LEFT * 1.0,
            color=ORANGE, buff=0, stroke_width=5
        )
        f_pw_label = MathTex(r"\vec{F}_{PW}", font_size=18, color=RED)
        f_pw_label.next_to(f_person_wall, UP, buff=0.05)
        f_wp_label = MathTex(r"\vec{F}_{WP}", font_size=18, color=ORANGE)
        f_wp_label.next_to(f_wall_person, UP, buff=0.05)

        self.play(Create(f_person_wall), Write(f_pw_label), run_time=0.75)
        self.play(Create(f_wall_person), Write(f_wp_label), run_time=0.75)

        eq1 = MathTex(r"|\vec{F}_{PW}| = |\vec{F}_{WP}|", font_size=22, color=YELLOW)
        eq1.move_to(LEFT * 3.5 + DOWN * 2.2)
        self.play(Write(eq1), run_time=0.75)
        self.wait(1.0)

        # ---- 예시 2: 지구와 사과 (오른쪽 절반) ----
        ex2_title = Text("예시 2: 사과와 지구", font_size=24, color=YELLOW)
        ex2_title.move_to(UP * 2.2 + RIGHT * 3.5)
        self.play(Write(ex2_title), run_time=0.5)

        # 지구
        earth = Circle(radius=1.0, color=GREEN, fill_opacity=0.5)
        earth.move_to(RIGHT * 3.5 + DOWN * 1.8)
        earth_label = MathTex("M", font_size=24, color=GREEN).move_to(earth)
        earth_name = Text("지구", font_size=18, color=GREEN).next_to(earth, DOWN, buff=0.1)

        # 사과
        apple = Circle(radius=0.15, color=RED, fill_opacity=0.9)
        apple.move_to(RIGHT * 3.5 + UP * 1.2)
        apple_label = MathTex("m", font_size=18, color=RED).next_to(apple, RIGHT, buff=0.1)
        apple_name = Text("사과", font_size=18, color=RED).next_to(apple, LEFT, buff=0.1)

        self.play(
            FadeIn(earth), Write(earth_label), Write(earth_name),
            FadeIn(apple), Write(apple_label), Write(apple_name),
            run_time=0.75
        )

        # 중력 화살표
        g_on_apple = Arrow(
            start=apple.get_bottom(),
            end=apple.get_bottom() + DOWN * 1.0,
            color=RED, buff=0, stroke_width=5
        )
        g_on_earth = Arrow(
            start=earth.get_top(),
            end=earth.get_top() + UP * 0.15,
            color=ORANGE, buff=0, stroke_width=5
        )
        g_apple_label = MathTex(r"mg", font_size=18, color=RED).next_to(g_on_apple, RIGHT, buff=0.05)
        g_earth_label = MathTex(r"mg", font_size=18, color=ORANGE).next_to(g_on_earth, LEFT, buff=0.05)

        self.play(Create(g_on_apple), Write(g_apple_label), run_time=0.75)
        self.play(Create(g_on_earth), Write(g_earth_label), run_time=0.75)

        # 설명
        accel_text = MathTex(
            r"a_{m} = g \approx 9.8\,\text{m/s}^2",
            font_size=20, color=WHITE
        )
        accel_text2 = MathTex(
            r"a_{M} = \frac{mg}{M} \approx 0",
            font_size=20, color=WHITE
        )
        accel_text.move_to(RIGHT * 3.5 + DOWN * 0.2)
        accel_text2.next_to(accel_text, DOWN, buff=0.2)

        self.play(Write(accel_text), run_time=0.75)
        self.play(Write(accel_text2), run_time=0.75)

        insight = Text("힘은 같지만, 질량 차이로 가속도가 다르다!", font_size=22, color=YELLOW)
        insight.to_edge(DOWN, buff=0.3)
        self.play(Write(insight), run_time=0.75)
        self.wait(2.0)

    # =========================================================
    # Phase 4: 오개념 타파 — 작용반작용 vs 힘의 평형
    # =========================================================
    def phase4_misconception(self):
        title = Text("작용 반작용 vs 힘의 평형", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- 왼쪽: 작용 반작용 ---
        left_title = Text("작용 반작용", font_size=24, color=YELLOW)
        left_title.move_to(UP * 2 + LEFT * 3.5)
        self.play(Write(left_title), run_time=0.5)

        ball_a = Circle(radius=0.35, color=BLUE, fill_opacity=0.8)
        ball_b = Circle(radius=0.35, color=RED, fill_opacity=0.8)
        ball_a.move_to(LEFT * 4.5 + UP * 0.5)
        ball_b.move_to(LEFT * 2.5 + UP * 0.5)
        lbl_a = Text("A", font_size=18, color=WHITE).move_to(ball_a)
        lbl_b = Text("B", font_size=18, color=WHITE).move_to(ball_b)

        self.play(FadeIn(ball_a), FadeIn(ball_b), Write(lbl_a), Write(lbl_b), run_time=0.75)

        self.play(
            ball_a.animate.move_to(LEFT * 3.8 + UP * 0.5),
            ball_b.animate.move_to(LEFT * 3.2 + UP * 0.5),
            lbl_a.animate.move_to(LEFT * 3.8 + UP * 0.5),
            lbl_b.animate.move_to(LEFT * 3.2 + UP * 0.5),
            run_time=0.5
        )

        f_ab = Arrow(
            start=ball_b.get_center(),
            end=ball_b.get_center() + RIGHT * 1.0,
            color=RED, buff=0, stroke_width=4
        )
        f_ba = Arrow(
            start=ball_a.get_center(),
            end=ball_a.get_center() + LEFT * 1.0,
            color=BLUE, buff=0, stroke_width=4
        )
        f_ab_label = MathTex(r"\vec{F}_{AB}", font_size=20, color=RED).next_to(f_ab, UP, buff=0.05)
        f_ba_label = MathTex(r"\vec{F}_{BA}", font_size=20, color=BLUE).next_to(f_ba, UP, buff=0.05)

        self.play(
            Create(f_ab), Create(f_ba),
            Write(f_ab_label), Write(f_ba_label),
            run_time=0.75
        )

        key1 = Text("힘의 주인이 서로 다르다", font_size=18, color=WHITE)
        key1.move_to(LEFT * 3.5 + DOWN * 0.4)
        arrow1 = Text("→ 상쇄 안됨", font_size=18, color=ORANGE)
        arrow1.next_to(key1, DOWN, buff=0.15)
        self.play(Write(key1), run_time=0.5)
        self.play(Write(arrow1), run_time=0.5)

        self.play(
            ball_a.animate.move_to(LEFT * 5.5 + UP * 0.5),
            ball_b.animate.move_to(LEFT * 1.5 + UP * 0.5),
            lbl_a.animate.move_to(LEFT * 5.5 + UP * 0.5),
            lbl_b.animate.move_to(LEFT * 1.5 + UP * 0.5),
            FadeOut(f_ab), FadeOut(f_ba), FadeOut(f_ab_label), FadeOut(f_ba_label),
            run_time=0.75
        )
        self.wait(0.3)

        # --- 오른쪽: 힘의 평형 ---
        right_title = Text("힘의 평형", font_size=24, color=YELLOW)
        right_title.move_to(UP * 2 + RIGHT * 3.5)
        self.play(Write(right_title), run_time=0.5)

        box_c = Square(side_length=0.6, color=GREEN, fill_opacity=0.8)
        box_c.move_to(RIGHT * 3.5 + UP * 0.5)
        lbl_c = Text("C", font_size=18, color=WHITE).move_to(box_c)
        self.play(FadeIn(box_c), Write(lbl_c), run_time=0.5)

        f1 = Arrow(
            start=box_c.get_left() + LEFT * 1.0,
            end=box_c.get_left(),
            color=ORANGE, buff=0, stroke_width=4
        )
        f2 = Arrow(
            start=box_c.get_right() + RIGHT * 1.0,
            end=box_c.get_right(),
            color=PURPLE, buff=0, stroke_width=4
        )
        f1_label = MathTex(r"\vec{F}_1", font_size=20, color=ORANGE).next_to(f1, UP, buff=0.05)
        f2_label = MathTex(r"\vec{F}_2", font_size=20, color=PURPLE).next_to(f2, UP, buff=0.05)

        self.play(Create(f1), Create(f2), Write(f1_label), Write(f2_label), run_time=0.75)

        key2 = Text("힘의 주인이 같다", font_size=18, color=WHITE)
        key2.move_to(RIGHT * 3.5 + DOWN * 0.4)
        arrow2 = Text("→ 상쇄됨 → 정지", font_size=18, color=ORANGE)
        arrow2.next_to(key2, DOWN, buff=0.15)
        self.play(Write(key2), run_time=0.5)
        self.play(Write(arrow2), run_time=0.5)

        sum_f = MathTex(r"\sum F = 0", font_size=24, color=GREEN)
        sum_f.next_to(arrow2, DOWN, buff=0.2)
        self.play(Write(sum_f), run_time=0.5)
        self.wait(0.5)

        # --- 비교 표 ---
        table = Table(
            [["서로 다른 두 물체", "같은 한 물체"],
             ["상쇄 안됨", "상쇄됨"]],
            row_labels=[Text("작용 물체", font_size=18), Text("상쇄 여부", font_size=18)],
            col_labels=[Text("작용 반작용", font_size=18, color=YELLOW), Text("힘의 평형", font_size=18, color=YELLOW)],
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": GRAY},
        ).scale(0.65)
        table.move_to(DOWN * 2.8)

        self.play(Create(table), run_time=1.5)
        self.wait(2.5)

    # =========================================================
    # Outro: 수식 마무리
    # =========================================================
    def outro(self):
        final_eq = MathTex(r"\vec{F}_{AB}", "=", r"-\vec{F}_{BA}", font_size=80, color=WHITE)
        final_eq.move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        subtitle = Text("뉴턴의 운동 제3법칙", font_size=40, color=YELLOW)
        subtitle.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.0)

        # 요약 포인트
        points = VGroup(
            Text("• 두 물체 사이의 힘은 항상 쌍으로 존재", font_size=24, color=WHITE),
            Text("• 크기는 같고 방향은 반대", font_size=24, color=WHITE),
            Text("• 서로 다른 물체에 작용 (상쇄 안 됨)", font_size=24, color=WHITE),
        )
        points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        points.next_to(subtitle, DOWN, buff=0.5)
        self.play(FadeIn(points), run_time=1.0)
        self.wait(3)
