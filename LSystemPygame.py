import numpy as np
import pygame
import os

DEBUG = False


# Draws and waits after execution of a function if DEBUG is true. Otherwise no change.
def Debug(function):
    if DEBUG == True:
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
            pygame.display.update()
            pygame.time.delay(100)

        return wrapper
    return function


class LSystem:
    def __init__(self, max_iteration, side_length, theta,
                 axiom, instructions, starting_info):
        self.rotation, self.char_pos, self.theta, self.width = 0, 0, 0, 1
        self.stack = []

        self.max_iteration = max_iteration
        self.side_length = side_length
        self.theta = theta * np.pi / 180
        self.next_string = axiom
        self.instructions = instructions
        self.starting_info = starting_info
        self.starting_pos = np.array([starting_info[0] * screen.get_width(),
                                    starting_info[1] * screen.get_height()])
        self.reset()

        # A dictionary of possible operations the fractal can take.
        self.ops = {
            **dict.fromkeys(('F', 'G'), lambda x: x.draw_line()),
            '>': lambda x: x.rotate(-x.theta),
            '<': lambda x: x.rotate(x.theta),
            '[': lambda x: x.save_pos(),
            ']': lambda x: x.restore_pos(),
            }

    # Reset position and angle to original position to draw
    def reset(self):
        self.rotation = self.starting_info[2]
        self.next_pos = np.copy(self.starting_pos)
        self.cur_pos = np.copy(self.starting_pos)

    # Grow the L-system string max_iteration times
    def grow(self):
        for _ in range(self.max_iteration):
            new_string = ''
            for char in self.next_string:
                new_string += self.instructions.get(char, char)
            self.next_string = new_string

    # Draw a fractal based on the string
    def interpret(self):
        for self.char_pos, char in enumerate(self.next_string):
            if char in self.ops:
                self.ops[char](self)

    # Change the angle of rotation and calculate height and width of next line to draw
    def rotate(self, theta):
        self.rotation += theta

    # Draw a line using rgb, starting at cur_pos and ending at next_pos
    @Debug
    def draw_line(self):
        x = self.side_length * np.cos(self.rotation)
        y = self.side_length * np.sin(self.rotation)

        self.next_pos = (self.cur_pos + [x, y])

        r, g, b = (self.char_pos % 255, (len(self.next_string) - self.char_pos) % 255,
                self.char_pos * 255 // len(self.next_string))
        pygame.draw.line(screen, (r, g, b), self.cur_pos, self.next_pos, self.width)
        self.cur_pos = self.next_pos

    def save_pos(self):
        self.stack.append((self.cur_pos, self.rotation))

    def restore_pos(self):
        self.cur_pos, self.rotation = self.stack.pop()


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.NOFRAME)
    screen.fill((0, 0, 0))
    # Create LSystem objects, each one defines a different fractal
    # LSystem(max_iteration, side_length, theta, axiom, intstructions, (x_offset, y_offset, theta))
    LSystems = [LSystem(5, 5, 120, 'F>G>G', {'F': 'F>G<F<G>F', 'G': 'GG'}, (2/3, 1/4, 0)),  # sierpinski triangle
                LSystem(6, 10, 60, 'F', {'F': 'G>F>G', 'G': 'F<G<F'}, (2/3, 2/3, 60)),         # sierpinski arrowhead
                LSystem(4, 7, 60, 'F>>F>>F', {'F': 'F<F>>F<F'}, (1/2, 1/2, 60)),               # koch snowflake
                LSystem(5, 5, 90, 'F', {'F': 'F<F>F>F<F'}, (4/5, 2/3, 90)),                    # koch square
                LSystem(8, 30, 90, 'FX', {'X': 'X>YF>', 'Y': '<FX<Y'}, (2/3, 1/2, 90)),        # dragon curve
                LSystem(10, 15, 45, 'F', {'F': 'G[<F]>F', 'G': 'GG'}, (1/2, 1/2, 45)),           # fractal tree
                LSystem(5, 20, 25, 'X', {'X': 'F>[[X]<X]<F[<FX]>X', 'F': 'FF'}, (1/2, 1/2, 25)),     # fractal plant
                LSystem(4, 8, 72, 'F<F<F<F<F', {'F': 'F<F>>F>F<F<F'}, (1/2, 1/2, 72)),         # hexagon thingy
                LSystem(4, 4, 90, 'F', {'F': 'F>F<F<F<G>F>F>F<F', 'G': 'GGG'}, (1/2, 1/2, 90))     # square thingy
                ]

    # Grow and Interpret each LSystem
    for i in range(len(LSystems)):
        LSystems[i].grow()
    for i in range(len(LSystems)):
        for j in range(1, 10):
            LSystems[i].width = j
            LSystems[i].reset()
            LSystems[i].interpret()
            pygame.display.flip()
            pygame.time.wait(50)
        screen.fill((0, 0, 0))
    pygame.quit()
    exit()
