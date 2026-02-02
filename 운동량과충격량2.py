from manim import TransformMatchingTex
from manim import *
import numpy as np


class ImpulseMomentum2(Scene):
    # ── 초기조건 ──
    MASS = 2
    G = 9.8
    T_FALL = 1.0
    V_IMPACT = 9.8       # = G * T_FALL
    IMPULSE = 19.6        # = MASS * V_IMPACT

    def construct(self):
        # ── 실험 파라미터 사전 계산 ──
        self.exp_a = self._make_experiment(
            label="실험 A (딱딱한 바닥)", delta_t=0.1,
            max_deform=0.08, floor_color=GRAY_BROWN,
        )
        self.exp_b = self._make_experiment(
            label="실험 B (부드러운 바닥)", delta_t=0.4,
            max_deform=0.2, floor_color=TEAL,
        )

        self.intro()
        self.clear_screen()
        self.derivation()
        self.clear_screen()
        self.sim_hard_floor()
        self.clear_screen()
        self.sim_soft_floor()
        self.clear_screen()
        self.comparison()
        self.clear_screen()
        self.outro()

    def _make_experiment(self, label, delta_t, max_deform, floor_color):
        """초기조건으로부터 실험에 필요한 모든 물리량을 한번에 계산"""
        return dict(
            label=label,
            delta_t=delta_t,
            max_deform=max_deform,
            floor_color=floor_color,
            F_peak=self._F_peak(delta_t),
            F_avg=self._F_avg(delta_t),
            t_coll_end=self.T_FALL + delta_t,
        )

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # ── Spring collision model ──
    # F(τ) = 12*I/Δt * u*(1-u)², u=τ/Δt  (peak at u=1/3)
    # v(τ) = v₀*(1 - 6u² + 8u³ - 3u⁴)
    # deform(τ) = 6u² - 8u³ + 3u⁴  (0→1, stays at 1)
    def _f_spring(self, tau, dt):
        if tau <= 0 or tau >= dt:
            return 0.0
        u = tau / dt
        return 12 * self.IMPULSE / dt * u * (1 - u) ** 2

    def _v_spring(self, tau, dt):
        if tau <= 0:
            return self.V_IMPACT
        if tau >= dt:
            return 0.0
        u = tau / dt
        return self.V_IMPACT * (1 - 6 * u**2 + 8 * u**3 - 3 * u**4)

    def _deform_frac(self, tau, dt):
        if tau <= 0:
            return 0.0
        if tau >= dt:
            return 1.0
        u = tau / dt
        return 6 * u**2 - 8 * u**3 + 3 * u**4

    def _F_peak(self, dt):
        return 48 * self.IMPULSE / (27 * dt)

    def _F_avg(self, dt):
        return self.IMPULSE / dt

    # ═══════════════════════════════════════
    # Phase 1
    # ═══════════════════════════════════════
    def intro(self):
        title = Text("충격량과 운동량 II", font_size=80, color=WHITE)
        box = SurroundingRectangle(title, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=1.0)
        self.play(Write(box), run_time=1.0)
        self.wait(0.5)

    # ═══════════════════════════════════════
    # Phase 2
    # ═══════════════════════════════════════
    def derivation(self):
        eq = MathTex("I", "=", "F", r"\times", r"\Delta t", font_size=72)
        self.play(Write(eq))
        self.wait(1)
        self.play(eq[2].animate.scale(1.3).set_color(RED), run_time=0.5)
        self.wait(0.5)
        self.play(eq[2].animate.scale(1 / 1.3), run_time=0.3)
        self.wait(0.5)
        self.play(eq[4].animate.scale(1.3).set_color(BLUE), run_time=0.5)
        self.wait(0.5)
        self.play(eq[4].animate.scale(1 / 1.3), run_time=0.3)
        self.wait(1)

    # ═══════════════════════════════════════
    # Phase 3 & 4
    # ═══════════════════════════════════════
    def sim_hard_floor(self):
        self._run_fall_sim(self.exp_a)

    def sim_soft_floor(self):
        self._run_fall_sim(self.exp_b)

    def _run_fall_sim(self, exp):
        exp_label = exp["label"]
        floor_color = exp["floor_color"]
        delta_t = exp["delta_t"]
        max_deform = exp["max_deform"]
        F_peak = exp["F_peak"]
        F_avg = exp["F_avg"]
        t_coll_end = exp["t_coll_end"]

        obj_radius = 0.3

        obj_x = -5.0
        floor_y = -2.5
        floor_top_y = floor_y + 0.15
        obj_land_y = floor_top_y + obj_radius
        obj_start_y = obj_land_y + 2.5

        # ── Label ──
        exp_title = Text(exp_label, font_size=28, color=floor_color).to_edge(UP, buff=0.3)

        # ── Objects ──
        ball = Circle(radius=obj_radius, color=BLUE, fill_opacity=0.8)
        ball.move_to([obj_x, obj_start_y, 0])
        ball_label = Text("2kg", font_size=16, color=WHITE).move_to(ball)

        floor_rect = Rectangle(width=2.5, height=0.3, color=floor_color,
                               fill_opacity=0.8, stroke_width=2)
        floor_rect.move_to([obj_x, floor_y, 0])
        floor_name = exp_label.split("(")[1].rstrip(")")
        floor_text = Text(floor_name, font_size=18, color=floor_color)
        floor_text.next_to(floor_rect, DOWN, buff=0.15)

        init_text = VGroup(
            MathTex(r"v_0 = 0", font_size=24),
            MathTex(r"m = 2\text{ kg}", font_size=24),
            MathTex(r"g = 9.8\text{ m/s}^2", font_size=24),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        init_text.next_to(ball, RIGHT, buff=0.4)

        # ── Graphs ──
        graph_cx = -0.8
        t_graph_end = t_coll_end + 0.3
        ft_y_max = F_peak * 1.2
        ft_y_step = max(round(ft_y_max / 4, -1), 10)

        vt_axes = Axes(
            x_range=[0, t_graph_end, 0.5], y_range=[0, 12, 2],
            x_length=3.5, y_length=2.2,
            axis_config={"include_tip": False, "font_size": 20},
            x_axis_config={"numbers_to_include": [0.5, 1.0]},
            y_axis_config={"numbers_to_include": [self.V_IMPACT]},
        ).move_to([graph_cx, 1.5, 0])
        vt_xl = Text("t (s)", font_size=14).next_to(vt_axes.x_axis, RIGHT, buff=0.1)
        vt_yl = Text("v (m/s)", font_size=14).next_to(vt_axes.y_axis, UP, buff=0.1)

        ft_axes = Axes(
            x_range=[0, t_graph_end, 0.5], y_range=[0, ft_y_max, ft_y_step],
            x_length=3.5, y_length=2.2,
            axis_config={"include_tip": False, "font_size": 20},
            x_axis_config={"numbers_to_include": [0.5, 1.0]},
            y_axis_config={"numbers_to_include": [round(F_peak)]},
        ).move_to([graph_cx, -1.8, 0])
        ft_xl = Text("t (s)", font_size=14).next_to(ft_axes.x_axis, RIGHT, buff=0.1)
        ft_yl = Text("|F| (N)", font_size=14).next_to(ft_axes.y_axis, UP, buff=0.1)

        # Collision end tick
        te_tick_ft = Line(ft_axes.c2p(t_coll_end, 0) + UP * 0.08,
                          ft_axes.c2p(t_coll_end, 0) + DOWN * 0.08,
                          color=WHITE, stroke_width=2)
        te_num_ft = MathTex(rf"{t_coll_end:.1f}", font_size=16, color=WHITE)
        te_num_ft.next_to(ft_axes.c2p(t_coll_end, 0), DOWN, buff=0.15)
        te_tick_vt = Line(vt_axes.c2p(t_coll_end, 0) + UP * 0.08,
                          vt_axes.c2p(t_coll_end, 0) + DOWN * 0.08,
                          color=WHITE, stroke_width=2)
        te_num_vt = MathTex(rf"{t_coll_end:.1f}", font_size=16, color=WHITE)
        te_num_vt.next_to(vt_axes.c2p(t_coll_end, 0), DOWN, buff=0.15)

        calc_x = 4.5

        # ── 1. Layout ──
        self.play(
            Write(exp_title),
            FadeIn(ball), FadeIn(ball_label),
            FadeIn(floor_rect), FadeIn(floor_text), FadeIn(init_text),
            Create(vt_axes), Write(vt_xl), Write(vt_yl),
            Create(ft_axes), Write(ft_xl), Write(ft_yl),
            FadeIn(te_tick_ft), FadeIn(te_num_ft),
            FadeIn(te_tick_vt), FadeIn(te_num_vt),
        )
        self.wait(1)

        # ── 2. Free fall + v label ──
        fall_dist = obj_start_y - obj_land_y
        v_tracker = ValueTracker(0)
        v_label = always_redraw(lambda: MathTex(
            rf"v = {v_tracker.get_value():.1f}", font_size=20, color=GREEN,
        ).next_to(ball, RIGHT, buff=0.15))

        vt_fall = vt_axes.plot(lambda t: self.G * t, x_range=[0, self.T_FALL],
                               color=GREEN, stroke_width=3)
        ft_fall = ft_axes.plot(lambda t: 0, x_range=[0, self.T_FALL],
                               color=WHITE, stroke_width=3)

        self.play(FadeOut(init_text), FadeIn(v_label), run_time=0.3)
        self.play(
            ball.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_dist),
            ball_label.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_dist),
            v_tracker.animate.set_value(self.V_IMPACT),
            Create(vt_fall), Create(ft_fall),
            run_time=2, rate_func=linear,
        )
        self.wait(0.5)

        vt_dot = Dot(vt_axes.c2p(self.T_FALL, self.V_IMPACT), color=RED, radius=0.06)
        vt_hd = DashedLine(vt_axes.c2p(0, self.V_IMPACT), vt_axes.c2p(self.T_FALL, self.V_IMPACT),
                           color=GRAY, stroke_width=1.5, dash_length=0.08)
        vt_vd = DashedLine(vt_axes.c2p(self.T_FALL, 0), vt_axes.c2p(self.T_FALL, self.V_IMPACT),
                           color=GRAY, stroke_width=1.5, dash_length=0.08)
        self.play(Create(vt_hd), Create(vt_vd), FadeIn(vt_dot), run_time=0.5)
        self.wait(0.5)

        # ── 3. p = mv ──
        self.play(FadeOut(v_label))
        p_calc = VGroup(
            MathTex(r"p = mv", font_size=36, color=WHITE),
            MathTex(r"= 2 \times 9.8", font_size=36, color=WHITE),
            MathTex(r"= 19.6 \text{ kg·m/s}", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([calc_x, 2.5, 0])
        for line in p_calc:
            self.play(Write(line), run_time=0.5)
        self.wait(1)

        # ── 4. Collision ──
        # Floor deformation setup
        coll_tracker = ValueTracker(0)
        orig_top = floor_rect.get_top()[1]
        orig_bot = floor_rect.get_bottom()[1]
        fl_w = floor_rect.get_width()
        fl_lx = floor_rect.get_left()[0]

        def get_def_floor():
            d = self._deform_frac(coll_tracker.get_value(), delta_t) * max_deform
            if d > 0.001:
                n = 30
                pts = []
                for i in range(n + 1):
                    frac = i / n
                    x = fl_lx + frac * fl_w
                    dist = (x - obj_x) / (fl_w * 0.3)
                    pts.append([x, orig_top - d * np.exp(-dist**2), 0])
                pts.append([fl_lx + fl_w, orig_bot, 0])
                pts.append([fl_lx, orig_bot, 0])
                return Polygon(*[np.array(p) for p in pts],
                               color=floor_color, fill_opacity=0.8, stroke_width=2)
            r = Rectangle(width=fl_w, height=0.3, color=floor_color,
                          fill_opacity=0.8, stroke_width=2)
            r.move_to([obj_x, floor_y, 0])
            return r

        def_floor = always_redraw(get_def_floor)

        def upd_ball(b):
            d = self._deform_frac(coll_tracker.get_value(), delta_t) * max_deform
            b.move_to([obj_x, obj_land_y - d, 0])
        def upd_bl(bl):
            bl.move_to(ball.get_center())

        ball.add_updater(upd_ball)
        ball_label.add_updater(upd_bl)
        self.play(FadeOut(floor_rect), FadeIn(def_floor), run_time=0.1)

        p_tracker = ValueTracker(self.IMPULSE)
        p_label = always_redraw(lambda: MathTex(
            rf"p = {p_tracker.get_value():.1f}", font_size=20, color=YELLOW,
        ).next_to(ball, RIGHT, buff=0.15))
        self.play(FadeIn(p_label), run_time=0.3)

        t0 = self.T_FALL
        ft_pulse = ft_axes.plot(lambda t: self._f_spring(t - t0, delta_t),
                                x_range=[t0, t_coll_end, 0.002], color=RED, stroke_width=3)
        vt_coll = vt_axes.plot(lambda t: self._v_spring(t - t0, delta_t),
                               x_range=[t0, t_coll_end, 0.002], color=YELLOW, stroke_width=3)

        t_peak = t0 + delta_t / 3
        ft_hd = DashedLine(ft_axes.c2p(0, F_peak), ft_axes.c2p(t_peak, F_peak),
                           color=GRAY, stroke_width=1.5, dash_length=0.08)
        ft_vdp = DashedLine(ft_axes.c2p(t_peak, 0), ft_axes.c2p(t_peak, F_peak),
                            color=GRAY, stroke_width=1.5, dash_length=0.08)
        ft_dotp = Dot(ft_axes.c2p(t_peak, F_peak), color=RED, radius=0.06)

        t_end = t_coll_end + 0.2
        vt_rest = vt_axes.plot(lambda t: 0, x_range=[t_coll_end, t_end], color=GREEN, stroke_width=3)
        ft_rest = ft_axes.plot(lambda t: 0, x_range=[t_coll_end, t_end], color=WHITE, stroke_width=3)
        vt_dot_e = Dot(vt_axes.c2p(t_coll_end, 0), color=RED, radius=0.06)

        self.play(
            coll_tracker.animate.set_value(delta_t),
            p_tracker.animate.set_value(0),
            Create(vt_coll), Create(ft_pulse),
            Create(ft_hd), Create(ft_vdp), FadeIn(ft_dotp),
            run_time=1.0, rate_func=linear,
        )
        self.play(Create(vt_rest), Create(ft_rest), FadeIn(vt_dot_e), run_time=0.3)
        self.wait(0.5)

        ball.clear_updaters()
        ball_label.clear_updaters()
        ball.move_to([obj_x, obj_land_y - max_deform, 0])
        ball_label.move_to(ball.get_center())
        self.play(FadeOut(p_label), run_time=0.3)

        # ── 5. Average force ──
        avg_line = DashedLine(ft_axes.c2p(0, F_avg), ft_axes.c2p(t_coll_end, F_avg),
                              color=ORANGE, stroke_width=2.5, dash_length=0.1)
        avg_txt = Text("평균힘", font_size=16, color=ORANGE)
        avg_txt.next_to(ft_axes.c2p(0, F_avg), LEFT, buff=0.15)
        avg_val = MathTex(rf"\bar{{F}} = {F_avg:.0f}" + r"\text{ N}",
                          font_size=18, color=ORANGE).next_to(avg_line, UP, buff=0.08)
        avg_rect = Polygon(
            ft_axes.c2p(t0, 0), ft_axes.c2p(t0, F_avg),
            ft_axes.c2p(t_coll_end, F_avg), ft_axes.c2p(t_coll_end, 0),
            color=ORANGE, fill_opacity=0.15, stroke_width=1.5, stroke_color=ORANGE,
        )
        self.play(Create(avg_line), Write(avg_txt), Write(avg_val), FadeIn(avg_rect), run_time=1.0)
        self.wait(0.5)

        area_ft = ft_axes.get_area(ft_pulse, x_range=[t0, t_coll_end], color=RED, opacity=0.3)
        self.play(FadeIn(area_ft))
        self.wait(0.5)

        # ── 6. Impulse calculation ──
        calc_grp = VGroup(
            MathTex(r"I = \bar{F} \times \Delta t", font_size=36, color=WHITE),
            MathTex(rf"= {F_avg:.0f} \times {delta_t}", font_size=36, color=WHITE),
            MathTex(rf"= {self.IMPULSE}" + r"\text{ N·s}", font_size=40, color=YELLOW),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([calc_x, -0.8, 0])
        for item in calc_grp:
            self.play(Write(item), run_time=0.6)
            self.wait(0.3)
        rbox = SurroundingRectangle(calc_grp[-1], color=YELLOW, buff=0.15,
                                    corner_radius=0.1, stroke_width=2)
        self.play(Create(rbox))
        self.wait(2)

    # ═══════════════════════════════════════
    # Phase 5: 비교
    # ═══════════════════════════════════════
    def comparison(self):
        ea, eb = self.exp_a, self.exp_b
        dt_a, dt_b = ea["delta_t"], eb["delta_t"]
        Fp_a, Fp_b = ea["F_peak"], eb["F_peak"]
        Fa_a, Fa_b = ea["F_avg"], eb["F_avg"]
        md_a, md_b = ea["max_deform"], eb["max_deform"]

        # ── Left column: mini setups ──
        mini_r = 0.15
        mini_fw = 1.2

        ax, ay_fl_a = -5.0, 1.0
        ay_top_a = ay_fl_a + 0.1 + mini_r
        ay_st_a = ay_top_a + 1.2

        lbl_a = Text("실험 A (딱딱한 바닥)", font_size=16, color=GRAY_BROWN)
        lbl_a.move_to([ax, ay_st_a + 0.4, 0])
        ba = Circle(radius=mini_r, color=BLUE, fill_opacity=0.8).move_to([ax, ay_st_a, 0])
        fl_a = Rectangle(width=mini_fw, height=0.2, color=GRAY_BROWN,
                         fill_opacity=0.8, stroke_width=2).move_to([ax, ay_fl_a, 0])

        ay_fl_b = -2.0
        ay_top_b = ay_fl_b + 0.1 + mini_r
        ay_st_b = ay_top_b + 1.2

        lbl_b = Text("실험 B (부드러운 바닥)", font_size=16, color=TEAL)
        lbl_b.move_to([ax, ay_st_b + 0.4, 0])
        bb = Circle(radius=mini_r, color=BLUE, fill_opacity=0.8).move_to([ax, ay_st_b, 0])
        fl_b = Rectangle(width=mini_fw, height=0.2, color=TEAL,
                         fill_opacity=0.8, stroke_width=2).move_to([ax, ay_fl_b, 0])

        # ── Right column: overlapped F-t ──
        comp_axes = Axes(
            x_range=[0, 0.55, 0.1], y_range=[0, Fp_a * 1.15, 50],
            x_length=5.5, y_length=4.5,
            axis_config={"include_tip": False, "font_size": 16, "include_numbers": False},
        ).move_to([2.5, 0, 0])

        x_txt = Text("충돌 시간", font_size=16, color=GRAY).next_to(comp_axes.x_axis, DR, buff=0.25)
        y_txt = Text("힘", font_size=16, color=GRAY).next_to(comp_axes.y_axis, UL, buff=0.2)

        # Static curves (for after animation)
        curve_a_static = comp_axes.plot(lambda t: self._f_spring(t, dt_a),
                                        x_range=[0, dt_a, 0.001], color=RED, stroke_width=3)
        curve_b_static = comp_axes.plot(lambda t: self._f_spring(t, dt_b),
                                        x_range=[0, dt_b, 0.001], color=TEAL, stroke_width=3)

        # ── 1. Layout ──
        self.play(
            FadeIn(lbl_a), FadeIn(ba), FadeIn(fl_a),
            FadeIn(lbl_b), FadeIn(bb), FadeIn(fl_b),
            Create(comp_axes), Write(x_txt), Write(y_txt),
        )
        self.wait(0.5)

        # ── 2. Simultaneous fall ──
        fall_a = ay_st_a - ay_top_a
        fall_b = ay_st_b - ay_top_b
        self.play(
            ba.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_a),
            bb.animate(rate_func=rate_functions.ease_in_quad).shift(DOWN * fall_b),
            run_time=1.5, rate_func=linear,
        )
        self.wait(0.3)

        # ── 3. Collision phase ──
        ct = ValueTracker(0)

        # Capture floor geometry before replacing
        fla_top = fl_a.get_top()[1]
        fla_bot = fl_a.get_bottom()[1]
        fla_lx = fl_a.get_left()[0]
        flb_top = fl_b.get_top()[1]
        flb_bot = fl_b.get_bottom()[1]
        flb_lx = fl_b.get_left()[0]

        def mk_dfl_a():
            d = self._deform_frac(ct.get_value(), dt_a) * md_a
            if d > 0.001:
                pts = []
                for i in range(21):
                    f = i / 20
                    x = fla_lx + f * mini_fw
                    dist = (x - ax) / (mini_fw * 0.3)
                    pts.append([x, fla_top - d * np.exp(-dist**2), 0])
                pts.append([fla_lx + mini_fw, fla_bot, 0])
                pts.append([fla_lx, fla_bot, 0])
                return Polygon(*[np.array(p) for p in pts],
                               color=GRAY_BROWN, fill_opacity=0.8, stroke_width=2)
            r = Rectangle(width=mini_fw, height=0.2, color=GRAY_BROWN,
                          fill_opacity=0.8, stroke_width=2)
            r.move_to([ax, ay_fl_a, 0])
            return r

        def mk_dfl_b():
            d = self._deform_frac(ct.get_value(), dt_b) * md_b
            if d > 0.001:
                pts = []
                for i in range(21):
                    f = i / 20
                    x = flb_lx + f * mini_fw
                    dist = (x - ax) / (mini_fw * 0.3)
                    pts.append([x, flb_top - d * np.exp(-dist**2), 0])
                pts.append([flb_lx + mini_fw, flb_bot, 0])
                pts.append([flb_lx, flb_bot, 0])
                return Polygon(*[np.array(p) for p in pts],
                               color=TEAL, fill_opacity=0.8, stroke_width=2)
            r = Rectangle(width=mini_fw, height=0.2, color=TEAL,
                          fill_opacity=0.8, stroke_width=2)
            r.move_to([ax, ay_fl_b, 0])
            return r

        dfl_a = always_redraw(mk_dfl_a)
        dfl_b = always_redraw(mk_dfl_b)

        def upd_ba(b):
            d = self._deform_frac(ct.get_value(), dt_a) * md_a
            b.move_to([ax, ay_top_a - d, 0])
        def upd_bb(b):
            d = self._deform_frac(ct.get_value(), dt_b) * md_b
            b.move_to([ax, ay_top_b - d, 0])

        ba.add_updater(upd_ba)
        bb.add_updater(upd_bb)

        self.play(FadeOut(fl_a), FadeIn(dfl_a), FadeOut(fl_b), FadeIn(dfl_b), run_time=0.05)

        # Growing curves
        def mk_gc_a():
            te = min(ct.get_value(), dt_a)
            if te < 0.003:
                return VGroup()
            return comp_axes.plot(lambda s: self._f_spring(s, dt_a),
                                 x_range=[0, te, 0.002], color=RED, stroke_width=3)
        def mk_gc_b():
            te = min(ct.get_value(), dt_b)
            if te < 0.003:
                return VGroup()
            return comp_axes.plot(lambda s: self._f_spring(s, dt_b),
                                 x_range=[0, te, 0.002], color=TEAL, stroke_width=3)

        gc_a = always_redraw(mk_gc_a)
        gc_b = always_redraw(mk_gc_b)
        self.add(gc_a, gc_b)

        self.play(ct.animate.set_value(dt_b), run_time=2.5, rate_func=linear)
        self.wait(0.5)

        # Fix state
        ba.clear_updaters()
        bb.clear_updaters()
        ba.move_to([ax, ay_top_a - md_a, 0])
        bb.move_to([ax, ay_top_b - md_b, 0])
        self.remove(gc_a, gc_b)
        self.add(curve_a_static, curve_b_static)

        # ── 4. Labels ──
        cl_a = Text("A", font_size=20, color=RED)
        cl_a.next_to(curve_a_static.get_top(), UR, buff=0.1)
        cl_b = Text("B", font_size=20, color=TEAL)
        cl_b.next_to(curve_b_static.get_right(), RIGHT, buff=0.1)
        self.play(Write(cl_a), Write(cl_b))
        self.wait(0.5)

        # ── 5. Average force lines (y축까지 연결) ──
        avg_a = DashedLine(comp_axes.c2p(0, Fa_a), comp_axes.c2p(dt_a, Fa_a),
                           color=RED, stroke_width=2, dash_length=0.08)
        avg_a_lbl = MathTex(rf"{Fa_a:.0f}" + r"\text{ N}", font_size=16, color=RED)
        avg_a_lbl.next_to(comp_axes.c2p(0, Fa_a), LEFT, buff=0.1)
        avg_a_txt = Text("평균힘", font_size=16, color=RED)
        avg_a_txt.next_to(avg_a_lbl, LEFT, buff=0.08)

        avg_b = DashedLine(comp_axes.c2p(0, Fa_b), comp_axes.c2p(dt_b, Fa_b),
                           color=TEAL, stroke_width=2, dash_length=0.08)
        avg_b_lbl = MathTex(rf"{Fa_b:.0f}" + r"\text{ N}", font_size=16, color=TEAL)
        avg_b_lbl.next_to(comp_axes.c2p(0, Fa_b), LEFT, buff=0.1)
        avg_b_txt = Text("평균힘", font_size=16, color=TEAL)
        avg_b_txt.next_to(avg_b_lbl, LEFT, buff=0.08)

        self.play(
            Create(avg_a), Write(avg_a_lbl), Write(avg_a_txt),
            Create(avg_b), Write(avg_b_lbl), Write(avg_b_txt),
            run_time=1.0,
        )
        self.wait(0.5)

        # Force difference arrow
        mid_x = comp_axes.c2p(dt_a + 0.03, 0)[0]
        f_arrow = DoubleArrow(
            [mid_x, comp_axes.c2p(0, Fa_b)[1], 0],
            [mid_x, comp_axes.c2p(0, Fa_a)[1], 0],
            color=YELLOW, buff=0, stroke_width=3, tip_length=0.15,
        )
        f_diff = Text("힘 4배", font_size=16, color=YELLOW)
        f_diff.next_to(f_arrow, RIGHT, buff=0.1)
        self.play(GrowFromCenter(f_arrow), Write(f_diff))
        self.wait(0.5)

        # ── 6. Time markers ──
        dt_line_a = DashedLine(comp_axes.c2p(dt_a, 0), comp_axes.c2p(dt_a, Fp_a * 0.3),
                               color=RED, stroke_width=2, dash_length=0.06)
        dt_lbl_a = MathTex(rf"\Delta t_A = {dt_a}", font_size=16, color=RED)
        dt_lbl_a.next_to(comp_axes.c2p(dt_a, 0), DOWN, buff=0.2)

        dt_line_b = DashedLine(comp_axes.c2p(dt_b, 0), comp_axes.c2p(dt_b, Fp_b * 0.3),
                               color=TEAL, stroke_width=2, dash_length=0.06)
        dt_lbl_b = MathTex(rf"\Delta t_B = {dt_b}", font_size=16, color=TEAL)
        dt_lbl_b.next_to(comp_axes.c2p(dt_b, 0), DOWN, buff=0.2)

        self.play(Create(dt_line_a), Write(dt_lbl_a), Create(dt_line_b), Write(dt_lbl_b), run_time=1.0)
        self.wait(0.5)

        # Time difference arrow
        bot_y = comp_axes.c2p(0, 0)[1] - 0.5
        t_arrow = DoubleArrow(
            [comp_axes.c2p(dt_a, 0)[0], bot_y, 0],
            [comp_axes.c2p(dt_b, 0)[0], bot_y, 0],
            color=YELLOW, buff=0, stroke_width=3, tip_length=0.15,
        )
        t_diff = Text("시간 4배", font_size=16, color=YELLOW)
        t_diff.next_to(t_arrow, DOWN, buff=0.1)
        self.play(GrowFromCenter(t_arrow), Write(t_diff))
        self.wait(0.5)

        # ── 7. Same impulse — show both areas then equality ──
        area_a = comp_axes.get_area(curve_a_static, x_range=[0, dt_a],
                                     color=RED, opacity=0.35)
        area_b = comp_axes.get_area(curve_b_static, x_range=[0, dt_b],
                                     color=TEAL, opacity=0.35)

        lbl_Sa = MathTex(r"S_A", font_size=24, color=RED)
        lbl_Sa.move_to(comp_axes.c2p(dt_a / 2, Fa_a * 0.5))
        lbl_Sb = MathTex(r"S_B", font_size=24, color=TEAL)
        lbl_Sb.move_to(comp_axes.c2p(dt_b / 2, Fa_b * 0.5))

        self.play(FadeIn(area_a), Write(lbl_Sa), run_time=0.8)
        self.play(FadeIn(area_b), Write(lbl_Sb), run_time=0.8)
        self.wait(0.5)

        same_grp = VGroup(
            MathTex(r"S_A", font_size=30, color=RED),
            MathTex(r"=", font_size=30, color=YELLOW),
            MathTex(r"S_B", font_size=30, color=TEAL),
            MathTex(r"= 19.6 \text{ N·s}", font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.15)
        same_title = Text("같은 충격량", font_size=26, color=YELLOW)
        same_box = VGroup(same_title, same_grp).arrange(DOWN, buff=0.15)
        same_box.next_to(comp_axes, UP, buff=0.3)
        sbox = SurroundingRectangle(same_box, color=YELLOW, buff=0.15,
                                    corner_radius=0.1, stroke_width=2)
        self.play(Write(same_box), Create(sbox))
        self.wait(2)

    # ═══════════════════════════════════════
    # Phase 6: 아웃트로
    # ═══════════════════════════════════════
    def outro(self):
        msg = Text(
            "같은 충격량(운동량변화량)이어도\n물체에 작용하는 평균힘의 크기가 달라질 수 있다.",
            font_size=40, color=WHITE, line_spacing=1.5,
        ).move_to(ORIGIN)
        self.play(Write(msg), run_time=2)
        self.wait(2)
        self.play(FadeOut(msg), run_time=1)
        self.wait(0.5)

        title = Text("충격량과 운동량 II", font_size=80, color=WHITE).move_to(ORIGIN)
        box = SurroundingRectangle(title, color=YELLOW, buff=0.4,
                                   corner_radius=0.15, stroke_width=4)
        self.play(Write(title), run_time=1.0)
        self.play(Create(box), run_time=0.8)
        self.wait(2)
