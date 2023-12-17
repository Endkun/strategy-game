import pygame
from pygame.locals import *
import sys
import random
import time
import opening
class BackGround():
    def __init__(self,font):
        self.mess=[]
        self.mes_tail=""
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
        self.font2=font
    def draw_tile(self,screen):
        tx = 0#タイル用x,y
        ty = 0
        screen.fill((255,255,255))
        for i in range(len(self.mapchip[0])):
            for j in range(len(self.mapchip)):
                mapnum = int(self.mapchip[j][i])            
                screen.blit(self.tiles[mapnum] ,Rect(tx+i*100,ty+j*100,50,50))            
    def draw_text(self,screen):
        y=20#文字の位置ｙ座標のみ
        for mes in self.mess:
            txt = self.font2.render(mes, True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [5, y])# 文字列の表示位置
            y+=40
    def draw_tail(self,screen):
        y=860#文字の位置ｙ座標のみ
        txt = self.font2.render(self.mes_tail, True, (0,0,0))   # 描画する文字列の設定
        screen.blit(txt, [5, y])# 文字列の表示位置


class Character():
    number=0#リアルタイムでキャラの切り替えができるようにするためのid番号、numberと一致したidを持つインスタンスだけが更新される
    def __init__(self,x,y,id,type,image,team,name,fonts,pocket,hp,ap,dp,energy):#-----------------------------------------------------------初期化
        self.id = id
        self.name = name#名前
        self.x = x      #キャラの座標
        self.y = y
        self.hp = hp
        self.hpOrg = self.hp
        self.ap = ap
        self.dp = dp
        self.shui={"up":[],"down":[], "right":[],"left":[]}   #各方向になにがあるか　敵や岩、なにもないときは[]のまま、
        self.pocket=pocket#持ち物
        self.type = type#キャラクタータイプ Player、Slime,Animal,Goutouなどキャラクタータイプ)
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム、モブチームOnly
        self.font = fonts[0]
        self.fontb = fonts[1]
        self.fontm = fonts[2]

        self.tick = 0#アニメ用 タイミング調節用
        self.mode="init"#各インスタンスが今どの状態なるかを把握するための変数
        self.canFight = False#戦えるか　四方に敵がいるか
        self.canHeal = False#回復できるか　薬草を持っているか
        self.canMove=False#移動できるか　四方に空間ががあるか

        self.energyOrg = energy #1ターンでどれだけ動けるか　移動１歩や攻撃１回で１energy消費
        self.energy=self.energyOrg#実際のエネルギー量のカウンタ
        #self.isAnime=False

    #-------------------------------基本のやつ-----------
    def draw(self,screen):#----------------------------描画
        if self.hp>=0:
            #画像表示    
            screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))
            #hp表示
            txt = str(self.hp)
            txtg = self.fontm.render(txt, True, (0,0,0))  
            screen.blit(txtg, [self.x*100+10,self.y*100+10])
            txtg = self.fontm.render(txt, True, (255,255,255))  
            screen.blit(txtg, [self.x*100+12,self.y*100+12])
            #ガイドの表示
            if Character.number==self.id :
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+0.5)*100),50,2)
        

    def update(self,screen,backGround,characters):#更新（最初に呼ばれるところ）
        if self.id != Character.number:#Character.numberと一致したインスタンスだけupdateする
            return
        if self.hp<0:#死んでいたら何もしないで次に送る
            self.x=-10
            self.y=-10
            Character.number=(Character.number+1)%len(characters)
            return

        txt=f"{self.name}のターン {self.energy=}"
        backGround.mes_tail=txt

        if self.team=="味方":
            self.mikata_update(screen,backGround,characters)    
        elif self.team=="敵":
            self.teki_update(screen,backGround,characters)    
        elif self.team=="モブ":
            #self.mob_update(screen,backGround,characters)    
            self.energy -=1
            pass
        if self.energy<=0:#キャラクターの交代
            Character.number=(Character.number+1)%len(characters)
            #ここで次のキャラを初期化するべし！
            characters[Character.number].energy = characters[Character.number].energyOrg
            characters[Character.number].tick = 0
            self.energy=self.energyOrg#自分も戻しておく

    #----------------------敵味方-共用-小物-----------------------------------------

    #------------------------------------------------------------周囲のチェック

    def check(self, mapchip, characters):
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
        #w1:壁　c1:味方　c2:敵　c3:モブ
        #w1:壁　m+id:味方　e+id:敵　b+id:モブ

        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]

        for direction, dx, dy in directions:
            self.check_direction(direction, dx, dy, mapchip, characters)

    def check_direction(self, direction, delta_x, delta_y, mapchip, characters):
        new_x = self.x + delta_x#新しい位置＝着目点
        new_y = self.y + delta_y
        map_w1 = 1 #マップの左端
        map_h1 = 3 #上
        map_w2 = 4 #右端
        map_h2 = 6 #下

        if not (map_w1 <= new_x < map_w2 and map_h1 <= new_y < map_h2):  # 範囲外のチェック
            self.shui[direction].append("w1")
        elif int(mapchip[new_y][new_x]) > 1:  # 壁や建造物のチェック
            self.shui[direction].append("w2")
        else:
            for ch in characters:  # キャラクターのチェック
                if new_x == ch.x and new_y == ch.y:
                    code = "c1" if ch.team == "味方" else "c2" if ch.team == "敵" else "c3"
                    self.shui[direction].append(code)




    def useYakusou(self,B):#薬草を使う
        self.hp+=30
        if self.hp>self.hpOrg:
            self.hp=self.hpOrg
        self.pocket.remove("薬草")   
        txt=f"{self.name}は薬草をつかった！"
        B.mess.append(txt) 
        txt=f"hpは{self.hp}に回復"
        B.mess.append(txt) 

    def dmg_calc_show(self,C):
        dmg=self.dmg_calc(C)
        txt1=f"{self.name}は{C.name}を攻撃"
        txt2=f"{dmg}のダメージを与え、{C.hp}になった"
        print(txt1)
        print(txt2)
        #self.isAnime=True

    def dmg_calc(self,C):
        dmg=self.ap-C.dp
        if dmg <0:
            dmg=0
        C.hp-=dmg  
        return dmg  

    def make_text(self, C1,B,dmg):
        B.mess=[]                
        txt1=f"{self.name}は{C1.name}に"
        txt2=f"{dmg}のダメージを与えた"
        B.mess.append(txt1)                
        B.mess.append(txt2)                

    #---------------------------------敵周り-----------------------------------
    def teki_update(self,screen,backGround,characters):    
        self.tick+=1
        if self.tick % 60 == 30:
            print(f"---@@@@172 {self.name=}-----")
            self.check(backGround.mapchip,characters)        #上下左右の周囲を見渡して以下のようなデータを作成する
            # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
            if self.hp/self.hpOrg < 0.5:
                if "薬草" in self.pocket:
                    self.useYakusou(backGround)#薬草を使う
                else:        #逃げるを実行    
                    self.teki_nigeru(backGround) 
            else:
                self.teki_kougeki(backGround,characters)
            self.energy -=1


    def teki_kougeki(self,B,Cs):
        kogekiDir=[]    
        if "c1" in self.shui["up"] and self.y-1 >=0:
            kogekiDir.append("up")
        elif "c1" in self.shui["down"] and self.y+1 <len(B.mapchip):
            kogekiDir.append("down")
        elif "c1" in self.shui["left"] and self.x-1 >=0:
            kogekiDir.append("left")
        elif "c1" in self.shui["right"] and self.y-1 < len(B.mapchip[0]):
            kogekiDir.append("right")
        if len(kogekiDir)>0:    #あるならランダムで選ぶ
            kogekiD=random.choice(kogekiDir)
        else:
            kogekiD=""    #ないときなにもしない
        #実行    
        print(f"@192 {kogekiDir=} {kogekiD=} {self.x=} {self.y=} ")
        txt=""

        if kogekiD=="up":
            for C1 in Cs:
                if C1.x==self.x and C1.y == self.y-1 and C1.team=="味方":
                    self.dmg_calc_show(C1)
        elif kogekiD=="down":
            for C1 in Cs:
                if C1.x==self.x and C1.y == self.y+1 and C1.team=="味方":
                    self.dmg_calc_show(C1)
        elif kogekiD=="right":
            for C1 in Cs:
                if C1.x ==self.x+1 and C1.y == self.y and C1.team=="味方":
                    self.dmg_calc_show(C1)
        elif kogekiD=="left":
            for C1 in Cs:
                if C1.x ==self.x-1 and C1.y == self.y and C1.team=="味方":
                    self.dmg_calc_show(C1)
        B.mess=[]
        B.mess.append(txt)

    def teki_nigeru(self,backGround):
        nigeDir=[]    
        if self.shui["up"]==[] and self.y-1 >=0:
            nigeDir.append("up")
        elif self.shui["down"]==[] and self.y+1 <len(backGround.mapchip):
            nigeDir.append("down")
        elif self.shui["left"]==[] and self.x-1 >= 0:

            nigeDir.append("left")
        elif self.shui["right"]==[] and self.x+1 < len(backGround.mapchip[0]):
            nigeDir.append("right")

        if len(nigeDir)>0:    #逃げ場があるならランダムで選ぶ
            nigeD=random.choice(nigeDir)
        else:
            nigeD=""    #逃げ場がないときなにもしない
            print("@246 do nothing")
        print(f"@172 {nigeDir=} {nigeD=}")
        #実行    nigeDの方向にいる味方のid番号を探知する　→　dmgを与えて引く
        if nigeD=="up":
            self.y-=1
        elif nigeD=="down":
            self.y+=1
        elif nigeD=="right":
            self.x+=1
        elif nigeD=="left":
            self.x-=1

    #------------------------------------味方周り----------------------------------------
    def mikata_update(self,screen,backGround,characters):    
        print(f"@323 mikata {self.mode=}")
        if self.mode=="init":#初期化モード
            self.check(backGround.mapchip,characters)#索敵
            self.draw_button_for_init(screen)#各種選択肢の表示
            self.handle_init()          #選択肢をチョイス
        elif self.mode=="move":#移動モード
            self.check(backGround.mapchip,characters)#索敵
            self.draw_guide_point_for_move(screen)
            self.handle_move()      
        elif self.mode=="heal":#移動モード
            pass
        elif self.mode=="fight":
            self.check(backGround.mapchip,characters)#索敵
            self.draw_guide_point_for_fight(screen)
            self.handle_fight(characters,backGround)      

    def draw_button_for_init(self,screen): #---------------------------ボタン描画
        self.check_for_mode()
        if self.canMove:
            pygame.draw.rect(screen, (255,255,255), Rect(50,800,120,40))
            txt = self.font.render("移動", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [80, 805])# 文字列の表示位置
        if self.canFight:
            pygame.draw.rect(screen, (255,255,255), Rect(200,800,120,40))
            txt = self.font.render("戦闘", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [230, 805])# 文字列の表示位置
        if self.canHeal:
            pygame.draw.rect(screen, (255,255,255), Rect(350,800,120,40))
            txt = self.font.render("回復", True, (0,0,0))   # 描画する文字列の設定
            screen.blit(txt, [380, 805])# 文字列の表示位置

    def check_for_mode(self):
        #動けるかのチェック
        if self.energy>0:
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

            #薬草を持っているかのチェック
            if "薬草" in self.pocket:
                self.canHeal=True
            else:
                self.canHeal=False   

    def handle_init(self):#初期化モードでの入力
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                self.mode="init"
                if 800< y_pos < 830:
                    if 50<x_pos<150 and self.canMove:
                        self.mode="move"
                    elif 200<x_pos<300 and self.canFight:
                        self.mode="fight"
                    elif 350<x_pos<500 and self.canHeal:
                        self.mode="heal" 
                print("p239 self.mode=",self.mode)        


    def handle_move(self):#移動モードでの入力
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/100)
                new_y=int(y_pos/100)
                #print("@195 new_x=",new_x," new_y=",new_y)
                if self.shui["up"]==[]     and new_y-self.y== -1 and self.x-new_x== 0:
                        self.y -= 1
                        self.energy-=1
                        self.mode="init"
                elif self.shui["down"]==[] and new_y-self.y== 1 and self.x-new_x== 0:
                        self.y += 1
                        self.energy-=1
                        self.mode="init"
                elif self.shui["left"]==[] and self.y-new_y== 0 and new_x-self.x== -1:
                        self.x -= 1
                        self.energy-=1
                        self.mode="init"
                elif self.shui["right"]==[] and self.y-new_y== 0 and new_x-self.x== 1:
                        self.x += 1
                        self.energy-=1
                        self.mode="init"

    def draw_guide_point_for_move(self, screen): #動ける場所に黄色いガイド点を描く
        #print("@250 self.shui=",self.shui)     
        if self.shui["up"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y-0.5)*100),10)
        if self.shui["down"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*100,(self.y+1.5)*100),10)
        if self.shui["right"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x+1.5)*100,(self.y+0.5)*100),10)
        if self.shui["left"] == []:
            pygame.draw.circle(screen,(250,250,0),((self.x-0.5)*100,(self.y+0.5)*100),10)

    def draw_guide_point_for_fight(self, screen): #戦える相手の場所に白いガイドを描く
        col=(250,250,250)
        if "c2" in self.shui["up"] :
            pygame.draw.rect(screen, col, Rect((self.x)*100,(self.y-1)*100,100,100), 3)  
        if "c2" in self.shui["down"]:
            pygame.draw.rect(screen, col, Rect((self.x)*100,(self.y+1)*100,100,100), 3)  
        if "c2" in self.shui["right"] :
            pygame.draw.rect(screen, col, Rect((self.x+1)*100,self.y*100,100,100), 3)  
        if "c2" in self.shui["left"] :
            pygame.draw.rect(screen, col, Rect((self.x-1)*100,self.y*100,100,100), 3)  



    # def handle_fight(self,Cs,B):#移動モードでの入力
    #     for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
    #         if event.type == QUIT:        # 閉じるボタンが押されたら終了
    #             pygame.quit()             # Pygameの終了(ないと終われない)
    #             sys.exit()                # 終了（ないとエラーで終了することになる）
    #         elif event.type == MOUSEBUTTONDOWN:
    #             x_pos, y_pos = event.pos
    #             new_x=int(x_pos/100)
    #             new_y=int(y_pos/100)
    #             #print(f"@275 new_x={new_x} new_y={new_y} self.shui={self.shui}")
    #             moved=False#実際に移動したか
    #             dfs=[(0,-1),(0,1),(1,0),(-1,0)]#上下左右の差分(x,y)
    #             for df in dfs:
    #                 if "c2" in self.shui["up"] and new_x-self.x ==df[0] and new_y-self.y == df[1]:
    #                     for C1 in Cs:
    #                         if C1.x==self.x and C1.y==self.y-1 and C1.team=="敵":
    #                             dmg=self.dmg_calc(C1)
    #                             self.make_text(C1,B,dmg)
    #                     moved=True

    #             if moved==True:
    #                 self.mode="init"#実際に動いたらmodeをもとに戻す
    #                 self.energy-=1#エネルギーを減らす


    def handle_fight(self,Cs,B):#移動モードでの入力
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/100)
                new_y=int(y_pos/100)
                #print(f"@275 new_x={new_x} new_y={new_y} self.shui={self.shui}")
                moved=False#実際に移動したか
                if "c2" in self.shui["up"] and new_y-self.y== -1 and self.x-new_x== 0:
                    for C1 in Cs:
                        if C1.x==self.x and C1.y==self.y-1 and C1.team=="敵":
                            dmg=self.dmg_calc(C1)
                            self.make_text(C1,B,dmg)
                    moved=True
                elif "c2" in self.shui["down"]  and new_y-self.y== 1 and self.x-new_x== 0:
                    for C1 in Cs:
                        if C1.x==self.x and C1.y==self.y+1 and C1.team=="敵":
                            dmg=self.dmg_calc(C1)
                            self.make_text(C1,B,dmg)
                    moved=True
                elif "c2" in self.shui["left"]  and new_y-self.y== 0 and self.x-new_x== 1:
                    for C1 in Cs:
                        if C1.x==self.x-1 and C1.y==self.y and C1.team=="敵":
                            dmg=self.dmg_calc(C1)
                            self.make_text(C1,B,dmg)
                    moved=True
                elif "c2" in self.shui["right"]  and new_y-self.y== 0 and self.x-new_x== -1:
                    for C1 in Cs:
                        if C1.x==self.x+1 and C1.y==self.y and C1.team=="敵":
                            dmg=self.dmg_calc(C1)
                            self.make_text(C1,B,dmg)
                    moved=True
                if moved==True:
                    self.mode="init"#実際に動いたらmodeをもとに戻す
                    self.energy-=1#エネルギーを減らす





    #オープニング周り-------------------------------------
    def firstAnimation(self):#----------最初のアニメーション
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
                    self.y = 4
                if self.tick == 500:
                    self.x = 3
        if self.type == "Goutou" and self.name == "Yakuza Sumiyoshi":
            if self.tick == 400:
                self.x = 2
                self.y = 2
        if self.type == "Player" and self.name == "girl":
            if self.tick == 300:
                self.y += 1
            if self.tick == 400:
                #self.y += 4
                self.y += 0
        if self.type == "Animal" and self.name == "Cat":
            if self.tick == 400:
                self.y += 1
            if self.tick == 550:
                self.x += 2
            if self.tick == 650:
                self.y += 4

def main():#-----------------------------------------------------------メイン
    pygame.init()        
    font = pygame.font.SysFont("yumincho", 30)       
    fontb = pygame.font.SysFont("yumincho", 60)                      
    fontm = pygame.font.SysFont("yumincho", 20)                      
    fonts=[font,fontb,fontm] 
    screen = pygame.display.set_mode((500, 900))  # 800
    ck = pygame.time.Clock()

    #image load
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主

    Db=[#キャラのデータベース
        #(初期位置x,y、id、タイプ、画像、チーム、名前、フォント、持ち物,hp,ap,dp,energy)
        (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],100,50,50,3),
        (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,10,10,2),
        (-1,0,2,"Slime",Sl1,"敵","BlueSlime",fonts,["薬草"],90,10,20,3),
        (-1,0,3,"Slime",Sl2,"敵","GreenSlime",fonts,["薬草"],60,30,30,4),
        (-1,0,4,"Goutou",Man,"敵","Yakuza Sumiyoshi",fonts,["剣","薬草"],200,50,50,3),
        (1,4,5,"Animal",Cat,"モブ","Cat",fonts,[],100,50,50,2),
    ]

    #データベースからインスタンス化
    Cs = [Character(*Db[i]) for i in range(len(Db))]
    B1 = BackGround(font)

    #opening
    Character.number=999
    opening.opening(screen,font,Cs,B1)#本番用
    #opening.opening2(screen,font,Cs,B1)#テスト用　オープニング省略バージョン
    Character.number=0
    #battle 　
    while True:
        B1.draw_tile(screen)
        B1.draw_text(screen)
        B1.draw_tail(screen)
        #---------更新と描画---------
        for ch in Cs:
            ch.update(screen,B1,Cs)
            ch.draw(screen)
        pygame.display.update() #こいつは引数がない        
        ck.tick(60) #1秒間で30フレームになるように33msecのwait
main()