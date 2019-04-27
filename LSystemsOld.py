import math
import numpy as np
import pygame
import os


class LSystem:
    x, x_pos, y, y_pos, rotation, char_pos, width = 0, 0, 0, 0, 0, 0, 1
    cur_pos = np.zeros(2, int)
    next_pos = np.zeros(2, int)

    def __init__(self, max_iteration, side_length,
                 axiom, instructions, starting_info=(1/2, 1/2, 0)):
        self.max_iteration = max_iteration
        self.side_length = side_length
        self.next_string = axiom
        self.instructions = instructions
        self.x_offset, self.y_offset = starting_info[0] * screen.get_width(), starting_info[1] * screen.get_height()
        self.theta = starting_info[2] * math.pi / 180
        self.stack = list([self.x_offset, self.y_offset, self.theta])
        self.switch = {
            **dict.fromkeys(('F', 'G'), lambda x: x.draw_line(x.x_pos - x.x, x.y_pos - x.y)),
            '>': lambda x: x.rotate(-x.theta),
            '<': lambda x: x.rotate(x.theta),
            '[': lambda x: x.save_pos(),
            ']': lambda x: x.restore_pos()
        }

    def grow(self):
        for _ in range(self.max_iteration):
            new_string = ''
            for char in self.next_string:
                new_string += self.instructions.get(char, char)
            self.next_string = new_string

    def interperet(self):
        self.x_pos, self.y_pos = self.x_offset, self.y_offset
        self.x, self.y = 0, 0
        self.rotation = 0
        self.cur_pos = (self.x_pos, self.y_pos)
        self.next_pos = (0, 0)
        for self.char_pos, char in enumerate(self.next_string):
            if char in self.switch:
                self.switch[char](self)

    def rotate(self, theta):
        self.rotation += theta
        self.x = self.side_length * math.cos(self.rotation)
        self.y = self.side_length * math.sin(self.rotation)
        x = self.side_length * math.cos(self.rotation)
        y = self.side_length * math.sin(self.rotation)
        self.next_pos = (self.cur_pos + (x, y))

    def draw_line(self, next_x_pos, next_y_pos):
        pygame.draw.line(screen, (self.char_pos % 255,
                         (len(self.next_string) - self.char_pos) % 255,
                         self.char_pos * 255 // len(self.next_string)),
                         (self.x_pos, self.y_pos), (next_x_pos, next_y_pos), self.width)
        self.x_pos, self.y_pos = next_x_pos, next_y_pos

    def save_pos(self):
        self.stack.append((self.x_pos, self.y_pos, self.rotation))

    def restore_pos(self):
        self.x_pos, self.y_pos, self.rotation = self.stack.pop()


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)
    screen.fill((0, 0, 0))
    pygame.event.get()
    # LSystem(max_iteration, side_length, axiom, intstructions, (x_offset, y_offset, theta))
    LSystems = [LSystem(5, 25, 'F>G>G', {'F': 'F>G<F<G>F', 'G': 'GG'}, (2/3, 1/4, 120)),         # sierpinski triangle
                LSystem(6, 10, 'F', {'F': 'G>F>G', 'G': 'F<G<F'}, (2/3, 2/3, 60)),               # sierpinski arrowhead
                LSystem(4, 7, 'F>>F>>F', {'F': 'F<F>>F<F'}, (1/2, 1/2, 60)),                  # koch snowflake
                LSystem(5, 5, 'F', {'F': 'F<F>F>F<F'}, (4/5, 2/3, 90)),                       # koch square
                LSystem(8, 30, 'FX', {'X': 'X>YF>', 'Y': '<FX<Y'}, (2/3, 1/2, 90)),          # dragon curve
                LSystem(7, 5, 'F', {'F': 'G[<F]>F', 'G': 'GG'}, (1/2, 1/2, 45)),                # fractal tree
                LSystem(6, 5, 'X', {'X': 'F>[[X]<X]<F[<FX]>X', 'F': 'FF'}, (1/2, 1/2, 25)),     # fractal plant
                LSystem(4, 6, 'F<F<F<F<F', {'F': 'F<F>>F>F<F<F'}, (1/2, 1/2, 72)),            # hexagon thingy
                LSystem(4, 10, 'F', {'F': 'F>F<F<F<G>F>F>F<F', 'G': 'GGG'}, (1/2, 1/2, 90))     # square thingy
                ]
    for i in range(len(LSystems)):
        LSystems[i].grow()
    for i in range(len(LSystems)):
        for j in range(1, 10):
            LSystems[i].width = j
            LSystems[i].interperet()
            pygame.display.flip()
            pygame.time.wait(100)
        screen.fill((0, 0, 0))
    pygame.quit()
    exit()
