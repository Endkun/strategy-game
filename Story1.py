import pygame
from pygame.locals import *
import sys
import random
import time

class Character():
    num = 0#クラス変数
    def __init__(self,x,y,characterType,image,team,name,font2,id,energy):#-----------------------------------------------------------初期化
        self.id = id#id番号 
        self.x = x
        self.y = y
        self.fight = False 
        self.font2 = font2
        self.animationTick = 0
        self.isButtonDown = "down"
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム
        self.name = name#名前
        self.energy = energy
        self.tenergy = energy#保存
        self.characterType = characterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        self.canMoveUp = False
        self.canMoveDown = False
        self.canMoveRight = False
        self.canMoveLeft = False
        self.canFightUp = False
        self.canFightDown = False
        self.canFightRight = False
        self.canFightLeft = False
        self.enemyMoveUp = False
        self.enemyMoveDown = False
        self.enemyMoveRight = False
        self.enemyMoveLeft = False
    def firstAnimation(self,screen,tick):#-----------------------------------------------------------最初のアニメーション
        self.animaionTick = tick
        if self.characterType == "Slime":   
            if self.name == "BlueSlime":
                if self.animaionTick >= 120:
                    self.x = 2
                    self.y = 2
                if self.animaionTick >= 200:
                    self.y = 3
                if self.animaionTick >= 400:
                    self.x = 3
            if self.name == "GreenSlime":
                if self.animaionTick >= 200:
                    self.x = 2
                    self.y = 2
                if self.animaionTick >= 400:
                    self.y = 3
                if self.animaionTick >= 500:
                    self.x = 1
        if self.characterType == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                if self.animaionTick >= 400:
                    self.x = 2
                    self.y = 2
        if self.characterType == "Player":
            if self.name == "Mikata1":
                if self.animaionTick >= 650:
                    self.y = 5
        if self.characterType == "Animal":
            if self.name == "Cat":
                if self.animaionTick >= 400:
                    self.y = 5
                if self.animaionTick >= 550:
                    self.x = 3
                if self.animaionTick >= 650:
                    self.y = 9
    def update(self,screen,mapchip,characters):#移動ボタン用
    #----------------------------------------------------------------------------------------------------------移動アクション
        if self.team == "敵":

            if mapchip[self.y-1][self.x] == "1": #上
                self.enemyMoveUp = True
            else:
                self.enemyMoveUp = False
            if mapchip[self.y+1][self.x] == "1": #下  
                self.enemyMoveDown = True
            else:
                self.enemyMoveDown = False
            if mapchip[self.y][self.x+1] == "1": #右
                self.enemyMoveRight = True
            else:
                self.enemyMoveRight = False
            if mapchip[self.y][self.x-1] == "1": #左
                self.enemyMoveLeft = True
            else:
                self.enemyMoveLeft = False
            for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
                if self.x == character.x and self.y-1 == character.y: #上
                    self.enemyMoveUp = False
                if self.x == character.x and self.y+1 == character.y: #下  
                    self.enemyMoveDown = False
                if self.x+1 == character.x and self.y == character.y: #右
                    self.enemyMoveRight = False
                if self.x-1 == character.x and self.y == character.y: #左
                    self.enemyMoveLeft = False
            self.direction = random.randint(0,4)
            if self.direction == 0:
                if self.enemyMoveRight == True:
                    self.x += 1
                    self.energy -= 1
            elif self.direction == 1:
                if self.enemyMoveLeft == True:
                    self.x -= 1
                    self.energy -= 1
            elif self.direction == 2:
                if self.enemyMoveDown == True:
                    self.y += 1
                    self.energy -= 1
            elif self.direction == 3:
                if self.enemyMoveUp == True:
                    self.y -= 1
                    self.energy -= 1
            if self.energy == 0:
                Character.num += 1
                self.energy = self.tenergy
            print(self.name,self.energy,Character.num)           
        elif self.team == "味方":
            self.detection(screen,mapchip)
            if self.energy == 0:
                Character.num += 1
                self.energy = self.tenergy
                self.isButtonDown = "isnotpushed"
            #-----------------------------------------------------------------------------------------ボタン・フラグ管理
            if self.isButtonDown != "MoveLighton":
                if self.isButtonDown != "FightDown":
                    self.isButtonDown = "isnotpushed"
            if self.isButtonDown == "isnotpushed":
                pygame.draw.rect(screen, (255,255,255), Rect(15,700,200,100))
                txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
                screen.blit(txt, [20, 720])# 文字列の表示位置
                if self.fight == True:#--------------------------------------------------戦う
                    if mapchip[self.y-1][self.x] == "5" or mapchip[self.y+1][self.x] == "5" or mapchip[self.y][self.x+1] == "5" or mapchip[self.y][self.x-1] == "5":
                        pygame.draw.rect(screen, (255,255,255), Rect(230,700,200,100))
                        txt = self.font2.render("戦う", True, (0,0,0))   # 描画する文字列の設定
                        screen.blit(txt, [250, 720])# 文字列の表示位置
                    else:
                        self.fight = False
            self.event()
            #-----------------------------------------------------------------------------------------イベント処理
    def event(self):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                if self.isButtonDown == "isnotpushed":
                    x, y = event.pos
                    print("x,y:",x,y)
                    if 15 < x < 215 and 700 < y < 800:
                            self.isButtonDown = "MoveLighton"
                if self.isButtonDown == "MoveLighton":
                    x, y = event.pos
                    #print(self.x*100)
                    if self.canMoveUp == True:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            self.y -= 1  
                            self.energy -= 1
                            self.Fight = True
                            self.isButtonDown = "isnotpushed"
                    if self.canMoveDown == True:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            self.y += 1  
                            self.energy -= 1
                            self.Fight = True
                            self.isButtonDown = "isnotpushed"
                    #print(self.y*100+100,y,self.y*100)
                    if self.canMoveLeft == True:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            self.x -= 1
                            self.energy -= 1
                            self.Fight = True
                            self.isButtonDown = "isnotpushed"
                    if self.canMoveRight == True:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            self.x += 1    
                            self.energy -= 1
                            self.Fight = True
                            self.isButtonDown = "isnotpushed"
                if self.fight == True:
                    x,y = event.pos
                    if 230 < x < 450 and 700 < y < 800:
                        self.isButtonDown = "FightDown"
                        if self.isButtonDown == "FightDown":
                            #print(self.canFightUp,self.canFightDown,self.canFightLeft,self.canFightRight)
                            if self.canFightUp == True:
                                if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                                    self.y -= 1  
                                    self.energy -= 1
                                    self.canFightUp = False
                                    self.isButtonDown = "isnotpushed"
                            if self.canFightDown == True:
                                if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                                    self.y += 1  
                                    self.energy -= 1
                                    self.canFightDown = False
                                    self.isButtonDown = "isnotpushed"
                            if self.canFightLeft == True:
                                if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                                    self.x -= 1
                                    self.energy -= 1
                                    self.canFightLeft = False
                                    self.isButtonDown = "isnotpushed"
                            if self.canFightRight == True:
                                if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                                    self.x += 1    
                                    self.energy -= 1
                                    self.canFightRight = False
                                    self.isButtonDown = "isnotpushed"
                                    
                        
    def detection(self,screen,mapchip):
        #-----------------------------------------------------------------------------------------動ける所の検出
        if self.isButtonDown == "MoveLighton":#プレイヤーはx=2,y=5
            if mapchip[self.y-1][self.x] == "1": #上
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
            if mapchip[self.y+1][self.x] == "1": #下  
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
            if mapchip[self.y][self.x+1] == "1": #右
                pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
            if mapchip[self.y][self.x-1] == "1": #左
                pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)
#        if self.isButtonDown == "FightDown":
#            if mapchip[self.y-1][self.x] == "5": #上
#                pygame.draw.circle(screen,(250,250,255),((self.x+0.5)*100,(self.y-0.5)*100),10)
#            if mapchip[self.y+1][self.x] == "5": #下  
#                pygame.draw.circle(screen,(250,250,255),((self.x+0.5)*100,(self.y+1.5)*100),10)
#            if mapchip[self.y][self.x+1] == "5": #右
#                pygame.draw.circle(screen,(250,250,255),((self.x+1.5)*100,(self.y+0.5)*100),10)
#            if mapchip[self.y][self.x-1] == "5": #左
#                pygame.draw.circle(screen,(250,250,255),((self.x-0.5)*100,(self.y+0.5)*100),10)
        #------------------------------------------------------------------------------------------禁止用
        if self.isButtonDown == "MoveLighton":
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

#        if self.isButtonDown == "FightDown":
#            if mapchip[self.y-1][self.x] == "5": #上
#                self.canFightUp = True
#                #print(self.canFightUp)
#            if mapchip[self.y+1][self.x] == "5": #下  
#                self.canFightDown = True
#            if mapchip[self.y][self.x+1] == "5": #右
#                self.canFightRight = True
#           if mapchip[self.y][self.x-1] == "5": #左
#               self.canFightLeft = True



    def place(self):#----------------------------------------------------------------アクション
        if self.characterType == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                self.y = 3
    def draw(self,screen):#-----------------------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))
 
def animation(tick,players,enemys,mobs,mapchip,tx,ty,screen,font,ck):
    pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
    pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
    pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
    door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
    door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
    while tick < 800:
        tick += 1
        screen.fill((255,255,255))
        if tick < 500:
            Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = font.render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        if tick > 500:
            Story = font.render("強盗だ！金を出せ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("打たれたくないなら金だ！", True, (0,0,0)) # 描画する文字列を画像にする
        screen.blit(Story, [70,40])
        screen.blit(Story2,[70,70]) 
        for i in range(5):
            for j in range(9):
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
                elif mapchip[j][i] == "6":#不可触タイル
                    screen.blit(pt1,Rect(tx+i*100,ty+j*100,50,50))
        #---------アニメーション---------
        for player in players:
            player.firstAnimation(screen,tick)
        for enemy in enemys:
            enemy.firstAnimation(screen,tick)
        for mob in mobs:
            mob.firstAnimation(screen,tick)    
        for player in players:
            player.draw(screen)
        for enemy in enemys:
            enemy.draw(screen)
        for mob in mobs:
            mob.draw(screen)
        pygame.display.update()
        ck.tick(60) #1秒間で30フレームになるように33msecのwait      
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
    tick = 700
    writeCircle = True
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2,0,1)
    player2 = Character(3,4,"Player",Pl2,"味方","Mikata1",font2,1,1)
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font2,2,1)
    slime2 = Character(-1,0,"Slime",Sl2,"敵","GreenSlime",font2,3,1)
    goutou = Character(-1,0,"Goutou",Man,"敵","Yakuza Sumiyoshi",font2,4,2)
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font2,5,1)
    players = [player1,player2]
    enemys = [slime1,slime2,goutou]
    mobs = [cat]
    characters = [player1,player2,slime1,slime2,goutou,cat]
    #for i in range(len(characters)):
        #print(characters[i].Name,":",characters[i].id)
    mapchip = [
        ["2","2","2","2","2"],
        ["0","0","3","0","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","0","0","4","0"],
        ["0","0","0","0","0"],
        ]
    ck = pygame.time.Clock()
    animation(tick,players,enemys,mobs,mapchip,tx,ty,screen,font,ck)                     
    while True:
        tick += 1
        screen.fill((0,0,255))
        for i in range(5):
            for j in range(9):
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
        #if tick%300 == 1:
        #    Character.num += 1
        #    print(Character.num)
        if Character.num >= 4:
            Character.num = 0
        #---------プレイヤー-------------------
        for character in characters:
            if Character.num == character.id:
                character.update(screen,mapchip,characters)
            character.draw(screen)
        #---------描画---------
        if writeCircle == True:
            pygame.draw.circle(screen, (255,255,255), ((players[0].x+0.5)*100,(players[0].y+0.5)*100), 30, 5)    
        if tick == 1000:
            writeCircle = False

        pygame.display.update()         
        ck.tick(30) #1秒間で30フレームになるように33msecのwait   
main()
