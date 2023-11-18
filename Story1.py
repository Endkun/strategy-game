import pygame
from pygame.locals import *
import sys
import random
import time
class Character():
    def __init__(self,x,y,CharacterType,Image,Team,Name,font2):#-----------------------------------------------------------初期化
        self.x = x
        self.y = y
        self.font2 = font2
        self.tick = 0
        self.isBUTTONDOWN = False
        self.Image = Image#イメージ画像
        self.Team = Team#チーム   味方チーム、敵チーム、モブチームOnly
        self.Name = Name#名前
        self.CharacterType = CharacterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
    def firstAnimation(self):#-----------------------------------------------------------最初のアニメーション
        self.tick += 1
        if self.CharacterType == "Slime":   
            if self.Name == "BlueSlime":
                if self.tick == 120:
                    self.x = 2
                    self.y = 2
                if self.tick == 200:
                    self.y = 3
                if self.tick == 400:
                    self.x = 3
            if self.Name == "GreenSlime":
                if self.tick == 200:
                    self.x = 2
                    self.y = 2
                if self.tick == 400:
                    self.y = 3
                if self.tick == 500:
                    self.x = 1
        if self.CharacterType == "Goutou":
            if self.Name == "Yakuza Sumiyoshi":
                if self.tick == 400:
                    self.x = 2
                    self.y = 2
                if self.tick == 600:
                    self.y = 3
        if self.CharacterType == "Player":
            if self.Name == "Mikata1":
                if self.tick == 300:
                    self.y += 1
                if self.tick == 400:
                    self.y += 4
        if self.CharacterType == "Animal":
            if self.Name == "Cat":
                if self.tick == 400:
                    self.y += 1
                if self.tick == 550:
                    self.x += 2
                if self.tick == 650:
                    self.y += 4
    def button(self,screen,mapchip):#移動ボタン用
        if self.isBUTTONDOWN == True:
            if mapchip[self.y-1][self.x] == "1": #上
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
            if mapchip[self.y+1][self.x] == "1": #下  
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10) 
            if mapchip[self.y][self.x+1] == "1": #右
                pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
            if mapchip[self.y][self.x-1] == "1": #左
                pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10) 
        if self.tick >= 700:
            pygame.draw.rect(screen, (255,255,255), Rect(150,700,200,100))
            txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [190, 720])# 文字列の表示位置
        # イベント処理
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                if self.tick >= 700:
                    if self.isBUTTONDOWN == False:
                        btn = event.button
                        x, y = event.pos
                        if x > 150 and x < 350:
                            if y > 700 and y < 800:
                                self.isBUTTONDOWN = True   
    def draw(self,screen):#-----------------------------------------------------------描画
        screen.blit(self.Image,Rect(self.x*100,self.y*100,50,50))
 

def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60)                       
    screen = pygame.display.set_mode((500, 900))  # 800
    pt1 = pygame.image.load("PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
    pt2 = pygame.image.load("PlotTile2.png").convert_alpha()   #モブタイル　
    pt3 = pygame.image.load("PlotTile3.png").convert_alpha()   #字幕タイル
    door = pygame.image.load("door.png").convert_alpha()   #ドアタイル
    door2 = pygame.image.load("door2.png").convert_alpha()   #裏口タイル
    Pl1 = pygame.image.load("player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("goutou1.png").convert_alpha()       #強盗、スライムの支配主
    tx = 0#タイル用x,y
    ty = 0
    tick = 0
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2)
    player2 = Character(3,4,"Player",Pl2,"味方","Mikata1",font2)
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font2)
    slime2 = Character(-1,0,"Slime",Sl2,"敵","GreenSlime",font2)
    goutou = Character(-1,0,"Goutou",Man,"敵","Yakuza Sumiyoshi",font2)
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font2)
    players = [player1]
    enemys = [slime1,slime2,goutou]
    mobs = [cat,player2]
    mapchip = [
        ["2","2","2","2","2"],
        ["0","0","0","0","0"],
        ["0","0","3","0","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","0","0","4","0"],
        ["0","0","0","0","0"],
        ["0","0","0","0","0"],
        ]
    ck = pygame.time.Clock()

    while True:
        tick += 1
        screen.fill((255,255,255))
        for i in range(5):
            for j in range(9):
                if mapchip[j][i] == "1":
                    screen.blit(pt1 ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "0":
                    screen.blit(pt2 ,Rect(tx+i*100,ty+j*100,50,50))  
                elif mapchip[j][i] == "2":
                    screen.blit(pt3 ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "3":
                    screen.blit(door ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "4":
                    screen.blit(door2,Rect(tx+i*100,ty+j*100,50,50))
        if tick < 500:
            Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = font.render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        if tick >= 500:
            Story = font.render("強盗だ！金を出せ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("打たれたくないなら金だ！", True, (0,0,0)) # 描画する文字列を画像にする
        screen.blit(Story, [70,40])
        screen.blit(Story2,[70,70])   
        #---------アニメーション---------
        for player in players:
            player.firstAnimation()
        for enemy in enemys:
            enemy.firstAnimation()
        for mob in mobs:
            mob.firstAnimation()

        #---------プレイヤー-------------------
        for player in players:
            player.button(screen,mapchip)
        #---------描画---------
        for player in players:
            player.draw(screen)
        for enemy in enemys:
            enemy.draw(screen)
        for mob in mobs:
            mob.draw(screen)
                          
        pygame.display.update()         
        ck.tick(60) #1秒間で30フレームになるように33msecのwait                           
main()