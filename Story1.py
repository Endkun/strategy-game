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
        self.at = at#アタックポイント
        self.tat = at#保存用1
        self.df = df#ディフェンスポイント
        self.tdf = df#保存用2
        self.hp = hp#ヘルス
        self.thp = hp#保存用3
        #---------------------キャラクターのタイプ変数
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム
        self.name = name#名前
        self.characterType = characterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        #--------------------キャラクターエネルギー
        self.energy = energy
        self.tenergy = energy#保存用エナジー
        #----------------------------------------------設定
        #--------------------フォント
        self.font2 = font2
        #---------------------ティック秒
        self.tick = 0#全体のティック
        self.animationTick = 0#アニメーションのティック
        #----------------------------------------------演算
        #----------------------味方の場合に動けるか
        self.findMove = []#"ue" = 上へ行ける "sita" = 下にいける "migi" = "右にいける" "hidari" = "左に行ける"
        #----------------------戦えるか
        self.findFight = []#fighton + isfight
        #----------------------対戦相手
        self.opponent = []
        
        #-----------------------------------------------判別・処理

        
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
        """上下左右に敵がいたらキャラクターリストにキャラクターの情報入れる
        　　　　　　　　　　　　　  例:{'左': ['敵', 'Gorotsuki'], '下': ['味方', 'Mikata1']}"""   
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
            if self.name == "YellowSlime":
                if self.animaionTick >= 200:
                    self.x = 2
                    self.y = 2
                if self.animaionTick >= 400:
                    self.y = 3
                if self.animaionTick >= 500:
                    self.x = 1
        if self.characterType == "Goutou":
            if self.name == "Gorotsuki":
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
        #print(f"{self.y-1=}")
        if mapchip[self.y-1][self.x] == "1": #上
            self.findMove.append("ue")
        else:
            if "ue" in self.findMove:
                self.findMove.remove("ue")
        if mapchip[self.y+1][self.x] == "1": #下  
            self.findMove.append("sita")
        else:
            if "sita" in self.findMove:
                self.findMove.remove("sita")
        if mapchip[self.y][self.x+1] == "1": #右
            self.findMove.append("migi")
        else:
            if "migi" in self.findMove:
                self.findMove.remove("migi")
        if mapchip[self.y][self.x-1] == "1": #左
            self.findMove.append("hidari")
        else:
            if "hidari" in self.findMove:
                self.findMove.remove("hidari")
    def enemyInfoDetection(self,mapchip,character):
        if self.x == character.x and self.y-1 == character.y: #移上
            if "ue" in self.findMove:
                self.findMove.remove("ue")
        if self.x == character.x and self.y+1 == character.y: #移下  
            if "sita" in self.findMove:
                self.findMove.remove("sita")
        if self.x+1 == character.x and self.y == character.y: #移右
            if "migi" in self.findMove:
                self.findMove.remove("migi")
        if self.x-1 == character.x and self.y == character.y: #移左
            if "hidari" in self.findMove:
                self.findMove.remove("hidari")
        if (self.x - 1 == character.x and self.y == character.y and \
            self.x + 1 == character.x and self.y == character.y) or \
           (self.x == character.x and self.y + 1 == character.y and \
            self.x == character.x and self.y - 1 == character.y):
            self.at-random.randint(10,15)
            self.df-random.randint(0,5)
            print(f"{self.at=} {self.tat=}")
        else:
            self.at = self.tat
            self.df = self.tdf

    def enemyEvent(self,character):
        self.enemyFightCalculation(character) 
        if self.hp < self.thp/3:
            print(self.name,"は薬草を使った！")
            self.hp += random.randint(0,20)  
    def enemyFightCalculation(self,character):
        if self.x == character.x and self.y-1 == character.y: #攻上
            if self.hp >= 25:
                if self.hp+10 >= character.hp:
                    self.findFight.append("ue")
                    self.findFight.append(character.name)
        #else:
        #    if "ue" in self.findFight:
        #        self.findFight.remove("ue")
        #        self.findFight.remove(character.name)

        if self.x == character.x and self.y+1 == character.y: #攻下
            if self.hp >= 25:
                if self.hp+10 >= character.hp:
                    self.findFight.append("sita")
                    self.findFight.append(character.name)
        #else:
        #    if "sita" in self.findFight:
        #        self.findFight.remove("sita")
        #        self.findFight.remove(character.name)

        if self.x+1 == character.x and self.y == character.y: #攻右
            if self.hp >= 25:
                if self.hp+10 >= character.hp:
                    self.findFight.append("migi")
                    self.findFight.append(character.name)
        #else:
        #    if "migi" in self.findFight:
        #        self.findFight.remove("migi") 
        #        self.findFight.remove(character.name)

        if self.x-1 == character.x and self.y == character.y: #攻左
            if self.hp >= 25:
                if self.hp+10 >= character.hp:
                    self.findFight.append("hidari")
                    self.findFight.append(character.name)
        #else:
        #    if "hidari" in self.findFight:
        #        self.findFight.remove("hidari")
        #        self.findFight.remove(character.name)
        #print(self.findFight)
    def enemyUpdate(self,screen,mapchip,characters,font2):#移動ボタン用
    #----------------------------------------------------------------------------------------------------------移動アクション
        self.findMove.clear()
        self.findFight.clear()
        #print(self.name,"A",self.x,self.y)
        if self.hp <= 0:
            self.x = -10
            self.y = -10
            Character.num += 1
            return
        if self.hp > 1:
            self.enemyMoveDetection(mapchip)
        for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
            if character.team == "味方":
                self.enemyEvent(character)
            self.enemyInfoDetection(mapchip,character)#情報収集
            """findMoveは配列,データにmigi,hidari,sita,ueの４つが入る
               例えば['sita', 'hidari']等"""
        #print(self.findFight)
        if self.findFight == []:
            self.randomc = random.randint(0,4)
            if self.randomc == 1:
                if "migi" in self.findMove:
                    self.x += 1   
            if self.randomc == 2:       
                if "hidari" in self.findMove:
                    self.x -= 1  
            if self.randomc == 3:       
                if "sita" in self.findMove:
                    self.y += 1
            if self.randomc == 4:
                if "ue" in self.findMove:
                    self.y -= 1
            self.energy -= 1
            if self.energy <= 1:
                Character.num += 1
                self.energy = self.tenergy
        else:
            print(self.name,"が",self.findFight[1],"に攻撃")
            for character in characters:
                if character.name == self.findFight[1]:
                    character.hp -= self.at-self.df
            #print(self.addName,"に攻撃")
            Character.num += 1
            
                
    def playerUpdate(self,screen,mapchip,characters,font2):#移動ボタン用
        #print(f"@275{self.name=} {self.characterlists=}") 
        if self.hp <= 0:
            Character.num += 1
            self.x = -10
            self.y = -10
            return
        self.detection(screen,mapchip,characters)
        if self.energy <= 0:
            Character.num += 1
            self.energy = self.tenergy

        self.event(screen,characters)
            #-----------------------------------------------------------------------------------------イベント処理
    def event(self,screen,characters):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos 
                if "ue" in self.findMove: 
                    if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                        self.y -= 1  
                        self.energy -= 1
                if "sita" in self.findMove:
                    if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                        self.y += 1 
                        self.energy -= 1
                if "hidari" in self.findMove:
                    if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                        self.x -= 1
                        self.energy -= 1
                if "migi" in self.findMove:
                    if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                        self.x += 1    
                        self.energy -= 1     
                if self.isFight == True:
                    x,y = event.pos
                    self.opponent.clear()
                    if "ue" in self.findFight:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            sc = self.characterlists['上']
                            self.opponent.append(sc[1])
                            self.fight(characters)
                            self.energy -= 1
                            self.fightFalses = True
                    if "sita" in self.findFight:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            sc = self.characterlists['下']
                            self.opponent.append(sc[1])
                            self.fight(characters)
                            self.energy -= 1
                            self.fightFalses = True
                    if "hidari" in self.findFight:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            sc = self.characterlists['左']
                            self.opponent.append(sc[1])
                            self.fight(characters)
                            self.energy -= 1
                            self.fightFalses = True
                    if  "migi" in self.findFight:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            sc = self.characterlists['右']
                            self.opponent.append(sc[1])
                            self.fight(characters)
                            self.energy -= 1
                            self.fightFalses = True
                    if self.fightFalses == True:
                        if "ue" in self.findFight:
                            self.findFight.remove("ue")
                        if "sita" in self.findFight:
                            self.findFight.remove("sita")
                        if "hidari" in self.findFight:
                            self.findFight.remove("hidari")
                        if "migi" in self.findFight:
                            self.findFight.remove("migi")
    def detection(self,screen,mapchip,characters):#動くときに周囲をチェックする関数
    #-----------------------------------------------------------------------------------------動ける所の検出
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
        #------------------------------------------------------------------壁検知
        if mapchip[self.y-1][self.x] != "1": #上
            self.wall.append("上")
        if mapchip[self.y+1][self.x] != "1": #上
            self.wall.append("下")
        if mapchip[self.y][self.x+1] != "1": #上
            self.wall.append("右")
        if mapchip[self.y][self.x-1] != "1": #上
            self.wall.append("左")
        #--------------------------------------------------------------------------------------動き判定
        if mapchip[self.y-1][self.x] == "1": #上
            self.findMove.append("ue")
        #else:
        #    self.canMoveUp = False
        if mapchip[self.y+1][self.x] == "1": #下  
            self.findMove.append("sita")
        #else:
        #    self.canMoveDown = False
        if mapchip[self.y][self.x+1] == "1": #右
            self.findMove.append("migi")
        #else:
        #    self.canMoveRight = False
        if mapchip[self.y][self.x-1] == "1": #左
            self.findMove.append("hidari")
        #else:
        #    self.canMoveLeft = False
        for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
            if self.x == character.x and self.y-1 == character.y: #上
                if "ue" in self.findMove:
                    self.findMove.remove("ue")
            if self.x == character.x and self.y+1 == character.y: #下  
                if "sita" in self.findMove:
                    self.findMove.remove("sita")
            if self.x+1 == character.x and self.y == character.y: #右
                if "migi" in self.findMove:
                    self.findMove.remove("migi")
            if self.x-1 == character.x and self.y == character.y: #左
                if "hidari" in self.findMove:
                    self.findMove.remove("hidari")

    def fight(self,characters):
        print(self.name,"は",self.opponent,"に攻撃をした！")
        for character in characters:
            if character.name == self.opponent[0]:
                print(self.opponent,"の前hpは",character.hp)
                character.hp -= self.at-self.df
                print(self.opponent,"のhpは",character.hp,"になった")
                if character.hp <= 0:
                    character.x = -10
                    character.y = -10

        return
    def place(self):#----------------------------------------------------------------アクション
        if self.characterType == "Goutou":
            if self.name == "Gorotsuki":
                self.y = 3
    def circle(self,screen,mapchip):
        self.findMove.clear()
        self.findFight.clear()
        if mapchip[self.y-1][self.x] == "1": #上
            if "上" in self.characterlists.keys():#上に何もなければ黄色い丸を表示
                cget = self.characterlists.get("上", [])  # キーが存在しない場合は空リストを返す  
                if cget[0] == "敵":
                    pygame.draw.circle(screen,(250,0,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
                    self.isFight = True
                    self.findFight.append("ue")
                elif cget[0] == "味方":
                    pygame.draw.circle(screen,(0,0,250),((self.x+0.5)*100,(self.y-0.5)*100),10)
            else:
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
        if mapchip[self.y+1][self.x] == "1": #下
            if "下" in self.characterlists.keys():#下に何もなければ黄色い丸を表示
                cget = self.characterlists.get("下", [])  # キーが存在しない場合は空リストを返す
                if cget[0] == "敵":
                    pygame.draw.circle(screen,(250,0,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
                    self.isFight = True
                    self.findFight.append("sita")
                    
                elif cget[0] == "味方":
                    pygame.draw.circle(screen,(0,0,250),((self.x+0.5)*100,(self.y+1.5)*100),10)
            else:
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)

        if mapchip[self.y][self.x-1] == "1": #左
            if "左" in self.characterlists.keys():#左に何もなければ黄色い丸を表示
                cget = self.characterlists.get("左", [])  # キーが存在しない場合は空リストを返す  
                if cget[0] == "敵":
                    pygame.draw.circle(screen,(250,0,0),((self.x-0.5)*100,(self.y+0.5)*100),10)
                    self.isFight = True
                    self.findFight.append("hidari")
                elif cget[0] == "味方":
                    pygame.draw.circle(screen,(0,0,255),((self.x-0.5)*100,(self.y+0.5)*100),10)
            else:
                pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)

        if mapchip[self.y][self.x+1] == "1": #右
            if "右" in self.characterlists.keys():#右に何もなければ黄色い丸を表示
                cget = self.characterlists.get("右", [])  # キーが存在しない場合は空リストを返す
                if cget[0] == "敵":
                    pygame.draw.circle(screen,(250,0,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
                    self.isFight = True
                    self.findFight.append("migi")
                elif cget[0] == "味方":
                    pygame.draw.circle(screen,(0,0,255),((self.x+1.5)*100,(self.y+0.5)*100),10)
            else:
                pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
        
    def draw(self,screen,font):#-----------------------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))#キャラクターの描画
        hpFont = font.render(str(self.hp), True, (255,255,255)) # 描画する文字列を画像にする
        screen.blit(hpFont, [self.x*100+10,self.y*100+2])

class Judge():
    def __init__(self,characters):
        self.dummys = []
        self.cm = 0
        self.ct = 0
        for i in characters:
            self.dummys.append(i.name)
            if i.team == "味方":
                self.cm += 1
            if i.team == "敵":
                self.ct += 1
        print(f"{self.cm=} {self.ct=}")
        
        self.winner = []
    def hantei(self,characters):
        dmikata = 0
        dteki = 0
        for character in characters:
            if character.hp <= 0:
                if character.team == "味方":
                    dmikata += 1
                if character.team == "敵":
                    dteki += 1
        if dmikata == self.cm:
            print("負け")
            print(f"{characters[3].hp=} {characters[3].name}")
            print(f"{characters[4].hp=} {characters[4].name}")
            import pdb; pdb.set_trace()
        if dteki == self.ct:
            print("勝ち")
            import pdb; pdb.set_trace()
            

        #print(f"{self.dmikata} {self.dteki}")
        #print(self.dummys)


def animation(tick,characters,mapchip,screen,font,ck,field,font3):
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
            character.draw(screen,font3)
        pygame.display.update()
        ck.tick(160) #1秒間で30フレームになるように33msecのwait      
def main():#-----------------------------------------------------------メイン
    #初期化
    pygame.init()        
    #フォント   
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60) 
    font3 = pygame.font.SysFont("yumincho", 15)                        
    #-
    screen = pygame.display.set_mode((500, 800))  # 800
    #キャラクターの画像(image)
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主
    #tick
    tick = 0
    #フィールド読み込み
    field = Field()
    #キャラクターインスタンス化
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2,0,3,24,12,50)#x、y、タイプ、画像、チーム、名前、フォント、id,行動力、攻撃力、防御力、体力
    player2 = Character(3,4,"Player",Pl2,"味方","Mikata1",font2,1,2,6,6,30)#攻撃力、防御力は6,行動力は1ずつ増えていく。最大30(行動力は最大5)
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",font2,2,1,12,12,60)
    slime2 = Character(-1,0,"Slime",Sl2,"敵","YellowSlime",font2,3,1,24,0,60)
    goutou = Character(-1,0,"Goutou",Man,"敵","Gorotsuki",font2,4,4,30,6,80)
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",font2,5,1,0,0,20)
    #キャラクター
    characters = [slime1,slime2,goutou,player1,player2]#catは戦わないから入れない
    judge = Judge(characters)   
    #敵味方の数
    valMikata = 2
    valTeki = 3
    #死亡カウント
    ck = pygame.time.Clock()
    animation(tick,characters,field.mapchip,screen,font,ck,field,font3)                     
    while True:
        tick += 1
        screen.fill((0,0,255))
        field.draw(screen)
        if Character.num >= len(characters):
            Character.num = 0
        #---------プレイヤー-------------------
        for character in characters:
            if Character.num == character.id:
                if character.team == "敵":
                    character.enemyUpdate(screen,field.mapchip,characters,font2)
                if character.team == "味方":
                    character.playerUpdate(screen,field.mapchip,characters,font2)
            character.draw(screen,font3)
        for character2 in characters:
            if Character.num == character2.id:
                if character2.team == "味方":
                    character2.circle(screen,field.mapchip)
        judge.hantei(characters)
        #---------描画---------  
        pygame.display.update()         
        ck.tick(33) #1秒間で30フレームになるように33msecのwait   
main()
