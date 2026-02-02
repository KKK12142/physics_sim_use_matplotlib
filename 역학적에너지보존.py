from manim import *
import numpy as np


class MechanicalEnergyConservation(Scene):
    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_potential_energy()
        self.clear_screen()
        self.phase2_freefall_energy()
        self.clear_screen()
        self.phase3_incline_energy()
        self.clear_screen()
        self.phase4_conservation_law()
        self.clear_screen()
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # =========================================================
    # Intro
    # =========================================================
    def intro(self):
        eq = MathTex("E", "=", "KE", "+", "PE", font_size=96, color=WHITE)
        eq.move_to(ORIGIN)
        self.play(Write(eq), run_time=2.0)
        box = SurroundingRectangle(eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.75)

        title = Text("역학적 에너지 보존", font_size=44, color=YELLOW)
        title.next_to(box, DOWN, buff=0.6)
        self.play(Write(title), run_time=1.0)

        subtitle = Text("에너지는 형태를 바꿀 뿐, 사라지지 않는다", font_size=28, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.5)

    # =========================================================
    # Phase 1: 위치에너지
    # =========================================================
    def phase1_potential_energy(self):
        title = Text("위치에너지", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 수식
        pe_eq = MathTex("PE", "=", "m", "g", "h", font_size=72)
        self.play(Write(pe_eq))
        self.wait(1)
        self.play(pe_eq.animate.scale(0.6).next_to(title, DOWN, buff=0.3))

        # 높이에 따른 PE 바 시각화
        g = 10  # m/s^2
        mass = 2  # kg

        # 기준면
        ground_y = -2.0
        ground = Line(LEFT * 3, RIGHT * 3, color=WHITE, stroke_width=3).move_to([0, ground_y, 0])
        ground_label = Text("기준면 (h=0)", font_size=18, color=GRAY).next_to(ground, DOWN, buff=0.1)
        self.play(Create(ground), Write(ground_label))

        # 높이 축
        h_axis = Arrow([0, ground_y, 0], [0, ground_y + 4.0, 0], color=WHITE, stroke_width=2, buff=0)
        h_label = Text("h", font_size=24, color=WHITE).next_to(h_axis, LEFT, buff=0.1)
        self.play(Create(h_axis), Write(h_label))

        # ValueTracker로 높이 변화
        h_tracker = ValueTracker(1.0)

        # 물체
        obj = always_redraw(lambda: Square(
            side_length=0.4, color=BLUE, fill_opacity=0.8,
        ).move_to([0, ground_y + h_tracker.get_value() * 0.6, 0]))

        h_line = always_redraw(lambda: DashedLine(
            [0.3, ground_y, 0],
            [0.3, ground_y + h_tracker.get_value() * 0.6, 0],
            color=GRAY, stroke_width=1.5, dash_length=0.08,
        ))

        h_val_label = always_redraw(lambda: MathTex(
            f"h = {h_tracker.get_value():.1f}" + r"\,\text{m}",
            font_size=20, color=WHITE,
        ).next_to(h_line, RIGHT, buff=0.1))

        # PE 바
        bar_x = 3.5
        bar_base_y = ground_y
        pe_max_height = 3.0
        h_max = 5.0

        pe_bar = always_redraw(lambda: Rectangle(
            width=0.8,
            height=max(h_tracker.get_value() / h_max * pe_max_height, 0.02),
            color=BLUE, fill_opacity=0.7,
        ).move_to([bar_x, bar_base_y + max(h_tracker.get_value() / h_max * pe_max_height, 0.02) / 2, 0]))

        pe_val = always_redraw(lambda: MathTex(
            f"PE = {mass * g * h_tracker.get_value():.0f}" + r"\,\text{J}",
            font_size=22, color=BLUE,
        ).next_to(pe_bar, UP, buff=0.1))

        pe_label = Text("PE", font_size=20, color=BLUE).move_to([bar_x, ground_y - 0.3, 0])

        self.play(
            FadeIn(obj), Create(h_line), Write(h_val_label),
            FadeIn(pe_bar), Write(pe_val), Write(pe_label),
        )
        self.wait(0.5)

        # 높이 변화 애니메이션
        for target_h in [3.0, 5.0, 2.0, 0.5]:
            self.play(h_tracker.animate.set_value(target_h), run_time=1.5)
            self.wait(0.5)

        self.wait(1)

    # =========================================================
    # Phase 2: 자유낙하 에너지 전환
    # =========================================================
    def phase2_freefall_energy(self):
        title = VGroup(
            Text("자유낙하 에너지 전환:", font_size=28, color=WHITE),
            MathTex(r"m=2\text{kg},\;h=5\text{m}", font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        self.play(Write(title))

        # 물리 파라미터
        mass = 2
        g = 10
        h0 = 5.0
        v_final = np.sqrt(2 * g * h0)  # = 10 m/s
        t_fall = np.sqrt(2 * h0 / g)   # = 1 s
        total_E = mass * g * h0         # = 100 J

        # 좌측: 물체 + 높이 표시
        ground_y = -2.5
        top_y = ground_y + 4.0  # 높이 5m → 4 화면 단위
        h_scale = (top_y - ground_y) / h0

        ground = Line(LEFT * 3.5 + RIGHT * 0, RIGHT * 0, color=WHITE, stroke_width=3)
        ground.move_to([-2.5, ground_y, 0])
        ground_label = Text("h = 0", font_size=16, color=GRAY).next_to(ground, DOWN, buff=0.1)

        # 높이 눈금
        h_ticks = VGroup()
        for i in range(6):
            y = ground_y + i * h_scale
            tick = Line(LEFT * 0.1, RIGHT * 0.1, color=WHITE, stroke_width=1.5)
            tick.move_to([-4.0, y, 0])
            h_ticks.add(tick)
            if i > 0:
                lbl = Text(f"{i}m", font_size=14, color=GRAY).next_to(tick, LEFT, buff=0.1)
                h_ticks.add(lbl)

        self.play(Create(ground), Write(ground_label), FadeIn(h_ticks))

        # ValueTracker
        t_tracker = ValueTracker(0)

        def current_h(t):
            h = h0 - 0.5 * g * t**2
            return max(h, 0)

        def current_v(t):
            return min(g * t, v_final)

        def current_pe(t):
            return mass * g * current_h(t)

        def current_ke(t):
            return 0.5 * mass * current_v(t)**2

        # 물체
        obj = always_redraw(lambda: Circle(
            radius=0.2, color=ORANGE, fill_opacity=0.8,
        ).move_to([-2.5, ground_y + current_h(t_tracker.get_value()) * h_scale, 0]))

        # 높이 점선
        h_dash = always_redraw(lambda: DashedLine(
            [-2.0, ground_y, 0],
            [-2.0, ground_y + current_h(t_tracker.get_value()) * h_scale, 0],
            color=GRAY, stroke_width=1.5, dash_length=0.08,
        ) if current_h(t_tracker.get_value()) > 0.1 else VMobject())

        h_val = always_redraw(lambda: MathTex(
            f"h={current_h(t_tracker.get_value()):.1f}" + r"\text{m}",
            font_size=18, color=WHITE,
        ).next_to([-1.8, ground_y + current_h(t_tracker.get_value()) * h_scale / 2, 0], RIGHT, buff=0.1))

        v_val = always_redraw(lambda: MathTex(
            f"v={current_v(t_tracker.get_value()):.1f}" + r"\text{m/s}",
            font_size=18, color=BLUE,
        ).next_to(obj, RIGHT, buff=0.3))

        self.play(FadeIn(obj), Create(h_dash), Write(h_val), Write(v_val))

        # 중앙: 에너지 스택 바
        bar_x = 1.5
        bar_width = 1.2
        bar_total_height = 3.5

        # PE 바 (하단부터)
        pe_bar = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=max(current_pe(t_tracker.get_value()) / total_E * bar_total_height, 0.02),
            color=BLUE, fill_opacity=0.7,
        ).move_to([bar_x, ground_y + max(current_pe(t_tracker.get_value()) / total_E * bar_total_height, 0.02) / 2, 0]))

        # KE 바 (PE 위에 쌓기)
        ke_bar = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=max(current_ke(t_tracker.get_value()) / total_E * bar_total_height, 0.02),
            color=ORANGE, fill_opacity=0.7,
        ).move_to([
            bar_x,
            ground_y + current_pe(t_tracker.get_value()) / total_E * bar_total_height
            + max(current_ke(t_tracker.get_value()) / total_E * bar_total_height, 0.02) / 2,
            0
        ]))

        # 총 에너지 점선
        total_line = DashedLine(
            [bar_x - bar_width, ground_y + bar_total_height, 0],
            [bar_x + bar_width, ground_y + bar_total_height, 0],
            color=YELLOW, stroke_width=2, dash_length=0.1,
        )
        total_label = MathTex(r"E_{total}=100\text{J}", font_size=18, color=YELLOW)
        total_label.next_to(total_line, UP, buff=0.1)

        pe_text = always_redraw(lambda: MathTex(
            f"PE={current_pe(t_tracker.get_value()):.0f}J",
            font_size=16, color=BLUE,
        ).move_to(pe_bar))

        ke_text = always_redraw(lambda: MathTex(
            f"KE={current_ke(t_tracker.get_value()):.0f}J",
            font_size=16, color=ORANGE,
        ).move_to(ke_bar))

        bar_label_pe = Text("PE", font_size=16, color=BLUE).move_to([bar_x - 0.3, ground_y - 0.3, 0])
        bar_label_ke = Text("KE", font_size=16, color=ORANGE).move_to([bar_x + 0.3, ground_y - 0.3, 0])

        self.play(
            FadeIn(pe_bar), FadeIn(ke_bar),
            Create(total_line), Write(total_label),
            Write(pe_text), Write(ke_text),
            Write(bar_label_pe), Write(bar_label_ke),
        )

        # 우측: h-t 그래프
        ht_axes = Axes(
            x_range=[0, 1.2, 0.2], y_range=[0, 6, 1],
            x_length=3.5, y_length=3.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0.5, 1.0]},
            y_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
        ).move_to([5.0, -0.5, 0])
        ht_x_label = Text("t (s)", font_size=18).next_to(ht_axes.x_axis, RIGHT, buff=0.15)
        ht_y_label = Text("h (m)", font_size=18).next_to(ht_axes.y_axis, UP, buff=0.15)
        self.play(Create(ht_axes), Write(ht_x_label), Write(ht_y_label))

        ht_line = always_redraw(lambda: ht_axes.plot(
            lambda t: max(h0 - 0.5 * g * t**2, 0),
            x_range=[0, max(min(t_tracker.get_value(), t_fall), 0.02)],
            color=GREEN, stroke_width=3,
        ) if t_tracker.get_value() > 0.01 else VMobject())
        self.add(ht_line)

        self.wait(0.5)

        # 낙하 애니메이션
        self.play(
            t_tracker.animate.set_value(t_fall),
            run_time=3, rate_func=rate_functions.ease_in_quad,
        )
        self.wait(1)

        # 수식 검증
        verify = MathTex(
            r"mgh = \frac{1}{2}mv^2 \;\Rightarrow\; v = \sqrt{2gh} = \sqrt{2 \times 10 \times 5} = 10\,\text{m/s}",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        bg = BackgroundRectangle(verify, color=BLACK, fill_opacity=0.85, buff=0.2)
        self.play(FadeIn(bg), Write(verify))
        self.wait(2)

    # =========================================================
    # Phase 3: 경사면 에너지 전환
    # =========================================================
    def phase3_incline_energy(self):
        title = VGroup(
            Text("경사면 에너지 전환:", font_size=28, color=WHITE),
            Text("θ=30°, h=5m, 마찰 없음", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.2).to_edge(UP)
        self.play(Write(title))

        # 물리 파라미터
        mass = 2
        g = 10
        h0 = 5.0
        angle_deg = 30
        angle_rad = np.radians(angle_deg)
        slope_len = h0 / np.sin(angle_rad)  # 10 m
        a_slope = g * np.sin(angle_rad)     # 5 m/s^2
        v_final = np.sqrt(2 * g * h0)       # 10 m/s
        t_slope = v_final / a_slope          # 2 s
        total_E = mass * g * h0             # 100 J

        # 경사면 그리기 (좌측)
        incline_base = [-5.5, -2.5, 0]
        incline_width = 5.0
        incline_height = incline_width * np.tan(angle_rad)

        incline_bottom_right = [incline_base[0] + incline_width, incline_base[1], 0]
        incline_top = [incline_base[0], incline_base[1] + incline_height, 0]

        incline = Polygon(
            incline_base, incline_bottom_right, incline_top,
            color=WHITE, fill_opacity=0.1, stroke_width=2,
        )

        # 수평면
        flat_line = Line(
            incline_bottom_right,
            [incline_bottom_right[0] + 3.0, incline_bottom_right[1], 0],
            color=WHITE, stroke_width=2,
        )

        self.play(Create(incline), Create(flat_line))

        # 높이 표시
        h_arrow = DoubleArrow(
            [incline_base[0] - 0.3, incline_base[1], 0],
            [incline_base[0] - 0.3, incline_top[1], 0],
            color=GRAY, stroke_width=2, buff=0,
        )
        h_label = MathTex(r"h=5\text{m}", font_size=20, color=GRAY).next_to(h_arrow, LEFT, buff=0.1)
        self.play(Create(h_arrow), Write(h_label))

        # ValueTracker: 경사면 위 거리 (0 ~ slope_len)
        s_tracker = ValueTracker(0)

        def current_s(val):
            return min(val, slope_len)

        def current_h_from_s(s):
            if s >= slope_len:
                return 0
            return h0 - s * np.sin(angle_rad)

        def current_v_from_s(s):
            h = current_h_from_s(s)
            return np.sqrt(max(2 * g * (h0 - h), 0))

        # 경사면 위 물체 위치
        slope_dir = np.array([np.cos(angle_rad), -np.sin(angle_rad), 0])  # 경사면 아래 방향
        start_pos = np.array(incline_top) + slope_dir * 0.0

        obj = always_redraw(lambda: Square(
            side_length=0.35, color=BLUE, fill_opacity=0.8,
        ).move_to(
            np.array(incline_top) + slope_dir * min(s_tracker.get_value() / slope_len * incline_width / np.cos(angle_rad), incline_width / np.cos(angle_rad))
            + np.array([0, 0.25, 0])
            if s_tracker.get_value() < slope_len
            else np.array(incline_bottom_right)
            + np.array([(s_tracker.get_value() - slope_len) / slope_len * 3.0, 0.25, 0])
        ))

        self.play(FadeIn(obj))

        # 우측: 에너지 스택 바
        bar_x = 4.5
        bar_width = 1.0
        bar_total_height = 3.0
        ground_y = incline_base[1]

        pe_bar = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=max(current_h_from_s(s_tracker.get_value()) / h0 * bar_total_height, 0.02),
            color=BLUE, fill_opacity=0.7,
        ).move_to([
            bar_x,
            ground_y + max(current_h_from_s(s_tracker.get_value()) / h0 * bar_total_height, 0.02) / 2,
            0
        ]))

        ke_height_func = lambda: max((1 - current_h_from_s(s_tracker.get_value()) / h0) * bar_total_height, 0.02)
        ke_bar = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=ke_height_func(),
            color=ORANGE, fill_opacity=0.7,
        ).move_to([
            bar_x,
            ground_y + current_h_from_s(s_tracker.get_value()) / h0 * bar_total_height + ke_height_func() / 2,
            0
        ]))

        total_line = DashedLine(
            [bar_x - bar_width, ground_y + bar_total_height, 0],
            [bar_x + bar_width, ground_y + bar_total_height, 0],
            color=YELLOW, stroke_width=2, dash_length=0.1,
        )
        total_label = MathTex(r"E=100\text{J}", font_size=18, color=YELLOW).next_to(total_line, UP, buff=0.1)

        pe_text = always_redraw(lambda: MathTex(
            f"PE={mass * g * current_h_from_s(s_tracker.get_value()):.0f}",
            font_size=16, color=BLUE,
        ).move_to(pe_bar))

        ke_text = always_redraw(lambda: MathTex(
            f"KE={total_E - mass * g * current_h_from_s(s_tracker.get_value()):.0f}",
            font_size=16, color=ORANGE,
        ).move_to(ke_bar))

        self.play(
            FadeIn(pe_bar), FadeIn(ke_bar),
            Create(total_line), Write(total_label),
            Write(pe_text), Write(ke_text),
        )
        self.wait(0.5)

        # 경사면 내려가기
        self.play(
            s_tracker.animate.set_value(slope_len),
            run_time=3, rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.5)

        # 수평면 등속 이동
        self.play(
            s_tracker.animate.set_value(slope_len + 5),
            run_time=2, rate_func=linear,
        )
        self.wait(0.5)

        # 핵심: 같은 높이 → 같은 속도
        key_msg = MathTex(
            r"v = \sqrt{2gh} = 10\,\text{m/s}",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        bg = BackgroundRectangle(key_msg, color=BLACK, fill_opacity=0.85, buff=0.2)
        self.play(FadeIn(bg), Write(key_msg))
        self.wait(2)

    # =========================================================
    # Phase 4: 역학적 에너지 보존 법칙
    # =========================================================
    def phase4_conservation_law(self):
        title = Text("역학적 에너지 보존 법칙", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 비교: 자유낙하 vs 경사면
        compare_title = Text("자유낙하 vs 경사면 (같은 높이 h=5m)", font_size=24, color=YELLOW)
        compare_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(compare_title))

        # 자유낙하 결과
        freefall = VGroup(
            Text("자유낙하", font_size=22, color=ORANGE),
            MathTex(r"h = 5\,\text{m}", font_size=20),
            MathTex(r"v = \sqrt{2 \times 10 \times 5} = 10\,\text{m/s}", font_size=20, color=BLUE),
        )
        freefall.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        freefall.move_to(LEFT * 3 + UP * 0.3)

        # 경사면 결과
        incline = VGroup(
            Text("경사면 (30°)", font_size=22, color=ORANGE),
            MathTex(r"h = 5\,\text{m}", font_size=20),
            MathTex(r"v = \sqrt{2 \times 10 \times 5} = 10\,\text{m/s}", font_size=20, color=BLUE),
        )
        incline.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        incline.move_to(RIGHT * 3 + UP * 0.3)

        # 등호
        eq_sign = MathTex(r"=", font_size=48, color=YELLOW).move_to(UP * 0.3)

        for v in freefall:
            self.play(Write(v), run_time=0.5)
        self.play(Write(eq_sign))
        for v in incline:
            self.play(Write(v), run_time=0.5)
        self.wait(1)

        # 핵심 수식
        conservation_eq = MathTex(
            "E", "=", "KE", "+", "PE", "=", r"\text{const}",
            font_size=56, color=YELLOW,
        ).shift(DOWN * 1.2)
        conservation_box = SurroundingRectangle(
            conservation_eq, color=YELLOW, buff=0.3, corner_radius=0.1, stroke_width=3,
        )
        condition = Text("(외력 · 마찰 없을 때)", font_size=22, color=GRAY)
        condition.next_to(conservation_box, DOWN, buff=0.2)

        self.play(Write(conservation_eq), Create(conservation_box))
        self.play(Write(condition))
        self.wait(1.5)

        # 마찰 있는 경우
        friction_note = VGroup(
            Text("마찰이 있다면?", font_size=22, color=RED),
            Text("역학적 에너지 ↓ → 열에너지로 전환", font_size=20, color=RED),
            VGroup(
                MathTex(r"W_{\text{non-cons}}", font_size=22, color=RED),
                MathTex(r"= \Delta E_{\text{mech}}", font_size=22, color=RED),
            ).arrange(RIGHT, buff=0.1),
        )
        friction_note.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        friction_note.to_edge(DOWN, buff=0.4)

        for f in friction_note:
            self.play(Write(f), run_time=0.6)
        self.wait(2)

    # =========================================================
    # Outro
    # =========================================================
    def outro(self):
        final_eq = MathTex(
            "KE", "+", "PE", "=", r"\text{const}",
            font_size=80, color=WHITE,
        )
        final_eq.move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4, corner_radius=0.15, stroke_width=4)
        subtitle = Text("역학적 에너지 보존", font_size=40, color=YELLOW)
        subtitle.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.0)

        points = VGroup(
            Text("• 역학적 에너지 = 운동에너지 + 위치에너지", font_size=24, color=WHITE),
            Text("• 비보존력이 없으면 역학적 에너지는 보존된다", font_size=24, color=WHITE),
            Text("• 경로에 무관: 같은 높이 변화 → 같은 속도", font_size=24, color=WHITE),
        )
        points.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        points.next_to(subtitle, DOWN, buff=0.5)
        self.play(FadeIn(points), run_time=1.0)
        self.wait(2)

        # 1편 연결
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

        connection = VGroup(
            Text("1편 연결", font_size=28, color=GRAY),
            MathTex(r"W = \Delta KE", font_size=40, color=WHITE),
            Text("일 = 에너지의 전환", font_size=32, color=YELLOW),
        )
        connection.arrange(DOWN, buff=0.4)
        connection.move_to(ORIGIN)

        for c in connection:
            self.play(Write(c), run_time=0.75)
        self.wait(3)
