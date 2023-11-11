import pygame
from pygame.locals import *
import sys
import random
import time
class Slime:
    def __init__(self,x,y,SlimeType):#-----------------------------------------------------------初期化
        self.Slx = -1
        self.Sly = -1
        self.tick = 0
        self.slimeType = SlimeType
        if self.slimeType == 1:
            self.sl = pygame.image.load("slime1.png").convert_alpha()      #青スライム
        if self.slimeType == 2:
            self.sl = pygame.image.load("slime2.png").convert_alpha()      #黄緑スライム
    def firstAnimation(self):#-----------------------------------------------------------最初のアニメーション
        self.tick += 1   
        if self.slimeType == 1:
            if self.tick == 800:
                self.Slx = 2
                self.Sly = 2
            if self.tick == 1000:
                self.Sly = 3
            if self.tick == 1300:
                self.Slx = 3
        if self.slimeType == 2:
            if self.tick == 1000:
                self.Slx = 2
                self.Sly = 2
            if self.tick == 1300:
                self.Sly = 3
            if self.tick == 1500:
                self.Slx = 1
    def draw(self,screen):#-----------------------------------------------------------描画
        screen.blit(self.sl,Rect(self.Slx*100,self.Sly*100,50,50)) 

def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 40)                       # Pygameの初期化
    screen = pygame.display.set_mode((500, 900))  # 800
    pt1 = pygame.image.load("PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
    pt2 = pygame.image.load("PlotTile2.png").convert_alpha()   #モブタイル　
    pl1 = pygame.image.load("player1.png").convert_alpha()       #プレイヤー
    pl2 = pygame.image.load("player2.png").convert_alpha()       #プレイヤー
    cat = pygame.image.load("cat.png").convert_alpha()       #プレイヤー
    tx = 0#タイル用x,y
    ty = 0
    px1 = 2#プレイヤー用xy
    py1 = 5
    px2 = 3#プレイヤー2用xy
    py2 = 4
    cx = 1#猫用xy
    cy = 4
    slime1 = Slime(0,0,1)
    slime2 = Slime(0,1,2)
    mapchip = [
        ["0","0","0","0","0"],
        ["0","0","0","0","0"],
        ["0","0","0","0","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","0","0","0","0"],
        ["0","0","0","0","0"],
        ["0","0","0","0","0"],
        ]
    while True:
        screen.fill((255,255,255))
        for i in range(5):
            for j in range(9):
                if mapchip[j][i] == "1":
                    screen.blit(pt1 ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "0":
                    screen.blit(pt2 ,Rect(tx+i*100,ty+j*100,50,50))  
        Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
        Story2 = font.render("突然スライムが入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        screen.blit(Story, [10,110])
        screen.blit(Story2,[10,170])   
        screen.blit(pl1 ,Rect(px1*100,py1*100,50,50))      
        screen.blit(pl2 ,Rect(px2*100,py2*100,50,50))    
        screen.blit(cat ,Rect(cx*100,cy*100,50,50))
        slime1.firstAnimation()     
        slime2.firstAnimation()
        slime1.draw(screen)
        slime2.draw(screen)
                          
        pygame.display.update()                                    
        # イベント処理
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
if __name__ == "__main__":
    main()