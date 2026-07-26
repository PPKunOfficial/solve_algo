from __future__ import annotations

from manim import *

BG = "#070B16"
WHITE_SOFT = "#E8EEF9"
BLUE_A = "#58C4DD"
BLUE_B = "#5B8FF9"
YELLOW_ACCENT = "#F7C948"
GREEN_OK = "#4DD599"
PURPLE = "#A78BFA"
MUTED = "#8290A7"
PANEL = "#10182B"
FONT = "Noto Sans SC"
MONO = "Maple Mono NF CN"


class ArrayRow(VGroup):
    """Stable geometry for an indexed integer array."""

    def __init__(self, label: str, values: list[int], color: str, cell_size: float = 0.82) -> None:
        super().__init__()
        self.cells = VGroup()
        self.numbers = VGroup()
        self.indices = VGroup()
        for index, value in enumerate(values):
            cell = RoundedRectangle(
                width=cell_size,
                height=cell_size,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2.5,
                fill_color=color,
                fill_opacity=0.09,
            )
            number = Text(str(value), font=MONO, font_size=31, color=WHITE_SOFT).move_to(cell)
            position = Text(str(index), font=MONO, font_size=17, color=MUTED).next_to(cell, DOWN, buff=0.1)
            self.cells.add(cell)
            self.numbers.add(number)
            self.indices.add(position)
        self.cells.arrange(RIGHT, buff=0.1)
        for cell, number, position in zip(self.cells, self.numbers, self.indices):
            number.move_to(cell)
            position.next_to(cell, DOWN, buff=0.1)
        self.label = Text(label, font=MONO, font_size=27, color=color).next_to(self.cells, LEFT, buff=0.3)
        self.add(self.label, self.cells, self.numbers, self.indices)


class ShuffleArrayExplainer(Scene):
    """Visual explanation of LeetCode 1470's zip + flat_map Rust solution."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.opening()
        self.split_problem()
        self.walkthrough()
        self.iterator_pipeline()
        self.map_vs_flat_map()
        self.rust_solution()
        self.finale()

    def heading(self, content: str, color: str = WHITE_SOFT) -> Text:
        return Text(content, font=FONT, font_size=42, weight=BOLD, color=color).to_edge(UP, buff=0.42)

    def caption(self, content: str, color: str = WHITE_SOFT) -> VGroup:
        plate = RoundedRectangle(
            width=12.2,
            height=0.68,
            corner_radius=0.16,
            fill_color=PANEL,
            fill_opacity=0.96,
            stroke_color="#263552",
            stroke_width=1.5,
        )
        words = Text(content, font=FONT, font_size=24, color=color).move_to(plate)
        return VGroup(plate, words).to_edge(DOWN, buff=0.24)

    def clear(self) -> None:
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.6)

    def opening(self) -> None:
        title = Text("重新排列数组", font=FONT, font_size=58, weight=BOLD, gradient=(BLUE_A, PURPLE))
        subtitle = Text("LeetCode 1470 · Rust 迭代器解法", font=FONT, font_size=30, color=WHITE_SOFT)
        rule = Line(LEFT * 3.85, RIGHT * 3.85, color=YELLOW_ACCENT, stroke_width=4)
        hero = VGroup(title, rule, subtitle).arrange(DOWN, buff=0.28).shift(UP * 0.8)
        prompt = Text("两段并排的数据，怎样交错成一段？", font=FONT, font_size=32, color=YELLOW_ACCENT)
        prompt.next_to(hero, DOWN, buff=0.68)
        self.play(Write(title), GrowFromCenter(rule), FadeIn(subtitle, shift=UP * 0.15))
        self.play(FadeIn(prompt, shift=UP * 0.12))
        self.wait(1.5)
        self.clear()

    def split_problem(self) -> None:
        title = self.heading("题目结构：从中间切开")
        source = ArrayRow("nums", [2, 5, 1, 3, 4, 7], BLUE_A).shift(UP * 0.65)
        divider_x = (source.cells[2].get_right()[0] + source.cells[3].get_left()[0]) / 2
        divider = DashedLine([divider_x, 1.45, 0], [divider_x, -0.7, 0], dash_length=0.1, color=YELLOW_ACCENT, stroke_width=4)
        left_label = Text("x = [2, 5, 1]", font=MONO, font_size=25, color=BLUE_A)
        right_label = Text("y = [3, 4, 7]", font=MONO, font_size=25, color=PURPLE)
        left_label.move_to([source.cells[1].get_center()[0] - 0.28, -1.05, 0])
        right_label.move_to([source.cells[4].get_center()[0] + 0.28, -1.05, 0])
        target = Text("输出顺序：x1, y1, x2, y2, ...", font=MONO, font_size=27, color=GREEN_OK).shift(DOWN * 2.0)
        cap = self.caption("前半段是 x，后半段是 y；两段长度都等于 n")
        self.play(Write(title), FadeIn(source), Create(divider))
        self.play(FadeIn(left_label, shift=UP * 0.1), FadeIn(right_label, shift=UP * 0.1), FadeIn(target), FadeIn(cap))
        self.wait(2.0)
        self.clear()

    def walkthrough(self) -> None:
        title = self.heading("用样例走一遍：每轮输出 xᵢ，再输出 yᵢ")
        left = ArrayRow("x", [2, 5, 1], BLUE_A, 0.9).shift(UP * 1.45 + LEFT * 2.7)
        right = ArrayRow("y", [3, 4, 7], PURPLE, 0.9).shift(UP * 1.45 + RIGHT * 2.5)
        output = ArrayRow("ans", ["?", "?", "?", "?", "?", "?"], GREEN_OK, 0.78).shift(DOWN * 1.0)
        output.label.set_color(GREEN_OK)
        cap = self.caption("第 0 对：(2, 3)；把 2、3 按顺序放进答案")
        operation = Text("i = 0", font=MONO, font_size=30, color=YELLOW_ACCENT).shift(UP * 0.28)
        self.play(Write(title), FadeIn(left), FadeIn(right), FadeIn(output), FadeIn(operation), FadeIn(cap))

        answer_values = [2, 3, 5, 4, 1, 7]
        notes = [
            "第 0 对：(2, 3)；把 2、3 按顺序放进答案",
            "第 1 对：(5, 4)；答案接着追加 5、4",
            "第 2 对：(1, 7)；所有对应位置恰好配完",
        ]
        for i, note in enumerate(notes):
            next_operation = Text(f"i = {i}  →  ({left.numbers[i].text}, {right.numbers[i].text})", font=MONO, font_size=30, color=YELLOW_ACCENT).move_to(operation)
            left_focus = SurroundingRectangle(left.cells[i], color=YELLOW_ACCENT, buff=0.07, corner_radius=0.14, stroke_width=4)
            right_focus = SurroundingRectangle(right.cells[i], color=YELLOW_ACCENT, buff=0.07, corner_radius=0.14, stroke_width=4)
            self.play(Transform(operation, next_operation), Create(left_focus), Create(right_focus), run_time=0.55)
            for out_index in (2 * i, 2 * i + 1):
                replacement = Text(str(answer_values[out_index]), font=MONO, font_size=31, color=WHITE_SOFT).move_to(output.cells[out_index])
                self.play(
                    Transform(output.numbers[out_index], replacement),
                    output.cells[out_index].animate.set_fill(GREEN_OK, opacity=0.2),
                    run_time=0.35,
                )
            self.play(Transform(cap, self.caption(note)), FadeOut(left_focus), FadeOut(right_focus), run_time=0.4)
        result = Text("[2, 3, 5, 4, 1, 7]", font=MONO, font_size=37, color=GREEN_OK, weight=BOLD).shift(DOWN * 2.2)
        self.play(FadeOut(operation), Write(result))
        self.wait(1.7)
        self.clear()

    def iterator_pipeline(self) -> None:
        title = self.heading("Rust 迭代器：把“切片、配对、展开”写成数据流")
        stages = [
            ("nums[..n]", "[2, 5, 1]", BLUE_A, "前半段切片", 23, 19),
            (".zip(&nums[n..])", "(2,3)  (5,4)  (1,7)", PURPLE, "一一配对", 18, 15),
            (".flat_map", "2  3  5  4  1  7", GREEN_OK, "每对展开", 20, 16),
            (".collect()", "Vec<i32>", YELLOW_ACCENT, "收集答案", 20, 19),
        ]
        blocks = VGroup()
        for api, data, color, label, api_size, data_size in stages:
            panel = RoundedRectangle(width=2.65, height=1.55, corner_radius=0.17, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.1)
            words = VGroup(
                Text(api, font=MONO, font_size=api_size, color=color),
                Text(data, font=MONO, font_size=data_size, color=WHITE_SOFT),
                Text(label, font=FONT, font_size=20, color=MUTED),
            ).arrange(DOWN, buff=0.15).move_to(panel)
            blocks.add(VGroup(panel, words))
        blocks.arrange(RIGHT, buff=0.34).shift(UP * 0.25)
        arrows = VGroup(*[Arrow(blocks[i].get_right(), blocks[i + 1].get_left(), buff=0.1, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.14) for i in range(3)])
        cap = self.caption("每个方法都对应一个清晰动作；末尾 collect() 才真正消费并生成 Vec")
        self.play(Write(title))
        for index, block in enumerate(blocks):
            animations = [FadeIn(block, shift=RIGHT * 0.15)]
            if index:
                animations.append(GrowArrow(arrows[index - 1]))
            self.play(*animations, run_time=0.6)
        self.play(FadeIn(cap))
        self.wait(2.2)
        self.clear()

    def map_vs_flat_map(self) -> None:
        title = self.heading("为什么是 flat_map：目标需要一维数组")
        pair = Text("每对输入  (x, y)", font=MONO, font_size=34, color=WHITE_SOFT).shift(UP * 1.8)
        mapped = VGroup(
            Text("map(|(&x, &y)| [x, y])", font=MONO, font_size=26, color=PURPLE),
            Text("→  Vec<[i32; 2]>", font=MONO, font_size=30, color=PURPLE),
            Text("[[2,3], [5,4], [1,7]]", font=MONO, font_size=24, color=WHITE_SOFT),
        ).arrange(DOWN, buff=0.18)
        flattened = VGroup(
            Text("flat_map(|(&x, &y)| [x, y])", font=MONO, font_size=26, color=GREEN_OK),
            Text("→  Vec<i32>", font=MONO, font_size=30, color=GREEN_OK),
            Text("[2, 3, 5, 4, 1, 7]", font=MONO, font_size=24, color=WHITE_SOFT),
        ).arrange(DOWN, buff=0.18)
        columns = VGroup(mapped, flattened).arrange(RIGHT, buff=1.15).shift(DOWN * 0.25)
        divider = Line([0, -1.9, 0], [0, 1.0, 0], color="#263552", stroke_width=2)
        cap = self.caption("map 保留每轮产出的数组；flat_map 把这些小数组摊平成连续元素")
        self.play(Write(title), FadeIn(pair, shift=DOWN * 0.12))
        self.play(FadeIn(mapped, shift=RIGHT * 0.18), Create(divider), FadeIn(flattened, shift=LEFT * 0.18), FadeIn(cap))
        self.play(Circumscribe(flattened[2], color=GREEN_OK), run_time=0.8)
        self.wait(2.0)
        self.clear()

    def rust_solution(self) -> None:
        title = self.heading("对应题解：没有显式索引，意图直接写在管道里")
        lines = [
            ("let n = n as usize;", YELLOW_ACCENT),
            ("nums[..n]", BLUE_A),
            ("    .iter()", WHITE_SOFT),
            ("    .zip(&nums[n..])", PURPLE),
            ("    .flat_map(|(&x, &y)| [x, y])", GREEN_OK),
            ("    .collect()", YELLOW_ACCENT),
        ]
        code = VGroup(*[Text(line, font=MONO, font_size=29, color=color) for line, color in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel = RoundedRectangle(width=11.8, height=4.45, corner_radius=0.22, stroke_color="#344563", fill_color="#0C1324", fill_opacity=1)
        code.move_to(panel).shift(UP * 0.08)
        notes = Text("切片  →  借用迭代  →  配对  →  展平  →  收集", font=FONT, font_size=28, color=WHITE_SOFT).next_to(panel, DOWN, buff=0.35)
        cap = self.caption("i32 是 Copy，|(&x, &y)| 可从 (&i32, &i32) 直接取出数值")
        self.play(Write(title), FadeIn(panel))
        for line in code:
            self.play(FadeIn(line, shift=RIGHT * 0.12), run_time=0.38)
        self.play(FadeIn(notes), FadeIn(cap))
        self.wait(2.1)
        self.clear()

    def finale(self) -> None:
        insight = Text("等长配对 + 交错输出  →  zip + flat_map", font=FONT, font_size=48, weight=BOLD, color=YELLOW_ACCENT).shift(UP * 1.15)
        costs = VGroup(
            Text("时间  O(n)", font=MONO, font_size=37, color=GREEN_OK),
            Text("额外空间  O(n)", font=MONO, font_size=37, color=BLUE_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(insight, DOWN, buff=0.65)
        divider = Line(LEFT * 4.8, RIGHT * 4.8, color="#263552", stroke_width=2).next_to(costs, DOWN, buff=0.55)
        footer = Text("LeetCode 1470 · 重新排列数组", font=FONT, font_size=26, color=MUTED).next_to(divider, DOWN, buff=0.34)
        self.play(Write(insight), run_time=1.25)
        self.play(FadeIn(costs, lag_ratio=0.25), Create(divider), FadeIn(footer))
        self.wait(3.0)
