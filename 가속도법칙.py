from manim import FadeOut
from manim import *
import numpy as np


class NewtonsSecondLaw(Scene):
    def construct(self):
        self.intro()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase1_varying_force()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase2_varying_mass()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase3_formula_derivation()

    # =========================================================
    # Intro
    # =========================================================
    def intro(self):
        # F = ma 수식 등장 (중앙, 크게)
        eq = MathTex("F", "=", "m", "a", font_size=96, color=WHITE)
        eq.move_to(ORIGIN)
        self.play(Write(eq), run_time=2.0)
        self.wait(0.5)

        box = SurroundingRectangle(eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        # 제목
        title = Text("뉴턴의 운동 제2법칙", font_size=44, color=YELLOW)
        title.next_to(box, DOWN, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.75)

        # 질문으로 전환
        question = Text("이 공식은 어디서 온 걸까요?", font_size=30, color=WHITE)
        question.next_to(title, DOWN, buff=0.5)
        self.play(Write(question), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 1: 실험 A — 힘 변화 (질량 일정)
    # =========================================================
    def phase1_varying_force(self):
        # --- Title ---
        title = Text("실험 A: 힘의 크기를 바꾸면? (질량 일정)", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track (0~24 m) ---
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(25):
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 24)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 6 == 0:
                label = Text(str(i), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        pos_label = Text("(m)", font_size=20, color=WHITE)
        pos_label.next_to(track, RIGHT, buff=0.3)

        self.play(Create(track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), Write(pos_label), run_time=1.0)
        self.wait(0.3)

        # --- v-t graph (lower left) ---
        axes_vt = Axes(
            x_range=[0, 4, 1], y_range=[0, 12, 3],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [3, 6, 9, 12]},
        )
        axes_vt.to_corner(DL, buff=0.8)
        x_lab_vt = Text("t (s)", font_size=20).next_to(axes_vt.x_axis, RIGHT, buff=0.2)
        y_lab_vt = Text("v (m/s)", font_size=20).next_to(axes_vt.y_axis, UP, buff=0.2)
        self.play(Create(axes_vt), Write(x_lab_vt), Write(y_lab_vt), run_time=1.0)

        # --- a-F result graph (lower right) ---
        axes_af = Axes(
            x_range=[0, 4, 1], y_range=[0, 4, 1],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3]},
            y_axis_config={"numbers_to_include": [1, 2, 3]},
        )
        axes_af.to_corner(DR, buff=0.8)
        x_lab_af = Text("F (N)", font_size=20).next_to(axes_af.x_axis, RIGHT, buff=0.2)
        y_lab_af = Text("a (m/s²)", font_size=20).next_to(axes_af.y_axis, UP, buff=0.2)
        self.play(Create(axes_af), Write(x_lab_af), Write(y_lab_af), run_time=1.0)
        self.wait(0.3)

        # --- Trials ---
        trials = [
            {"F": 1, "a": 1, "color": BLUE,   "label": "F"},
            {"F": 2, "a": 2, "color": GREEN,  "label": "2F"},
            {"F": 3, "a": 3, "color": ORANGE, "label": "3F"},
        ]

        total_time = 4
        total_dist = 24  # max distance on track
        obj_size = 0.4
        prev_trial_mobs = VGroup()  # ghosts of previous trials
        vt_lines = VGroup()
        result_dots = VGroup()

        for trial in trials:
            F_val = trial["F"]
            accel = trial["a"]
            color = trial["color"]

            # 박스
            obj = Square(side_length=obj_size, color=color, fill_opacity=0.8)
            obj.move_to([track_start[0], track.get_center()[1] + obj_size / 2 + 0.1, 0])

            # 힘 화살표
            force_arrow = always_redraw(lambda f=F_val: Arrow(
                start=obj.get_right(),
                end=obj.get_right() + RIGHT * 0.4 * f,
                color=RED, buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            ))
            force_label = always_redraw(lambda lbl=trial["label"]: MathTex(
                f"{lbl}", font_size=22, color=RED
            ).next_to(force_arrow, UP, buff=0.05))

            mass_label = always_redraw(lambda: MathTex(
                "m", font_size=20, color=color
            ).next_to(obj, UP, buff=0.15))

            ghost_group = VGroup()

            self.play(FadeIn(obj), FadeIn(force_arrow), FadeIn(force_label), FadeIn(mass_label), run_time=0.5)
            self.add(ghost_group)

            # 이동 애니메이션
            time_tracker = ValueTracker(0)
            time_tracker.last_int_t = 0

            def make_updater(a_val, g_group, t_tracker):
                def update_obj(m):
                    t = t_tracker.get_value()
                    s = 0.5 * a_val * t ** 2
                    x_ratio = min(s / total_dist, 1.0)
                    new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
                    m.move_to([new_x, track.get_center()[1] + obj_size / 2 + 0.1, 0])
                    current_int_t = int(t)
                    if current_int_t > t_tracker.last_int_t:
                        ghost = Square(side_length=obj_size, color=m.get_color(), fill_opacity=0.3, stroke_width=0)
                        ghost.move_to(m.get_center())
                        g_group.add(ghost)
                        t_tracker.last_int_t = current_int_t
                return update_obj

            obj.add_updater(make_updater(accel, ghost_group, time_tracker))
            self.play(time_tracker.animate.set_value(total_time), run_time=5, rate_func=linear)
            obj.remove_updater(obj.updaters[-1])

            # v-t 직선 그리기
            vt_line = axes_vt.plot(lambda t, a=accel: a * t, x_range=[0, 4], color=color, stroke_width=3)
            vt_label = MathTex(f"a={accel}", font_size=20, color=color).next_to(
                axes_vt.c2p(4, accel * 4), RIGHT, buff=0.1
            )
            self.play(Create(vt_line), Write(vt_label), run_time=1.0)
            vt_lines.add(vt_line, vt_label)

            # a-F 결과 점
            dot = Dot(axes_af.c2p(F_val, accel), color=RED, radius=0.1)
            dot_label = MathTex(f"({F_val},{accel})", font_size=18, color=WHITE).next_to(dot, UR, buff=0.1)
            self.play(FadeIn(dot), Write(dot_label), run_time=0.5)
            result_dots.add(dot, dot_label)

            # 이전 시행 고스트화
            self.play(FadeOut(force_arrow, force_label, mass_label))
            trial_mobs = VGroup(obj, ghost_group)
            self.play(trial_mobs.animate.set_opacity(0.15), run_time=0.5)
            prev_trial_mobs.add(trial_mobs)

            self.wait(0.3)

        # 결과 직선
        result_line = axes_af.plot(lambda F: F, x_range=[0, 3.5], color=RED, stroke_width=3)
        self.play(Create(result_line), run_time=1.0)

        # 결론
        conclusion = MathTex("a \\propto F", font_size=44, color=YELLOW)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 2: 실험 B — 질량 변화 (힘 일정)
    # =========================================================
    def phase2_varying_mass(self):
        # --- Title ---
        title = Text("실험 B: 질량을 바꾸면? (힘 일정)", font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track (0~8 m) ---
        track_start = LEFT * 6
        track_end = RIGHT * 6
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(9):
            x_pos = track_start[0] + (track_end[0] - track_start[0]) * (i / 8)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 2 == 0:
                label = Text(str(i), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)

        pos_label = Text("(m)", font_size=20, color=WHITE)
        pos_label.next_to(track, RIGHT, buff=0.3)

        self.play(Create(track), run_time=0.75)
        self.play(Create(tick_marks), Write(tick_labels), Write(pos_label), run_time=1.0)
        self.wait(0.3)

        # --- v-t graph ---
        axes_vt = Axes(
            x_range=[0, 4, 1], y_range=[0, 5, 1],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [1, 2, 3, 4]},
        )
        axes_vt.to_corner(DL, buff=0.8)
        x_lab_vt = Text("t (s)", font_size=20).next_to(axes_vt.x_axis, RIGHT, buff=0.2)
        y_lab_vt = Text("v (m/s)", font_size=20).next_to(axes_vt.y_axis, UP, buff=0.2)
        self.play(Create(axes_vt), Write(x_lab_vt), Write(y_lab_vt), run_time=1.0)

        # --- a-m result graph ---
        axes_am = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.5, 0.5],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3]},
            y_axis_config={"numbers_to_include": [0.5, 1.0]},
        )
        axes_am.to_corner(DR, buff=0.8)
        x_lab_am = Text("m (kg)", font_size=20).next_to(axes_am.x_axis, RIGHT, buff=0.2)
        y_lab_am = Text("a (m/s²)", font_size=20).next_to(axes_am.y_axis, UP, buff=0.2)
        self.play(Create(axes_am), Write(x_lab_am), Write(y_lab_am), run_time=1.0)
        self.wait(0.3)

        # --- Trials ---
        trials = [
            {"m": 1, "a": 1,     "color": BLUE,   "label": "m"},
            {"m": 2, "a": 0.5,   "color": GREEN,  "label": "2m"},
            {"m": 3, "a": 1/3,   "color": ORANGE, "label": "3m"},
        ]

        total_time = 4
        total_dist = 8
        obj_size = 0.4
        prev_trial_mobs = VGroup()
        vt_lines = VGroup()
        result_dots = VGroup()

        for trial in trials:
            m_val = trial["m"]
            accel = trial["a"]
            color = trial["color"]

            # 박스 쌓기
            boxes = VGroup(*[
                Square(side_length=obj_size, color=color, fill_opacity=0.8)
                for _ in range(m_val)
            ])
            boxes.arrange(UP, buff=0)
            boxes.move_to([
                track_start[0],
                track.get_center()[1] + boxes.get_height() / 2 + 0.1,
                0
            ])

            # 힘 화살표 (길이 고정, F=1N)
            force_arrow = always_redraw(lambda: Arrow(
                start=boxes.get_right(),
                end=boxes.get_right() + RIGHT * 0.4,
                color=RED, buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            ))
            force_label = always_redraw(lambda: MathTex(
                "F", font_size=22, color=RED
            ).next_to(force_arrow, UP, buff=0.05))

            mass_label = always_redraw(lambda lbl=trial["label"]: MathTex(
                f"{lbl}", font_size=20, color=color
            ).next_to(boxes, LEFT, buff=0.15))

            ghost_group = VGroup()

            self.play(FadeIn(boxes), FadeIn(force_arrow), FadeIn(force_label), FadeIn(mass_label), run_time=0.5)
            self.add(ghost_group)

            # 이동 애니메이션
            time_tracker = ValueTracker(0)
            time_tracker.last_int_t = 0
            box_h = boxes.get_height()

            def make_updater(a_val, g_group, t_tracker, bxs, bh, clr):
                def update_boxes(m):
                    t = t_tracker.get_value()
                    s = 0.5 * a_val * t ** 2
                    x_ratio = min(s / total_dist, 1.0)
                    new_x = track_start[0] + (track_end[0] - track_start[0]) * x_ratio
                    m.move_to([new_x, track.get_center()[1] + bh / 2 + 0.1, 0])
                    current_int_t = int(t)
                    if current_int_t > t_tracker.last_int_t:
                        ghost = VGroup(*[
                            Square(side_length=obj_size, color=clr, fill_opacity=0.3, stroke_width=0)
                            for _ in range(len(bxs))
                        ])
                        ghost.arrange(UP, buff=0)
                        ghost.move_to(m.get_center())
                        g_group.add(ghost)
                        t_tracker.last_int_t = current_int_t
                return update_boxes

            boxes.add_updater(make_updater(accel, ghost_group, time_tracker, boxes, box_h, color))
            self.play(time_tracker.animate.set_value(total_time), run_time=5, rate_func=linear)
            boxes.remove_updater(boxes.updaters[-1])

            # v-t 직선
            vt_line = axes_vt.plot(lambda t, a=accel: a * t, x_range=[0, 4], color=color, stroke_width=3)
            a_str = f"{accel:.2f}" if accel < 1 else f"{accel}"
            vt_label = MathTex(f"a={a_str}", font_size=20, color=color).next_to(
                axes_vt.c2p(4, accel * 4), RIGHT, buff=0.1
            )
            self.play(Create(vt_line), Write(vt_label), run_time=1.0)
            vt_lines.add(vt_line, vt_label)

            # a-m 결과 점
            dot = Dot(axes_am.c2p(m_val, accel), color=RED, radius=0.1)
            a_display = f"{accel:.1f}" if accel != 1/3 else "0.33"
            dot_label = MathTex(f"({m_val},{a_display})", font_size=18, color=WHITE).next_to(dot, UR, buff=0.1)
            self.play(FadeIn(dot), Write(dot_label), run_time=0.5)
            result_dots.add(dot, dot_label)

            # 이전 시행 고스트화
            self.play(FadeOut(force_arrow, force_label, mass_label))
            trial_mobs = VGroup(boxes, ghost_group)
            self.play(trial_mobs.animate.set_opacity(0.15), run_time=0.5)
            prev_trial_mobs.add(trial_mobs)

            self.wait(0.3)

        # 결과 반비례 곡선
        result_curve = axes_am.plot(lambda m: 1 / m, x_range=[0.5, 3.5], color=RED, stroke_width=3)
        self.play(Create(result_curve), run_time=1.0)

        # 결론
        conclusion = MathTex("a \\propto \\frac{1}{m}", font_size=44, color=YELLOW)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 3: 공식 유도 및 검증
    # =========================================================
    def phase3_formula_derivation(self):
        # --- 3a. 수식 유도 ---
        title = Text("공식의 완성", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        eq1 = MathTex("a", "\\propto", "F", font_size=48, color=WHITE)
        eq2 = MathTex("a", "\\propto", "\\frac{1}{m}", font_size=48, color=WHITE)
        eq1.move_to(UP * 1)
        eq2.next_to(eq1, DOWN, buff=0.6)

        self.play(Write(eq1), run_time=1.0)
        self.wait(0.5)
        self.play(Write(eq2), run_time=1.0)
        self.wait(0.75)

        # 합치기 → F = kma
        eq_combined = MathTex("a", "=", "k", "\\frac{F}{m}", font_size=52, color=WHITE)
        eq_combined.move_to(ORIGIN)
        self.play(
            TransformMatchingTex(VGroup(eq1, eq2), eq_combined),
            run_time=1.5
        )
        self.wait(0.5)

        eq_kma = MathTex("F", "=", "k", "m", "a", font_size=56, color=WHITE)
        eq_kma.move_to(ORIGIN)
        self.play(TransformMatchingTex(eq_combined, eq_kma), run_time=1.5)
        self.wait(0.75)

        # --- 3b. 의문 제기: k는 뭐지? ---
        question = Text("잠깐, 이 상수 k는 뭘까?", font_size=30, color=YELLOW)
        question.next_to(eq_kma, DOWN, buff=0.8)
        self.play(Write(question), run_time=1.0)
        self.wait(1.0)

        # k 강조
        k_highlight = SurroundingRectangle(eq_kma[2], color=RED, buff=0.1)
        self.play(Create(k_highlight), run_time=0.5)
        self.wait(0.75)

        # 위로 올리고 정리
        self.play(
            FadeOut(title), FadeOut(question), FadeOut(k_highlight),
            eq_kma.animate.scale(0.7).to_edge(UP).shift(DOWN * 0.3),
            run_time=1.0
        )

        # --- 1kg 박스를 1m/s²로 미는 시뮬레이션 ---
        demo_title = Text("1 kg 물체를 1 m/s² 으로 가속시키려면?", font_size=26, color=WHITE)
        demo_title.next_to(eq_kma, DOWN, buff=0.4)
        self.play(Write(demo_title), run_time=0.75)

        # 간단한 트랙
        track_start = LEFT * 5
        track_end = RIGHT * 5
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.move_to(ORIGIN + UP * 0.2)
        self.play(Create(track), run_time=0.5)

        # 1kg 박스
        obj_size = 0.5
        obj = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        obj.move_to([track_start[0] + 0.5, track.get_center()[1] + obj_size / 2 + 0.1, 0])

        mass_lbl = MathTex("1\\,\\text{kg}", font_size=24, color=WHITE).move_to(obj.get_center())

        force_arrow = always_redraw(lambda: Arrow(
            start=obj.get_right(),
            end=obj.get_right() + RIGHT * 0.6,
            color=RED, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
        ))
        force_q = always_redraw(lambda: MathTex(
            "?\\,\\text{N}", font_size=22, color=RED
        ).next_to(force_arrow, UP, buff=0.05))

        accel_lbl = always_redraw(lambda: MathTex(
            "a = 1\\,\\text{m/s}^2", font_size=20, color=YELLOW
        ).next_to(obj, DOWN, buff=0.3))

        self.play(FadeIn(obj), Write(mass_lbl), run_time=0.5)
        self.play(FadeIn(force_arrow), Write(force_q), Write(accel_lbl), run_time=0.75)

        # 박스 이동 애니메이션
        total_dist = 8
        time_tracker = ValueTracker(0)

        def upd_obj(m):
            t = time_tracker.get_value()
            s = 0.5 * 1 * t ** 2
            x_ratio = min(s / total_dist, 1.0)
            new_x = track_start[0] + 0.5 + (track_end[0] - track_start[0] - 1.0) * x_ratio
            m.move_to([new_x, track.get_center()[1] + obj_size / 2 + 0.1, 0])

        obj.add_updater(upd_obj)
        mass_lbl.add_updater(lambda m: m.move_to(obj.get_center()))
        self.play(time_tracker.animate.set_value(3), run_time=4, rate_func=linear)
        obj.remove_updater(upd_obj)
        mass_lbl.remove_updater(mass_lbl.updaters[-1])
        self.wait(0.5)

        # 정지 후 정의 설명
        self.play(FadeOut(force_q), run_time=0.3)
        force_def = always_redraw(lambda: MathTex(
            "1\\,\\text{N}", font_size=24, color=RED
        ).next_to(force_arrow, UP, buff=0.05))
        self.play(FadeIn(force_def), run_time=0.5)

        # 뉴턴 정의 텍스트
        def_text1 = Text(
            "이 힘의 크기를 1 뉴턴(N)이라고 정의합니다",
            font_size=24, color=YELLOW
        )
        def_text1.next_to(track, DOWN, buff=0.8)
        self.play(Write(def_text1), run_time=1.0)
        self.wait(1.0)

        def_text2 = Text(
            "이 약속 덕분에 상수 k = 1 이 됩니다!",
            font_size=24, color=YELLOW
        )
        def_text2.next_to(def_text1, DOWN, buff=0.3)
        self.play(Write(def_text2), run_time=1.0)
        self.wait(1.0)

        # k=1 대입 수식 변환
        eq_k1 = MathTex("F", "=", "1", "\\cdot", "m", "a", font_size=48, color=WHITE)
        eq_k1.move_to(UP * 3)
        self.play(TransformMatchingTex(eq_kma, eq_k1), run_time=1.0)
        self.wait(0.5)

        eq_final = MathTex("F", "=", "m", "a", font_size=56, color=YELLOW)
        eq_final.move_to(UP * 3)
        self.play(TransformMatchingTex(eq_k1, eq_final), run_time=1.0)

        final_box = SurroundingRectangle(eq_final, color=YELLOW, buff=0.2, corner_radius=0.1)
        self.play(Create(final_box), run_time=0.5)
        self.wait(1.5)

        # --- 3c. 마무리 ---
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        final_eq = MathTex("F", "=", "m", "a", font_size=80, color=WHITE)
        final_eq.move_to(ORIGIN)
        final_box2 = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        subtitle = Text("뉴턴의 운동 제2법칙", font_size=40, color=YELLOW)
        subtitle.next_to(final_box2, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box2), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(3)
