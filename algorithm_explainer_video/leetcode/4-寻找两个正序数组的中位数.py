from __future__ import annotations

from manim import *

BG = "#070B16"
WHITE_SOFT = "#E8EEF9"
BLUE_A = "#58C4DD"
BLUE_B = "#5B8FF9"
YELLOW_ACCENT = "#F7C948"
GREEN_OK = "#4DD599"
RED_BAD = "#FF6B6B"
PURPLE = "#A78BFA"
MUTED = "#8290A7"
FONT = "Noto Sans SC"
MONO = "Maple Mono NF CN"


class ArrayRow(VGroup):
    """A compact array visualization with stable cell geometry."""

    def __init__(
        self,
        label: str,
        values: list[int],
        color: str,
        cell_size: float = 0.72,
    ) -> None:
        super().__init__()
        self.values = values
        self.cell_size = cell_size
        self.cells = VGroup()
        self.numbers = VGroup()
        for value in values:
            box = RoundedRectangle(
                corner_radius=0.08,
                width=cell_size,
                height=cell_size,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.09,
            )
            number = Text(str(value), font=FONT, font_size=26, color=WHITE_SOFT)
            number.move_to(box)
            self.cells.add(box)
            self.numbers.add(number)
        self.cells.arrange(RIGHT, buff=0.08)
        for number, box in zip(self.numbers, self.cells):
            number.move_to(box)
        self.label = Text(label, font=MONO, font_size=28, color=color)
        self.label.next_to(self.cells, LEFT, buff=0.28)
        self.add(self.label, self.cells, self.numbers)

    def cut_x(self, index: int) -> float:
        if index == 0:
            return self.cells[0].get_left()[0] - 0.04
        if index == len(self.cells):
            return self.cells[-1].get_right()[0] + 0.04
        return (self.cells[index - 1].get_right()[0] + self.cells[index].get_left()[0]) / 2

    def partition(self, index: int, color: str = YELLOW_ACCENT) -> DashedLine:
        x = self.cut_x(index)
        return DashedLine(
            [x, self.get_bottom()[1] - 0.18, 0],
            [x, self.get_top()[1] + 0.18, 0],
            dash_length=0.09,
            color=color,
            stroke_width=4,
        )


class MedianOfTwoSortedArrays(Scene):
    """Visual explanation of LeetCode 4 and the matching Rust implementation."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.opening_question()
        self.partition_invariant()
        self.binary_search_walkthrough()
        self.boundaries_and_answer()
        self.map_to_rust()
        self.complexity_finale()

    def heading(self, text: str, color: str = WHITE_SOFT) -> Text:
        title = Text(text, font=FONT, font_size=42, weight=BOLD, color=color)
        title.to_edge(UP, buff=0.42)
        return title

    def caption(self, text: str, color: str = WHITE_SOFT) -> VGroup:
        plate = RoundedRectangle(
            width=12.2,
            height=0.68,
            corner_radius=0.16,
            fill_color="#10182B",
            fill_opacity=0.94,
            stroke_color="#263552",
            stroke_width=1.5,
        )
        words = Text(text, font=FONT, font_size=25, color=color)
        words.move_to(plate)
        group = VGroup(plate, words).to_edge(DOWN, buff=0.24)
        return group

    def opening_question(self) -> None:
        title = Text(
            "两个有序数组的中位数",
            font=FONT,
            font_size=58,
            weight=BOLD,
            gradient=(BLUE_A, PURPLE),
        )
        rule = Line(LEFT * 3.4, RIGHT * 3.4, color=YELLOW_ACCENT, stroke_width=4)
        rule.next_to(title, DOWN, buff=0.24)
        target = Text("不合并，能找到它吗？", font=FONT, font_size=34, color=WHITE_SOFT)
        target.next_to(rule, DOWN, buff=0.38)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.5)
        self.play(FadeIn(target, shift=UP * 0.2))
        self.wait(1.2)

        a = ArrayRow("A", [1, 3, 8, 9, 15], BLUE_A).shift(UP * 0.55)
        b = ArrayRow("B", [7, 11, 18, 19, 21, 25], BLUE_B).shift(DOWN * 0.55)
        rows = VGroup(a, b).move_to(ORIGIN)
        caption = self.caption("直接归并当然可行，但要扫描 O(m+n) 个元素")
        self.play(FadeOut(title), FadeOut(rule), FadeOut(target), FadeIn(rows))
        self.play(FadeIn(caption, shift=UP * 0.15))

        linear = Text("O(m+n)", font=MONO, font_size=58, color=RED_BAD)
        linear.to_edge(RIGHT, buff=1.0).shift(UP * 2.3)
        strike = Line(linear.get_left(), linear.get_right(), color=RED_BAD, stroke_width=6)
        self.play(Write(linear), Create(strike))
        self.wait(1.0)

        better = Text("把问题变成：找一条正确的分割线", font=FONT, font_size=35, color=YELLOW_ACCENT)
        better.to_edge(UP, buff=0.55)
        self.play(
            FadeOut(linear),
            FadeOut(strike),
            FadeOut(caption),
            rows.animate.shift(DOWN * 0.35),
            FadeIn(better, shift=DOWN * 0.2),
        )
        self.wait(1.2)
        self.play(FadeOut(rows), FadeOut(better))

    def partition_invariant(self) -> None:
        title = self.heading("中位数，本质上是一道分割题")
        a = ArrayRow("A", [1, 3, 8, 9, 15], BLUE_A).shift(UP * 0.8)
        b = ArrayRow("B", [7, 11, 18, 19, 21, 25], BLUE_B).shift(DOWN * 0.55)
        rows = VGroup(a, b).move_to(ORIGIN).shift(LEFT * 1.2)
        cut_a = a.partition(3)
        cut_b = b.partition(3)
        left_brace = BraceBetweenPoints(
            [a.cells[0].get_left()[0], b.get_bottom()[1] - 0.15, 0],
            [a.cut_x(3), b.get_bottom()[1] - 0.15, 0],
            direction=DOWN,
            color=GREEN_OK,
        )
        right_brace = BraceBetweenPoints(
            [a.cut_x(3), b.get_bottom()[1] - 0.15, 0],
            [b.cells[-1].get_right()[0], b.get_bottom()[1] - 0.15, 0],
            direction=DOWN,
            color=PURPLE,
        )
        left_text = Text("左半边", font=FONT, font_size=25, color=GREEN_OK).next_to(left_brace, DOWN)
        right_text = Text("右半边", font=FONT, font_size=25, color=PURPLE).next_to(right_brace, DOWN)
        caption = self.caption("目标一：左边恰好放一半元素；奇数时让左边多一个")

        self.play(Write(title), FadeIn(rows, lag_ratio=0.08))
        self.play(Create(cut_a), Create(cut_b), GrowFromCenter(left_brace), GrowFromCenter(right_brace))
        self.play(FadeIn(left_text), FadeIn(right_text), FadeIn(caption))
        self.wait(1.5)

        info = VGroup(
            Text("i + j = (m+n+1) / 2", font=MONO, font_size=30, color=YELLOW_ACCENT),
            VGroup(
                Text("目标二", font=FONT, font_size=27, color=WHITE_SOFT),
                Text("左边所有数 ≤ 右边所有数", font=FONT, font_size=26, color=GREEN_OK),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(
                Text("A左 ≤ B右", font=MONO, font_size=25, color=BLUE_A),
                Text("B左 ≤ A右", font=MONO, font_size=25, color=BLUE_B),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        formula, condition, checks = info
        self.play(Write(formula))
        self.wait(1.2)
        self.play(ReplacementTransform(caption, self.caption("无需检查全部元素，只需比较分割线旁边的四个数")))
        self.play(FadeIn(condition), FadeIn(checks, lag_ratio=0.2))
        self.wait(1.8)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def binary_search_walkthrough(self) -> None:
        title = self.heading("只在更短的数组 A 上二分")
        a = ArrayRow("A", [1, 3, 8, 9, 15], BLUE_A).shift(UP * 0.72)
        b = ArrayRow("B", [7, 11, 18, 19, 21, 25], BLUE_B).shift(DOWN * 0.58)
        rows = VGroup(a, b).move_to(ORIGIN).shift(LEFT * 1.65)
        self.play(Write(title), FadeIn(rows))

        search = Text("left=0     right=5", font=MONO, font_size=28, color=MUTED)
        search.to_edge(RIGHT, buff=0.55).shift(UP * 1.85)
        self.play(FadeIn(search))

        cut_a_1 = a.partition(2)
        cut_b_1 = b.partition(4)
        ij_1 = Text("i=2,  j=6-i=4", font=MONO, font_size=30, color=YELLOW_ACCENT)
        ij_1.next_to(search, DOWN, buff=0.38)
        self.play(Create(cut_a_1), Create(cut_b_1), Write(ij_1))

        bad = VGroup(
            Text("B左最大 = 19", font=FONT, font_size=27, color=BLUE_B),
            Text(">", font=MONO, font_size=34, color=RED_BAD),
            Text("A右最小 = 8", font=FONT, font_size=27, color=BLUE_A),
        ).arrange(RIGHT, buff=0.12).next_to(ij_1, DOWN, buff=0.45)
        verdict = Text("A 切得太靠左 → i 增大", font=FONT, font_size=29, color=RED_BAD)
        verdict.next_to(bad, DOWN, buff=0.32)
        caption1 = self.caption("若 B左 > A右，A 的左半边装得不够：left = i + 1")
        self.play(FadeIn(bad), Circumscribe(b.cells[3], color=RED_BAD), Circumscribe(a.cells[2], color=RED_BAD))
        self.play(FadeIn(verdict), FadeIn(caption1))
        self.wait(1.6)

        search_2 = Text("left=3     right=5", font=MONO, font_size=28, color=MUTED)
        search_2.move_to(search)
        cut_a_2 = a.partition(4, GREEN_OK)
        cut_b_2 = b.partition(2, GREEN_OK)
        ij_2 = Text("i=4,  j=6-i=2", font=MONO, font_size=30, color=YELLOW_ACCENT).move_to(ij_1)
        self.play(
            Transform(search, search_2),
            Transform(cut_a_1, cut_a_2),
            Transform(cut_b_1, cut_b_2),
            Transform(ij_1, ij_2),
            FadeOut(bad),
            FadeOut(verdict),
            FadeOut(caption1),
        )

        good = VGroup(
            Text("9 ≤ 18", font=MONO, font_size=31, color=GREEN_OK),
            Text("且", font=FONT, font_size=26, color=MUTED),
            Text("11 ≤ 15", font=MONO, font_size=31, color=GREEN_OK),
        ).arrange(RIGHT, buff=0.2).next_to(ij_1, DOWN, buff=0.48)
        checkmark = Text("✓  分割正确", font=FONT, font_size=34, color=GREEN_OK).next_to(good, DOWN, buff=0.35)
        caption2 = self.caption("两组交叉条件同时成立，分割线两侧已经整体有序")
        self.play(FadeIn(good, lag_ratio=0.2))
        self.play(Write(checkmark), FadeIn(caption2))
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def boundaries_and_answer(self) -> None:
        title = self.heading("分割正确后，答案就在边界上")
        left_values = VGroup(
            *[
                RoundedRectangle(
                    width=0.92,
                    height=0.82,
                    corner_radius=0.1,
                    stroke_color=GREEN_OK,
                    fill_color=GREEN_OK,
                    fill_opacity=0.12,
                )
                for _ in range(6)
            ]
        ).arrange(RIGHT, buff=0.1)
        nums = [1, 3, 7, 8, 9, 11]
        for box, n in zip(left_values, nums):
            box.add(Text(str(n), font=FONT, font_size=28, color=WHITE_SOFT).move_to(box))
        left_values.move_to(ORIGIN).shift(UP * 0.45)
        label = Text("左半边的最大值", font=FONT, font_size=30, color=MUTED).next_to(left_values, UP, buff=0.42)
        eleven = left_values[-1]
        halo = SurroundingRectangle(eleven, color=YELLOW_ACCENT, buff=0.08, corner_radius=0.14, stroke_width=5)
        answer = Text("总数为奇数  →  中位数 = 11", font=FONT, font_size=38, color=YELLOW_ACCENT)
        answer.next_to(left_values, DOWN, buff=0.62)
        caption = self.caption("max(A左最大, B左最大) = max(9, 11) = 11")
        self.play(Write(title), FadeIn(label), FadeIn(left_values, lag_ratio=0.1))
        self.play(Create(halo), Write(answer), FadeIn(caption))
        self.wait(1.8)

        even_title = Text("如果总数为偶数", font=FONT, font_size=32, color=PURPLE)
        even_title.move_to(label)
        even_formula = Text(
            "( 左边最大值 + 右边最小值 ) / 2",
            font=FONT,
            font_size=35,
            color=WHITE_SOFT,
        ).move_to(answer)
        self.play(Transform(label, even_title), Transform(answer, even_formula), FadeOut(halo))
        self.play(Transform(caption, self.caption("例如 [1,2] 与 [3,4]：答案是 (2+3)/2 = 2.5")))
        self.wait(1.8)

        sentinels = VGroup(
            Text("切在数组最左端：左边界视为 −∞", font=FONT, font_size=29, color=BLUE_A),
            Text("切在数组最右端：右边界视为 +∞", font=FONT, font_size=29, color=BLUE_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(ORIGIN)
        self.play(*[FadeOut(mob) for mob in [left_values, label, answer, title]])
        self.play(FadeIn(sentinels, lag_ratio=0.25))
        self.play(Transform(caption, self.caption("哨兵消除了边界分支：Rust 中正好对应 i32::MIN / i32::MAX")))
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def map_to_rust(self) -> None:
        title = self.heading("回到 p0004.rs：每一行都对应一个几何量")
        code_lines = [
            ("if nums1.len() > nums2.len() { swap }", BLUE_A),
            ("half_l = (m + n + 1) / 2", YELLOW_ACCENT),
            ("i = (left + right) / 2", PURPLE),
            ("j = half_l - i", PURPLE),
            ("A左 ≤ B右  &&  B左 ≤ A右", GREEN_OK),
            ("right = i - 1  /  left = i + 1", RED_BAD),
        ]
        code = VGroup(
            *[
                Text(line, font=MONO, font_size=27, color=color)
                for line, color in code_lines
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        panel = RoundedRectangle(
            width=10.8,
            height=4.2,
            corner_radius=0.22,
            stroke_color="#344563",
            fill_color="#0C1324",
            fill_opacity=1,
        )
        code.move_to(panel)
        group = VGroup(panel, code).shift(DOWN * 0.12)
        caption = self.caption("先保证 A 更短，才能把复杂度锁定在更小的搜索空间")
        self.play(Write(title), FadeIn(panel))
        for line in code:
            self.play(FadeIn(line, shift=RIGHT * 0.18), run_time=0.42)
        self.play(FadeIn(caption))
        self.wait(2.2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def complexity_finale(self) -> None:
        title = Text("不是寻找中位数", font=FONT, font_size=44, color=MUTED)
        insight = Text("而是寻找正确的分割线", font=FONT, font_size=58, weight=BOLD, color=YELLOW_ACCENT)
        pair = VGroup(title, insight).arrange(DOWN, buff=0.28).shift(UP * 1.2)
        time = Text("时间  O(log min(m,n))", font=MONO, font_size=37, color=GREEN_OK)
        space = Text("空间  O(1)", font=MONO, font_size=37, color=BLUE_A)
        costs = VGroup(time, space).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(pair, DOWN, buff=0.72)
        divider = Line(LEFT * 4.6, RIGHT * 4.6, color="#263552", stroke_width=2).next_to(costs, DOWN, buff=0.55)
        footer = Text(
            "LeetCode 4 · 寻找两个正序数组的中位数",
            font=FONT,
            font_size=26,
            color=MUTED,
        ).next_to(divider, DOWN, buff=0.34)
        self.play(FadeIn(title, shift=UP * 0.2))
        self.play(Write(insight), run_time=1.2)
        self.play(FadeIn(costs, lag_ratio=0.3), Create(divider), FadeIn(footer))
        self.wait(3.0)
        self.play(FadeOut(VGroup(pair, costs, divider, footer)), run_time=1.2)
