import pygame
from pygame.locals import *
import sys
import random
import time
class Field():
    def __init__(self):
        self.tx = 0
        self.ty = 0
        self.pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
        self.pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
        self.pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
        self.door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
        self.door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
        self.mapchip = [
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
    def draw(self,screen):
        for i in range(5):
            for j in range(9):
                if self.mapchip[j][i] == "1":#動けるタイル
                    screen.blit(self.pt1 ,Rect(self.tx+i*100,self.ty+j*100,50,50))
                elif self.mapchip[j][i] == "0":#壁
                    screen.blit(self.pt2 ,Rect(self.tx+i*100,self.ty+j*100,50,50))  
                elif self.mapchip[j][i] == "2":#字幕
                    screen.blit(self.pt3 ,Rect(self.tx+i*100,self.ty+j*100,50,50))
                elif self.mapchip[j][i] == "3":#ドア
                    screen.blit(self.door ,Rect(self.tx+i*100,self.ty+j*100,50,50))
                elif self.mapchip[j][i] == "4":#ドア
                    screen.blit(self.door2,Rect(self.tx+i*100,self.ty+j*100,50,50))
class Character():
    num = 0#クラス変数
    def __init__(self,x,y,characterType,image,team,name,font2,id,energy,at,df,hp):#-----------------------------------------------------------初期化
        #-------------------------------キャラクター
        #------------------キャラクターID
        self.id = id#id番号 
        #------------------キャラクターの基本変数
        self.x = x
        self.y = y
        self.at = at
        self.df = df
        self.hp = hp
        #---------------------キャラクターのタイプ変数
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム
        self.name = name#名前
        self.characterType = characterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        #--------------------キャラクターエネルギー
        self.energy = energy
        self.tenergy = energy#保存
        #----------------------------------------------設定
        #--------------------フォント
        self.font2 = font2
        #---------------------ティック秒
        self.tick = 0#全体のティック
        self.animationTick = 0#アニメーションのティック
        #----------------------------------------------演算
        #----------------------味方の場合に動けるか
        self.playerMove = []#"ue" = 上へ行ける "sita" = 下にいける "migi" = "右にいける" "hidari" = "左に行ける"
        #----------------------戦えるか
        self.playerFight = []#fighton + isfight
        self.enemyFight = []
        #----------------------敵の場合に動けるか
        self.enemyMove = []
        #-----------------------------------------------判別・処理
        self.buttonStatus = "Down"#イベントキーが現在どうなってるか
        self.buttonEvent = "isnotpushed"
        """ステータス
          ・Downは未稼働
        　・MoveLightonの場合は移動ができる   
        　・FightDownの場合は攻撃ができる"""  
        """イベント
        　・isnotpushedの場合はボタンが押されてない
        　・ispushedの場合はボタンが押されている"""
        #------------------------戦うフラグ
        self.isFight = False#戦えるか判別
        #------------------------リセットキー                    
        self.fightFalses = False
        #------------------------索敵
        self.characterlists = {}
        self.wall = []
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
    def enemyMoveDetection(self,mapchip):
        if mapchip[self.y-1][self.x] == "1": #上
            self.enemyMove.append("ue")
        else:
            if "ue" in self.enemyMove:
                self.enemyMove.remove("ue")
        if mapchip[self.y+1][self.x] == "1": #下  
            self.enemyMove.append("sita")
        else:
            if "sita" in self.enemyMove:
                self.enemyMove.remove("sita")
        if mapchip[self.y][self.x+1] == "1": #右
            self.enemyMove.append("migi")
        else:
            if "migi" in self.enemyMove:
                self.enemyMove.remove("migi")
        if mapchip[self.y][self.x-1] == "1": #左
            self.enemyMove.append("hidari")
        else:
            if "hidari" in self.enemyMove:
                self.enemyMove.remove("hidari")
    def enemyInfoDetection(self,mapchip,character):
        if self.x == character.x and self.y-1 == character.y: #移上
            if "ue" in self.enemyMove:
                self.enemyMove.remove("ue")
        if self.x == character.x and self.y+1 == character.y: #移下  
            if "sita" in self.enemyMove:
                self.enemyMove.remove("sita")
        if self.x+1 == character.x and self.y == character.y: #移右
            if "migi" in self.enemyMove:
                self.enemyMove.remove("migi")
        if self.x-1 == character.x and self.y == character.y: #移左
            if "hidari" in self.enemyMove:
                self.enemyMove.remove("hidari")
        #攻
        if self.x == character.x and self.y-1 == character.y: #攻上
            self.enemyFight.append("ue")
        if self.x == character.x and self.y+1 == character.y: #攻下
            self.enemyFight.append("sita")
        if self.x+1 == character.x and self.y == character.y: #攻右
            self.enemyFight.append("migi")
        if self.x-1 == character.x and self.y == character.y: #攻左
            self.enemyFight.append("hidari")
    def enemyEvent(self,character):
        self.enemyFightCalculation(character)
    def enemyFightCalculation(self,character):
        if self.x == character.x and self.y-1 == character.y: #攻上
            if self.hp+10 <= character.hp:
                self.enemyFight.remove("ue")
        if self.x == character.x and self.y+1 == character.y: #攻下
            if self.hp+10 <= character.hp:
                self.enemyFight.append("sita")
        if self.x+1 == character.x and self.y == character.y: #攻右
            if self.hp+10 <= character.hp:
                self.enemyFight.append("migi")              
        if self.x-1 == character.x and self.y == character.y: #攻左
            if self.hp+10 <= character.hp:
                self.enemyFight.append("hidari")        
    def enemyUpdate(self,screen,mapchip,characters,font2):#移動ボタン用
    #----------------------------------------------------------------------------------------------------------移動アクション
        self.playerMove.clear()
        self.enemyMove.clear()
        self.enemyFight.clear()
        """update
        update敵
        　敵の上下左右が壁じゃないか調べる
        　　上下左右に壁がない限り動けるリストに挿入する
        　ループ
            敵の情報収集enemydetection
        　　    索敵して情報を集める  流れ1.敵にとっての敵がいるかを探す,2.敵の数を確認する　　
            敵と戦う時のイベントenemyEvent
                敵の戦う時の計算enemyFightCalculation
                    相手と自分の体力で有利か不利かを調べる
                    有利なら攻撃             2.相手の体力が自分より低ければ戦う
                    不利なら撤退            　相手の体力が〝 より高ければ逃げる
                    enemydetectionで調べた2体以上いるか
                    自分が無鉄砲かビビりか
                ↑の判断で戦うor逃げる
                (↓戦う場合)
                相手に攻撃を仕掛ける
                相手が逃げた場合、相手がいた方向へ進む
                無鉄砲は体力25%以下でも攻撃を仕掛けてくる
                (↓逃げる場合)
                相手と戦わずに
                energyを0にするまで奥へと逃げる
                直前に薬草で体力を少し回復する
            　　ビビりなら25%以下になったら奥へと逃げ、回復する

        update味方
        　　索敵
            行動をリセット
            　動くや攻撃などが次のターンまで続かないように、
        　　　イベントをisnotpushed(未操作状態)にする
                ステータスを"動く"にする
                イベント
                    (あらかじめcircleが
                　　索敵して相手が上下左右にいないか調べる
                　    範囲(●)を表示)
            　  索敵で縮められた範囲で動く
                　動いた(動いてない時も含む)時に範囲内に敵がいる場合●を押すと攻撃する
        """
        self.enemyMoveDetection(mapchip)
        for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
            if "味方" in character.team:
                self.enemyInfoDetection(mapchip,character)#情報収集
                self.enemyEvent(character)
                
                """if "migi" in self.enemyMove:
                    self.x += 1
                    self.energy -= 1
                    
                if "hidari" in self.enemyMove:
                    self.x -= 1
                    self.energy -= 1
                if "sita" in self.enemyMove:
                    self.y += 1
                    self.energy -= 1
                if "ue" in self.enemyMove:
                    self.y -= 1
                    self.energy -= 1
                print(self.name,self.energy)#-2になる。
                print(self.enemyMove)
                #ターン攻撃
                if "migi" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "hidari" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "sita" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "ue" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if self.energy <= 0:
                    Character.num += 1
                    self.energy = self.tenergy"""
    def playerUpdate(self,screen,mapchip,characters,font2):#移動ボタン用
        self.detection(screen,mapchip,characters)
        if self.energy <= 0:
            Character.num += 1
            self.energy = self.tenergy
            self.buttonEvent = "isnotpushed"

        #-----------------------------------------------------------------------------------------ボタン・フラグ管理
        if self.buttonStatus != "MoveLighton":#上下左右のどれかに動ける
            if self.buttonStatus != "FightDown":#戦える
                self.buttonEvent = "isnotpushed"
        self.buttonStatus = "MoveLighton"    
        self.event(screen)
            #-----------------------------------------------------------------------------------------イベント処理
    def event(self,screen):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                if self.buttonEvent == "isnotpushed":
                    x, y = event.pos
                    #print("x,y:",x,y)　イベントの座標
                if self.buttonStatus == "MoveLighton":
                    x, y = event.pos 
                    if "ue" in self.playerMove: 
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            self.y -= 1  
                            self.energy -= 1
                            self.buttonEvent = "isnotpushed"
                    if "sita" in self.playerMove:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            self.y += 1 
                            #print("MOVE") 
                            self.energy -= 1
                            self.buttonEvent = "isnotpushed"
                    #print(self.y*100+100,y,self.y*100)
                    if "hidari" in self.playerMove:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            self.x -= 1
                            self.energy -= 1
                            self.buttonEvent = "isnotpushed"
                    if "migi" in self.playerMove:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            self.x += 1    
                            self.energy -= 1
                            self.buttonEvent = "isnotpushed"     
                if self.isFight == True:
                    x,y = event.pos
                    self.buttonStatus = "FightDown"
                    #print("hannou")
                    if "ue" in self.playerFight:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            self.fight()
                            self.energy -= 1
                            self.fightFalses = True
                            self.buttonEvent = "MoveLighton"
                    if "sita" in self.playerFight:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            self.fight()
                            self.energy -= 1
                            self.fightFalses = True
                            self.buttonEvent = "MoveLighton"
                    if "hidari" in self.playerFight:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            self.fight()
                            self.energy -= 1
                            self.fightFalses = True
                            self.buttonEvent = "MoveLighton"
                    if  "migi" in self.playerFight:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            self.fight()
                            self.energy -= 1
                            self.fightFalses = True
                            self.buttonEvent = "MoveLighton"
                    if self.fightFalses == True:
                        if "ue" in self.playerFight:
                            self.playerFight.remove("ue")
                        if "sita" in self.playerFight:
                            self.playerFight.remove("sita")
                        if "hidari" in self.playerFight:
                            self.playerFight.remove("hidari")
                        if "migi" in self.playerFight:
                            self.playerFight.remove("migi")
    def detection(self,screen,mapchip,characters):#動くときに周囲をチェックする関数
        #-----------------------------------------------------------------------------------------動ける所の検出
        if self.buttonStatus == "MoveLighton":#プレイヤーはx=2,y=5
            self.wall = []
            self.characterlists = {}
            for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
                #-----------------------------------------------------------索敵(敵)
                if self.x == character.x and self.y-1 == character.y:
                    if character.team == "味方":
                        self.characterlists["上"] = ["味方",character.name]
                    else:
                        self.characterlists["上"] = ["敵",character.name]

                if self.x == character.x and self.y+1 == character.y:
                    if character.team == "味方":
                        self.characterlists["下"] = ["味方",character.name]
                    else:
                        self.characterlists["下"] = ["敵",character.name]

                if self.x+1 == character.x and self.y == character.y:
                    if character.team == "味方":
                        self.characterlists["右"] = ["味方",character.name]
                    else:
                        self.characterlists["右"] = ["敵",character.name]

                if self.x-1 == character.x and self.y == character.y:
                    if character.team == "味方":
                        self.characterlists["左"] = ["味方",character.name]
                    else:
                        self.characterlists["左"] = ["敵",character.name]
            #print(self.characterlists)
            #------------------------------------------------------------------壁検知
            #print(self.characterlists)
            if mapchip[self.y-1][self.x] != "1": #上
               self.wall.append("上")
            if mapchip[self.y+1][self.x] != "1": #上
                self.wall.append("下")
            if mapchip[self.y][self.x+1] != "1": #上
                self.wall.append("右")
            if mapchip[self.y][self.x-1] != "1": #上
                self.wall.append("左")
            #print("キャラクター",self.characterlists)
            #print("壁",self.wall)
            #-------------------黄色い丸を書く
            #--------------------------------------------------------------------------------------動き判定
            #if mapchip[self.y-1][self.x] == "1": #上
            #    #print("上" in self.characterlists.keys())
            #    if "上" in self.characterlists.keys():#上に何もなければ黄色い丸を表示
            #        self.cget = self.characterlists.get("上", [])  # キーが存在しない場合は空リストを返す
            #        #print(self.cget)   
            #        if self.cget[0] == "敵":
            #            pygame.draw.circle(screen,(250,0,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
            #        elif self.cget[0] == "味方":
            #            pygame.draw.circle(screen,(0,0,250),((self.x+0.5)*100,(self.y-0.5)*100),10)
            #        self.isFight = True
            #        self.playerFight.append("ue")
            #    else:
            #            pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)

        #------------------------------------------------------------------------------------------禁止用
        if self.buttonStatus == "MoveLighton":
            if mapchip[self.y-1][self.x] == "1": #上
                self.playerMove.append("ue")
            #else:
            #    self.canMoveUp = False
            if mapchip[self.y+1][self.x] == "1": #下  
                self.playerMove.append("sita")
            #else:
            #    self.canMoveDown = False
            if mapchip[self.y][self.x+1] == "1": #右
                self.playerMove.append("migi")
            #else:
            #    self.canMoveRight = False
            if mapchip[self.y][self.x-1] == "1": #左
                self.playerMove.append("hidari")
            #else:
            #    self.canMoveLeft = False
            for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
                if self.x == character.x and self.y-1 == character.y: #上
                    if "ue" in self.playerMove:
                        self.playerMove.remove("ue")
                if self.x == character.x and self.y+1 == character.y: #下  
                    if "sita" in self.playerMove:
                        self.playerMove.remove("sita")
                if self.x+1 == character.x and self.y == character.y: #右
                    if "migi" in self.playerMove:
                        self.playerMove.remove("migi")
                if self.x-1 == character.x and self.y == character.y: #左
                    if "hidari" in self.playerMove:
                        self.playerMove.remove("hidari")

    def fight(self):
        print(self.name,"は","に攻撃をした！")
        return
    """def fightupdate(self,screen,font2,characters):
        for character in characters:
            if self.x == enemy.x and self.y-1 == enemy.y or self.x == enemy.x and self.y+1 == enemy.y or self.x+1 == enemy.x and self.y == enemy.y or self.x-1 == enemy.x and self.y == enemy.y:
                self.isFight = True
            else:
                self.isFight = False"""
    def place(self):#----------------------------------------------------------------アクション
        if self.characterType == "Goutou":
            if self.name == "Yakuza Sumiyoshi":
                self.y = 3
    def circle(self,screen,mapchip):
        self.playerFight.clear()
        #print(self.y-1,self.x)
        if mapchip[self.y-1][self.x] == "1": #上
            #print("上" in self.characterlists.keys())
            if "上" in self.characterlists.keys():#上に何もなければ黄色い丸を表示
                self.cget = self.characterlists.get("上", [])  # キーが存在しない場合は空リストを返す
                #print(self.cget)   
                if self.cget[0] == "敵":
                    pygame.draw.circle(screen,(250,0,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
                    self.isFight = True
                    self.playerFight.append("ue")
                elif self.cget[0] == "味方":
                    pygame.draw.circle(screen,(0,0,250),((self.x+0.5)*100,(self.y-0.5)*100),10)
            else:
                    pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)

            if mapchip[self.y-1][self.x] == "1": #下
                #print("下" in self.characterlists.keys())
                if "下" in self.characterlists.keys():#下に何もなければ黄色い丸を表示
                    self.cget = self.characterlists.get("下", [])  # キーが存在しない場合は空リストを返す
                    #print(self.cget)   
                    if self.cget[0] == "敵":
                        pygame.draw.circle(screen,(250,0,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
                        self.isFight = True
                        self.playerFight.append("sita")
                    elif self.cget[0] == "味方":
                        pygame.draw.circle(screen,(0,0,250),((self.x+0.5)*100,(self.y+1.5)*100),10)
                else:
                    pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)

            if mapchip[self.y][self.x-1] == "1": #左
                #print("左" in self.characterlists.keys())
                if "左" in self.characterlists.keys():#左に何もなければ黄色い丸を表示
                    self.cget = self.characterlists.get("左", [])  # キーが存在しない場合は空リストを返す
                    #print(self.cget)   
                    if self.cget[0] == "敵":
                        pygame.draw.circle(screen,(250,0,0),((self.x-0.5)*100,(self.y+0.5)*100),10)
                        self.isFight = True
                        self.playerFight.append("hidari")
                    elif self.cget[0] == "味方":
                        pygame.draw.circle(screen,(0,0,255),((self.x-0.5)*100,(self.y+0.5)*100),10)
                else:
                    pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)

            if mapchip[self.y][self.x+1] == "1": #右
                #print("右" in self.characterlists.keys())
                if "右" in self.characterlists.keys():#右に何もなければ黄色い丸を表示
                    self.cget = self.characterlists.get("右", [])  # キーが存在しない場合は空リストを返す
                    #print(self.cget)   
                    if self.cget[0] == "敵":
                        pygame.draw.circle(screen,(250,0,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
                        self.isFight = True
                        self.playerFight.append("migi")
                    elif self.cget[0] == "味方":
                        pygame.draw.circle(screen,(0,0,255),((self.x+1.5)*100,(self.y+0.5)*100),10)
                else:
                    pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)


        
    def draw(self,screen):#-----------------------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))#キャラクターの描画

def animation(tick,characters,mapchip,screen,font,ck,field):
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
        field.draw(screen)
        #---------アニメーション---------
        for character in characters:
            character.firstAnimation(screen,tick)
            character.draw(screen)
        pygame.display.update()
        ck.tick(160) #1秒間で30フレームになるように33msecのwait      
def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60)                       
    screen = pygame.display.set_mode((500, 900))  # 800
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主
    tick = 700
    field = Field()
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2,0,3,24,12,50)#x、y、タイプ、画像、チーム、名前、フォント、id,行動力、攻撃力、防御力、体力
    player2 = Character(3,4,"Player",Pl2,"味方","Mikata1",font2,1,2,6,6,30)#攻撃力、防御力は6,行動力は1ずつ増えていく。最大30(行動力は最大5)
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font2,2,1,12,12,60)
    slime2 = Character(-1,0,"Slime",Sl2,"敵","GreenSlime",font2,3,1,24,0,60)
    goutou = Character(-1,0,"Goutou",Man,"敵","Yakuza Sumiyoshi",font2,4,4,30,6,80)
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font2,5,1,0,0,20)
    characters = [slime1,slime2,goutou,cat,player1,player2]
    #for i in range(len(characters)):
        #print(characters[i].Name,":",characters[i].id)

    ck = pygame.time.Clock()
    animation(tick,characters,field.mapchip,screen,font,ck,field)                     
    while True:
        tick += 1
        screen.fill((0,0,255))
        field.draw(screen)
        #if tick%300 == 1:
        #    Character.num += 1
        #    print(Character.num)
        if Character.num >= 4:
            Character.num = 0
        #---------プレイヤー-------------------
        for character in characters:
            if Character.num == character.id:
                #if character.team == "敵":
               character.enemyUpdate(screen,field.mapchip,characters,font2)
                #if character.team == "味方":
                character.playerUpdate(screen,field.mapchip,characters,font2)
            character.draw(screen)
        for character2 in characters:
            if Character.num == character2.id:
                if character2.team == "味方":
                    character2.circle(screen,field.mapchip)
            
        #---------描画---------  
        pygame.display.update()         
        ck.tick(33) #1秒間で30フレームになるように33msecのwait   
main()
