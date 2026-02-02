from manim import VGroup
from manim import *
import numpy as np


class MomentumConservation(Scene):
    def construct(self):
        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{kotex}")

        self.intro()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase1_momentum_concept()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase2_equal_mass_collision()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase3_different_mass_collision()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.phase4_inelastic_collision()
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        self.outro()

    # =========================================================
    # Intro
    # =========================================================
    def intro(self):
        eq = MathTex(r"\vec{p}", "=", "m", r"\vec{v}", font_size=96, color=WHITE)
        eq.move_to(ORIGIN)
        self.play(Write(eq), run_time=2.0)
        self.wait(0.5)

        box = SurroundingRectangle(eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        title = Text("운동량 보존 법칙", font_size=44, color=YELLOW)
        title.next_to(box, DOWN, buff=0.6)
        self.play(Write(title), run_time=1.0)
        self.wait(0.75)

        subtitle = Text("외력이 없으면 총 운동량은 변하지 않는다", font_size=28, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 1: 운동량이란?
    # =========================================================
    def phase1_momentum_concept(self):
        title = Text("운동량이란?", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- 두 개의 트랙 ---
        track_a = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track_a.shift(UP * 1.5)
        track_b = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track_b.shift(DOWN * 0.2)

        # --- 물체 ---
        obj_size = 0.45
        obj_a = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        obj_a.move_to([-5, track_a.get_center()[1] + obj_size / 2 + 0.1, 0])

        obj_b_size = 0.65
        obj_b = Square(side_length=obj_b_size, color=RED, fill_opacity=0.8)
        obj_b.move_to([-5, track_b.get_center()[1] + obj_b_size / 2 + 0.1, 0])
        mass_a = MathTex("1\\,\\text{kg}", font_size=20, color=BLUE).next_to(obj_a, UP, buff=0.1)
        mass_b = MathTex("3\\,\\text{kg}", font_size=20, color=RED).next_to(obj_b, UP, buff=0.1)

        obj_a_label = Text("A", font_size=20, color=WHITE).move_to(obj_a.get_center())
        obj_b_label = Text("B", font_size=20, color=WHITE).move_to(obj_b.get_center())

        self.play(Create(track_a), Create(track_b), run_time=0.75)

        # 속도 화살표 (always_redraw로 물체 추종)
        vel_a = always_redraw(lambda: Arrow(
            start=obj_a.get_right(), end=obj_a.get_right() + RIGHT * 0.9,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3
        ))
        vel_b = always_redraw(lambda: Arrow(
            start=obj_b.get_right(), end=obj_b.get_right() + RIGHT * 0.9,
            color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3
        ))
        vel_a_label = MathTex("v=3", font_size=18, color=BLUE).next_to(vel_a, UP, buff=0.05)
        vel_b_label = MathTex("v=3", font_size=18, color=RED).next_to(vel_b, UP, buff=0.05)

        # updater로 라벨/질량 자동 추종
        obj_a_label.add_updater(lambda m: m.move_to(obj_a))
        obj_b_label.add_updater(lambda m: m.move_to(obj_b))
        mass_a.add_updater(lambda m: m.next_to(obj_a, UP, buff=0.1))
        mass_b.add_updater(lambda m: m.next_to(obj_b, UP, buff=0.1))
        vel_a_label.add_updater(lambda m: m.next_to(vel_a, UP, buff=0.05))
        vel_b_label.add_updater(lambda m: m.next_to(vel_b, UP, buff=0.05))

        self.play(
            FadeIn(obj_a), FadeIn(obj_b),
            Write(obj_a_label), Write(obj_b_label),
            Write(mass_a), Write(mass_b),
            run_time=0.75
        )
        self.play(
            Create(vel_a), Create(vel_b), Write(vel_a_label), Write(vel_b_label),
            run_time=0.75
        )

        same_v_text = Text("두 물체가 3m/s의 동일한 속력으로 움직인다.", font_size=24, color=WHITE)
        same_v_text.move_to(RIGHT * 3 + UP * 0.6)
        self.play(Write(same_v_text), run_time=0.5)
        self.wait(0.5)

        # 이동 애니메이션 (updater가 라벨/화살표 자동 추종)
        self.play(
            obj_a.animate.shift(RIGHT * 5),
            obj_b.animate.shift(RIGHT * 5),
            run_time=3, rate_func=linear
        )
        self.wait(0.5)

        # 운동량 비교
        self.play(FadeOut(same_v_text), run_time=0.3)

        but_text = Text("하지만 운동량은?", font_size=28, color=YELLOW)
        but_text.move_to(RIGHT * 3 + UP * 0.6)
        self.play(Write(but_text), run_time=0.75)

        # updater 해제 후 운동량 화살표로 변환
        vel_a_label.clear_updaters()
        vel_b_label.clear_updaters()
        self.remove(vel_a, vel_b, vel_a_label, vel_b_label)

        p_a = Arrow(
            start=obj_a.get_right(), end=obj_a.get_right() + RIGHT * 0.5,
            color=PURPLE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.3
        )
        p_b = Arrow(
            start=obj_b.get_right(), end=obj_b.get_right() + RIGHT * 1.5,
            color=PURPLE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.3
        )
        p_a_label = MathTex(r"p=3\,\text{kg}\!\cdot\!\text{m/s}", font_size=18, color=PURPLE).next_to(p_a, UP, buff=0.05).shift(RIGHT * 0.45)
        p_b_label = MathTex(r"p=9\,\text{kg}\!\cdot\!\text{m/s}", font_size=18, color=PURPLE).next_to(p_b, UP, buff=0.05)

        self.play(
            FadeIn(p_a), FadeIn(p_b), Write(p_a_label), Write(p_b_label),
            run_time=1.0
        )
        self.wait(0.5)

        # 수식 정리 (좌하단)
        info = VGroup(
            MathTex(r"p_A = 1 \times 3 = 3\,\text{kg}\!\cdot\!\text{m/s}", font_size=24, color=BLUE),
            MathTex(r"p_B = 3 \times 3 = 9\,\text{kg}\!\cdot\!\text{m/s}", font_size=24, color=RED),
        )
        info.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        info.to_corner(DL, buff=2.3)
        self.play(Write(info[0]), run_time=0.75)
        self.play(Write(info[1]), run_time=0.75)

        conclusion = Text("질량이 다르면 운동량도 다르다", font_size=26, color=YELLOW)
        conclusion.next_to(info, DOWN, buff=0.4)
        self.play(Write(conclusion), run_time=0.75)

        p_eq = MathTex(r"p = mv", font_size=56, color=YELLOW)
        p_eq.to_corner(DR, buff=2.3)
        p_box = SurroundingRectangle(p_eq, color=YELLOW, buff=0.2, corner_radius=0.1)
        self.play(Write(p_eq), Create(p_box), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 2: 같은 질량 완전 탄성 충돌
    # =========================================================
    def phase2_equal_mass_collision(self):
        title = VGroup(
            Text("실험 A: 같은 질량 완전 탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m = 1kg, v_A = 4m/s, v_B = 0)", font_size=30, color=WHITE)
        )
        title.arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track ---
        track = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(13):
            val = i - 6
            x_pos = -6 + 12 * (i / 12)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 3 == 0:
                label = Text(str(val), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)
        self.play(Create(track), run_time=0.5)
        self.play(Create(tick_marks), Write(tick_labels), run_time=0.5)

        # --- p-t 그래프 ---
        sim_total = 6.0
        axes_pt = Axes(
            x_range=[0, sim_total, 1], y_range=[-1, 6, 1],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5, 6]},
            y_axis_config={"numbers_to_include": [0, 2, 4]},
        )
        axes_pt.to_corner(DL, buff=0.8)
        x_lab = Text("t (s)", font_size=18).next_to(axes_pt.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex("p", font_size=24).next_to(axes_pt.y_axis, UP, buff=0.15)
        self.play(Create(axes_pt), Write(x_lab), Write(y_lab), run_time=0.75)

        # --- 운동량 막대 ---
        bar_origin = RIGHT * 3.5 + DOWN * 2.5
        bar_scale = 0.5
        bar_width = 0.6
        bar_a = Rectangle(width=bar_width, height=4 * bar_scale, color=BLUE, fill_opacity=0.7)
        bar_b = Rectangle(width=bar_width, height=0.05, color=RED, fill_opacity=0.7)
        bar_tot = Rectangle(width=bar_width, height=4 * bar_scale, color=YELLOW, fill_opacity=0.7)
        bars = VGroup(bar_a, bar_b, bar_tot)
        bars.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        bars.move_to(bar_origin)
        bars.align_to(bar_origin + DOWN * 0.5, DOWN)
        bar_labels_text = VGroup(
            MathTex("p_A", font_size=22, color=BLUE),
            MathTex("p_B", font_size=22, color=RED),
            MathTex("p_{tot}", font_size=22, color=YELLOW),
        )
        for i, lbl in enumerate(bar_labels_text):
            lbl.next_to(bars[i], DOWN, buff=0.15)
        bar_title = Text("운동량", font_size=20, color=WHITE).next_to(bars, UP, buff=0.5)
        bar_val_a = MathTex("4", font_size=18, color=WHITE).next_to(bar_a, UP, buff=0.05)
        bar_val_b = MathTex("0", font_size=18, color=WHITE).next_to(bar_b, UP, buff=0.05)
        bar_val_tot = MathTex("4", font_size=18, color=WHITE).next_to(bar_tot, UP, buff=0.05)
        self.play(
            FadeIn(bars), Write(bar_labels_text), Write(bar_title),
            Write(bar_val_a), Write(bar_val_b), Write(bar_val_tot),
            run_time=0.75
        )

        # --- 물체 ---
        obj_size = 0.45
        center_y = track.get_center()[1]
        box_a = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        box_b = Square(side_length=obj_size, color=RED, fill_opacity=0.8)
        start_a_x, start_b_x = -4.0, 0.0
        box_a.move_to([start_a_x, center_y + obj_size / 2 + 0.1, 0])
        box_b.move_to([start_b_x, center_y + obj_size / 2 + 0.1, 0])

        label_a = Text("A", font_size=16, color=WHITE).move_to(box_a)
        label_b = Text("B", font_size=16, color=WHITE).move_to(box_b)
        mass_a = MathTex("1\\,\\text{kg}", font_size=18, color=BLUE).next_to(box_a, UP, buff=0.1)
        mass_b = MathTex("1\\,\\text{kg}", font_size=18, color=RED).next_to(box_b, UP, buff=0.1)
        vel_arrow = Arrow(
            start=box_a.get_right(), end=box_a.get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        )
        vel_label = MathTex("v=4", font_size=18, color=BLUE).next_to(vel_arrow, UP, buff=0.05)
        self.play(
            FadeIn(box_a), FadeIn(box_b), Write(label_a), Write(label_b),
            Write(mass_a), Write(mass_b), Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # --- 충돌 시뮬레이션 (ValueTracker) ---
        # 물리: m1=m2=1, v_a=4, v_b=0 → 충돌 후 v_a'=0, v_b'=4
        scale_v = 0.5  # 물리 속도 → 화면 속도
        v_a_phys, v_b_phys = 4.0, 0.0
        v_a_after, v_b_after = 0.0, 4.0

        # 충돌 시간: A 오른쪽 가장자리가 B 왼쪽 가장자리에 닿는 시점
        dist = (start_b_x - obj_size / 2) - (start_a_x + obj_size / 2)
        collision_t = dist / (v_a_phys * scale_v)  # 화면 시간

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return start_a_x + v_a_phys * scale_v * t
            return start_a_x + v_a_phys * scale_v * collision_t + v_a_after * scale_v * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return start_b_x
            return start_b_x + v_b_after * scale_v * (t - collision_t)

        y_a = center_y + obj_size / 2 + 0.1
        y_b = center_y + obj_size / 2 + 0.1

        box_a.add_updater(lambda m: m.move_to([pos_a(time_tracker.get_value()), y_a, 0]))
        box_b.add_updater(lambda m: m.move_to([pos_b(time_tracker.get_value()), y_b, 0]))
        label_a.add_updater(lambda m: m.move_to(box_a))
        label_b.add_updater(lambda m: m.move_to(box_b))
        mass_a.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))
        mass_b.add_updater(lambda m: m.next_to(box_b, UP, buff=0.1))

        # 동적 속도 화살표
        vel_arrow_dyn = always_redraw(lambda: Arrow(
            start=box_a.get_right(), end=box_a.get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() < collision_t else VMobject())
        vel_arrow_b_dyn = always_redraw(lambda: Arrow(
            start=box_b.get_right(), end=box_b.get_right() + RIGHT * 0.8,
            color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() > collision_t else VMobject())

        self.remove(vel_arrow)
        self.add(vel_arrow_dyn, vel_arrow_b_dyn)

        # p-t 그래프 (smooth)
        def smooth_step(t, t0, width=0.15):
            return 1 / (1 + np.exp(-(t - t0) / (width / 4)))

        def p_a_func(t):
            s = smooth_step(t, collision_t)
            return 4 * (1 - s)

        def p_b_func(t):
            s = smooth_step(t, collision_t)
            return 4 * s

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 4, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전 이동 (run_time을 시뮬레이션 시간에 비례)
        real_per_sim = 0.8  # 1 sim초 = 0.8 real초
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t), run_time=collision_t * real_per_sim, rate_func=linear)

        # 충돌 Flash + 막대 업데이트 동시
        collision_point = box_a.get_right()
        new_bar_a = Rectangle(width=bar_width, height=0.05, color=BLUE, fill_opacity=0.7)
        new_bar_b = Rectangle(width=bar_width, height=4 * bar_scale, color=RED, fill_opacity=0.7)
        new_bar_a.move_to(bar_a.get_bottom(), aligned_edge=DOWN)
        new_bar_b.move_to(bar_b.get_bottom(), aligned_edge=DOWN)
        new_val_a = MathTex("0", font_size=18, color=WHITE).next_to(new_bar_a, UP, buff=0.05)
        new_val_b = MathTex("4", font_size=18, color=WHITE).next_to(new_bar_b, UP, buff=0.05)
        self.play(
            Flash(collision_point, color=YELLOW, flash_radius=0.5, line_length=0.3),
            Transform(bar_a, new_bar_a), Transform(bar_b, new_bar_b),
            Transform(bar_val_a, new_val_a), Transform(bar_val_b, new_val_b),
            run_time=0.5
        )

        # 충돌 후 이동 (같은 비율)
        self.play(time_tracker.animate.set_value(sim_total), run_time=(sim_total - collision_t) * real_per_sim, rate_func=linear)

        # 정리
        box_a.clear_updaters()
        box_b.clear_updaters()
        label_a.clear_updaters()
        label_b.clear_updaters()
        mass_a.clear_updaters()
        mass_b.clear_updaters()
        self.remove(vel_arrow_dyn, vel_arrow_b_dyn, pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, sim_total], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, sim_total], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 4, x_range=[0, sim_total], color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=14, color=BLUE).next_to(axes_pt.c2p(sim_total, 0), RIGHT, buff=0.15)
        pt_lbl_b = Text("B의 운동량", font_size=14, color=RED).next_to(axes_pt.c2p(sim_total, 4), RIGHT, buff=0.15)
        pt_lbl_tot = Text("총 운동량", font_size=14, color=YELLOW).next_to(axes_pt.c2p(0, 4), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)

        conclusion = MathTex(r"p_1 + p_2 = p_1' + p_2'", font_size=36, color=YELLOW)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(2.0)

    # =========================================================
    # Phase 3: 다른 질량 완전 탄성 충돌
    # =========================================================
    def phase3_different_mass_collision(self):
        title = VGroup(
            Text("실험 B: 다른 질량 탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m_A = 1kg, v_A = 6m/s, m_B = 2kg, v_B = 0)", font_size=30, color=WHITE)
        )
        title.arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track ---
        track = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(13):
            val = i - 6
            x_pos = -6 + 12 * (i / 12)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 3 == 0:
                label = Text(str(val), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)
        self.play(Create(track), Create(tick_marks), Write(tick_labels), run_time=0.75)

        # --- p-t 그래프 ---
        sim_total = 6.0
        axes_pt = Axes(
            x_range=[0, sim_total, 1], y_range=[-4, 10, 2],
            x_length=5, y_length=3.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5, 6]},
            y_axis_config={"numbers_to_include": [-2, 0, 2, 4, 6, 8]},
        )
        axes_pt.to_corner(DL, buff=0.8)
        x_lab = Text("t (s)", font_size=18).next_to(axes_pt.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex("p", font_size=24).next_to(axes_pt.y_axis, UP, buff=0.15)
        self.play(Create(axes_pt), Write(x_lab), Write(y_lab), run_time=0.75)

        info_origin = RIGHT * 1.5 + DOWN * 1.5

        # --- 물체 ---
        obj_a_size = 0.4
        obj_b_size = 0.55
        center_y = track.get_center()[1]
        start_a_x, start_b_x = -4.0, 0.0

        box_a = Square(side_length=obj_a_size, color=BLUE, fill_opacity=0.8)
        box_b = Square(side_length=obj_b_size, color=RED, fill_opacity=0.8)
        box_a.move_to([start_a_x, center_y + obj_a_size / 2 + 0.1, 0])
        box_b.move_to([start_b_x, center_y + obj_b_size / 2 + 0.1, 0])

        label_a = Text("A", font_size=16, color=WHITE).move_to(box_a)
        label_b = Text("B", font_size=16, color=WHITE).move_to(box_b)
        mass_a = MathTex("1\\,\\text{kg}", font_size=18, color=BLUE).next_to(box_a, UP, buff=0.1)
        mass_b = MathTex("2\\,\\text{kg}", font_size=18, color=RED).next_to(box_b, UP, buff=0.1)
        vel_arrow = Arrow(
            start=box_a.get_right(), end=box_a.get_right() + RIGHT * 1.0,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        )
        vel_label = MathTex("v=6", font_size=18, color=BLUE).next_to(vel_arrow, UP, buff=0.05)
        self.play(
            FadeIn(box_a), FadeIn(box_b), Write(label_a), Write(label_b),
            Write(mass_a), Write(mass_b), Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # --- 충돌 시뮬레이션 (ValueTracker) ---
        # v_A' = (1-2)/(1+2)*6 = -2, v_B' = 2*1/(1+2)*6 = 4
        scale_v = 0.35
        v_a_phys, v_b_phys = 6.0, 0.0
        v_a_after, v_b_after = -2.0, 4.0

        dist = (start_b_x - obj_b_size / 2) - (start_a_x + obj_a_size / 2)
        collision_t = dist / (v_a_phys * scale_v)

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return start_a_x + v_a_phys * scale_v * t
            return start_a_x + v_a_phys * scale_v * collision_t + v_a_after * scale_v * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return start_b_x
            return start_b_x + v_b_after * scale_v * (t - collision_t)

        y_a = center_y + obj_a_size / 2 + 0.1
        y_b = center_y + obj_b_size / 2 + 0.1

        box_a.add_updater(lambda m: m.move_to([pos_a(time_tracker.get_value()), y_a, 0]))
        box_b.add_updater(lambda m: m.move_to([pos_b(time_tracker.get_value()), y_b, 0]))
        label_a.add_updater(lambda m: m.move_to(box_a))
        label_b.add_updater(lambda m: m.move_to(box_b))
        mass_a.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))
        mass_b.add_updater(lambda m: m.next_to(box_b, UP, buff=0.1))

        # 동적 속도 화살표
        vel_arrow_a_dyn = always_redraw(lambda: (
            Arrow(
                start=box_a.get_right(), end=box_a.get_right() + RIGHT * 1.0,
                color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
            ) if time_tracker.get_value() < collision_t else (
                Arrow(
                    start=box_a.get_left(), end=box_a.get_left() + LEFT * 0.4,
                    color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
                ) if time_tracker.get_value() > collision_t else VMobject()
            )
        ))
        vel_arrow_b_dyn = always_redraw(lambda: Arrow(
            start=box_b.get_right(), end=box_b.get_right() + RIGHT * 0.7,
            color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() > collision_t else VMobject())

        self.remove(vel_arrow)
        self.add(vel_arrow_a_dyn, vel_arrow_b_dyn)

        # p-t 그래프 (smooth)
        def smooth_step(t, t0, width=0.15):
            return 1 / (1 + np.exp(-(t - t0) / (width / 4)))

        def p_a_func(t):
            s = smooth_step(t, collision_t)
            return 6 * (1 - s) + (-2) * s

        def p_b_func(t):
            s = smooth_step(t, collision_t)
            return 8 * s

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 6, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전 (run_time을 시뮬레이션 시간에 비례)
        real_per_sim = 0.8
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t), run_time=collision_t * real_per_sim, rate_func=linear)

        # 충돌 Flash
        collision_point = box_a.get_right()
        self.play(Flash(collision_point, color=YELLOW, flash_radius=0.5, line_length=0.3, run_time=0.3))

        # 충돌 후 (같은 비율)
        self.play(time_tracker.animate.set_value(sim_total), run_time=(sim_total - collision_t) * real_per_sim, rate_func=linear)

        # 정리
        box_a.clear_updaters()
        box_b.clear_updaters()
        label_a.clear_updaters()
        label_b.clear_updaters()
        mass_a.clear_updaters()
        mass_b.clear_updaters()
        self.remove(vel_arrow_a_dyn, vel_arrow_b_dyn, pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, sim_total], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, sim_total], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 6, x_range=[0, sim_total], color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=14, color=BLUE).next_to(axes_pt.c2p(sim_total, -2), RIGHT, buff=0.15)
        pt_lbl_b = Text("B의 운동량", font_size=14, color=RED).next_to(axes_pt.c2p(sim_total, 8), RIGHT, buff=0.15)
        pt_lbl_tot = Text("총 운동량", font_size=14, color=YELLOW).next_to(axes_pt.c2p(0, 6), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)

        # 수식 검증
        before_collision = VGroup(
            Text("충돌 전 운동량", font_size=22, color=YELLOW),
            MathTex(r"p_A = 1 \times (6) = 6", font_size=22, color=BLUE),
            MathTex(r"p_B = 2 \times 0 = 0", font_size=22, color=RED),
            MathTex(r"p_{tot} = 6 + 0 = 6\;\checkmark", font_size=24, color=YELLOW),
        )
        after_collision = VGroup(
            Text("충돌 후 운동량", font_size=22, color=YELLOW),
            MathTex(r"p_A' = 1 \times (-2) = -2", font_size=22, color=BLUE),
            MathTex(r"p_B' = 2 \times 4 = 8", font_size=22, color=RED),
            MathTex(r"p_{tot}' = -2 + 8 = 6\;\checkmark", font_size=24, color=YELLOW),
        )

        before_collision.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        before_collision.move_to(info_origin)
        for v in before_collision:
            self.play(Write(v), run_time=0.5)

        self.wait(1.0)

        after_collision.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        after_collision.move_to(info_origin + RIGHT * 3)
        for v in after_collision:
            self.play(Write(v), run_time=0.5)



        self.wait(2.0)

    # =========================================================
    # Phase 4: 완전 비탄성 충돌
    # =========================================================
    def phase4_inelastic_collision(self):
        title = VGroup(
            Text("실험 C: 완전 비탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m_A = 1kg, v_A = 4m/s, m_B = 1kg, v_B = 0)", font_size=30, color=WHITE)
        )
        title.arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Track ---
        track = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(13):
            val = i - 6
            x_pos = -6 + 12 * (i / 12)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 3 == 0:
                label = Text(str(val), font_size=16, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)
        self.play(Create(track), Create(tick_marks), Write(tick_labels), run_time=0.75)

        # --- p-t 그래프 ---
        sim_total = 6.0
        axes_pt = Axes(
            x_range=[0, sim_total, 1], y_range=[-1, 6, 1],
            x_length=5, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5, 6]},
            y_axis_config={"numbers_to_include": [0, 2, 4]},
        )
        axes_pt.to_corner(DL, buff=0.8)
        x_lab = Text("t (s)", font_size=18).next_to(axes_pt.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex("p", font_size=24).next_to(axes_pt.y_axis, UP, buff=0.15)
        self.play(Create(axes_pt), Write(x_lab), Write(y_lab), run_time=0.75)

        # --- 운동량 막대 ---
        bar_origin = RIGHT * 3.5 + DOWN * 2.5
        bar_scale = 0.5
        bar_width = 0.6
        bar_a = Rectangle(width=bar_width, height=4 * bar_scale, color=BLUE, fill_opacity=0.7)
        bar_b = Rectangle(width=bar_width, height=0.05, color=RED, fill_opacity=0.7)
        bar_tot = Rectangle(width=bar_width, height=4 * bar_scale, color=YELLOW, fill_opacity=0.7)
        bars = VGroup(bar_a, bar_b, bar_tot)
        bars.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        bars.move_to(bar_origin)
        bars.align_to(bar_origin + DOWN * 0.5, DOWN)
        bar_labels_text = VGroup(
            MathTex("p_A", font_size=22, color=BLUE),
            MathTex("p_B", font_size=22, color=RED),
            MathTex("p_{tot}", font_size=22, color=YELLOW),
        )
        for i, lbl in enumerate(bar_labels_text):
            lbl.next_to(bars[i], DOWN, buff=0.15)
        bar_title = Text("운동량", font_size=20, color=WHITE).next_to(bars, UP, buff=0.5)
        bar_val_a = MathTex("4", font_size=18, color=WHITE).next_to(bar_a, UP, buff=0.05)
        bar_val_b = MathTex("0", font_size=18, color=WHITE).next_to(bar_b, UP, buff=0.05)
        bar_val_tot = MathTex("4", font_size=18, color=WHITE).next_to(bar_tot, UP, buff=0.05)
        self.play(
            FadeIn(bars), Write(bar_labels_text), Write(bar_title),
            Write(bar_val_a), Write(bar_val_b), Write(bar_val_tot),
            run_time=0.75
        )

        # --- 물체 ---
        obj_size = 0.45
        center_y = track.get_center()[1]
        start_a_x, start_b_x = -4.0, 0.0

        box_a = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        box_b = Square(side_length=obj_size, color=RED, fill_opacity=0.8)
        box_a.move_to([start_a_x, center_y + obj_size / 2 + 0.1, 0])
        box_b.move_to([start_b_x, center_y + obj_size / 2 + 0.1, 0])

        label_a = Text("A", font_size=16, color=WHITE).move_to(box_a)
        label_b = Text("B", font_size=16, color=WHITE).move_to(box_b)
        mass_a = MathTex("1\\,\\text{kg}", font_size=18, color=BLUE).next_to(box_a, UP, buff=0.1)
        mass_b = MathTex("1\\,\\text{kg}", font_size=18, color=RED).next_to(box_b, UP, buff=0.1)
        vel_arrow = Arrow(
            start=box_a.get_right(), end=box_a.get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        )
        vel_label = MathTex("v=4", font_size=18, color=BLUE).next_to(vel_arrow, UP, buff=0.05)
        self.play(
            FadeIn(box_a), FadeIn(box_b), Write(label_a), Write(label_b),
            Write(mass_a), Write(mass_b), Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # --- ValueTracker 기반 시뮬레이션 ---
        # 비탄성: v' = (1*4)/(1+1) = 2, 합체 후 둘 다 v=2
        scale_v = 0.5
        v_before = 4.0
        v_after = 2.0

        dist = (start_b_x - obj_size / 2) - (start_a_x + obj_size / 2)
        collision_t = dist / (v_before * scale_v)

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return start_a_x + v_before * scale_v * t
            return start_a_x + v_before * scale_v * collision_t + v_after * scale_v * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return start_b_x
            return start_b_x + v_after * scale_v * (t - collision_t)

        y_pos = center_y + obj_size / 2 + 0.1

        box_a.add_updater(lambda m: m.move_to([pos_a(time_tracker.get_value()), y_pos, 0]))
        box_b.add_updater(lambda m: m.move_to([pos_b(time_tracker.get_value()), y_pos, 0]))
        label_a.add_updater(lambda m: m.move_to(box_a))
        label_b.add_updater(lambda m: m.move_to(box_b))
        mass_a.add_updater(lambda m: m.next_to(box_a, UP, buff=0.1))
        mass_b.add_updater(lambda m: m.next_to(box_b, UP, buff=0.1))

        vel_dyn = always_redraw(lambda: Arrow(
            start=box_a.get_right(), end=box_a.get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() < collision_t else VMobject())

        self.remove(vel_arrow)
        self.add(vel_dyn)

        # p-t 그래프 (smooth) — 비탄성: p_A: 4→2, p_B: 0→2, total=4
        def smooth_step(t, t0, width=0.15):
            return 1 / (1 + np.exp(-(t - t0) / (width / 4)))

        def p_a_func(t):
            s = smooth_step(t, collision_t)
            return 4 * (1 - s) + 2 * s  # 4 → 2

        def p_b_func(t):
            s = smooth_step(t, collision_t)
            return 2 * s  # 0 → 2

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 4, x_range=[0, min(max(time_tracker.get_value(), 0.02), sim_total)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전 이동
        real_per_sim = 0.8
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t), run_time=collision_t * real_per_sim, rate_func=linear)

        # 충돌 Flash + 막대 업데이트 동시
        collision_point = box_a.get_right()
        new_bar_a = Rectangle(width=bar_width, height=2 * bar_scale, color=BLUE, fill_opacity=0.7)
        new_bar_b = Rectangle(width=bar_width, height=2 * bar_scale, color=RED, fill_opacity=0.7)
        new_bar_a.move_to(bar_a.get_bottom(), aligned_edge=DOWN)
        new_bar_b.move_to(bar_b.get_bottom(), aligned_edge=DOWN)
        new_val_a = MathTex("2", font_size=18, color=WHITE).next_to(new_bar_a, UP, buff=0.05)
        new_val_b = MathTex("2", font_size=18, color=WHITE).next_to(new_bar_b, UP, buff=0.05)
        self.play(
            Flash(collision_point, color=YELLOW, flash_radius=0.5, line_length=0.3),
            Transform(bar_a, new_bar_a), Transform(bar_b, new_bar_b),
            Transform(bar_val_a, new_val_a), Transform(bar_val_b, new_val_b),
            run_time=0.5
        )

        # 합체 처리
        box_b.clear_updaters()
        label_b.clear_updaters()
        mass_b.clear_updaters()
        self.remove(vel_dyn)
        self.play(box_b.animate.next_to(box_a, RIGHT, buff=0), run_time=0.3)
        label_b.move_to(box_b)
        self.play(FadeOut(mass_a), FadeOut(mass_b), run_time=0.2)

        merged_label = MathTex("2\\,\\text{kg}", font_size=18, color=PURPLE)
        merged_label.add_updater(lambda m: m.next_to(VGroup(box_a, box_b), UP, buff=0.1))
        self.play(Write(merged_label), run_time=0.3)

        merged_vel = always_redraw(lambda: Arrow(
            start=box_b.get_right(), end=box_b.get_right() + RIGHT * 0.4,
            color=PURPLE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ))
        merged_vel_label = always_redraw(lambda: MathTex(
            "v'=2", font_size=18, color=PURPLE
        ).next_to(merged_vel, UP, buff=0.05))
        self.add(merged_vel, merged_vel_label)

        box_b.add_updater(lambda m: m.next_to(box_a, RIGHT, buff=0))
        label_b.add_updater(lambda m: m.move_to(box_b))

        # 충돌 후
        self.play(time_tracker.animate.set_value(sim_total), run_time=(sim_total - collision_t) * real_per_sim, rate_func=linear)

        # 정리
        box_a.clear_updaters()
        box_b.clear_updaters()
        label_a.clear_updaters()
        label_b.clear_updaters()
        merged_label.clear_updaters()
        self.remove(merged_vel, merged_vel_label, vel_dyn, pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, sim_total], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, sim_total], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 4, x_range=[0, sim_total], color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=14, color=BLUE).next_to(axes_pt.c2p(sim_total, 2), RIGHT, buff=0.15).shift(UP * 0.15)
        pt_lbl_b = Text("B의 운동량", font_size=14, color=RED).next_to(axes_pt.c2p(sim_total, 2), RIGHT, buff=0.15).shift(DOWN * 0.15)
        pt_lbl_tot = Text("총 운동량", font_size=14, color=YELLOW).next_to(axes_pt.c2p(0, 4), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)

        conclusion = VGroup(
            MathTex(r"p_{tot} = 4", font_size=36, color=YELLOW),
            Text("(보존)", font_size=24, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(1.5)

        # --- 그래프 후 에너지 비교 ---
        self.play(
            *[FadeOut(m) for m in [
                final_pt_a, final_pt_b, final_pt_tot,
                pt_lbl_a, pt_lbl_b, pt_lbl_tot,
                axes_pt, x_lab, y_lab, conclusion,
                bars, bar_labels_text, bar_title,
                bar_val_a, bar_val_b, bar_val_tot,
                bar_a, bar_b, bar_tot,
            ]],
            run_time=0.5
        )

        # --- 운동량 보존 수식 (상단) ---
        p_section_title = Text("운동량 (보존)", font_size=22, color=GREEN)
        p_section_title.move_to(LEFT * 5 + DOWN * 0.5)

        p_before = VGroup(
            Text("충돌 전", font_size=18, color=YELLOW),
            MathTex(r"p_A = 1 \times 4 = 4", font_size=20, color=BLUE),
            MathTex(r"p_B = 1 \times 0 = 0", font_size=20, color=RED),
            MathTex(r"p_{tot} = 4", font_size=22, color=GREEN),
        )
        p_before.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        p_before.next_to(p_section_title, DOWN, buff=0.25).align_to(p_section_title, LEFT)

        p_arrow = MathTex(r"\Rightarrow", font_size=36, color=WHITE)
        p_arrow.next_to(p_before, RIGHT, buff=0.4)

        p_after = VGroup(
            Text("충돌 후", font_size=18, color=YELLOW),
            MathTex(r"p_{AB}' = 2 \times 2 = 4", font_size=20, color=PURPLE),
            MathTex(r"p_{tot}' = 4\;\checkmark", font_size=22, color=GREEN),
        )
        p_after.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        p_after.next_to(p_arrow, RIGHT, buff=0.4).align_to(p_before, UP)

        self.play(Write(p_section_title), run_time=0.3)
        for v in p_before:
            self.play(Write(v), run_time=0.4)
        self.play(Write(p_arrow), run_time=0.3)
        for v in p_after:
            self.play(Write(v), run_time=0.4)

        self.wait(0.5)

        # --- 운동에너지 비보존 수식 (우측) ---
        e_section_title = Text("운동에너지 (비보존)", font_size=22, color="#9ACD32")
        e_section_title.move_to(RIGHT * 1.5 + DOWN * 0.5)

        e_before = VGroup(
            Text("충돌 전", font_size=18, color=YELLOW),
            MathTex(r"KE_A = \tfrac{1}{2}(1)(4^2) = 8\,\text{J}", font_size=20, color=BLUE),
            MathTex(r"KE_B = 0\,\text{J}", font_size=20, color=RED),
            MathTex(r"KE_{tot} = 8\,\text{J}", font_size=22, color="#9ACD32"),
        )
        e_before.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        e_before.next_to(e_section_title, DOWN, buff=0.25).align_to(e_section_title, LEFT)

        e_arrow = MathTex(r"\Rightarrow", font_size=36, color=WHITE)
        e_arrow.next_to(e_before, RIGHT, buff=0.3)

        e_after = VGroup(
            Text("충돌 후", font_size=18, color=YELLOW),
            MathTex(r"KE_{AB}' = \tfrac{1}{2}(2)(2^2) = 4\,\text{J}", font_size=20, color=PURPLE),
            MathTex(r"KE_{tot}' = 4\,\text{J}\;\;(\downarrow 50\%)", font_size=22, color=RED),
        )
        e_after.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        e_after.next_to(e_arrow, RIGHT, buff=0.3).align_to(e_before, UP)

        self.play(Write(e_section_title), run_time=0.3)
        for v in e_before:
            self.play(Write(v), run_time=0.4)
        self.play(Write(e_arrow), run_time=0.3)
        for v in e_after:
            self.play(Write(v), run_time=0.4)

        key_msg = Text("운동량은 항상 보존, 운동에너지는 충돌 종류에 따라 다르다!", font_size=22, color=YELLOW)
        key_msg.to_edge(DOWN, buff=0.2)
        self.play(Write(key_msg), run_time=1.0)
        self.wait(2.0)

    # =========================================================
    # Outro
    # =========================================================
    def outro(self):
        final_eq = MathTex(
            "m_1", "v_1", "+", "m_2", "v_2", "=",
            "m_1", "v_1'", "+", "m_2", "v_2'",
            font_size=64, color=WHITE
        )
        final_eq.move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        subtitle = Text("운동량 보존 법칙", font_size=40, color=YELLOW)
        subtitle.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.0)

        points = VGroup(
            Text("• 운동량 = 질량 × 속도 (벡터량)", font_size=24, color=WHITE),
            Text("• 외력이 없으면 총 운동량 보존", font_size=24, color=WHITE),
            Text("• 충돌 종류와 무관하게 항상 성립", font_size=24, color=WHITE),
        )
        points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        points.next_to(subtitle, DOWN, buff=0.5)
        self.play(FadeIn(points), run_time=1.0)
        self.wait(3)
