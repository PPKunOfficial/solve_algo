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


class NumberArray(VGroup):
    """Fixed-geometry array that can reveal its index and sign state."""

    def __init__(self, values: list[int]) -> None:
        super().__init__()
        self.values = values.copy()
        self.boxes = VGroup()
        self.numbers = VGroup()
        self.indices = VGroup()
        for i, value in enumerate(values):
            box = RoundedRectangle(
                width=1.02,
                height=0.88,
                corner_radius=0.12,
                stroke_color=BLUE_A,
                stroke_width=2,
                fill_color=BLUE_A,
                fill_opacity=0.08,
            )
            number = Text(str(value), font=MONO, font_size=31, color=WHITE_SOFT).move_to(box)
            index = Text(str(i), font=MONO, font_size=19, color=MUTED).next_to(box, DOWN, buff=0.12)
            self.boxes.add(box)
            self.numbers.add(number)
            self.indices.add(index)
        self.boxes.arrange(RIGHT, buff=0.1)
        for box, number, index in zip(self.boxes, self.numbers, self.indices):
            number.move_to(box)
            index.next_to(box, DOWN, buff=0.12)
        self.add(self.boxes, self.numbers, self.indices)

    def changed_number(self, index: int, value: int, color: str = WHITE_SOFT) -> Text:
        return Text(str(value), font=MONO, font_size=31, color=color).move_to(self.boxes[index])


class FindAllDisappearedNumbers(Scene):
    """Visual explanation for LeetCode 448's in-place sign-marking Rust solution."""

    def construct(self) -> None:
        self.camera.background_color = BG
        self.opening()
        self.key_observation()
        self.walkthrough()
        self.collect_answer()
        self.map_to_rust()
        self.finale()

    def heading(self, text: str, color: str = WHITE_SOFT) -> Text:
        return Text(text, font=FONT, font_size=42, weight=BOLD, color=color).to_edge(UP, buff=0.42)

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
        words = Text(text, font=FONT, font_size=25, color=color).move_to(plate)
        return VGroup(plate, words).to_edge(DOWN, buff=0.24)

    def clear(self) -> None:
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.65)

    def opening(self) -> None:
        title = Text("找到所有数组中消失的数字", font=FONT, font_size=55, weight=BOLD, gradient=(BLUE_A, PURPLE))
        subtitle = Text("LeetCode 448 · 原地标记进阶做法", font=FONT, font_size=30, color=WHITE_SOFT)
        rule = Line(LEFT * 4.2, RIGHT * 4.2, color=YELLOW_ACCENT, stroke_width=4)
        group = VGroup(title, rule, subtitle).arrange(DOWN, buff=0.28)
        prompt = Text("不借助哈希表，怎么记住哪些数字出现过？", font=FONT, font_size=30, color=YELLOW_ACCENT)
        prompt.next_to(group, DOWN, buff=0.7)
        self.play(Write(title), GrowFromCenter(rule), FadeIn(subtitle, shift=UP * 0.15))
        self.play(FadeIn(prompt, shift=UP * 0.15))
        self.wait(1.4)
        self.clear()

    def key_observation(self) -> None:
        title = self.heading("数组本身，就是一张可复用的签到表")
        domain = Text("nums 中每个数都在 1 … n", font=MONO, font_size=39, color=YELLOW_ACCENT).shift(UP * 1.85)
        mapping = VGroup(
            Text("数字 x 出现过", font=FONT, font_size=32, color=WHITE_SOFT),
            Text("→", font=MONO, font_size=36, color=MUTED),
            Text("第 x−1 格改成负数", font=FONT, font_size=32, color=GREEN_OK),
        ).arrange(RIGHT, buff=0.22)
        mapping.move_to(ORIGIN).shift(UP * 0.15)
        example = VGroup(
            Text("看到 4", font=FONT, font_size=30, color=BLUE_A),
            Text("→", font=MONO, font_size=32, color=MUTED),
            Text("标记 nums[3]", font=MONO, font_size=30, color=PURPLE),
        ).arrange(RIGHT, buff=0.18).shift(DOWN * 1.15)
        caption = self.caption("数值 x 映射到下标 x−1；正负号只表示“是否签到”，绝对值仍是原来的数")
        self.play(Write(title), FadeIn(domain, shift=DOWN * 0.15))
        self.play(FadeIn(mapping, lag_ratio=0.15))
        self.play(FadeIn(example, shift=UP * 0.15), FadeIn(caption))
        self.wait(2.2)
        self.clear()

    def walkthrough(self) -> None:
        title = self.heading("用样例走一遍：每次把对应位置变负")
        values = [4, 3, 2, 7, 8, 2, 3, 1]
        array = NumberArray(values).move_to(ORIGIN).shift(UP * 0.65)
        label = Text("nums", font=MONO, font_size=29, color=BLUE_A).next_to(array.boxes, LEFT, buff=0.3)
        caption = self.caption("处理 i=0：nums[0]=4，所以标记下标 4−1=3")
        self.play(Write(title), FadeIn(array), FadeIn(label), FadeIn(caption))

        steps = [
            (0, 4, 3, "i=0，x=|4|=4  →  标记 nums[3]", "把 7 变成 −7：数字 4 已签到"),
            (1, 3, 2, "i=1，x=|3|=3  →  标记 nums[2]", "把 2 变成 −2：数字 3 已签到"),
            (2, 2, 1, "i=2，x=|−2|=2  →  标记 nums[1]", "先取 abs，标记不会被之前的负号干扰"),
            (3, 7, 6, "i=3，x=|−7|=7  →  标记 nums[6]", "继续把第 x−1 格变负"),
            (4, 8, 7, "i=4，x=|8|=8  →  标记 nums[7]", "数字 8 也已经签到"),
        ]
        state = values.copy()
        operation = Text("", font=MONO, font_size=27, color=YELLOW_ACCENT).next_to(array, UP, buff=0.7)
        for i, x, target, text, note in steps:
            next_operation = Text(text, font=MONO, font_size=27, color=YELLOW_ACCENT).move_to(operation)
            pointer = SurroundingRectangle(array.boxes[i], color=YELLOW_ACCENT, buff=0.07, corner_radius=0.14, stroke_width=4)
            target_box = SurroundingRectangle(array.boxes[target], color=PURPLE, buff=0.07, corner_radius=0.14, stroke_width=4)
            state[target] = -abs(state[target])
            replacement = array.changed_number(target, state[target], GREEN_OK)
            self.play(Transform(operation, next_operation), Create(pointer), Create(target_box), run_time=0.55)
            self.play(Transform(array.numbers[target], replacement), array.boxes[target].animate.set_fill(GREEN_OK, opacity=0.16), run_time=0.55)
            self.play(Transform(caption, self.caption(note)), FadeOut(pointer), FadeOut(target_box), run_time=0.45)

        duplicate = Text("后面再次遇到 2、3：目标格已经是负数，重复标记也安全", font=FONT, font_size=28, color=GREEN_OK)
        duplicate.next_to(array, DOWN, buff=0.7)
        self.play(FadeOut(operation), FadeIn(duplicate, shift=UP * 0.15))
        self.play(Transform(caption, self.caption("关键是 −abs(nums[index])：无论原来正负，结果始终保持为负")))
        self.wait(1.8)
        self.clear()

    def collect_answer(self) -> None:
        title = self.heading("仍为正数的位置，从未被任何数字指向")
        final_values = [-4, -3, -2, -7, 8, 2, -3, -1]
        array = NumberArray(final_values).move_to(ORIGIN).shift(UP * 0.75)
        for i, value in enumerate(final_values):
            if value < 0:
                array.numbers[i].set_color(MUTED)
                array.boxes[i].set_fill(GREEN_OK, opacity=0.09)
            else:
                array.numbers[i].set_color(YELLOW_ACCENT)
                array.boxes[i].set_stroke(YELLOW_ACCENT, width=4)
                array.boxes[i].set_fill(YELLOW_ACCENT, opacity=0.16)
        scan = Text("扫描下标 i：nums[i] > 0  就收集 i+1", font=MONO, font_size=30, color=WHITE_SOFT).next_to(array, UP, buff=0.68)
        answer = Text("正数在下标 4、5  →  缺失数字 [5, 6]", font=FONT, font_size=37, weight=BOLD, color=YELLOW_ACCENT).shift(DOWN * 1.25)
        caption = self.caption("第 4、5 格没有被标记，说明数字 5、6 从未出现")
        self.play(Write(title), FadeIn(array), Write(scan))
        self.play(Circumscribe(array.boxes[4], color=YELLOW_ACCENT), Circumscribe(array.boxes[5], color=YELLOW_ACCENT))
        self.play(Write(answer), FadeIn(caption))
        self.wait(2.0)
        self.clear()

    def map_to_rust(self) -> None:
        title = self.heading("对应 Rust：三行就是完整的原地标记")
        code_lines = [
            ("let index = (nums[i].abs() as usize) - 1;", YELLOW_ACCENT),
            ("nums[index] = -nums[index].abs();", GREEN_OK),
            ("nums[i] > 0  =>  Some((i + 1) as i32)", PURPLE),
        ]
        code = VGroup(*[Text(line, font=MONO, font_size=27, color=color) for line, color in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        panel = RoundedRectangle(width=12.1, height=3.45, corner_radius=0.22, stroke_color="#344563", fill_color="#0C1324", fill_opacity=1)
        panel.shift(UP * 0.45)
        code.move_to(panel)
        notes = VGroup(
            Text("abs：读取原始数字", font=FONT, font_size=23, color=YELLOW_ACCENT),
            Text("−abs：幂等地写入签到标记", font=FONT, font_size=23, color=GREEN_OK),
            Text("i+1：下标还原为数字", font=FONT, font_size=23, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(panel, DOWN, buff=0.27)
        self.play(Write(title), FadeIn(panel))
        for line in code:
            self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.45)
        self.play(FadeIn(notes, lag_ratio=0.2))
        self.wait(2.0)
        self.clear()

    def finale(self) -> None:
        insight = Text("用符号位存一张“是否出现”的表", font=FONT, font_size=52, weight=BOLD, color=YELLOW_ACCENT).shift(UP * 1.2)
        time = Text("时间  O(n)", font=MONO, font_size=38, color=GREEN_OK)
        space = Text("额外空间  O(1)", font=MONO, font_size=38, color=BLUE_A)
        costs = VGroup(time, space).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(insight, DOWN, buff=0.7)
        divider = Line(LEFT * 4.8, RIGHT * 4.8, color="#263552", stroke_width=2).next_to(costs, DOWN, buff=0.55)
        footer = Text("LeetCode 448 · 找到所有数组中消失的数字", font=FONT, font_size=26, color=MUTED).next_to(divider, DOWN, buff=0.34)
        self.play(Write(insight), run_time=1.2)
        self.play(FadeIn(costs, lag_ratio=0.25), Create(divider), FadeIn(footer))
        self.wait(3.0)
