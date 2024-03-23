import pygame
from pygame.locals import *
import sys
import random
import math
WATER1=(100,100,255)
WATER2=(200,200,255)
WATER3=(10,200,255)
HEIGHT=600
WIDTH=800
# 楕円のパラメータ
center_x, center_y = WIDTH // 2, HEIGHT // 2
a, b = 300, 200  # 水平軸と垂直軸の長さ
class Drop():
    def __init__(self,x,y,vy):
        self.x=x
        self.y=y
        self.vy=vy
        self.a=0.03
    def update(self):
        self.vy+=self.a
        self.y+=self.vy
        if self.vy>0:
            self.x+=random.randint(-2,2)
        else :
            self.x+=random.randint(-1,1)/3
    def draw(self,screen):
        pygame.draw.circle(screen,WATER1,(self.x,self.y),2)
class Fountain():#噴水１基分
    def __init__(self,x,y,ct):
        self.x=x
        self.y=y
        self.Ds=[]
        self.id=ct
        self.ct=ct*100
        #print(self.ct)
    def update(self,screen,f):#関数引数
        self.ct+=1
        #print(f"{self.id=},{self.ct=}")
        # 新しいDropインスタンスを追加
        f()
        # Dropインスタンスの更新と描画、画面内にあるインスタンスのみを保持
        self.Ds = [D for D in self.Ds if D.y <= HEIGHT]
        for D in self.Ds:
            D.update()
            D.draw(screen)
    def f1(self):
        if self.ct%3000<300:
            self.Ds.append(Drop(self.x, self.y, -2))
        else:
            self.Ds.append(Drop(self.x, self.y, -3))
    def f2(self):
        if self.ct%1000<300:
            self.Ds.append(Drop(self.x, self.y, -1))
        else:
            self.Ds.append(Drop(self.x, self.y, -4))
def main():
    pygame.init()                                 # Pygameの初期化
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 20個の点を楕円状に描画
    bases=[]#噴水の基点座標
    dv=30
    for i in range(dv):
        angle = 2 * math.pi * i / dv
        x = center_x + a * math.cos(angle)
        y = center_y + b * math.sin(angle)
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 5)
        bases.append([int(x),int(y),i])
    #print(bases)
    Fs=[Fountain(d[0],d[1],d[2]) for d in bases]
    mainCt=0
    while True:
        mainCt+=1
        screen.fill((255,255,255))       # 背景を白
        for F in Fs:
          if mainCt<1000:
              F.update(screen,F.f1)
          else:
              F.update(screen,F.f2)
        pygame.display.update()          # 画面更新
        # イベント処理
        for event in pygame.event.get():  # イベントを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら
                pygame.quit()
                sys.exit()                # 終了
if __name__ == "__main__":
    main()