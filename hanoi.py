from manim import *
import sys
import os

class Hanoi(Scene):
    stack_distance = 4
    stack_height = 5

    def __init__(self, size, **kwargs):
        self.size = size
        self.block_height = min(self.stack_height / size, 0.75)
        self.block_max_width = self.stack_distance - 1
        self.step_time = 1 / size
        super().__init__(**kwargs)

    def construct(self):
        self.draw_stacks()
        self.init_blocks()
        self.solve(size, 0, 2)
        self.wait()
    
    def draw_stacks(self):
        stacks = [
            RoundedRectangle(
                width=0.4, height=self.stack_height, corner_radius=0.1
            ).shift(
                (LEFT * self.stack_distance) + (RIGHT * self.stack_distance * i)
            ).to_edge(DOWN)
            for i in range(3)
        ]
        self.play(*(Create(rect) for rect in stacks))

    def init_blocks(self):
        self.stacks = [[], [], []]
        step = (self.block_max_width - 1) / max(self.size - 1, 1)
        for i in range(self.size):
            self.stacks[0].append(
                RoundedRectangle(
                    width=self.block_max_width - i * step,
                    height = self.block_height,
                    corner_radius=0.1
                ).set_fill(
                    BLACK, opacity=1
                ).to_edge(DOWN).shift(
                    LEFT * self.stack_distance + (UP * self.block_height * i)
                )
            )
        self.play(*(Create(block) for block in self.stacks[0]))
    
    def move_block(self, from_stack, to_stack):
        block = self.stacks[from_stack][-1]
        self.play(Transform(block, block.copy().to_edge(UP)), run_time=self.step_time)

        target_x = (LEFT * self.stack_distance) + (RIGHT * self.stack_distance * to_stack)
        move_x = target_x - block.get_center()[0]
        self.play(block.animate.shift(RIGHT * move_x), run_time=self.step_time)

        self.play(
            Transform(block, block.copy().to_edge(DOWN).shift(UP * self.block_height * len(self.stacks[to_stack]))),
            run_time=self.step_time
        )

        self.stacks[to_stack].append(self.stacks[from_stack].pop())
    
    def solve(self, depth, from_stack, to_stack):
        if depth == 1:
            return self.move_block(from_stack, to_stack)
        
        buffer = (from_stack + to_stack) ^ 3

        self.solve(depth - 1, from_stack, buffer)
        self.move_block(from_stack, to_stack)
        self.solve(depth - 1, buffer, to_stack)

        

def error(message):
    print(message)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Usage: python hanoi.py <size>")
    try:
        size = int(sys.argv[1])
        if size < 1 or size > 8:
            error("Size must be a value in the range 1 - 8.")
        with tempconfig({"output_file": f"Hanoi_{size}"}):
            Hanoi(size).render()
    except ValueError:
        error("Size is not an integer.")