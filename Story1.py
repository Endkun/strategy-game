import pygame
from pygame.locals import *
import sys
import random
import time


class BackGround():
    def __init__(self):
        pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
        pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
        pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
        door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
        door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
        self.tiles=[pt2,pt1,pt3,door,door2,pt1]
        self.mapchip = [
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

    def draw(self,screen,enemys):
        tx = 0#タイル用x,y
        ty = 0
        screen.fill((255,255,255))
        for i in range(5):
            for j in range(9):
                # for enemy in enemys:
                #     if enemy.x == i and enemy.y == j:
                #         if self.mapchip[j][i] == "1":
                #             self.mapchip[j][i] = "5"
                mapnum = int(self.mapchip[j][i])            
                screen.blit(self.tiles[mapnum] ,Rect(tx+i*100,ty+j*100,50,50))            

def opening(screen,font,enemys,players,mobs,backGround):#--------------------
    ##オープニング
    ck = pygame.time.Clock()
    tick=0
    while True:
        tick += 1
        if tick>800:
            break

        backGround.draw(screen,enemys)

        if tick <= 500:
            Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = font.render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        elif 500 < tick <= 700:
            Story = font.render("強盗だ！金を出せ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("56されたくないなら金だ！", True, (0,0,0)) # 描画する文字列を画像にする
        if tick > 700:
            Story = font.render("こいつ、逆らう気だぞ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("野郎ども　やっちまえ", True, (0,0,0)) # 描画する文字列を画像にする
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
        for player in players:
            player.draw(screen)
        for enemy in enemys:
            enemy.draw(screen)
        for mob in mobs:
            mob.draw(screen)
                          
        pygame.display.update()         
        ck.tick(60) #1秒間で30フレームになるように33msecのwait                           

class Character():
    def __init__(self,x,y,type,image,team,name,font2,pocket):#-----------------------------------------------------------初期化
        self.name = name#名前
        self.x = x      #キャラの座標
        self.y = y
        self.shui={"up":[],"down":[], "right":[],"left":[]}   #各方向になにがあるか　敵や岩、なにもないときは[]のまま、
        self.pocket=pocket#持ち物
        self.type = type#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム、モブチームOnly
        self.font2 = font2

        self.tick = 0
        self.button=""
        self.canFight = False
        self.canHeal = False
        self.canMove=False
        self.mode = "first"


    def moveCheck(self):
        #動けるかのチェック
        #print("@104 self.shui=",self.shui)
        if self.shui["up"]==[] or self.shui["down"]==[] or self.shui["right"]==[] or self.shui["left"]==[]:
            self.canMove=True
        else:
            self.canMove=False

        #周囲に敵がいるかのチェック
        teki="c2"
        if teki in self.shui["up"] or teki in self.shui["down"] or teki in self.shui["right"] or teki in self.shui["left"]:
            self.canFight=True
        else:
            self.canFight=False
        #print("@115 self.canFight=",self.canFight)

        #薬草を持っているかのチェック
        if "薬草" in self.pocket:
            self.canHeal=True
        else:
            self.canHeal=False   

    #------------------------------------------------------------周囲のチェック
    def check_direction(self, direction, delta_x, delta_y, mapchip, characters):
        new_x = self.x + delta_x
        new_y = self.y + delta_y
        map_w1 = 1
        map_h1 =3
        map_w2 = 4
        map_h2 =6

        if not (map_w1 <= new_x < map_w2 and map_h1 <= new_y < map_h2):  # 範囲外のチェック
            self.shui[direction].append("w1")
        elif int(mapchip[new_y][new_x]) > 1:  # 壁や建造物のチェック
            self.shui[direction].append("w2")
        else:
            for ch in characters:  # キャラクターのチェック
                if new_x == ch.x and new_y == ch.y:
                    code = "c1" if ch.team == "味方" else "c2" if ch.team == "敵" else "c3"
                    self.shui[direction].append(code)


    def check(self, mapchip, characters):
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]

        for direction, dx, dy in directions:
            self.check_direction(direction, dx, dy, mapchip, characters)

    def draw_button(self,screen): #---------------------------ボタン描画
        #print("@195 self.canMove=",self.canMove)   
        self.moveCheck()
        #print("@197 self.canMove=",self.canMove)   
        if self.canMove:
            pygame.draw.rect(screen, (255,255,255), Rect(50,800,120,40))
            txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [80, 805])# 文字列の表示位置
        if self.canFight:
            pygame.draw.rect(screen, (255,255,255), Rect(200,800,120,40))
            txt = self.font2.render("戦闘", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [230, 805])# 文字列の表示位置
        if self.canHeal:
            pygame.draw.rect(screen, (255,255,255), Rect(350,800,120,40))
            txt = self.font2.render("回復", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [380, 805])# 文字列の表示位置

    def player_mouse(self):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                self.button=""
                if 800< y_pos < 830:
                    if 50<x_pos<150 and self.canMove:
                        self.button="move"
                    elif 200<x_pos<300 and self.canFight:
                        self.button="fight"
                    elif 350<x_pos<500 and self.canHeal:
                        self.button="heal" 
                print("p239 self.button=",self.button)        


    def player_mouse2(self):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/100)
                new_y=int(y_pos/100)
                print("@195 new_x=",new_x," new_y=",new_y)
                if self.shui["up"]==[]     and new_y-self.y== -1 and self.x-new_x== 0:
                        self.y -= 1
                elif self.shui["down"]==[] and new_y-self.y== 1 and self.x-new_x== 0:
                        self.y += 1
                elif self.shui["left"]==[] and self.y-new_y== 0 and new_x-self.x== -1:
                        self.x -= 1
                elif self.shui["right"]==[] and self.y-new_y== 0 and new_x-self.x== 1:
                        self.x += 1



    def update(self,screen,backGround,characters):#移動ボタン用
        if self.button=="":
            self.check(backGround.mapchip,characters)
            self.player_mouse()          
            self.draw_button(screen)
        elif self.button=="move":
            self.check(backGround.mapchip,characters)
            self.draw_point(screen)
            self.player_mouse2()          

    def draw_point(self, screen): #動ける場所に黄色いガイド点を描く
        #print("@250 self.shui=",self.shui)     
        if self.shui["up"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
        if self.shui["down"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
        if self.shui["right"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
        if self.shui["left"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)


    def place(self):#---------------------------------------------アクション
        if self.type == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                self.y = 3
    def draw(self,screen):#--------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))


    def firstAnimation(self):#----------------------------最初のアニメーション
        self.tick += 1
        if self.type == "Slime":   
            if self.name == "BlueSlime":
                if self.tick == 120:
                    self.x = 2
                    self.y = 2
                if self.tick == 200:
                    self.y = 4
                if self.tick == 400:
                    self.x = 1
            if self.name == "GreenSlime":
                if self.tick == 200:
                    self.x = 2
                    self.y = 2
                if self.tick == 400:
                    self.y = 3
                if self.tick == 500:
                    self.x = 1
        if self.type == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                if self.tick == 400:
                    self.x = 2
                    self.y = 2
        if self.type == "Player":
            if self.name == "girl":
                if self.tick == 300:
                    self.y += 1
                if self.tick == 400:
                    #self.y += 4
                    self.y += 0
        if self.type == "Animal":
            if self.name == "Cat":
                if self.tick == 400:
                    self.y += 1
                if self.tick == 550:
                    self.x += 2
                if self.tick == 650:
                    self.y += 4

def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60)                       
    screen = pygame.display.set_mode((500, 900))  # 800
    ck = pygame.time.Clock()

    #image load
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主

    #instance
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font,["剣","薬草"])
    girl = Character(3,4,"Player",Pl2,"モブ","girl",font,["薬草"])
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font,["薬草"])
    slime2 = Character(-1,0,"Slime",Sl2,"敵","GreenSlime",font,["薬草"])
    goutou = Character(-1,0,"Goutou",Man,"敵","Yakuza Sumiyoshi",font,["剣","薬草"])
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font,[])

    characters=[player1,slime1,slime2,goutou,cat,girl]

    #敵や味方の分類
    players=[]
    mobs=[]
    enemys=[]
    for ch in characters:
        if ch.team=="味方":
            players.append(ch)
        elif ch.team=="敵":
            enemys.append(ch)
        elif ch.team=="モブ":
            mobs.append(ch)

    backGround=BackGround()

    #opening
    opening(screen,font,enemys,players,mobs,backGround)

    # for ch in characters:
    #     print("ch.name=",ch.name," ch.x=",ch.x,"ch.y=",ch.y)
    #ct=0


    #battle 　
    while True:
        backGround.draw(screen,enemys)

        #---------プレイヤー-------------------
        for player in players:
            player.update(screen,backGround,characters)
        #---------描画---------
        for ch in characters:
            ch.draw(screen)
                        
        pygame.display.update() #こいつは引数がない        
        ck.tick(60) #1秒間で30フレームになるように33msecのwait
        # ct+=1
        # if ct>500:
        #     break

main()