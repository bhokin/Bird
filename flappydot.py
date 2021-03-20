import tkinter as tk
import random
from tkinter import messagebox

from gamelib import Sprite, GameApp, Text

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
PILLAR_SPEED = 6
JUMP_VELOCITY = -20
POSITION_PILLAR_PAIR_2 = random.randint(100, 400)


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True

    def jump(self):
        self.vy = JUMP_VELOCITY

    def is_out_of_screen(self):
        if self.y >= CANVAS_HEIGHT or self.y <= 0:
            return True
        return False


class PillarPair(Sprite):
    def init_element(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= PILLAR_SPEED

    def start(self):
        self.is_started = True

    def is_out_of_screen(self):
        if self.x < -40:
            return True
        return False

    def is_collision(self, other):
        if self.x - 45 <= other.x <= self.x + 45:
            if other.y <= self.y - 95 or self.y + 95 <= other.y:
                return True

    def reset_position(self):
        self.x = CANVAS_WIDTH + 40

    def random_height(self):
        self.y = random.randint(100, 400)


class BackGround(Sprite):
    def init_element(self):
        self.is_started = False

    def update(self):
        if self.is_started:
            self.x -= PILLAR_SPEED

    def start(self):
        self.is_started = True

    def is_out_of_screen(self):
        if self.x < -0:
            return True
        return False

    def reset_position(self):
        self.x = 872


class FlappyGame(GameApp):
    def create_sprites(self):
        self.background = BackGround(self, 'images/Flappy-BG.png', 872, CANVAS_HEIGHT // 2)
        self.elements.append(self.background)
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.pillar_pair_2 = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH*1.54, POSITION_PILLAR_PAIR_2)
        self.elements.append(self.pillar_pair)
        self.elements.append(self.pillar_pair_2)

    def init_game(self):
        self.create_sprites()

    def pre_update(self):
        pass

    def post_update(self):
        if self.pillar_pair.is_out_of_screen():
            self.pillar_pair.reset_position()
            self.pillar_pair.random_height()
        if self.pillar_pair_2.is_out_of_screen():
            self.pillar_pair_2.reset_position()
            self.pillar_pair_2.random_height()
        if self.background.is_out_of_screen():
            self.background.reset_position()
        if self.dot.is_out_of_screen() or self.pillar_pair.is_collision(self.dot)\
                or self.pillar_pair_2.is_collision(self.dot):
            messagebox.showinfo(title="Flappy Dot Game", message="Boommmmmmmmm!")
            root.destroy()

    def on_key_pressed(self, event):
        self.dot.start()
        self.dot.jump()
        self.pillar_pair.start()
        self.pillar_pair_2.start()
        self.background.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy Dot Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
