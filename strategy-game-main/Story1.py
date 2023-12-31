import pygame
from pygame.locals import *
import sys
import random
import time

class Character():
    def __init__(self,x,y,CharacterType,Image,Team,Name,font2):#-----------------------------------------------------------初期化
        self.x = x
        self.y = y
        self.Fight = False 
        self.font2 = font2
        self.tick = 0
        self.isBUTTONDOWN = "down"
        self.Image = Image#イメージ画像
        self.Team = Team#チーム   味方チーム、敵チーム、モブチームOnly
        self.Name = Name#名前
        self.CharacterType = CharacterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        self.canMoveUp = False
        self.canMoveDown = False
        self.canMoveRight = False
        self.canMoveLeft = False
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
    #----------------------------------------------------------------------------------------------------------移動アクション
        #-----------------------------------------------------------------------------------------動ける所の検出
        if self.isBUTTONDOWN == "MoveLighton":#プレイヤーはx=2,y=5
            if mapchip[self.y-1][self.x] == "1": #上
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
            if mapchip[self.y+1][self.x] == "1": #下  
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
            if mapchip[self.y][self.x+1] == "1": #右
                pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
            if mapchip[self.y][self.x-1] == "1": #左
                pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)
        #------------------------------------------------------------------------------------------禁止用
        if self.isBUTTONDOWN == "MoveLighton":
            if mapchip[self.y-1][self.x] == "1": #上
                self.canMoveUp = True
            else:
                self.canMoveUp = False
            if mapchip[self.y+1][self.x] == "1": #下  
                self.canMoveDown = True
            else:
                self.canMoveDown = False
            if mapchip[self.y][self.x+1] == "1": #右
                self.canMoveRight = True
            else:
                self.canMoveRight = False
            if mapchip[self.y][self.x-1] == "1": #左
                self.canMoveLeft = True
            else:
                self.canMoveLeft = False
        if self.isBUTTONDOWN == "FightDown":
            if mapchip[self.y-1][self.x] == "5": #上
                pygame.draw.circle(screen,(250,250,255),((self.x+0.5)*100,(self.y-0.5)*100),10)
            if mapchip[self.y+1][self.x] == "5": #下  
                pygame.draw.circle(screen,(250,250,255),((self.x+0.5)*100,(self.y+1.5)*100),10)
            if mapchip[self.y][self.x+1] == "5": #右
                #print(self.y,self.x)
                pygame.draw.circle(screen,(250,250,255),((self.x+1.5)*100,(self.y+0.5)*100),10)
            if mapchip[self.y][self.x-1] == "5": #左
                pygame.draw.circle(screen,(250,250,255),((self.x-0.5)*100,(self.y+0.5)*100),10)

        #-----------------------------------------------------------------------------------------ボタン・フラグ管理
        if self.tick == 700:
            self.isBUTTONDOWN = "isnotpushed"
        if self.isBUTTONDOWN == "isnotpushed":
            pygame.draw.rect(screen, (255,255,255), Rect(15,700,200,100))
            txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [20, 720])# 文字列の表示位置
            if self.Fight == True:#--------------------------------------------------戦う
                if mapchip[self.y-1][self.x] == "5" or mapchip[self.y+1][self.x] == "5" or mapchip[self.y][self.x+1] == "5" or mapchip[self.y][self.x-1] == "5":
                    pygame.draw.rect(screen, (255,255,255), Rect(230,700,200,100))
                    txt = self.font2.render("戦う", True, (0,0,0))   # 描画する文字列の設定
                    screen.blit(txt, [250, 720])# 文字列の表示位置
                else:
                    self.Fight = False
        #-----------------------------------------------------------------------------------------イベント処理
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                if self.isBUTTONDOWN == "isnotpushed":
                    x, y = event.pos
                    print(x,y)
                    if 15 < x < 215 and 700 < y < 800:
                            self.isBUTTONDOWN = "MoveLighton"
                if self.isBUTTONDOWN == "MoveLighton":
                    x, y = event.pos
                    print(self.x*100)
                    if self.canMoveUp == True:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            self.y -= 1  
                            self.Fight = True
                            self.isBUTTONDOWN = "isnotpushed"
                    if self.canMoveDown == True:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            self.y += 1  
                            self.Fight = True
                            self.isBUTTONDOWN = "isnotpushed"
                    print(self.y*100+100,y,self.y*100)
                    if self.canMoveLeft == True:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            self.x -= 1
                            self.Fight = True
                            self.isBUTTONDOWN = "isnotpushed"
                    if self.canMoveRight == True:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            self.x += 1    
                            self.Fight = True
                            self.isBUTTONDOWN = "isnotpushed"
                if self.Fight == True:
                    x,y = event.pos
                    if 230 < x < 450 and 700 < y < 800:
                        self.isBUTTONDOWN = "FightDown"
                                
                    


    def place(self):#----------------------------------------------------------------アクション
        if self.CharacterType == "Goutou":
            if self.Name == "Yakuza Sumiyoshi":
                self.y = 3
    def draw(self,screen):#-----------------------------------------------------------描画
        screen.blit(self.Image,Rect(self.x*100,self.y*100,50,50))
        
 

def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60)                       
    screen = pygame.display.set_mode((500, 900))  # 800
    pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
    pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
    pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
    door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
    door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主
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
                if mapchip[j][i] == "5":
                    mapchip[j][i] = "1"
                for enemy in enemys:
                    if enemy.x == i and enemy.y == j:
                        if mapchip[j][i] == "1":
                            mapchip[j][i] = "5"
                if mapchip[j][i] == "1":#動けるタイル
                    screen.blit(pt1 ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "0":#壁
                    screen.blit(pt2 ,Rect(tx+i*100,ty+j*100,50,50))  
                elif mapchip[j][i] == "2":#字幕
                    screen.blit(pt3 ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "3":#ドア
                    screen.blit(door ,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "4":#ドア
                    screen.blit(door2,Rect(tx+i*100,ty+j*100,50,50))
                elif mapchip[j][i] == "5":#不可触タイル
                    screen.blit(pt1,Rect(tx+i*100,ty+j*100,50,50))
        if tick < 500:
            Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = font.render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        if tick > 500:
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

       
        #---------描画---------
        #---------敵-------------------
        for enemy in enemys:
            enemy.draw(screen)
        #---------プレイヤー-------------------
        for player in players:
            player.button(screen,mapchip)
        for player in players:
            player.draw(screen)
        for mob in mobs:
            mob.draw(screen)
                          
        pygame.display.update()         
        ck.tick(60) #1秒間で30フレームになるように33msecのwait                           
main()