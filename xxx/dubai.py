#順序
"""
class circle() 10個くらいの球が降ってくるようにする
class2 towers() それを球の塔ごとに整える"""
class Circle():
    def __init__(self,ox1,ox2,oy1,oy2):
        #------------座標
        self.mode = "up" #upは上がる,dropは下がる
        self.ox = random.randint(ox1+5,ox2-5)
        self.oy = random.randint(oy1+300,oy2+300)
        #------------ランダム数値
        self.ox1 = ox1
        self.ox2 = ox2
        self.oy1 = oy1
        self.oy2 = oy2
    def reset(self):
        #------------座標リセット
        self.ox = random.randint(self.ox1-5,self.ox2+5)
    def update(self):
        #------------落下
        self.roy = 0
        self.rox = 0
        self.roy += random.randint(1,5)
        self.rox += random.randint(-5,5)
        if self.mode == "drop":
            self.oy += self.roy/10
            self.ox += self.rox/10
        elif self.mode == "up":
            self.oy -= self.roy/5

        #------------条件
        if self.oy >= 600:
            self.mode = "finish"
        if self.oy <= 100:
            self.mode = "drop"
            self.reset()
    def draw(self,screen):
        #------------描画
        pygame.draw.circle(screen,(0,0,255),(self.ox,self.oy),1)
class Tower():
    def __init__(self,cx1,cx2,cy1,cy2):
        self.c = 0
        self.tick = 0
        self.cl = []
        self.cx1 = cx1
        self.cx2 = cx2
        self.cy1 = cy1
        self.cy2 = cy2
    def update(self,):
        self.tick += 1
        for i in range(3):
            if self.tick == 10:
                self.c = Circle(self.cx1,self.cx2,self.cy1,self.cy2)
                self.cl.append(self.c)
                if self.cl[i].mode == "finish":
                    self.cl.pop(i)
                self.tick = 0
    def draw(self,screen,):
        for i in range(len(self.cl)):
            self.cl[i].update()
            self.cl[i].draw(screen)
                

import pygame
from pygame.locals import *
import sys
import random
def main():
    pygame.init()                                 # Pygameの初期化
    screen = pygame.display.set_mode((800, 600))  # 800*600の画面
    t1 = Tower(50,70,130,150)
    t2 = Tower(100,120,130,150)
    t3 = Tower(150,170,130,150)
    t4 = Tower(200,220,130,150)
    t5 = Tower(250,270,130,150)
    t6 = Tower(300,320,130,150)
    t7 = Tower(350,370,130,150)
    t8 = Tower(400,420,130,150)
    t9 = Tower(450,470,130,150)
    t10 = Tower(500,520,130,150)
    tl = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]
    #c = Circle(140,150,140,150)
    pygame.display.update()
    while True:
        screen.fill((255,255,255))
        for t in tl:
            t.update()
            t.draw(screen)
        #c.update()
        #c.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit() 
main()