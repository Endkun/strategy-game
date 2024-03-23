import pygame
from pygame.locals import *
import sys
import random

class Circle():
    def __init__(self, ox1, ox2, oy1, oy2):
        self.mode = "up"
        self.ox = random.randint(ox1 + 5, ox2 - 5)
        self.oy = random.randint(oy1 + 300, oy2 + 300)
        self.ox1 = ox1
        self.ox2 = ox2
        self.oy1 = oy1
        self.oy2 = oy2

    def reset(self):
        self.ox = random.randint(self.ox1 - 5, self.ox2 + 5)

    def update(self):
        self.roy = 0
        self.rox = 0
        self.roy += random.randint(1, 5)
        self.rox += random.randint(-5, 5)

        if self.mode == "drop":
            self.oy += self.roy / 10
            self.ox += self.rox / 10
        elif self.mode == "up":
            self.oy -= self.roy / 5

        if self.oy >= 600:
            self.mode = "finish"
        if self.oy <= 100:
            self.mode = "drop"
            self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.ox), int(self.oy)), 1)

class Tower():
    def __init__(self, cx1, cx2, cy1, cy2):
        self.c = 0
        self.tick = 0
        self.cl = []
        self.cx1 = cx1
        self.cx2 = cx2
        self.cy1 = cy1
        self.cy2 = cy2

    def update(self):
        self.tick += 1
        for i in range(len(self.cl)):
            if self.cl[i].mode == "finish":
                self.cl.pop(i)
                continue
            self.cl[i].update()

        if self.tick == 10:
            self.c = Circle(self.cx1, self.cx2, self.cy1, self.cy2)
            self.cl.append(self.c)
            self.tick = 0

    def draw(self, screen):
        for c in self.cl:
            c.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    t1 = Tower(50, 70, 130, 150)
    t2 = Tower(100, 120, 130, 150)
    t3 = Tower(150, 170, 130, 150)
    t4 = Tower(200, 220, 130, 150)
    t5 = Tower(250, 270, 130, 150)
    t6 = Tower(300, 320, 130, 150)
    t7 = Tower(350, 370, 130, 150)
    t8 = Tower(400, 420, 130, 150)
    t9 = Tower(450, 470, 130, 150)
    t10 = Tower(500, 520, 130, 150)
    tl = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]

    clock = pygame.time.Clock()  # クロックオブジェクトを作成

    pygame.display.update()

    while True:
        screen.fill((255, 255, 255))

        for t in tl:
            t.update()
            t.draw(screen)

        pygame.display.update()

        clock.tick(30)  # ゲームループを30FPSに制限

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

main()