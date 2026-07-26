from __future__ import annotations

from manim import *

BG = "#070B16"
WHITE_SOFT = "#E8EEF9"
BLUE_A = "#58C4DD"
YELLOW = "#F7C948"
GREEN = "#4DD599"
PURPLE = "#A78BFA"
RED = "#FF6B6B"
MUTED = "#8290A7"
PANEL = "#10182B"
FONT = "Noto Sans SC"
MONO = "Maple Mono NF CN"


class IndexedArray(VGroup):
    """An integer array whose index labels stay aligned with their cells."""

    def __init__(self, values: list[int], cell_size: float = 0.82) -> None:
        super().__init__()
        self.cells = VGroup()
        self.numbers = VGroup()
        self.indices = VGroup()
        for index, value in enumerate(values):
            cell = RoundedRectangle(
                width=cell_size, height=cell_size, corner_radius=0.12,
                stroke_color=BLUE_A, stroke_width=2.5,
                fill_color=BLUE_A, fill_opacity=0.08,
            )
            number = Text(str(value), font=MONO, font_size=29, color=WHITE_SOFT).move_to(cell)
            index_text = Text(str(index), font=MONO, font_size=17, color=MUTED).next_to(cell, DOWN, buff=0.1)
            self.cells.add(cell)
            self.numbers.add(number)
            self.indices.add(index_text)
        self.cells.arrange(RIGHT, buff=0.1)
        for cell, number, index_text in zip(self.cells, self.numbers, self.indices):
            number.move_to(cell)
            index_text.next_to(cell, DOWN, buff=0.1)
        self.add(self.cells, self.numbers, self.indices)

    def marker(self, index: int, color: str = YELLOW) -> SurroundingRectangle:
        return SurroundingRectangle(
            self.cells[index], color=color, buff=0.065,
            corner_radius=0.14, stroke_width=4,
        )


class ThreeEqualElementsDistanceII(Scene):
    """LeetCode 3741: group positions, then inspect consecutive triples."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.opening()
        self.distance_formula()
        self.consecutive_triples()
        self.grouping_walkthrough()
        self.iterator_pipeline()
        self.compare_with_i()
        self.rust_solution()
        self.finale()

    def heading(self, text: str, color: str = WHITE_SOFT) -> Text:
        return Text(text, font=FONT, font_size=42, weight=BOLD, color=color).to_edge(UP, buff=0.42)

    def caption(self, text: str, color: str = WHITE_SOFT) -> VGroup:
        plate = RoundedRectangle(
            width=12.2, height=0.68, corner_radius=0.16,
            fill_color=PANEL, fill_opacity=0.96,
            stroke_color="#263552", stroke_width=1.5,
        )
        words = Text(text, font=FONT, font_size=24, color=color).move_to(plate)
        return VGroup(plate, words).to_edge(DOWN, buff=0.24)

    def clear(self) -> None:
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

    def opening(self) -> None:
        title = Text("三个相等元素之间的最小距离 II", font=FONT, font_size=49, weight=BOLD, gradient=(BLUE_A, PURPLE))
        subtitle = Text("LeetCode 3741 · Rust 分组滑窗", font=FONT, font_size=29, color=WHITE_SOFT)
        rule = Line(LEFT * 4.1, RIGHT * 4.1, color=YELLOW, stroke_width=4)
        hero = VGroup(title, rule, subtitle).arrange(DOWN, buff=0.27).shift(UP * 0.65)
        prompt = Text("不枚举三元组，怎样一次扫描找到最短跨度？", font=FONT, font_size=31, color=YELLOW)
        prompt.next_to(hero, DOWN, buff=0.66)
        self.play(Write(title), GrowFromCenter(rule), FadeIn(subtitle, shift=UP * 0.15))
        self.play(FadeIn(prompt, shift=UP * 0.12))
        self.wait(1.7)
        self.clear()

    def distance_formula(self) -> None:
        title = self.heading("距离公式：中间下标会抵消")
        arr = IndexedArray([7, 2, 7, 7, 3, 2, 2, 2]).scale(0.94).shift(UP * 0.62)
        labels = VGroup(
            Text("i = 1", font=MONO, font_size=25, color=YELLOW),
            Text("j = 5", font=MONO, font_size=25, color=YELLOW),
            Text("k = 6", font=MONO, font_size=25, color=YELLOW),
        )
        labels.arrange(RIGHT, buff=0.7).shift(DOWN * 0.57)
        formula = Text("(j − i) + (k − j) + (k − i)  =  2 × (k − i)", font=MONO, font_size=31, color=GREEN).shift(DOWN * 1.48)
        cap = self.caption("只要固定最左和最右的相等元素；中间位置不影响总距离")
        marks = [arr.marker(i) for i in (1, 5, 6)]
        self.play(Write(title), FadeIn(arr))
        self.play(*[Create(mark) for mark in marks], FadeIn(labels), FadeIn(formula), FadeIn(cap))
        self.wait(2.1)
        self.clear()

    def consecutive_triples(self) -> None:
        title = self.heading("关键结论：只检查同值的连续三个位置")
        positions = VGroup(*[
            RoundedRectangle(width=1.0, height=0.78, corner_radius=0.12, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.22).shift(UP * 0.85)
        values = [1, 5, 6, 7, 12]
        for box, value in zip(positions, values):
            box.add(Text(str(value), font=MONO, font_size=30, color=WHITE_SOFT).move_to(box))
        positions_label = Text("值 2 出现的位置", font=FONT, font_size=28, color=PURPLE).next_to(positions, UP, buff=0.34)
        candidates = VGroup(
            Text("[1, 5, 6]  →  2 × (6 − 1) = 10", font=MONO, font_size=26, color=WHITE_SOFT),
            Text("[5, 6, 7]  →  2 × (7 − 5) = 4", font=MONO, font_size=26, color=GREEN),
            Text("[6, 7, 12] →  2 × (12 − 6) = 12", font=MONO, font_size=26, color=WHITE_SOFT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN * 1.02)
        cap = self.caption("如果三元组跳过中间出现的位置，换成它只会让两端更近，绝不会更差")
        windows = [SurroundingRectangle(VGroup(*positions[i:i + 3]), color=YELLOW, buff=0.09, corner_radius=0.15) for i in range(3)]
        self.play(Write(title), FadeIn(positions), FadeIn(positions_label), FadeIn(cap))
        for window, line in zip(windows, candidates):
            self.play(Create(window), FadeIn(line, shift=RIGHT * 0.12), run_time=0.65)
            self.play(FadeOut(window), run_time=0.25)
        self.play(Circumscribe(candidates[1], color=GREEN))
        self.wait(1.5)
        self.clear()

    def grouping_walkthrough(self) -> None:
        title = self.heading("一次扫描：把每个值的下标收集起来")
        arr = IndexedArray([7, 2, 7, 7, 3, 2, 2, 2]).scale(0.88).shift(UP * 1.25)
        mapping = VGroup(
            Text("7  →  [0, 2, 3]", font=MONO, font_size=31, color=BLUE_A),
            Text("2  →  [1, 5, 6, 7]", font=MONO, font_size=31, color=PURPLE),
            Text("3  →  [4]", font=MONO, font_size=31, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 0.42)
        cap = self.caption("HashMap 的键是数值，值是按扫描顺序自然递增的下标 Vec")
        self.play(Write(title), FadeIn(arr), FadeIn(cap))
        for line in mapping:
            self.play(FadeIn(line, shift=RIGHT * 0.18), run_time=0.5)
        check_7 = Text("[0, 2, 3]  →  2 × (3 − 0) = 6", font=MONO, font_size=27, color=BLUE_A).shift(DOWN * 2.13)
        check_2 = Text("[5, 6, 7]  →  2 × (7 − 5) = 4  ✓", font=MONO, font_size=27, color=GREEN).move_to(check_7)
        self.play(Write(check_7))
        self.play(Transform(check_7, check_2), Transform(cap, self.caption("遍历 windows(3)，全局取 min；答案是 4")))
        self.wait(1.7)
        self.clear()

    def iterator_pipeline(self) -> None:
        title = self.heading("Rust 管道：分组后，滑动窗口求最小值")
        stages = [
            ("enumerate()", "(下标, 值)", BLUE_A, "给每个元素编号"),
            ("fold(HashMap)", "值 → 下标列表", PURPLE, "按值分组"),
            ("windows(3)", "连续三元组", YELLOW, "只看候选窗口"),
            ("2 × (w₂ − w₀)", "距离", GREEN, "首尾决定答案"),
            ("min()", "最小距离", GREEN, "汇总所有值"),
        ]
        blocks = VGroup()
        for api, output, color, note in stages:
            panel = RoundedRectangle(width=2.18, height=1.58, corner_radius=0.16, stroke_color=color, stroke_width=2.3, fill_color=color, fill_opacity=0.1)
            text = VGroup(
                Text(api, font=MONO, font_size=20, color=color),
                Text(output, font=FONT, font_size=21, color=WHITE_SOFT),
                Text(note, font=FONT, font_size=17, color=MUTED),
            ).arrange(DOWN, buff=0.12).move_to(panel)
            blocks.add(VGroup(panel, text))
        blocks.arrange(RIGHT, buff=0.2).scale(0.88).shift(UP * 0.28)
        arrows = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.06, color=MUTED, stroke_width=2.6, max_tip_length_to_length_ratio=0.16) for i in range(4)])
        cap = self.caption("所有迭代器都是惰性的；min() 才消费数据流并产出最终答案")
        self.play(Write(title))
        for index, block in enumerate(blocks):
            animations = [FadeIn(block, shift=RIGHT * 0.12)]
            if index:
                animations.append(GrowArrow(arrows[index - 1]))
            self.play(*animations, run_time=0.48)
        self.play(FadeIn(cap))
        self.wait(2.0)
        self.clear()

    def compare_with_i(self) -> None:
        title = self.heading("和 3740-I 相同题意，不同约束，不同策略")
        left_panel = RoundedRectangle(width=5.65, height=4.35, corner_radius=0.2, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.06)
        right_panel = RoundedRectangle(width=5.65, height=4.35, corner_radius=0.2, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.06)
        panels = VGroup(left_panel, right_panel).arrange(RIGHT, buff=0.42).shift(DOWN * 0.2)
        i_content = VGroup(
            Text("3740 · I", font=FONT, font_size=34, color=YELLOW, weight=BOLD),
            Text("从每个起点向后找两次", font=FONT, font_size=25, color=WHITE_SOFT),
            Text("find_next(...) × 2", font=MONO, font_size=24, color=YELLOW),
            Text("小规模可接受", font=FONT, font_size=24, color=MUTED),
            Text("时间  O(n²)\n空间  O(1)*", font=MONO, font_size=25, color=RED),
        ).arrange(DOWN, buff=0.23).move_to(left_panel)
        ii_content = VGroup(
            Text("3741 · II", font=FONT, font_size=34, color=GREEN, weight=BOLD),
            Text("先按值收集所有位置", font=FONT, font_size=25, color=WHITE_SOFT),
            Text("HashMap + windows(3)", font=MONO, font_size=24, color=GREEN),
            Text("大规模仍只扫描一遍", font=FONT, font_size=24, color=MUTED),
            Text("时间  O(n)\n空间  O(n)", font=MONO, font_size=25, color=GREEN),
        ).arrange(DOWN, buff=0.23).move_to(right_panel)
        cap = self.caption("*3740 的当前实现还在每轮 clone nums；实际额外分配也会随 n 增长")
        self.play(Write(title), FadeIn(panels), FadeIn(i_content), FadeIn(ii_content), FadeIn(cap))
        self.play(Circumscribe(ii_content[2], color=GREEN), run_time=0.8)
        self.wait(2.4)
        self.clear()

    def rust_solution(self) -> None:
        title = self.heading("对应 3741.rs：每一段都在缩小搜索空间")
        lines = [
            ("nums.iter().enumerate()", BLUE_A),
            (".fold(HashMap::new(), |mut map, (i, x)| {", PURPLE),
            ("    map.entry(x).or_insert_with(Vec::new).push(i);", WHITE_SOFT),
            ("    map", WHITE_SOFT),
            ("})", PURPLE),
            (".values().filter(|v| v.len() >= 3)", YELLOW),
            (".flat_map(|v| v.windows(3).map(|w| 2 * (w[2] - w[0])))", GREEN),
            (".min().map_or(-1, |ans| ans as i32)", GREEN),
        ]
        code = VGroup(*[Text(line, font=MONO, font_size=22, color=color) for line, color in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        panel = RoundedRectangle(width=12.25, height=5.2, corner_radius=0.2, stroke_color="#344563", fill_color="#0C1324", fill_opacity=1)
        code.move_to(panel)
        cap = self.caption("没有出现三次的值直接过滤；全部过滤掉时 map_or 返回 −1")
        self.play(Write(title), FadeIn(panel))
        for line in code:
            self.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.27)
        self.play(FadeIn(cap))
        self.wait(2.2)
        self.clear()

    def finale(self) -> None:
        insight = Text("按值分组  +  连续三元窗口", font=FONT, font_size=51, weight=BOLD, color=YELLOW).shift(UP * 1.1)
        conclusion = Text("把 O(n²) 的重复查找，变成 O(n) 的一次扫描", font=FONT, font_size=34, color=WHITE_SOFT).next_to(insight, DOWN, buff=0.4)
        costs = VGroup(
            Text("时间  O(n)", font=MONO, font_size=37, color=GREEN),
            Text("额外空间  O(n)", font=MONO, font_size=37, color=BLUE_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(conclusion, DOWN, buff=0.56)
        divider = Line(LEFT * 4.8, RIGHT * 4.8, color="#263552", stroke_width=2).next_to(costs, DOWN, buff=0.55)
        footer = Text("LeetCode 3741 · 三个相等元素之间的最小距离 II", font=FONT, font_size=25, color=MUTED).next_to(divider, DOWN, buff=0.32)
        self.play(Write(insight), run_time=1.15)
        self.play(FadeIn(conclusion), FadeIn(costs, lag_ratio=0.2), Create(divider), FadeIn(footer))
        self.wait(3.0)
