from manim import *
import numpy as np


class WorkAndKineticEnergy(Scene):
    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_work_definition()
        self.clear_screen()
        self.phase2_work_simulation()
        self.clear_screen()
        self.phase3_kinetic_energy()
        self.clear_screen()
        self.phase4_work_energy_theorem()
        self.clear_screen()
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # =========================================================
    # Intro
    # =========================================================
    def intro(self):
        title = Text("일과 운동에너지", font_size=80, color=WHITE)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=1.0)
        box = SurroundingRectangle(title, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        subtitle = Text("힘이 물체에 한 일은 어디로 갈까?", font_size=28, color=WHITE)
        subtitle.next_to(box, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 1: 일의 정의
    # =========================================================
    def phase1_work_definition(self):
        title = Text("일의 정의", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: W = F·d
        eq1 = MathTex("W", "=", r"\vec{F}", r"\cdot", r"\vec{d}", font_size=80)
        self.play(Write(eq1))
        self.wait(1)

        # Step 2: W = Fd cosθ
        eq2 = MathTex("W", "=", "F", "d", r"\cos\theta", font_size=80)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1.5)

        # 위로 이동
        self.play(eq2.animate.scale(0.6).to_edge(UP).shift(DOWN * 0.8))
        self.wait(0.5)

        # 세 가지 경우 시각화
        cases = [
            (r"\theta = 0°", "양의 일 (W > 0)", 0, YELLOW),
            (r"\theta = 90°", "일 = 0 (W = 0)", PI / 2, GRAY),
            (r"\theta = 180°", "음의 일 (W < 0)", PI, RED),
        ]

        case_groups = VGroup()
        for i, (angle_tex, desc, angle_val, color) in enumerate(cases):
            x_offset = (i - 1) * 4.2
            center = np.array([x_offset, -0.5, 0])

            # 물체
            obj = Square(side_length=0.4, color=BLUE, fill_opacity=0.8).move_to(center)

            # 변위 화살표 (항상 오른쪽)
            d_arrow = Arrow(
                center, center + RIGHT * 1.5,
                color=GREEN, buff=0, stroke_width=4,
            )
            d_label = MathTex(r"\vec{d}", font_size=22, color=GREEN).next_to(d_arrow, DOWN, buff=0.1)

            # 힘 화살표 (각도에 따라)
            f_dir = np.array([np.cos(angle_val), np.sin(angle_val), 0])
            f_arrow = Arrow(
                center, center + f_dir * 1.5,
                color=RED, buff=0, stroke_width=4,
            )
            f_label = MathTex(r"\vec{F}", font_size=22, color=RED).next_to(f_arrow.get_end(), UP, buff=0.1)

            # 각도 표시
            angle_label = MathTex(angle_tex, font_size=24, color=color)
            angle_label.next_to(obj, UP, buff=0.8)

            # 설명
            desc_text = Text(desc, font_size=18, color=color)
            desc_text.next_to(obj, DOWN, buff=1.0)

            group = VGroup(obj, d_arrow, d_label, f_arrow, f_label, angle_label, desc_text)
            case_groups.add(group)

        for g in case_groups:
            self.play(FadeIn(g), run_time=1.0)
            self.wait(0.8)

        self.wait(1.5)

    # =========================================================
    # Phase 2: 일 시뮬레이션 (수평면 밀기)
    # =========================================================
    def phase2_work_simulation(self):
        # 물리 파라미터
        mass = 2       # kg
        F_val = 4      # N
        a_val = F_val / mass  # 2 m/s^2
        d_total = 5    # m (이동 거리)
        t_total = np.sqrt(2 * d_total / a_val)  # sqrt(5) ≈ 2.24 s
        v_final = a_val * t_total  # ≈ 4.47 m/s
        obj_size = 0.4

        # 타이틀
        title = VGroup(
            Text("수평면 위 물체 밀기:", font_size=24, color=WHITE),
            MathTex(r"m=2\text{kg},\;F=4\text{N}", font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        self.play(Write(title))

        # 트랙 (상단)
        track_start = LEFT * 5.5
        track_end = RIGHT * 5.5
        track = Line(track_start, track_end, color=WHITE, stroke_width=3)
        track.shift(UP * 1.5)

        # 눈금
        tick_marks = VGroup()
        tick_labels = VGroup()
        track_len = track_end[0] - track_start[0]  # 11
        total_m = 6  # 트랙이 나타내는 총 미터
        def m2x(m):
            return track_start[0] + track_len * (m / total_m)

        for i in range(7):
            x_pos = m2x(i)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            label = Text(str(i), font_size=16, color=GRAY)
            label.next_to(tick, DOWN, buff=0.15)
            tick_labels.add(label)

        # 물체
        obj = Square(side_length=obj_size, color=BLUE, fill_opacity=0.8)
        obj_y = track.get_center()[1] + obj_size / 2 + 0.1
        obj.move_to([m2x(0), obj_y, 0])
        obj_label = Text("2kg", font_size=18, color=WHITE).move_to(obj)

        # F-x 그래프 (하단 좌)
        fx_axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 6, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config={"numbers_to_include": [4]},
        ).to_corner(DL, buff=0.8)
        fx_x_label = Text("x (m)", font_size=20).next_to(fx_axes.x_axis, RIGHT, buff=0.2)
        fx_y_label = Text("F (N)", font_size=20).next_to(fx_axes.y_axis, UP, buff=0.2)

        # v-t 그래프 (하단 우)
        vt_axes = Axes(
            x_range=[0, 3, 0.5], y_range=[0, 6, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2]},
            y_axis_config={"numbers_to_include": [2, 4]},
        ).to_corner(DR, buff=0.8)
        vt_x_label = Text("t (s)", font_size=20).next_to(vt_axes.x_axis, RIGHT, buff=0.2)
        vt_y_label = Text("v (m/s)", font_size=20).next_to(vt_axes.y_axis, UP, buff=0.2)

        # 레이아웃 등장
        self.play(
            Create(track), FadeIn(tick_marks), FadeIn(tick_labels),
            FadeIn(obj), FadeIn(obj_label),
            Create(fx_axes), Write(fx_x_label), Write(fx_y_label),
            Create(vt_axes), Write(vt_x_label), Write(vt_y_label),
        )
        self.wait(0.5)

        # 힘 화살표
        f_arrow = Arrow(
            obj.get_right(), obj.get_right() + RIGHT * 1.0,
            color=RED, buff=0, stroke_width=5,
        )
        f_label_mob = MathTex(r"F=4\text{N}", font_size=22, color=RED).next_to(f_arrow, UP, buff=0.1)
        self.play(GrowArrow(f_arrow), FadeIn(f_label_mob))

        # ValueTracker 기반 시뮬레이션
        time_tracker = ValueTracker(0)

        def pos_m(t):
            return 0.5 * a_val * t**2

        def vel(t):
            return a_val * t

        obj.add_updater(lambda m: m.move_to([m2x(min(pos_m(time_tracker.get_value()), d_total)), obj_y, 0]))
        obj_label.add_updater(lambda m: m.move_to(obj))
        f_arrow.add_updater(lambda m: m.put_start_and_end_on(
            obj.get_right(), obj.get_right() + RIGHT * 1.0
        ))
        f_label_mob.add_updater(lambda m: m.next_to(f_arrow, UP, buff=0.1))

        # 동적 그래프
        fx_line = always_redraw(lambda: fx_axes.plot(
            lambda x: F_val, x_range=[0, max(min(pos_m(time_tracker.get_value()), d_total), 0.02)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        vt_line = always_redraw(lambda: vt_axes.plot(
            lambda t: vel(t), x_range=[0, max(min(time_tracker.get_value(), t_total), 0.02)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())

        self.add(fx_line, vt_line)

        # 애니메이션
        self.play(
            time_tracker.animate.set_value(t_total),
            run_time=4, rate_func=linear,
        )

        # clear updaters
        obj.clear_updaters()
        obj_label.clear_updaters()
        f_arrow.clear_updaters()
        f_label_mob.clear_updaters()
        self.remove(fx_line, vt_line)

        # 정적 그래프
        static_fx = fx_axes.plot(lambda x: F_val, x_range=[0, d_total], color=RED, stroke_width=3)
        static_vt = vt_axes.plot(lambda t: vel(t), x_range=[0, t_total], color=BLUE, stroke_width=3)
        self.add(static_fx, static_vt)
        self.wait(0.5)

        # F-x 면적 색칠
        area_fx = Polygon(
            fx_axes.c2p(0, 0), fx_axes.c2p(0, F_val),
            fx_axes.c2p(d_total, F_val), fx_axes.c2p(d_total, 0),
            color=YELLOW, fill_opacity=0.4, stroke_width=1,
        )
        self.play(FadeIn(area_fx))
        self.wait(0.5)

        # W = Fd 계산
        w_text = MathTex(
            r"W = Fd = 4 \times 5 = 20\,\text{J}",
            font_size=28, color=YELLOW,
        ).next_to(fx_axes, DOWN, buff=0.3)
        self.play(Write(w_text))
        self.wait(1.5)

        # 그래프 연결 설명
        connection = VGroup(
            Text("F-x 면적", font_size=20, color=WHITE),
            MathTex(r"= W = \Delta KE", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.15).next_to(vt_axes, DOWN, buff=0.3)
        self.play(Write(connection))
        self.wait(2)

    # =========================================================
    # Phase 3: 운동에너지
    # =========================================================
    def phase3_kinetic_energy(self):
        title = Text("운동에너지", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 수식
        ke_eq = MathTex(r"KE", "=", r"\frac{1}{2}", "m", "v^2", font_size=72)
        self.play(Write(ke_eq))
        self.wait(1)
        self.play(ke_eq.animate.scale(0.6).shift(UP * 2))

        # v^2 강조
        self.play(Indicate(ke_eq[4], color=ORANGE))
        self.wait(0.5)

        # 에너지 바 차트: 속도 1배 vs 2배 비교
        mass = 2  # kg

        # 바 차트 세팅
        bar_base_y = -1.5
        bar_width = 1.0
        speeds = [2, 4, 6]
        energies = [0.5 * mass * v**2 for v in speeds]
        max_e = max(energies)
        bar_height_scale = 3.0 / max_e  # 최대 3 단위 높이

        bars = VGroup()
        labels = VGroup()
        val_labels = VGroup()

        for i, (v, e) in enumerate(zip(speeds, energies)):
            x = (i - 1) * 3.0
            h = e * bar_height_scale
            bar = Rectangle(
                width=bar_width, height=h,
                color=ORANGE, fill_opacity=0.7,
            )
            bar.move_to([x, bar_base_y + h / 2, 0])
            bars.add(bar)

            v_label = MathTex(f"v={v}" + r"\,\text{m/s}", font_size=22, color=WHITE)
            v_label.next_to(bar, DOWN, buff=0.2)
            labels.add(v_label)

            e_label = MathTex(f"KE={int(e)}" + r"\,\text{J}", font_size=20, color=ORANGE)
            e_label.next_to(bar, UP, buff=0.1)
            val_labels.add(e_label)

        self.play(
            *[GrowFromEdge(b, DOWN) for b in bars],
            *[Write(l) for l in labels],
            run_time=1.5,
        )
        self.play(*[Write(v) for v in val_labels], run_time=0.75)
        self.wait(1)

        # 속도 2배 → 에너지 4배 강조
        arrow_2x = CurvedArrow(
            bars[0].get_top() + UP * 0.5,
            bars[1].get_top() + UP * 0.5,
            color=WHITE, angle=-TAU / 8,
        )
        text_2x = MathTex(r"v \times 2", font_size=20, color=WHITE).next_to(arrow_2x, UP, buff=0.1)

        arrow_4x = CurvedArrow(
            val_labels[0].get_top() + UP * 0.3 + LEFT * 0.3,
            val_labels[1].get_top() + UP * 0.3 + RIGHT * 0.3,
            color=YELLOW, angle=-TAU / 8,
        )
        text_4x = MathTex(r"KE \times 4", font_size=20, color=YELLOW).next_to(arrow_4x, UP, buff=0.1)

        self.play(Create(arrow_2x), Write(text_2x))
        self.play(Create(arrow_4x), Write(text_4x))
        self.wait(1)

        conclusion = VGroup(
            Text("속도가 2배", font_size=28, color=YELLOW),
            MathTex(r"\Rightarrow", font_size=32, color=YELLOW),
            Text("운동에너지 4배", font_size=28, color=YELLOW),
        ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)

    # =========================================================
    # Phase 4: 일-운동에너지 정리
    # =========================================================
    def phase4_work_energy_theorem(self):
        title = Text("일-운동에너지 정리", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 핵심 수식
        theorem = MathTex(
            r"W_{\text{net}}", "=", r"\Delta KE", "=",
            r"\frac{1}{2}", "m", "v_f^2", "-",
            r"\frac{1}{2}", "m", "v_i^2",
            font_size=48,
        )
        self.play(Write(theorem))
        self.wait(1.5)
        self.play(theorem.animate.scale(0.7).next_to(title, DOWN, buff=0.3))

        # Phase 2 결과 검증
        verify_title = Text("Phase 2 검증", font_size=24, color=YELLOW).shift(UP * 0.5 + LEFT * 3)
        self.play(Write(verify_title))

        verify = VGroup(
            MathTex(r"W = Fd = 4 \times 5 = 20\,\text{J}", font_size=24, color=YELLOW),
            MathTex(r"v_f = \sqrt{\frac{2W}{m}} = \sqrt{\frac{2 \times 20}{2}} \approx 4.47\,\text{m/s}", font_size=24, color=BLUE),
            MathTex(r"\Delta KE = \frac{1}{2}(2)(4.47^2) - 0 = 20\,\text{J}\;\checkmark", font_size=24, color=YELLOW),
        )
        verify.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        verify.next_to(verify_title, DOWN, buff=0.3).align_to(verify_title, LEFT)

        for v in verify:
            self.play(Write(v), run_time=0.75)
        self.wait(1)

        # 마찰이 있는 경우
        friction_title = Text("마찰이 있는 경우", font_size=24, color=RED).shift(UP * 0.5 + RIGHT * 2)
        self.play(Write(friction_title))

        friction = VGroup(
            MathTex(r"W_F = Fd = 4 \times 5 = 20\,\text{J}", font_size=22, color=YELLOW),
            MathTex(r"W_f = -f \cdot d = -2 \times 5 = -10\,\text{J}", font_size=22, color=RED),
            MathTex(r"W_{\text{net}} = 20 - 10 = 10\,\text{J}", font_size=22, color=WHITE),
            MathTex(r"\Delta KE = 10\,\text{J}", font_size=22, color=ORANGE),
        )
        friction.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        friction.next_to(friction_title, DOWN, buff=0.3).align_to(friction_title, LEFT)

        for f in friction:
            self.play(Write(f), run_time=0.6)
        self.wait(1)

        # 결론 강조
        conclusion = MathTex(
            r"W_{\text{net}} = \Delta KE",
            font_size=64, color=YELLOW,
        ).move_to(DOWN * 2.5)
        conclusion_box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.3, corner_radius=0.1, stroke_width=3)
        self.play(Write(conclusion), Create(conclusion_box))
        self.wait(2)

    # =========================================================
    # Outro
    # =========================================================
    def outro(self):
        final_eq = MathTex(
            r"W_{\text{net}}", "=", r"\Delta KE",
            font_size=80, color=WHITE,
        )
        final_eq.move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        subtitle = Text("일과 운동에너지", font_size=40, color=YELLOW)
        subtitle.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.0)

        points = VGroup(
            Text("• 일 = 힘 × 이동거리 × cosθ", font_size=24, color=WHITE),
            Text("• 운동에너지 = ½mv²", font_size=24, color=WHITE),
            Text("• 알짜힘이 한 일 = 운동에너지의 변화량", font_size=24, color=WHITE),
        )
        points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        points.next_to(subtitle, DOWN, buff=0.5)
        self.play(FadeIn(points), run_time=1.0)
        self.wait(2)

        # 다음 편 예고
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        next_title = Text("다음 시간", font_size=36, color=GRAY).shift(UP * 0.5)
        next_q = Text("높이에서 에너지를 저장할 수 있을까?", font_size=32, color=YELLOW)
        next_q.next_to(next_title, DOWN, buff=0.4)
        next_hint = MathTex(r"E = KE + PE = \text{const?}", font_size=40, color=WHITE)
        next_hint.next_to(next_q, DOWN, buff=0.4)

        self.play(Write(next_title))
        self.play(Write(next_q))
        self.play(Write(next_hint))
        self.wait(3)
