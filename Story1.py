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
                for enemy in enemys:
                    if enemy.x == i and enemy.y == j:
                        if self.mapchip[j][i] == "1":
                            self.mapchip[j][i] = "5"
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
    def __init__(self,x,y,CharacterType,Image,Team,name,font2):#-----------------------------------------------------------初期化
        self.x = x      #キャラの座標
        self.y = y
        self.shui={"up":[],"down":[], "right":[],"left":[]}   #各方向になにがあるか　敵や岩、なにもないときは[]のまま、外枠の壁は"waku"

        self.action = ["move"] #取り敢えず"Move"は動く "Fight"は戦う 
        self.font2 = font2
        self.tick = 0
        self.isBUTTONDOWN = "down"
        self.Image = Image#イメージ画像
        self.Team = Team#チーム   味方チーム、敵チーム、モブチームOnly
        self.name = name#名前
        self.CharacterType = CharacterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        self.canMoveUp = False
        self.canMoveDown = False
        self.canMoveRight = False
        self.canMoveLeft = False
        self.canMove=False


    def moveCheck(self):
        #動けるかのチェック
        if self.shui["up"]==[] or self.shui["down"]==[] or self.shui["right"]==[] or self.shui["left"]==[]:
            self.canMove=True
        else:
            self.canMove=False
        print("@109 self.canMove=",self.canMove)    
        #周囲に敵がいるかのチェック


    #------------------------------------------------------------周囲のチェック
    def check(self,mapchip,characters):
        #print("------@103 self.name=",self.name)
        self.shui={"up":[],"down":[], "right":[],"left":[]}  #リセット
        #上方向のチェック
        new_y=self.y-1
        new_x=self.x
        if new_y<0:#範囲外かのチェック
            self.shui["up"].append("w1")
        else:    
            #print("@109 newy=",new_y,"new_x=",new_x)
            if int(mapchip[new_y][new_x]) > 1:#壁など建造物があるかのチェック
                self.shui["up"].append("w2")
            for ch in characters:#キャラクターがいるかのチェック
                if new_x==ch.x and new_y==ch.y:
                    if ch.Team=="味方":
                        self.shui["up"].append("c1")
                    elif ch.Team=="敵":   
                        self.shui["up"].append("c2")
                    elif ch.Team=="モブ":   
                        self.shui["up"].append("c3")

        #下方向のチェック
        new_y=self.y+1
        new_x=self.x
        if new_y>=5:
            self.shui["down"].append("w1")
        else:    
            #print("@122 newy=",new_y,"new_x=",new_x)
            if int(mapchip[new_y][new_x]) > 1:#壁など建造物があるかのチェック
                self.shui["down"].append("w2")
            for ch in characters:#キャラクターがいるかのチェック
                if new_x==ch.x and new_y==ch.y:
                    if ch.Team=="味方":
                        self.shui["down"].append("c1")
                    elif ch.Team=="敵":   
                        self.shui["down"].append("c2")
                    elif ch.Team=="モブ":   
                        self.shui["down"].append("c3")

        #右方向のチェック
        new_y=self.y
        new_x=self.x+1
        if new_x>=5:
            self.shui["right"].append("w1")
        else:    
            #print("@134 newy=",new_y,"new_x=",new_x)
            if int(mapchip[new_y][new_x]) > 1:#壁など建造物があるかのチェック
                self.shui["right"].append("w2")
            for ch in characters:#キャラクターがいるかのチェック
                if new_x==ch.x and new_y==ch.y:
                    if ch.Team=="味方":
                        self.shui["right"].append("c1")
                    elif ch.Team=="敵":   
                        self.shui["right"].append("c2")
                    elif ch.Team=="モブ":   
                        self.shui["right"].append("c3")

        #左方向のチェック
        new_y=self.y
        new_x=self.x-1
        if new_x<0:
            self.shui["left"].append("w1")
        else:    
            #print("@147 newy=",new_y,"new_x=",new_x)
            if int(mapchip[new_y][new_x]) > 1:#壁など建造物があるかのチェック
                self.shui["left"].append("w2")
            for ch in characters:#キャラクターがいるかのチェック
                if new_x==ch.x and new_y==ch.y:
                    if ch.Team=="味方":
                        self.shui["left"].append("c1")
                    elif ch.Team=="敵":   
                        self.shui["left"].append("c2")
                    elif ch.Team=="モブ":   
                        self.shui["left"].append("c3")

        print("@148 self.shui=",self.shui)

    def update(self,backGround,characters):#移動ボタン用
        self.check(backGround.mapchip,characters)

    def draw_button(self,screen): 
        print("@195 self.canMove=",self.canMove)   
        self.moveCheck()
        print("@197 self.canMove=",self.canMove)   
        if self.canMove:
            pygame.draw.rect(screen, (255,255,255), Rect(150,700,200,100))
            txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [190, 720])# 文字列の表示位置


    #---------------------------------------------------------------------------------------------------移動アクション
        #if "move" in self.action :
            #print("@53 move")
            # #----------------------------------------------------------------------------動ける所の描画
            # if self.isBUTTONDOWN == "MoveLighton":#プレイヤーはx=2,y=5
            #     if backGround.mapchip[self.y-1][self.x] == "1": #上
            #         pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
            #     if backGround.mapchip[self.y+1][self.x] == "1": #下  
            #         pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
            #     if backGround.mapchip[self.y][self.x+1] == "1": #右
            #         pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
            #     if backGround.mapchip[self.y][self.x-1] == "1": #左
            #         pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)
            #------------------------------------------------------------------------------------------動ける所の検出
            # if backGround.mapchip[self.y-1][self.x] == "1": #上
            #     self.canMoveUp = True
            # else:
            #     self.canMoveUp = False

            # if backGround.mapchip[self.y+1][self.x] == "1": #下  
            #     self.canMoveDown = True
            # else:
            #     self.canMoveDown = False

            # if backGround.mapchip[self.y][self.x+1] == "1": #右
            #     self.canMoveRight = True
            # else:
            #     self.canMoveRight = False

            # if backGround.mapchip[self.y][self.x-1] == "1": #左
            #     self.canMoveLeft = True
            # else:
            #     self.canMoveLeft = False
            #-----------------------------------------------------------------------------------------ボタン・フラグ管理
            # if self.canMoveUp or self.canMoveDown or self.canMoveRight or self.canMoveLeft:
            #     pygame.draw.rect(screen, (255,255,255), Rect(150,700,200,100))
            #     txt = self.font2.render("移動", True, (0,0,0))   # 描画する文字列の設定
            #     screen.blit(txt, [190, 720])# 文字列の表示位置
#----------------------------------------------------------------------------------------------------------戦うアクション
        # if "fight" in self.action: #--------------------------------------------------戦う
        #     print("@101 fight")

        #     if backGround.mapchip[self.y-1][self.x] == "5" or backGround.mapchip[self.y+1][self.x] == "5" or backGround.mapchip[self.y][self.x+1] == "5" or backGround.mapchip[self.y][self.x-1] == "5":
        #         pygame.draw.rect(screen, (255,255,255), Rect(150,700,200,100))
        #         txt = self.font2.render("戦う", True, (0,0,0))   # 描画する文字列の設定
        #         screen.blit(txt, [200, 720])# 文字列の表示位置
        #     else:
        #         self.action = "move"
        #         self.isBUTTONDOWN = "isnotpushed"
        #-----------------------------------------------------------------------------------------イベント処理
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 < x < 350 and 700 < y < 800:
                        self.isBUTTONDOWN = "MoveLighton"
                if self.isBUTTONDOWN == "MoveLighton":
                    if self.canMoveUp == True:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                                self.y -= 1  
                                self.isBUTTONDOWN = "Moved"
                    if self.canMoveDown == True:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                                self.y += 1  
                                self.isBUTTONDOWN = "Moved"
                    if self.canMoveLeft == True:
                        if self.x*100-100 < x < self.x*100:
                            self.x -= 1
                            self.isBUTTONDOWN = "Moved"
                    if self.canMoveRight == True:
                        if self.x*100+100 < x < self.x*100+200:
                            self.x += 1    
                            self.isBUTTONDOWN = "Moved"
    def place(self):#---------------------------------------------アクション
        if self.CharacterType == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                self.y = 3
    def draw(self,screen):#--------------------------------------------描画
        screen.blit(self.Image,Rect(self.x*100,self.y*100,50,50))


    def firstAnimation(self):#----------------------------最初のアニメーション
        self.tick += 1
        if self.CharacterType == "Slime":   
            if self.name == "BlueSlime":
                if self.tick == 120:
                    self.x = 2
                    self.y = 2
                if self.tick == 200:
                    self.y = 3
                if self.tick == 400:
                    self.x = 3
            if self.name == "GreenSlime":
                if self.tick == 200:
                    self.x = 2
                    self.y = 2
                if self.tick == 400:
                    self.y = 3
                if self.tick == 500:
                    self.x = 1
        if self.CharacterType == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                if self.tick == 400:
                    self.x = 2
                    self.y = 2
        if self.CharacterType == "Player":
            if self.name == "girl":
                if self.tick == 300:
                    self.y += 1
                if self.tick == 400:
                    #self.y += 4
                    self.y += 0
        if self.CharacterType == "Animal":
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
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2)
    girl = Character(3,4,"Player",Pl2,"モブ","girl",font2)
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font2)
    slime2 = Character(-1,0,"Slime",Sl2,"敵","GreenSlime",font2)
    goutou = Character(-1,0,"Goutou",Man,"敵","Yakuza Sumiyoshi",font2)
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font2)

    characters=[player1,slime1,slime2,goutou,cat,girl]

    #敵や味方の分類
    players=[]
    mobs=[]
    enemys=[]
    for ch in characters:
        if ch.Team=="味方":
            players.append(ch)
        elif ch.Team=="敵":
            enemys.append(ch)
        elif ch.Team=="モブ":
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
            player.update(backGround,characters)
            player.draw_button(screen)
        #---------描画---------
        for ch in characters:
            ch.draw(screen)
                        
        pygame.display.update() #こいつは引数がない        
        ck.tick(60) #1秒間で30フレームになるように33msecのwait
        # ct+=1
        # if ct>500:
        #     break

main()