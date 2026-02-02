from manim import *
import numpy as np


class MomentumConservation(Scene):
    # ── 폰트 크기 ──
    FONT_TITLE = 80
    FONT_SUBTITLE = 28
    FONT_LABEL = 20
    FONT_AXIS_LABEL = 16
    FONT_AXIS_NUM = 20
    FONT_CALC = 36
    FONT_CALC_RESULT = 40
    FONT_FORMULA = 28

    # ── 공통 상수 ──
    TRACK_Y = 1.5
    OBJ_SIZE_SMALL = 0.45
    OBJ_SIZE_MEDIUM = 0.55
    OBJ_SIZE_LARGE = 0.65
    SCALE_V = 0.5
    REAL_PER_SIM = 0.8
    SIM_TOTAL = 6.0
    BAR_SCALE = 0.5
    BAR_WIDTH = 0.6

    def construct(self):
        self.intro()
        self.clear_screen()
        self.phase1_momentum_concept()
        self.clear_screen()
        self.phase2_equal_mass_collision()
        self.clear_screen()
        self.phase3_different_mass_collision()
        self.clear_screen()
        self.phase4_three_body_collision()
        self.clear_screen()
        self.phase5_inelastic_collision()
        self.clear_screen()
        self.summary()
        self.clear_screen()
        self.outro()

    def clear_screen(self):
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)

    # ═══════════ 헬퍼 메서드 ═══════════

    def _make_track(self, y_pos=None):
        """트랙 라인 + 눈금 + 라벨 생성 → dict 반환"""
        if y_pos is None:
            y_pos = self.TRACK_Y
        track = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        track.shift(UP * y_pos)
        tick_marks = VGroup()
        tick_labels = VGroup()
        for i in range(13):
            val = i - 6
            x_pos = -6 + 12 * (i / 12)
            tick = Line(UP * 0.1, DOWN * 0.1, color=WHITE, stroke_width=2)
            tick.move_to([x_pos, track.get_center()[1], 0])
            tick_marks.add(tick)
            if i % 3 == 0:
                label = Text(str(val), font_size=self.FONT_AXIS_LABEL, color=GRAY)
                label.next_to(tick, DOWN, buff=0.15)
                tick_labels.add(label)
        return {"track": track, "ticks": tick_marks, "labels": tick_labels}

    def _make_pt_axes(self, y_range, y_numbers, x_length=5, y_length=3):
        """p-t 그래프 축 생성 → dict 반환"""
        axes = Axes(
            x_range=[0, self.SIM_TOTAL, 1], y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": list(range(1, int(self.SIM_TOTAL) + 1))},
            y_axis_config={"numbers_to_include": y_numbers},
        )
        axes.to_corner(DL, buff=0.8)
        x_lab = Text("t (s)", font_size=self.FONT_AXIS_LABEL + 2).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex("p", font_size=24).next_to(axes.y_axis, UP, buff=0.15)
        return {"axes": axes, "x_lab": x_lab, "y_lab": y_lab}

    def _make_momentum_bars(self, values, colors, labels, bar_origin=None, bar_scale=None):
        """운동량 막대 차트 → dict 반환"""
        if bar_origin is None:
            bar_origin = RIGHT * 3.5 + DOWN * 2.5
        if bar_scale is None:
            bar_scale = self.BAR_SCALE
        bars = VGroup()
        for val, col in zip(values, colors):
            h = max(abs(val) * bar_scale, 0.05)
            bar = Rectangle(width=self.BAR_WIDTH, height=h, color=col, fill_opacity=0.7)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        bars.move_to(bar_origin)
        bars.align_to(bar_origin + DOWN * 0.5, DOWN)

        bar_labels = VGroup()
        for i, lbl_tex in enumerate(labels):
            lbl = MathTex(lbl_tex, font_size=22, color=colors[i])
            lbl.next_to(bars[i], DOWN, buff=0.15)
            bar_labels.add(lbl)

        # 타이틀은 bar_origin 기준 고정 위치 (스케일 변화에 무관)
        bar_title = Text("운동량", font_size=self.FONT_LABEL, color=WHITE)
        bar_title.move_to([bar_origin[0], bar_origin[1] + 2.0, 0]).shift(UP*1)

        val_labels = VGroup()
        for i, val in enumerate(values):
            vl = MathTex(str(int(val)) if val == int(val) else f"{val:.1f}",
                         font_size=24, color=WHITE)
            vl.next_to(bars[i], UP, buff=0.05)
            val_labels.add(vl)

        return {"bars": bars, "bar_labels": bar_labels, "bar_title": bar_title,
                "val_labels": val_labels, "bar_scale": bar_scale}

    def _make_object(self, x, y, size, color, label_text, mass_text):
        """충돌 물체 + 라벨 + 질량표시 → dict 반환"""
        box = Square(side_length=size, color=color, fill_opacity=0.8)
        box.move_to([x, y + size / 2 + 0.1, 0])
        label = Text(label_text, font_size=self.FONT_LABEL - 4, color=WHITE).move_to(box)
        mass = MathTex(mass_text, font_size=18, color=color).next_to(box, UP, buff=0.1)
        return {"box": box, "label": label, "mass": mass}

    def _smooth_step(self, t, t0, width=0.15):
        """시그모이드 기반 부드러운 전환"""
        return 1 / (1 + np.exp(-(t - t0) / (width / 4)))

    def _collision_effect(self, point, box_a, box_b, extra_anims=None):
        """충돌 순간 효과: Flash + squash + 색 번쩍임"""
        anims = [Flash(point, color=YELLOW, flash_radius=0.5, line_length=0.3)]
        if extra_anims:
            anims.extend(extra_anims)
        self.play(*anims, run_time=0.3)
        self.play(
            box_a.animate.scale([1.15, 0.85, 1]),
            box_b.animate.scale([1.15, 0.85, 1]),
            run_time=0.1, rate_func=there_and_back
        )

    def _setup_object_updaters(self, obj_dict, pos_func, time_tracker, y_pos):
        """물체, 라벨, 질량에 updater 부착"""
        obj_dict["box"].add_updater(
            lambda m, pf=pos_func: m.move_to([pf(time_tracker.get_value()), y_pos, 0]))
        obj_dict["label"].add_updater(lambda m: m.move_to(obj_dict["box"]))
        obj_dict["mass"].add_updater(lambda m: m.next_to(obj_dict["box"], UP, buff=0.1))

    def _clear_object_updaters(self, *obj_dicts):
        """여러 물체 dict에서 updater 일괄 해제"""
        for d in obj_dicts:
            d["box"].clear_updaters()
            d["label"].clear_updaters()
            d["mass"].clear_updaters()

    def _update_bars(self, bar_data, new_values, colors):
        """막대 차트를 새 값으로 Transform"""
        scale = bar_data.get("bar_scale", self.BAR_SCALE)
        anims = []
        for i, (val, col) in enumerate(zip(new_values, colors)):
            h = max(abs(val) * scale, 0.05)
            new_bar = Rectangle(width=self.BAR_WIDTH, height=h, color=col, fill_opacity=0.7)
            new_bar.move_to(bar_data["bars"][i].get_bottom(), aligned_edge=DOWN)
            anims.append(Transform(bar_data["bars"][i], new_bar))
            val_str = str(int(val)) if val == int(val) else f"{val:.1f}"
            new_vl = MathTex(val_str, font_size=24, color=WHITE)
            new_vl.next_to(new_bar, UP, buff=0.05)
            anims.append(Transform(bar_data["val_labels"][i], new_vl))
        return anims

    def _make_vel_arrow_and_label(self, box, velocity, color, arrow_scale=0.15):
        """속도에 비례하는 화살표 + 라벨을 생성하는 always_redraw용 VGroup 반환"""
        vel_abs = abs(velocity)
        if vel_abs < 0.01:
            lbl = MathTex(f"v=0", font_size=16, color=color)
            lbl.next_to(box, RIGHT, buff=0.15)
            return VGroup(lbl)
        arrow_len = vel_abs * arrow_scale
        arrow_len = max(arrow_len, 0.25)
        if velocity > 0:
            arrow = Arrow(
                start=box.get_right(), end=box.get_right() + RIGHT * arrow_len,
                color=color, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            vel_str = f"{velocity:.1f}" if velocity != int(velocity) else f"{int(velocity)}"
            lbl = MathTex(f"v={vel_str}", font_size=16, color=color)
            lbl.next_to(arrow, UP, buff=0.05)
            return VGroup(arrow, lbl)
        else:
            arrow = Arrow(
                start=box.get_left(), end=box.get_left() + LEFT * arrow_len,
                color=color, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            vel_str = f"{velocity:.1f}" if velocity != int(velocity) else f"{int(velocity)}"
            lbl = MathTex(f"v={vel_str}", font_size=16, color=color)
            lbl.next_to(arrow, UP, buff=0.05)
            return VGroup(arrow, lbl)

    # ═══════════ Phase 0: Intro ═══════════

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

        subtitle = Text("외력이 없으면 총 운동량은 변하지 않는다",
                         font_size=self.FONT_SUBTITLE, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(1.5)

    # ═══════════ Phase 1: 운동량 개념 ═══════════

    def phase1_momentum_concept(self):
        # ── 1. 타이틀 ──
        title = Text("운동량이란?", font_size=40, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ── 2. 두 트랙 ──
        TRACK_A_Y = 1.5
        TRACK_B_Y = -0.2
        track_a = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3).shift(UP * TRACK_A_Y)
        track_b = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3).shift(UP * TRACK_B_Y)

        # ── 3. 물체 ──
        obj_a_size = self.OBJ_SIZE_SMALL
        obj_b_size = self.OBJ_SIZE_LARGE
        obj_a = Square(side_length=obj_a_size, color=BLUE, fill_opacity=0.8)
        obj_a.move_to([-5, TRACK_A_Y + obj_a_size / 2 + 0.1, 0])
        obj_b = Square(side_length=obj_b_size, color=RED, fill_opacity=0.8)
        obj_b.move_to([-5, TRACK_B_Y + obj_b_size / 2 + 0.1, 0])

        mass_a = MathTex("1\\,\\text{kg}", font_size=self.FONT_LABEL, color=BLUE).next_to(obj_a, UP, buff=0.1)
        mass_b = MathTex("3\\,\\text{kg}", font_size=self.FONT_LABEL, color=RED).next_to(obj_b, UP, buff=0.1)
        obj_a_label = Text("A", font_size=self.FONT_LABEL, color=WHITE).move_to(obj_a)
        obj_b_label = Text("B", font_size=self.FONT_LABEL, color=WHITE).move_to(obj_b)

        self.play(Create(track_a), Create(track_b), run_time=0.75)

        # ── 4. 속도 화살표 ──
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

        same_v_text = Text("두 물체가 3m/s의 동일한 속력으로 움직인다.",
                           font_size=24, color=WHITE)
        same_v_text.move_to(RIGHT * 3 + UP * 0.6)
        self.play(Write(same_v_text), run_time=0.5)
        self.wait(0.5)

        # ── 5. 이동 ──
        self.play(
            obj_a.animate.shift(RIGHT * 5),
            obj_b.animate.shift(RIGHT * 5),
            run_time=3, rate_func=linear
        )
        self.wait(0.5)

        # ── 6. 운동량 비교 ──
        self.play(FadeOut(same_v_text), run_time=0.3)

        but_text = Text("하지만 운동량은?", font_size=self.FONT_SUBTITLE, color=YELLOW)
        but_text.move_to(RIGHT * 3 + UP * 0.6)
        self.play(Write(but_text), run_time=0.75)

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
        p_a_label = MathTex(r"p=3\,\text{kg}\!\cdot\!\text{m/s}", font_size=18, color=PURPLE)
        p_a_label.next_to(p_a, UP, buff=0.05).shift(RIGHT * 0.45)
        p_b_label = MathTex(r"p=9\,\text{kg}\!\cdot\!\text{m/s}", font_size=18, color=PURPLE)
        p_b_label.next_to(p_b, UP, buff=0.05)

        self.play(FadeIn(p_a), FadeIn(p_b), Write(p_a_label), Write(p_b_label), run_time=1.0)
        self.wait(0.5)

        # ── 7. 수식 정리 ──
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

    # ═══════════ Phase 2: 같은 질량 완전 탄성 충돌 ═══════════

    def phase2_equal_mass_collision(self):
        # ── 1. 타이틀 ──
        title = VGroup(
            Text("실험 A: 같은 질량 완전 탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m = 1\text{kg},\; v_A = 4\text{m/s},\; v_B = 0)", font_size=self.FONT_SUBTITLE, color=WHITE)
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ── 2. 트랙 ──
        track_data = self._make_track()
        self.play(Create(track_data["track"]), run_time=0.5)
        self.play(Create(track_data["ticks"]), Write(track_data["labels"]), run_time=0.5)
        center_y = track_data["track"].get_center()[1]

        # ── 3. p-t 그래프 ──
        pt_data = self._make_pt_axes(y_range=[-1, 6, 1], y_numbers=[0, 2, 4])
        axes_pt = pt_data["axes"]
        self.play(Create(axes_pt), Write(pt_data["x_lab"]), Write(pt_data["y_lab"]), run_time=0.75)

        # ── 4. 운동량 막대 ──
        bar_data = self._make_momentum_bars(
            values=[4, 0, 4], colors=[BLUE, RED, YELLOW],
            labels=["p_A", "p_B", "p_{tot}"], bar_scale=0.35)
        self.play(
            FadeIn(bar_data["bars"]), Write(bar_data["bar_labels"]),
            Write(bar_data["bar_title"]), Write(bar_data["val_labels"]),
            run_time=0.75
        )

        # ── 5. 물체 ──
        START_A_X, START_B_X = -4.0, 0.0
        obj_a = self._make_object(START_A_X, center_y, self.OBJ_SIZE_SMALL, BLUE, "A", "1\\,\\text{kg}")
        obj_b = self._make_object(START_B_X, center_y, self.OBJ_SIZE_SMALL, RED, "B", "1\\,\\text{kg}")
        vel_arrow = Arrow(
            start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        TRACK_BOTTOM_Y = center_y - 0.15
        vel_label = MathTex("v=4", font_size=20, color=BLUE)
        vel_label.move_to([obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        self.play(
            FadeIn(obj_a["box"]), FadeIn(obj_b["box"]),
            Write(obj_a["label"]), Write(obj_b["label"]),
            Write(obj_a["mass"]), Write(obj_b["mass"]),
            Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # ── 6. 충돌 시뮬레이션 ──
        V_A, V_B = 4.0, 0.0
        V_A_AFTER, V_B_AFTER = 0.0, 4.0
        obj_size = self.OBJ_SIZE_SMALL

        dist = (START_B_X - obj_size / 2) - (START_A_X + obj_size / 2)
        collision_t = dist / (V_A * self.SCALE_V)
        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return START_A_X + V_A * self.SCALE_V * t
            return START_A_X + V_A * self.SCALE_V * collision_t + V_A_AFTER * self.SCALE_V * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return START_B_X
            return START_B_X + V_B_AFTER * self.SCALE_V * (t - collision_t)

        y_a = center_y + obj_size / 2 + 0.1
        self._setup_object_updaters(obj_a, pos_a, time_tracker, y_a)
        self._setup_object_updaters(obj_b, pos_b, time_tracker, y_a)

        vel_arrow_dyn = always_redraw(lambda: Arrow(
            start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() < collision_t else VMobject())
        vel_label_a_dyn = always_redraw(lambda: MathTex(
            "v=4", font_size=20, color=BLUE
        ).move_to([obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        if time_tracker.get_value() < collision_t else VMobject())

        vel_arrow_b_dyn = always_redraw(lambda: Arrow(
            start=obj_b["box"].get_right(), end=obj_b["box"].get_right() + RIGHT * 0.8,
            color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() > collision_t + 0.2 else VMobject())
        vel_label_b_dyn = always_redraw(lambda: MathTex(
            "v=4", font_size=20, color=RED
        ).move_to([obj_b["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        if time_tracker.get_value() > collision_t + 0.2 else VMobject())

        self.remove(vel_arrow)
        self.add(vel_arrow_dyn, vel_label_a_dyn, vel_arrow_b_dyn, vel_label_b_dyn)

        # p-t 그래프
        def p_a_func(t):
            s = self._smooth_step(t, collision_t)
            return 4 * (1 - s)

        def p_b_func(t):
            s = self._smooth_step(t, collision_t)
            return 4 * s

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 4, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전 이동
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t),
                  run_time=collision_t * self.REAL_PER_SIM, rate_func=linear)

        # 충돌 효과 + 막대 업데이트
        collision_point = obj_a["box"].get_right()
        bar_anims = self._update_bars(bar_data, [0, 4, 4], [BLUE, RED, YELLOW])
        self._collision_effect(collision_point, obj_a["box"], obj_b["box"], bar_anims)

        # 충돌 후
        self.play(time_tracker.animate.set_value(self.SIM_TOTAL),
                  run_time=(self.SIM_TOTAL - collision_t) * self.REAL_PER_SIM, rate_func=linear)

        # 정리
        self._clear_object_updaters(obj_a, obj_b)
        self.remove(vel_arrow_dyn, vel_label_a_dyn, vel_arrow_b_dyn, vel_label_b_dyn,
                    pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, self.SIM_TOTAL], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, self.SIM_TOTAL], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 4, x_range=[0, self.SIM_TOTAL],
                                    color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=self.FONT_LABEL, color=BLUE)
        pt_lbl_a.next_to(axes_pt.c2p(self.SIM_TOTAL, 0), RIGHT, buff=0.15)
        pt_lbl_b = Text("B의 운동량", font_size=self.FONT_LABEL, color=RED)
        pt_lbl_b.next_to(axes_pt.c2p(self.SIM_TOTAL, 4), RIGHT, buff=0.15)
        pt_lbl_tot = Text("총 운동량", font_size=self.FONT_LABEL, color=YELLOW)
        pt_lbl_tot.next_to(axes_pt.c2p(0, 4), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)

        conclusion = MathTex(r"p_1 + p_2 = p_1' + p_2'",
                             font_size=self.FONT_CALC, color=YELLOW)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(2.0)

    # ═══════════ Phase 3: 다른 질량 완전 탄성 충돌 ═══════════

    def phase3_different_mass_collision(self):
        # ── 1. 타이틀 ──
        title = VGroup(
            Text("실험 B: 다른 질량 탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m_A = 1\text{kg},\; v_A = 6\text{m/s},\; m_B = 2\text{kg},\; v_B = 0)",
                    font_size=self.FONT_SUBTITLE, color=WHITE)
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ── 2. 트랙 ──
        track_data = self._make_track()
        self.play(Create(track_data["track"]), Create(track_data["ticks"]),
                  Write(track_data["labels"]), run_time=0.75)
        center_y = track_data["track"].get_center()[1]

        # ── 3. p-t 그래프 ──
        pt_data = self._make_pt_axes(y_range=[-4, 10, 2], y_numbers=[-2, 0, 2, 4, 6, 8],
                                     y_length=3.5)
        axes_pt = pt_data["axes"]
        self.play(Create(axes_pt), Write(pt_data["x_lab"]), Write(pt_data["y_lab"]), run_time=0.75)

        # ── 4. 운동량 막대 ──
        bar_data = self._make_momentum_bars(
            values=[6, 0, 6], colors=[BLUE, RED, YELLOW],
            labels=["p_A", "p_B", "p_{tot}"], bar_scale=0.3)
        self.play(
            FadeIn(bar_data["bars"]), Write(bar_data["bar_labels"]),
            Write(bar_data["bar_title"]), Write(bar_data["val_labels"]),
            run_time=0.75
        )

        # ── 5. 물체 ──
        START_A_X, START_B_X = -4.0, 0.0
        obj_a = self._make_object(START_A_X, center_y, self.OBJ_SIZE_SMALL, BLUE, "A", "1\\,\\text{kg}")
        obj_b = self._make_object(START_B_X, center_y, self.OBJ_SIZE_MEDIUM, RED, "B", "2\\,\\text{kg}")
        vel_arrow = Arrow(
            start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 1.0,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        TRACK_BOTTOM_Y = center_y - 0.15
        vel_label = MathTex("v=6", font_size=20, color=BLUE)
        vel_label.move_to([obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        self.play(
            FadeIn(obj_a["box"]), FadeIn(obj_b["box"]),
            Write(obj_a["label"]), Write(obj_b["label"]),
            Write(obj_a["mass"]), Write(obj_b["mass"]),
            Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # ── 6. 충돌 시뮬레이션 ──
        SCALE_V = 0.35
        V_A, V_B = 6.0, 0.0
        V_A_AFTER, V_B_AFTER = -2.0, 4.0
        obj_a_size = self.OBJ_SIZE_SMALL
        obj_b_size = self.OBJ_SIZE_MEDIUM

        dist = (START_B_X - obj_b_size / 2) - (START_A_X + obj_a_size / 2)
        collision_t = dist / (V_A * SCALE_V)
        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return START_A_X + V_A * SCALE_V * t
            return START_A_X + V_A * SCALE_V * collision_t + V_A_AFTER * SCALE_V * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return START_B_X
            return START_B_X + V_B_AFTER * SCALE_V * (t - collision_t)

        y_a = center_y + obj_a_size / 2 + 0.1
        y_b = center_y + obj_b_size / 2 + 0.1
        self._setup_object_updaters(obj_a, pos_a, time_tracker, y_a)
        self._setup_object_updaters(obj_b, pos_b, time_tracker, y_b)

        vel_arrow_a_dyn = always_redraw(lambda: (
            Arrow(
                start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 1.0,
                color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
            ) if time_tracker.get_value() < collision_t else (
                Arrow(
                    start=obj_a["box"].get_left(), end=obj_a["box"].get_left() + LEFT * 0.4,
                    color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
                ) if time_tracker.get_value() > collision_t + 0.2 else VMobject()
            )
        ))
        vel_label_a_dyn = always_redraw(lambda: (
            MathTex("v=6", font_size=20, color=BLUE).move_to(
                [obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
            if time_tracker.get_value() < collision_t else (
                MathTex("v=-2", font_size=20, color=BLUE).move_to(
                    [obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
                if time_tracker.get_value() > collision_t + 0.2 else VMobject()
            )
        ))
        vel_arrow_b_dyn = always_redraw(lambda: Arrow(
            start=obj_b["box"].get_right(), end=obj_b["box"].get_right() + RIGHT * 0.7,
            color=RED, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() > collision_t + 0.2 else VMobject())
        vel_label_b_dyn = always_redraw(lambda: MathTex(
            "v=4", font_size=20, color=RED
        ).move_to([obj_b["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        if time_tracker.get_value() > collision_t + 0.2 else VMobject())

        self.remove(vel_arrow)
        self.add(vel_arrow_a_dyn, vel_label_a_dyn, vel_arrow_b_dyn, vel_label_b_dyn)

        # p-t 그래프
        def p_a_func(t):
            s = self._smooth_step(t, collision_t)
            return 6 * (1 - s) + (-2) * s

        def p_b_func(t):
            s = self._smooth_step(t, collision_t)
            return 8 * s

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 6, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t),
                  run_time=collision_t * self.REAL_PER_SIM, rate_func=linear)

        # 충돌 효과 + 막대 업데이트
        collision_point = obj_a["box"].get_right()
        bar_anims = self._update_bars(bar_data, [-2, 8, 6], [BLUE, RED, YELLOW])
        self._collision_effect(collision_point, obj_a["box"], obj_b["box"], bar_anims)

        # 충돌 후
        self.play(time_tracker.animate.set_value(self.SIM_TOTAL),
                  run_time=(self.SIM_TOTAL - collision_t) * self.REAL_PER_SIM, rate_func=linear)

        # 정리
        self._clear_object_updaters(obj_a, obj_b)
        self.remove(vel_arrow_a_dyn, vel_label_a_dyn, vel_arrow_b_dyn, vel_label_b_dyn,
                    pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, self.SIM_TOTAL], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, self.SIM_TOTAL], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 6, x_range=[0, self.SIM_TOTAL],
                                    color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=self.FONT_LABEL, color=BLUE)
        pt_lbl_a.next_to(axes_pt.c2p(self.SIM_TOTAL, -2), RIGHT, buff=0.15)
        pt_lbl_b = Text("B의 운동량", font_size=self.FONT_LABEL, color=RED)
        pt_lbl_b.next_to(axes_pt.c2p(self.SIM_TOTAL, 8), RIGHT, buff=0.15)
        pt_lbl_tot = Text("총 운동량", font_size=self.FONT_LABEL, color=YELLOW)
        pt_lbl_tot.next_to(axes_pt.c2p(0, 6), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)
        self.wait(1.5)

        # ── 7. 그래프/막대 정리 후 수식 검증 ──
        self.play(
            *[FadeOut(m) for m in [
                final_pt_a, final_pt_b, final_pt_tot,
                pt_lbl_a, pt_lbl_b, pt_lbl_tot,
                axes_pt, pt_data["x_lab"], pt_data["y_lab"],
                bar_data["bars"], bar_data["bar_labels"], bar_data["bar_title"],
                bar_data["val_labels"],
            ]],
            run_time=0.5
        )

        before_collision = VGroup(
            Text("충돌 전 운동량", font_size=24, color=YELLOW),
            MathTex(r"p_A = 1 \times 6 = 6", font_size=24, color=BLUE),
            MathTex(r"p_B = 2 \times 0 = 0", font_size=24, color=RED),
            MathTex(r"p_{tot} = 6 + 0 = 6\;\checkmark", font_size=26, color=YELLOW),
        )
        after_collision = VGroup(
            Text("충돌 후 운동량", font_size=24, color=YELLOW),
            MathTex(r"p_A' = 1 \times (-2) = -2", font_size=24, color=BLUE),
            MathTex(r"p_B' = 2 \times 4 = 8", font_size=24, color=RED),
            MathTex(r"p_{tot}' = -2 + 8 = 6\;\checkmark", font_size=26, color=YELLOW),
        )

        before_collision.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        after_collision.arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        formulas = VGroup(before_collision, after_collision)
        formulas.arrange(RIGHT, buff=1.5)
        formulas.move_to(DOWN * 1.0)

        for v in before_collision:
            self.play(Write(v), run_time=0.5)
        self.wait(0.5)
        for v in after_collision:
            self.play(Write(v), run_time=0.5)

        self.wait(2.0)

    # ═══════════ Phase 4: 3물체 연쇄 탄성 충돌 (다른 질량) ═══════════

    def phase4_three_body_collision(self):
        # ── 1. 타이틀 ──
        # A(1kg, v=6) → B(2kg, 정지) → C(3kg, 정지)
        # 1차 충돌(A→B): v_A'=(1-2)/(1+2)*6=-2, v_B'=2*1/(1+2)*6=4
        # 2차 충돌(B→C): v_B''=(2-3)/(2+3)*4=-0.8, v_C'=2*2/(2+3)*4=3.2
        title = VGroup(
            Text("실험 C: 3물체 연쇄 탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m_A\!=\!1,\; m_B\!=\!2,\; m_C\!=\!3\text{kg},\; v_A\!=\!6\text{m/s})",
                    font_size=self.FONT_SUBTITLE, color=WHITE)
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ── 2. 트랙 ──
        track_data = self._make_track()
        self.play(Create(track_data["track"]), Create(track_data["ticks"]),
                  Write(track_data["labels"]), run_time=0.75)
        center_y = track_data["track"].get_center()[1]

        # ── 3. p-t 그래프 ──
        pt_data = self._make_pt_axes(y_range=[-4, 12, 2],
                                     y_numbers=[-2, 0, 2, 4, 6, 8, 10],
                                     y_length=3.5)
        axes_pt = pt_data["axes"]
        self.play(Create(axes_pt), Write(pt_data["x_lab"]), Write(pt_data["y_lab"]), run_time=0.75)

        # ── 4. 운동량 막대 ──
        bar_data = self._make_momentum_bars(
            values=[6, 0, 0, 6], colors=[BLUE, RED, GREEN, YELLOW],
            labels=["p_A", "p_B", "p_C", "p_{tot}"],
            bar_origin=RIGHT * 4.0 + DOWN * 2.5, bar_scale=0.25)
        self.play(
            FadeIn(bar_data["bars"]), Write(bar_data["bar_labels"]),
            Write(bar_data["bar_title"]), Write(bar_data["val_labels"]),
            run_time=0.75
        )

        # ── 5. 물체 ──
        START_A_X, START_B_X, START_C_X = -5.0, -1.0, 3.0
        obj_a_size = self.OBJ_SIZE_SMALL   # 1kg
        obj_b_size = self.OBJ_SIZE_MEDIUM  # 2kg
        obj_c_size = self.OBJ_SIZE_LARGE   # 3kg

        obj_a = self._make_object(START_A_X, center_y, obj_a_size, BLUE, "A", "1\\,\\text{kg}")
        obj_b = self._make_object(START_B_X, center_y, obj_b_size, RED, "B", "2\\,\\text{kg}")
        obj_c = self._make_object(START_C_X, center_y, obj_c_size, GREEN, "C", "3\\,\\text{kg}")

        self.play(
            FadeIn(obj_a["box"]), FadeIn(obj_b["box"]), FadeIn(obj_c["box"]),
            Write(obj_a["label"]), Write(obj_b["label"]), Write(obj_c["label"]),
            Write(obj_a["mass"]), Write(obj_b["mass"]), Write(obj_c["mass"]),
            run_time=0.75
        )
        self.wait(0.3)

        # ── 6. 충돌 물리 계산 ──
        SCALE_V = 0.35
        # 초기: v_A=6, v_B=0, v_C=0
        # 1차(A→B): v_A'=-2, v_B'=4
        # 2차(B→C): v_B''=-0.8, v_C'=3.2
        V_A_INIT = 6.0
        V_A_AFTER1 = -2.0
        V_B_AFTER1 = 4.0
        V_B_AFTER2 = -0.8
        V_C_AFTER2 = 3.2

        # 1차 충돌 시간: A 오른쪽 → B 왼쪽
        dist_ab = (START_B_X - obj_b_size / 2) - (START_A_X + obj_a_size / 2)
        collision1_t = dist_ab / (V_A_INIT * SCALE_V)

        # 2차 충돌 시간: B가 v=4로 이동, C 정지, B 오른쪽 → C 왼쪽
        dist_bc = (START_C_X - obj_c_size / 2) - (START_B_X + obj_b_size / 2)
        collision2_t = collision1_t + dist_bc / (V_B_AFTER1 * SCALE_V)

        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision1_t:
                return START_A_X + V_A_INIT * SCALE_V * t
            return START_A_X + V_A_INIT * SCALE_V * collision1_t + V_A_AFTER1 * SCALE_V * (t - collision1_t)

        def pos_b(t):
            if t <= collision1_t:
                return START_B_X
            if t <= collision2_t:
                return START_B_X + V_B_AFTER1 * SCALE_V * (t - collision1_t)
            return (START_B_X + V_B_AFTER1 * SCALE_V * (collision2_t - collision1_t)
                    + V_B_AFTER2 * SCALE_V * (t - collision2_t))

        def pos_c(t):
            if t <= collision2_t:
                return START_C_X
            return START_C_X + V_C_AFTER2 * SCALE_V * (t - collision2_t)

        # 현재 속도 함수 (화살표 표시용)
        def vel_a(t):
            if t < collision1_t:
                return V_A_INIT
            return V_A_AFTER1

        def vel_b(t):
            if t < collision1_t:
                return 0.0
            if t < collision2_t:
                return V_B_AFTER1
            return V_B_AFTER2

        def vel_c(t):
            if t < collision2_t:
                return 0.0
            return V_C_AFTER2

        y_a = center_y + obj_a_size / 2 + 0.1
        y_b = center_y + obj_b_size / 2 + 0.1
        y_c = center_y + obj_c_size / 2 + 0.1
        self._setup_object_updaters(obj_a, pos_a, time_tracker, y_a)
        self._setup_object_updaters(obj_b, pos_b, time_tracker, y_b)
        self._setup_object_updaters(obj_c, pos_c, time_tracker, y_c)

        # ── 7. 항상 표시되는 속도 화살표 + 라벨 (트랙 아래 표시) ──
        ARROW_SCALE = 0.13
        TRACK_BOTTOM_Y = center_y - 0.15  # 트랙 라인 바로 아래
        VEL_FONT = 20

        def _make_vel_group(box, v, color):
            """속도값에 따라 화살표+라벨 반환, 라벨은 트랙 아래"""
            vel_abs = abs(v)
            v_str = f"{v:.1f}" if v != int(v) else f"{int(v)}"
            # 라벨은 항상 물체 아래(트랙 아래)에 표시
            lbl = MathTex(f"v={v_str}", font_size=VEL_FONT, color=color)
            lbl.move_to([box.get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
            if vel_abs < 0.01:
                return VGroup(lbl)
            arrow_len = max(vel_abs * ARROW_SCALE, 0.25)
            if v > 0:
                arrow = Arrow(
                    start=box.get_right(), end=box.get_right() + RIGHT * arrow_len,
                    color=color, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            else:
                arrow = Arrow(
                    start=box.get_left(), end=box.get_left() + LEFT * arrow_len,
                    color=color, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            return VGroup(arrow, lbl)

        vel_display_a = always_redraw(
            lambda: _make_vel_group(obj_a["box"], vel_a(time_tracker.get_value()), BLUE))
        vel_display_b = always_redraw(
            lambda: _make_vel_group(obj_b["box"], vel_b(time_tracker.get_value()), RED))
        vel_display_c = always_redraw(
            lambda: _make_vel_group(obj_c["box"], vel_c(time_tracker.get_value()), GREEN))
        self.add(vel_display_a, vel_display_b, vel_display_c)

        # ── 8. p-t 그래프 ──
        # p_A: 6 → -2 (at c1)
        # p_B: 0 → 8 (at c1) → -1.6 (at c2)
        # p_C: 0 → 0 → 9.6 (at c2)
        # total = 6

        def p_a_func(t):
            s1 = self._smooth_step(t, collision1_t)
            return V_A_INIT * (1 - s1) + V_A_AFTER1 * s1  # 6 → -2

        def p_b_func(t):
            s1 = self._smooth_step(t, collision1_t)
            s2 = self._smooth_step(t, collision2_t)
            # 0 → 8 (at c1) → -1.6 (at c2)
            p_b_after1 = 2 * V_B_AFTER1  # = 8
            p_b_after2 = 2 * V_B_AFTER2  # = -1.6
            before = 0.0
            mid = p_b_after1
            after = p_b_after2
            return before * (1 - s1) + mid * s1 * (1 - s2) + after * s2

        def p_c_func(t):
            s2 = self._smooth_step(t, collision2_t)
            return 3 * V_C_AFTER2 * s2  # 0 → 9.6

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_c = always_redraw(lambda: axes_pt.plot(
            p_c_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=GREEN, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 6, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_c, pt_line_tot)

        # ── 9. 1차 충돌 (A→B) ──
        self.play(time_tracker.animate.set_value(collision1_t),
                  run_time=collision1_t * self.REAL_PER_SIM, rate_func=linear)

        collision_point_1 = obj_a["box"].get_right()
        bar_anims_1 = self._update_bars(bar_data, [-2, 8, 0, 6], [BLUE, RED, GREEN, YELLOW])
        self._collision_effect(collision_point_1, obj_a["box"], obj_b["box"], bar_anims_1)

        # ── 10. B가 C로 이동 → 2차 충돌 ──
        self.play(time_tracker.animate.set_value(collision2_t),
                  run_time=(collision2_t - collision1_t) * self.REAL_PER_SIM, rate_func=linear)

        collision_point_2 = obj_b["box"].get_right()
        bar_anims_2 = self._update_bars(bar_data, [-2, -1.6, 9.6, 6], [BLUE, RED, GREEN, YELLOW])
        self._collision_effect(collision_point_2, obj_b["box"], obj_c["box"], bar_anims_2)

        # ── 11. 충돌 후 이동 ──
        self.play(time_tracker.animate.set_value(self.SIM_TOTAL),
                  run_time=(self.SIM_TOTAL - collision2_t) * self.REAL_PER_SIM, rate_func=linear)

        # 정리
        self._clear_object_updaters(obj_a, obj_b, obj_c)
        self.remove(vel_display_a, vel_display_b, vel_display_c,
                    pt_line_a, pt_line_b, pt_line_c, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, self.SIM_TOTAL], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, self.SIM_TOTAL], color=RED, stroke_width=3)
        final_pt_c = axes_pt.plot(p_c_func, x_range=[0, self.SIM_TOTAL], color=GREEN, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 6, x_range=[0, self.SIM_TOTAL],
                                    color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_c, final_pt_tot)

        # 정적 속도 화살표 (최종 상태)
        final_vel_a = _make_vel_group(obj_a["box"], V_A_AFTER1, BLUE)
        final_vel_b = _make_vel_group(obj_b["box"], V_B_AFTER2, RED)
        final_vel_c = _make_vel_group(obj_c["box"], V_C_AFTER2, GREEN)
        self.add(final_vel_a, final_vel_b, final_vel_c)

        pt_lbl_a = Text("A의 운동량", font_size=self.FONT_LABEL, color=BLUE)
        pt_lbl_a.next_to(axes_pt.c2p(self.SIM_TOTAL, -2), RIGHT, buff=0.15)
        pt_lbl_b = Text("B의 운동량", font_size=self.FONT_LABEL, color=RED)
        pt_lbl_b.next_to(axes_pt.c2p(self.SIM_TOTAL, -1.6), RIGHT, buff=0.15).shift(DOWN * 0.2)
        pt_lbl_c = Text("C의 운동량", font_size=self.FONT_LABEL, color=GREEN)
        pt_lbl_c.next_to(axes_pt.c2p(self.SIM_TOTAL, 9.6), RIGHT, buff=0.15)
        pt_lbl_tot = Text("총 운동량", font_size=self.FONT_LABEL, color=YELLOW)
        pt_lbl_tot.next_to(axes_pt.c2p(0, 6), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_c), Write(pt_lbl_tot), run_time=0.5)

        conclusion = Text("질량이 달라도, 연쇄 충돌에서도 총 운동량은 보존된다!",
                          font_size=24, color=YELLOW)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(2.0)

    # ═══════════ Phase 5: 완전 비탄성 충돌 ═══════════

    def phase5_inelastic_collision(self):
        # ── 1. 타이틀 ──
        title = VGroup(
            Text("실험 D: 완전 비탄성 충돌", font_size=30, color=WHITE),
            MathTex(r"(m_A = 1\text{kg},\; v_A = 4\text{m/s},\; m_B = 1\text{kg},\; v_B = 0)",
                    font_size=self.FONT_SUBTITLE, color=WHITE)
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ── 2. 트랙 ──
        track_data = self._make_track()
        self.play(Create(track_data["track"]), Create(track_data["ticks"]),
                  Write(track_data["labels"]), run_time=0.75)
        center_y = track_data["track"].get_center()[1]

        # ── 3. p-t 그래프 ──
        pt_data = self._make_pt_axes(y_range=[-1, 6, 1], y_numbers=[0, 2, 4])
        axes_pt = pt_data["axes"]
        self.play(Create(axes_pt), Write(pt_data["x_lab"]), Write(pt_data["y_lab"]), run_time=0.75)

        # ── 4. 운동량 막대 ──
        bar_data = self._make_momentum_bars(
            values=[4, 0, 4], colors=[BLUE, RED, YELLOW],
            labels=["p_A", "p_B", "p_{tot}"], bar_scale=0.35)
        self.play(
            FadeIn(bar_data["bars"]), Write(bar_data["bar_labels"]),
            Write(bar_data["bar_title"]), Write(bar_data["val_labels"]),
            run_time=0.75
        )

        # ── 5. 물체 ──
        START_A_X, START_B_X = -4.0, 0.0
        obj_size = self.OBJ_SIZE_SMALL
        obj_a = self._make_object(START_A_X, center_y, obj_size, BLUE, "A", "1\\,\\text{kg}")
        obj_b = self._make_object(START_B_X, center_y, obj_size, RED, "B", "1\\,\\text{kg}")
        vel_arrow = Arrow(
            start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        TRACK_BOTTOM_Y = center_y - 0.15
        vel_label = MathTex("v=4", font_size=20, color=BLUE)
        vel_label.move_to([obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        self.play(
            FadeIn(obj_a["box"]), FadeIn(obj_b["box"]),
            Write(obj_a["label"]), Write(obj_b["label"]),
            Write(obj_a["mass"]), Write(obj_b["mass"]),
            Create(vel_arrow), Write(vel_label),
            run_time=0.75
        )
        self.wait(0.3)

        # ── 6. 충돌 시뮬레이션 ──
        V_BEFORE = 4.0
        V_AFTER = 2.0

        dist = (START_B_X - obj_size / 2) - (START_A_X + obj_size / 2)
        collision_t = dist / (V_BEFORE * self.SCALE_V)
        time_tracker = ValueTracker(0)

        def pos_a(t):
            if t <= collision_t:
                return START_A_X + V_BEFORE * self.SCALE_V * t
            return START_A_X + V_BEFORE * self.SCALE_V * collision_t + V_AFTER * self.SCALE_V * (t - collision_t)

        def pos_b(t):
            if t <= collision_t:
                return START_B_X
            return START_B_X + V_AFTER * self.SCALE_V * (t - collision_t)

        y_pos = center_y + obj_size / 2 + 0.1
        self._setup_object_updaters(obj_a, pos_a, time_tracker, y_pos)
        self._setup_object_updaters(obj_b, pos_b, time_tracker, y_pos)

        vel_dyn = always_redraw(lambda: Arrow(
            start=obj_a["box"].get_right(), end=obj_a["box"].get_right() + RIGHT * 0.8,
            color=BLUE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ) if time_tracker.get_value() < collision_t else VMobject())
        vel_label_dyn = always_redraw(lambda: MathTex(
            "v=4", font_size=20, color=BLUE
        ).move_to([obj_a["box"].get_center()[0], TRACK_BOTTOM_Y - 0.35, 0])
        if time_tracker.get_value() < collision_t else VMobject())

        self.remove(vel_arrow)
        self.add(vel_dyn, vel_label_dyn)

        # p-t 그래프
        def p_a_func(t):
            s = self._smooth_step(t, collision_t)
            return 4 * (1 - s) + 2 * s

        def p_b_func(t):
            s = self._smooth_step(t, collision_t)
            return 2 * s

        pt_line_a = always_redraw(lambda: axes_pt.plot(
            p_a_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=BLUE, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_b = always_redraw(lambda: axes_pt.plot(
            p_b_func, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=RED, stroke_width=3
        ) if time_tracker.get_value() > 0.01 else VMobject())
        pt_line_tot = always_redraw(lambda: axes_pt.plot(
            lambda t: 4, x_range=[0, min(max(time_tracker.get_value(), 0.02), self.SIM_TOTAL)],
            color=YELLOW, stroke_width=3, stroke_opacity=0.7
        ) if time_tracker.get_value() > 0.01 else VMobject())
        self.add(pt_line_a, pt_line_b, pt_line_tot)

        # 충돌 전
        self.play(FadeOut(vel_label), run_time=0.3)
        self.play(time_tracker.animate.set_value(collision_t),
                  run_time=collision_t * self.REAL_PER_SIM, rate_func=linear)

        # 충돌 효과 + 막대 업데이트
        collision_point = obj_a["box"].get_right()
        bar_anims = self._update_bars(bar_data, [2, 2, 4], [BLUE, RED, YELLOW])
        self._collision_effect(collision_point, obj_a["box"], obj_b["box"], bar_anims)

        # 합체 처리
        obj_b["box"].clear_updaters()
        obj_b["label"].clear_updaters()
        obj_b["mass"].clear_updaters()
        self.remove(vel_dyn, vel_label_dyn)
        self.play(obj_b["box"].animate.next_to(obj_a["box"], RIGHT, buff=0), run_time=0.3)
        obj_b["label"].move_to(obj_b["box"])

        # PURPLE 테두리로 합체 표현
        merged_border = SurroundingRectangle(
            VGroup(obj_a["box"], obj_b["box"]), color=PURPLE, buff=0.05,
            corner_radius=0.05, stroke_width=3)
        merged_border.add_updater(lambda m: m.become(
            SurroundingRectangle(VGroup(obj_a["box"], obj_b["box"]), color=PURPLE, buff=0.05,
                                 corner_radius=0.05, stroke_width=3)))

        self.play(FadeOut(obj_a["mass"]), FadeOut(obj_b["mass"]), run_time=0.2)
        self.play(Create(merged_border), run_time=0.3)

        merged_label = MathTex("2\\,\\text{kg}", font_size=18, color=PURPLE)
        merged_label.add_updater(lambda m: m.next_to(VGroup(obj_a["box"], obj_b["box"]), UP, buff=0.1))
        self.play(Write(merged_label), run_time=0.3)

        merged_vel = always_redraw(lambda: Arrow(
            start=obj_b["box"].get_right(), end=obj_b["box"].get_right() + RIGHT * 0.4,
            color=PURPLE, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3,
        ))
        merged_vel_label = always_redraw(lambda: MathTex(
            "v'=2", font_size=20, color=PURPLE
        ).move_to([obj_a["box"].get_center()[0] + 0.25, TRACK_BOTTOM_Y - 0.35, 0]))
        self.add(merged_vel, merged_vel_label)

        obj_b["box"].add_updater(lambda m: m.next_to(obj_a["box"], RIGHT, buff=0))
        obj_b["label"].add_updater(lambda m: m.move_to(obj_b["box"]))

        # 충돌 후
        self.play(time_tracker.animate.set_value(self.SIM_TOTAL),
                  run_time=(self.SIM_TOTAL - collision_t) * self.REAL_PER_SIM, rate_func=linear)

        # 정리
        obj_a["box"].clear_updaters()
        obj_b["box"].clear_updaters()
        obj_a["label"].clear_updaters()
        obj_b["label"].clear_updaters()
        merged_label.clear_updaters()
        merged_border.clear_updaters()
        self.remove(merged_vel, merged_vel_label, vel_dyn, pt_line_a, pt_line_b, pt_line_tot)

        # 정적 그래프
        final_pt_a = axes_pt.plot(p_a_func, x_range=[0, self.SIM_TOTAL], color=BLUE, stroke_width=3)
        final_pt_b = axes_pt.plot(p_b_func, x_range=[0, self.SIM_TOTAL], color=RED, stroke_width=3)
        final_pt_tot = axes_pt.plot(lambda t: 4, x_range=[0, self.SIM_TOTAL],
                                    color=YELLOW, stroke_width=3, stroke_opacity=0.7)
        self.add(final_pt_a, final_pt_b, final_pt_tot)

        pt_lbl_a = Text("A의 운동량", font_size=self.FONT_LABEL, color=BLUE)
        pt_lbl_a.next_to(axes_pt.c2p(self.SIM_TOTAL, 2), RIGHT, buff=0.15).shift(UP * 0.15)
        pt_lbl_b = Text("B의 운동량", font_size=self.FONT_LABEL, color=RED)
        pt_lbl_b.next_to(axes_pt.c2p(self.SIM_TOTAL, 2), RIGHT, buff=0.15).shift(DOWN * 0.15)
        pt_lbl_tot = Text("총 운동량", font_size=self.FONT_LABEL, color=YELLOW)
        pt_lbl_tot.next_to(axes_pt.c2p(0, 4), RIGHT, buff=0.15).shift(UP * 0.3)
        self.play(Write(pt_lbl_a), Write(pt_lbl_b), Write(pt_lbl_tot), run_time=0.5)

        conclusion = VGroup(
            MathTex(r"p_{tot} = 4", font_size=self.FONT_CALC, color=YELLOW),
            Text("(보존)", font_size=24, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        conclusion.next_to(title, DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=1.0)
        self.wait(1.5)

        # ── 에너지 비교 ──
        self.play(
            *[FadeOut(m) for m in [
                final_pt_a, final_pt_b, final_pt_tot,
                pt_lbl_a, pt_lbl_b, pt_lbl_tot,
                axes_pt, pt_data["x_lab"], pt_data["y_lab"], conclusion,
                bar_data["bars"], bar_data["bar_labels"], bar_data["bar_title"],
                bar_data["val_labels"],
            ]],
            run_time=0.5
        )

        # 운동량 보존 수식
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

        # 운동에너지 비보존
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

        key_msg = Text("운동량은 항상 보존, 운동에너지는 충돌 종류에 따라 다르다!",
                       font_size=22, color=YELLOW)
        key_msg.to_edge(DOWN, buff=0.2)
        self.play(Write(key_msg), run_time=1.0)
        self.wait(2.0)

    # ═══════════ 정리 (Summary) ═══════════

    def summary(self):
        summary_title = Text("정리", font_size=44, color=YELLOW)
        summary_title.to_edge(UP, buff=0.8)
        self.play(Write(summary_title), run_time=0.75)

        points = VGroup(
            Text("• 운동량 = 질량 × 속도 (벡터량)", font_size=28, color=WHITE),
            Text("• 외력이 없으면 총 운동량 보존", font_size=28, color=WHITE),
            Text("• 탄성/비탄성/연쇄 충돌 모두 성립", font_size=28, color=WHITE),
            Text("• 운동에너지는 충돌 종류에 따라 보존 여부가 다름", font_size=28, color=WHITE),
        )
        points.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.next_to(summary_title, DOWN, buff=0.8)

        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.3)

        self.wait(2.0)

    # ═══════════ Outro ═══════════

    def outro(self):
        final_eq = MathTex(
            "m_1", "v_1", "+", "m_2", "v_2", "=",
            "m_1", "v_1'", "+", "m_2", "v_2'",
            font_size=64, color=WHITE
        )
        final_eq.move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=YELLOW, buff=0.4,
                                          corner_radius=0.15, stroke_width=4)
        subtitle = Text("운동량 보존 법칙", font_size=40, color=YELLOW)
        subtitle.next_to(final_box, DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)
        self.play(Create(final_box), run_time=0.75)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(3)
