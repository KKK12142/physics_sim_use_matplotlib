from manim import always_redraw
from manim import VMobject
from manim import ValueTracker
from manim import FadeIn
from manim import TransformMatchingTex
from manim import *
import numpy as np

class ImpulseMomentum(Scene):
    def construct(self):
        
        self.intro()
        self.clear_screen()
        self.driving_eq()
        self.clear_screen()
        self.simulation_accelation()
        self.clear_screen()
        self.simulation_braking()
        self.clear_screen()
        self.summary()
        self.clear_screen()
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    def intro(self):
        title = Text("충격량과 운동량", font_size=80, color=WHITE)
        box = SurroundingRectangle(title, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        title.move_to(ORIGIN)
        self.play(Write(title), run_time=1.0)
        self.play(Write(box), run_time=1.0)
        self.wait(0.5)

    def driving_eq(self):
        # Step 1: F = ma
        eq1 = MathTex("F", "=", "m", "a", font_size=80)
        self.play(Write(eq1))
        self.wait(1)

        # a 강조
        self.play(eq1[3].animate.set_color(RED))
        self.wait(0.5)

        # Step 2: a → Δv/Δt
        eq2 = MathTex("F", "=", "m", r"\times", r"\frac{\Delta v}{\Delta t}", font_size=80)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(1)

        # Step 3: m을 분자로 합치기
        eq2b = MathTex("F", "=", r"\frac{m \Delta v}{\Delta t}", font_size=80)
        self.play(TransformMatchingTex(eq2, eq2b))
        self.wait(0.5)

        # mΔv 부분 강조
        self.play(Indicate(eq2b[2], color=RED))
        self.wait(0.5)

        # Step 4: mΔv → Δp
        eq3 = MathTex("F", "=", r"\frac{\Delta p}{\Delta t}", font_size=80)
        self.play(TransformMatchingTex(eq2b, eq3))
        self.wait(1)

        # Step 5: Δt 이항 (개별 조각 이동)
        eq4 = MathTex("F", r"\times", r"\Delta t", "=", r"\Delta p", font_size=80)
        eq4.move_to(ORIGIN)
        self.play(
            ReplacementTransform(eq3[0], eq4[0]),  # F → F
            FadeIn(eq4[1]),                         # × 새로 등장
            FadeIn(eq4[2]),                         # Δt 새로 등장
            ReplacementTransform(eq3[1], eq4[3]),  # = → =
            ReplacementTransform(eq3[2], eq4[4]),  # Δp/Δt → Δp
            run_time=1.5
        )
        self.wait(2)

        # Step 6: 충격량 정의
        eq5 = MathTex("I", "=", r"\Delta p", font_size=96, color=YELLOW)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(2)

    def simulation_accelation(self):
        #===================================#
        #==== 파트 1: 등속운동 하던 물체의 가속 ===#
        #===================================#

        # ── 물리 파라미터 ──
        mass = 2
        v0 = 1
        F_val = 4       # 절댓값으로 처리
        a_val = F_val / mass  # 2 m/s^2
        t_accel_start = 2
        t_accel_end = 4
        t_end = 5
        obj_size = 0.5

        # -- 위치 함수 --
        def pos_func(t):
            if t < t_accel_start:
                return v0 * t # 2m
            elif t <= t_accel_end:
                dt = t - t_accel_start
                return 2 + v0 * dt + 0.5 * a_val * dt ** 2 # 8m
            else:
                return pos_func(t_accel_end) + v_func(t_accel_end) * (t - t_accel_end)

        # -- 속도 함수 --
        def v_func(t):
            if t < t_accel_start:
                return v0
            elif t <= t_accel_end:
                dt = t - t_accel_start
                return v0 + a_val * dt
            else:
                return v_func(t_accel_end)

        # -- 힘 힘수 -- 
        def f_func(t):
            if t < t_accel_start:
                return 0
            elif t <= t_accel_end:
                return F_val
            else:
                return 0

        # ── 트랙 (상단) ──
        track = NumberLine(
            x_range=[0, 13, 1],
            length = 12,
            color = WHITE,
            stroke_width = 3,
            include_numbers=True,
            numbers_to_include = range(0, 13, 2),
            label_direction=DOWN,
            font_size=24
        )
        track.shift(UP * 1.5)

        # ── 물체 (상단) ──
        obj = Rectangle(
            width=obj_size, height=obj_size, color=BLUE, fill_opacity=0.8
        )
        obj.move_to(track.n2p(0), 
            aligned_edge=DOWN).shift(UP * 0.1)

        obj_label = Text("2kg", font_size=18, color=WHITE)
        obj_label.move_to(obj.get_center())
        
        # -- 가속 구간 표시 (1-9m) ──
        acc_bar = Line(track.n2p(2), track.n2p(8), color=GREEN, stroke_width=8)

        acc_bar_label = Text("가속 구간", font_size=24,color=GREEN)
        acc_bar_label.move_to(acc_bar.get_center()).shift(DOWN * 0.5)

        # ── F-t 그래프 (하단 왼쪽) ──
        ft_axis = Axes(
            x_range=[0, t_end, 1], y_range=[0, F_val+1, 1],
            x_length=5, y_length=3,
            axis_config = {"include_tip": False},
            x_axis_config = {"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config = {"numbers_to_include": [2, 4]}
        ).to_corner(DL, buff=0.8)
        ft_x_label = Text("t(s)", font_size=20).next_to(ft_axis.x_axis, RIGHT, buff=0.2)
        ft_y_label = Text("|F|(N)", font_size=20).next_to(ft_axis.y_axis, UP, buff=0.2)

        # ── v-t 그래프 (하단 오른쪽) ──

        vt_axis = Axes(
            x_range=[0, t_end, 1], y_range=[0, 7, 1],
            x_length=5, y_length=3,
            axis_config = {"include_tip": False},
            x_axis_config = {"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config = {"numbers_to_include": [1, 2, 4, 6]}
        ).to_corner(DR, buff=0.8).shift(LEFT * 1)
        vt_x_label = Text("t(s)", font_size=20).next_to(vt_axis.x_axis, RIGHT, buff=0.2)
        vt_y_label = Text("v(m/s)", font_size=20).next_to(vt_axis.y_axis, UP, buff=0.2)

        # ── 타이틀 ──
        title = VGroup(
            MathTex(r"v_0 = 1\text{m/s}", font_size=36, color=WHITE),
            Text(" 로 등속운동 하던 물체가 가속 구간을 지나는 상황", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)

        self.play(Write(title), Write(track),
        Write(acc_bar), Write(acc_bar_label),
        Write(ft_axis), Write(ft_x_label), Write(ft_y_label),
        Write(vt_axis), Write(vt_x_label), Write(vt_y_label),
        FadeIn(obj), FadeIn(obj_label)
        )
        self.wait(1)

        # -- 물체 운동 시작 애니메이션  --
        time_tracker = ValueTracker(0)

        def update_obj(obj):
            obj.move_to(track.n2p(pos_func(time_tracker.get_value())), aligned_edge=DOWN).shift(UP * 0.1)

        obj.add_updater(update_obj)
        obj_label.add_updater(lambda m : m.move_to(obj.get_center()))
        self.wait(1)

        # -- v-t 그래프 애니메이션 --
        vt_graph = always_redraw(lambda: 
            vt_axis.plot(v_func, x_range=[0, time_tracker.get_value()], color=BLUE, stroke_width=3, use_smoothing=False)
        )

        # -- f-t 그래프 애니메이션 --
        ft_graph = always_redraw(lambda:
            ft_axis.plot(lambda t: F_val,
                x_range=[t_accel_start, min(time_tracker.get_value(), t_accel_end)],
                color=RED, stroke_width=3, use_smoothing=False)
            if time_tracker.get_value() > t_accel_start else VMobject()
        )

        # -- 힘 화살표 (가속 구간에서만 표시) --
        force_arrow = always_redraw(lambda:
            Arrow(
                start=obj.get_right(), end=obj.get_right() + RIGHT * 0.8,
                color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3
            ) if t_accel_start <= time_tracker.get_value() <= t_accel_end else VMobject()
        )
        force_arrow_label = always_redraw(lambda:
            MathTex("F", font_size=28, color=RED).next_to(obj.get_right() + RIGHT * 0.8, UP, buff=0.1)
            if t_accel_start <= time_tracker.get_value() <= t_accel_end else VMobject()
        )

        self.add(vt_graph, ft_graph, force_arrow, force_arrow_label)

        self.play(time_tracker.animate.set_value(t_end), run_time=t_end,rate_func=linear)

        obj.clear_updaters()
        obj_label.clear_updaters()
        self.remove(force_arrow, force_arrow_label)

        self.remove(vt_graph, ft_graph)

        static_vt = vt_axis.plot(v_func, x_range=[0, t_end], color=BLUE, stroke_width=3, use_smoothing=False)
        static_ft = ft_axis.plot(f_func, x_range=[t_accel_start, t_accel_end], color=RED, stroke_width=3, use_smoothing=False)
        self.add(static_vt, static_ft)
        self.wait(0.5)

        # -- 점선 그리기 --
        ft_dashline1 = DashedLine(ft_axis.c2p(t_accel_start, 0), ft_axis.c2p(t_accel_start, F_val), color=RED, stroke_width=2, dash_length=0.08)
        ft_dashline2 = DashedLine(ft_axis.c2p(t_accel_end, 0), ft_axis.c2p(t_accel_end, F_val),  color=RED, stroke_width=2, dash_length=0.08)
        ft_dashline_h = DashedLine(ft_axis.c2p(0, F_val), ft_axis.c2p(t_accel_start, F_val), color=RED, stroke_width=2, dash_length=0.08)
        vt_dashline = DashedLine(vt_axis.c2p(t_accel_start, 0), vt_axis.c2p(t_accel_start, v0), color=BLUE, stroke_width=2, dash_length=0.08)
        self.play(Create(ft_dashline1), Create(ft_dashline2), Create(ft_dashline_h), Create(vt_dashline))
        vt_dashline2 = DashedLine(vt_axis.c2p(t_accel_end, 0), vt_axis.c2p(t_accel_end, v_func(t_end)), color=BLUE, stroke_width=2, dash_length=0.08)
        self.play(Create(vt_dashline2))
        self.wait(1)

        x_end = ValueTracker(t_accel_start)

        # -- f-t그래프 면적 --
        area_ft = always_redraw(lambda:
            ft_axis.get_area( static_ft,
                x_range = [t_accel_start, x_end.get_value()],
                color = RED,
                opacity = 0.3
        ))

        # -- v-t그래프 위 움직이는 점 --
        vt_dot_static = Dot(vt_axis.c2p(t_accel_start, v_func(t_accel_start)), color=YELLOW)
        self.play(FadeIn(vt_dot_static))

        vt_dot = always_redraw(lambda:
            Dot(vt_axis.c2p(x_end.get_value(), v_func(x_end.get_value())), color=YELLOW)
            if x_end.get_value() <= t_accel_end else VMobject()
            )
        vt_dot_label = always_redraw(
            lambda: Text(f"v = {v_func(x_end.get_value()):.1f}", font_size=24, color=BLUE).next_to(vt_dot, RIGHT, buff=0.2).shift(UP * 0.3
            ) if x_end.get_value() <= t_accel_end else VMobject())

        self.add(area_ft, vt_dot, vt_dot_label)
        self.play(x_end.animate.set_value(t_accel_end), run_time=2, rate_func=linear)
        self.wait(0.5)

        계산식모음 = VGroup(
            MathTex(r"|\Delta v| = 4\,\text{m/s}", font_size=24),
            MathTex(r"m = 2\,\text{kg}", font_size=24),
            MathTex(r"|\Delta p| = m \Delta v = 2 \times 4 = 8\,\text{N·s}", font_size=24),
            MathTex(r"I = |\Delta p| = 8\,\text{N·s}", font_size=24),
        ).set_color(YELLOW).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        계산식모음.move_to(vt_axis.c2p(0.5, 5)).shift(RIGHT * 1.5)

        area_ft_label = MathTex(r"I = 8\,\text{N·s}", font_size=30, color=WHITE).move_to(area_ft.get_center())
        self.play(Write(area_ft_label))
        self.play(Write(계산식모음))
        self.wait(1)

        self.play(Indicate(area_ft_label, color=YELLOW, scale_factor=2))
        self.play(Indicate(계산식모음[-1], color=YELLOW, scale_factor=2))
        self.wait(1)

    def simulation_braking(self):
        #===================================#
        #==== 파트 2: 등속 운동하던 물체의 감속 ===#
        #===================================#

        # ── 물리 파라미터 ──
        mass = 2
        v0 = 4
        F_val = 4       # 절댓값으로 처리
        a_val = F_val / mass  # 2 m/s^2
        t_brake = 2
        t_stop = 4
        t_end = 5
        obj_size = 0.5
        time_tracker = ValueTracker(0)

        # ── 트랙 (상단) ──
        track = NumberLine(
            x_range=[0, 12, 1],
            length = 12,
            color = WHITE,
            stroke_width = 3,
            include_numbers=True,
            numbers_to_include = range(0, 13, 3),
            label_direction=DOWN,
            font_size=24
        )
        track.shift(UP * 1.5)

        # ── 물체 (상단) ──
        obj = Rectangle(
            width=obj_size, height=obj_size, color=BLUE, fill_opacity=0.8
        )
        obj_label = Text("2kg", font_size=18, color=WHITE)
        obj.move_to(track.n2p(0), 
            aligned_edge=DOWN).shift(UP * 0.1)
        obj_label.move_to(obj.get_center())
        
        # -- 마찰 구간 표시 (8-12m) ──
        braking_bar = Line(track.n2p(8), track.n2p(12), color=RED, stroke_width=5)

        braking_bar_label = Text("마찰 구간", font_size=24,color=RED)
        braking_bar_label.move_to(braking_bar.get_center()).shift(DOWN * 0.5)

        # ── F-t 그래프 (하단 왼쪽) ──
        ft_axis = Axes(
            x_range=[0, t_stop+1, 1], y_range=[0, F_val+1, 1],
            x_length=5, y_length=3,
            axis_config = {"include_tip": False},
            x_axis_config = {"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config = {"numbers_to_include": [4]}
        ).to_corner(DL, buff=0.8)
        ft_x_label = Text("t(s)", font_size=20).next_to(ft_axis.x_axis, RIGHT, buff=0.2)
        ft_y_label = Text("|F|(N)", font_size=20).next_to(ft_axis.y_axis, UP, buff=0.2)

        # ── v-t 그래프 (하단 오른쪽) ──

        vt_axis = Axes(
            x_range=[0, t_stop+1, 1], y_range=[0, v0+1, 1],
            x_length=5, y_length=3,
            axis_config = {"include_tip": False},
            x_axis_config = {"numbers_to_include": [1, 2, 3, 4, 5]},
            y_axis_config = {"numbers_to_include": [0, 2, 4]}
        ).to_corner(DR, buff=0.8).shift(LEFT * 1)
        vt_x_label = Text("t(s)", font_size=20).next_to(vt_axis.x_axis, RIGHT, buff=0.2)
        vt_y_label = Text("v(m/s)", font_size=20).next_to(vt_axis.y_axis, UP, buff=0.2)

        # ── 타이틀 ──
        title = VGroup(
            MathTex(r"v_0 = 4\text{m/s}", font_size=36, color=WHITE),
            Text(" 로 등속운동 하던 물체가 마찰 구간을 지나는 상황", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)

        self.play(Write(title))
        self.play(Create(track), FadeIn(obj), FadeIn(obj_label), FadeIn(braking_bar), Write(braking_bar_label))
        self.play(Create(ft_axis), Write(ft_x_label), Write(ft_y_label))
        self.play(Create(vt_axis), Write(vt_x_label), Write(vt_y_label))
        self.wait(1)

        # ── 위치 함수 ──
        def pos_func(t):
            if t <= t_brake:
                return v0 * t
            elif t <= t_stop:
                dt = t - t_brake
                return 8 + v0 * dt - 0.5 * a_val * dt ** 2
            else:
                return 12

        # ── 속도 함수 ──
        def v_func(t):
            if t <= t_brake:
                return v0
            elif t <= t_stop:
                return v0 - a_val * (t - t_brake)
            else:
                return 0

        # ── 힘 함수 ──
        def f_func(t):
            if t <= t_brake:
                return 0
            elif t < t_stop:
                return F_val
            else:
                return 0

        # updater 연결하기

        obj.add_updater(lambda m: m.move_to(track.n2p(pos_func(time_tracker.get_value())), aligned_edge=DOWN).shift(UP * 0.1))

        obj_label.add_updater(lambda m: m.move_to(obj))


        # ── 물체의 운동 애니메이션 ──
        vt_graph = always_redraw(lambda: vt_axis.plot(v_func,
        x_range=[0, max(time_tracker.get_value(), 0.01)], color=BLUE, stroke_width=3, use_smoothing=False))

        # F-t 그래프 그리기
        ft_graph = always_redraw(lambda:
            ft_axis.plot(
                lambda t: F_val,
                x_range=[t_brake, time_tracker.get_value()], color=RED, stroke_width=3)
                if time_tracker.get_value() > t_brake else VMobject()
            )

        # -- 힘 화살표 (마찰 구간에서만 표시, 운동 반대 방향) --
        force_arrow = always_redraw(lambda:
            Arrow(
                start=obj.get_left(), end=obj.get_left() + LEFT * 0.8,
                color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3
            ) if t_brake < time_tracker.get_value() <= t_stop else VMobject()
        )
        force_arrow_label = always_redraw(lambda:
            MathTex("F", font_size=28, color=RED).next_to(obj.get_left() + LEFT * 0.8, UP, buff=0.1)
            if t_brake < time_tracker.get_value() <= t_stop else VMobject()
        )

        self.add(vt_graph, ft_graph, force_arrow, force_arrow_label)

        self.play(time_tracker.animate.set_value(t_stop), run_time = t_stop, rate_func = linear)

        # 애니메이션 멈추고 그래프 고정하기
        obj.clear_updaters()
        obj_label.clear_updaters()
        self.remove(force_arrow, force_arrow_label)
        self.remove(vt_graph, ft_graph)

        static_vt = vt_axis.plot(v_func, x_range=[0, t_end], color=BLUE, stroke_width=3, use_smoothing=False)
        static_ft = ft_axis.plot(f_func, x_range=[t_brake+0.01, t_stop-0.01], color=RED, stroke_width=3, use_smoothing=False)
        self.add(static_vt, static_ft)
        self.wait(1)

        # 점선 그리기
        ft_dashline1 = DashedLine(ft_axis.c2p(t_brake, 0), ft_axis.c2p(t_brake, F_val), color=RED, stroke_width=2, dash_length=0.08)
        ft_dashline2 = DashedLine(ft_axis.c2p(t_stop, 0), ft_axis.c2p(t_stop, F_val),  color=RED, stroke_width=2, dash_length=0.08)
        ft_dashline_h = DashedLine(ft_axis.c2p(0, F_val), ft_axis.c2p(t_brake, F_val), color=RED, stroke_width=2, dash_length=0.08)
        vt_dashline = DashedLine(vt_axis.c2p(t_brake, 0), vt_axis.c2p(t_brake, v0), color=BLUE, stroke_width=2, dash_length=0.08)
        self.play(Create(ft_dashline1), Create(ft_dashline2), Create(ft_dashline_h), Create(vt_dashline))
        self.wait(1)

        x_end = ValueTracker(t_brake)

        # F-t그래프 면적 그리기
        area_ft = always_redraw(lambda: ft_axis.get_area(
            static_ft, x_range=[t_brake, x_end.get_value()], color=RED, opacity=0.3
        ) if x_end.get_value() > t_brake else VMobject() )

        # 정적 점 먼저 등장시키기
        vt_dot_static = Dot(vt_axis.c2p(t_brake, v_func(t_brake)), color=YELLOW)
        self.play(FadeIn(vt_dot_static))

        # v-t그래프 점 찍기
        vt_dot = always_redraw(
            lambda: Dot(vt_axis.c2p(x_end.get_value(), v_func(x_end.get_value())), color=YELLOW)
        if x_end.get_value() > t_brake else VMobject())

        vt_dot_label = always_redraw(
            lambda: Text(f"v = {v_func(x_end.get_value()):.1f}", font_size=24, color=BLUE).next_to(vt_dot, RIGHT, buff=0.2).shift(UP * 0.3
            ) if x_end.get_value() > t_brake else VMobject())

        self.add(area_ft, vt_dot, vt_dot_label)
        self.play(x_end.animate.set_value(t_stop), run_time = 2, rate_func=linear)
        self.wait(1)


        계산식모음 = VGroup(
            MathTex(r"|\Delta v| = 4[m/s]", font_size=24),
            MathTex(r"m = 2 [kg]", font_size=24),
            MathTex(r"|\Delta p| = m \Delta v = 2 \times 4 = 8[N \cdot s]", font_size=24),
            MathTex(r"I = |\Delta p| = 8[N \cdot s]", font_size=24)
        ).set_color(YELLOW).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(vt_axis.c2p(4, 4)).shift(RIGHT * 1)

        # 면적 계산식 라벨링
        area_ft_label = MathTex(r"I = 8[N \cdot s] ", font_size=30, color=WHITE).move_to(area_ft.get_center())
        self.play(Write(area_ft_label))
        self.play(Write(계산식모음))
        self.wait(1)

        # 충격량과 운동량 변화량 비교해 강조하기
        self.play(Indicate(area_ft_label, color=YELLOW, scale_factor=2))
        self.play(Indicate(계산식모음[-1], color=YELLOW, scale_factor=2))
        self.wait(1)

    def summary(self):
        title = Text("정리", font_size=48, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ① 정의
        step1 = VGroup(
            Text("① 충격량의 정의", font_size=28, color=WHITE),
            MathTex(r"I = F \cdot \Delta t", font_size=36, color=YELLOW),
        ).arrange(RIGHT, buff=0.5)

        # ② 관계식
        step2 = VGroup(
            Text("② 충격량과 운동량의 관계", font_size=28, color=WHITE),
            MathTex(r"I = \Delta p = m \Delta v", font_size=36, color=YELLOW),
        ).arrange(RIGHT, buff=0.5)

        # ③ 결론
        step3 = VGroup(
            Text("③ 결론", font_size=28, color=WHITE),
            Text("충격량 = 운동량의 변화량", font_size=32, color=YELLOW),
        ).arrange(RIGHT, buff=0.5)

        steps = VGroup(step1, step2, step3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        steps.next_to(title, DOWN, buff=0.8)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3))
            self.wait(1)

        # 전체 강조 박스
        box = SurroundingRectangle(steps, color=YELLOW, buff=0.3, corner_radius=0.1)
        self.play(Create(box))
        self.wait(2)

    def outro(self):
        title = Text("충격량과 운동량", font_size=80, color=WHITE)
        box = SurroundingRectangle(title, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Write(title), run_time=1.0)
        self.play(Write(box), run_time=1.0)
        self.wait(1)
