import pygame
from pygame.locals import *
import sys
import random
import math
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

        self.w1 = 0 #マップの左端
        self.w2 = 5 #右端(実際の取る値は-1まで)
        self.h1 = 1 #上
        self.h2 = 6 #下(実際の取る値は-1まで)

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
        # self.mode="init"#各インスタンスが今どの状態なるかを把握するための変数
        # self.canFight = False#戦えるか　四方に敵がいるか
        # self.canHeal = False#回復できるか　薬草を持っているか
        # self.canMove=False#移動できるか　四方に空間ががあるか

        self.energyOrg = energy #1ターンでどれだけ動けるか　移動１歩や攻撃１回で１energy消費
        self.energy=self.energyOrg#実際のエネルギー量のカウンタ

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
            #self.mikata_update(screen,backGround,characters)  
            self.mikata_update2(screen,backGround,characters)  
  
        elif self.team=="敵":
            self.teki_update(screen,backGround,characters)    
        elif self.team=="モブ":
            self.energy -=1
            pass
        if self.energy<=0:#キャラクターの交代
            Character.number=(Character.number+1)%len(characters)
            #ここで次のキャラを初期化するべし！
            characters[Character.number].energy = characters[Character.number].energyOrg
            characters[Character.number].tick = 0
            self.energy=self.energyOrg#自分も戻しておく



    #----------------------------敵味方共通-------------周囲のチェック------------

    def check(self, mapchip, characters):
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
        #w1:壁　w2:地形　c1:味方　c2:敵　c3:モブ

        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]

        for direction, dx, dy in directions:
            self.check_direction(direction, dx, dy, mapchip, characters)

    def check_direction(self, direction, delta_x, delta_y, mapchip, characters):
        new_x = self.x + delta_x#新しい位置＝着目点
        new_y = self.y + delta_y
        map_w1 = 0 #マップの左端
        map_h1 = 1 #上
        map_w2 = 5 #右端
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

    #全キャラ用、新ガイドを描画するだけ
    def new_guide(self,screen):
        if self.id != Character.number:#Character.numberと一致したインスタンスだけupdateする
            return
        for k,v in self.shui.items():
            #print(f"@166 {k=} {v=}")
            #位置の特定
            px=self.x
            py=self.y
            if k=="up":
                py-=1
            elif k=="down":
                py+=1
            elif k=="right":
                px+=1
            elif k=="left":
                px-=1
            #敵がいるなら赤ガイド
            if "c2" in v:
                pygame.draw.circle(screen,(250,0,0),((px+0.5)*100,(py+.5)*100),10)
            #味方がいるなら黄ガイド
            elif "c1" in v:
                pygame.draw.circle(screen,(250,255,0),((px+0.5)*100,(py+.5)*100),10)
            #何もないなら青ガイド
            elif v==[]:
                pygame.draw.circle(screen,(0,0,255),((px+0.5)*100,(py+.5)*100),10)
                #移動可能表示

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
            print(f"------@172 {self.name=}-----")
            self.check(backGround.mapchip,characters)        #上下左右の周囲を見渡して以下のようなデータを作成する
            # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
            #self.calc_jyusin(characters)
            if self.hp/self.hpOrg < 0.5:
                if "薬草" in self.pocket:
                    self.useYakusou(backGround)#薬草を使う
                else:        #逃げるを実行    
                    self.teki_nigeru(backGround) 
            else:
                self.teki_kougeki(backGround,characters)
            self.energy -=1


    def teki_kougeki(self,B,Cs):
        #接敵状況を把握する
        kogekiDir=[]    
        if "c1" in self.shui["up"] and self.y-1 >=0:
            kogekiDir.append("up")
        elif "c1" in self.shui["down"] and self.y+1 <len(B.mapchip):
            kogekiDir.append("down")
        elif "c1" in self.shui["left"] and self.x-1 >=0:
            kogekiDir.append("left")
        elif "c1" in self.shui["right"] and self.y-1 < len(B.mapchip[0]):
            kogekiDir.append("right")

        if len(kogekiDir)>0:    #接敵数が１つ以上あるならランダムで選ぶ
            kogekiD=random.choice(kogekiDir)
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

        else:#接敵がないときの向敵アルゴリズム
            self.easy_koteki(B)#とりあえずランダムで動く簡易化されたやつ
            #self.koteki(B)#本格的なやつ

    # def easy_koteki2(self,B):
    #     dfs={"up":(0,-1),"down":(0,1),"right":(1,0),"left":(-1,0)}#デルタ
    #     koteki=[]
    #     if self.shui["up"] ==[] and self.y-1 >=0:
    #         koteki.append("up")
    #     elif self.shui["down"] ==[] and self.y+1 <len(B.mapchip):
    #         koteki.append("down")
    #     elif self.shui["right"] ==[] and self.x-1 >=0:
    #         koteki.append("right")
    #     elif self.shui["left"] ==[] and self.x+1 <len(B.mapchip[0]):
    #         koteki.append("left")
    #     kk=random.choice(koteki)    
    #     dx,dy=dfs[kk]
    #     #print(f"@288 {kk=} {dfs[kk]=} {dx=} {dy=}")
    #     self.x+=dx
    #     self.y+=dy

    def easy_koteki(self,B):
        deltas=[]

        if self.shui["up"] ==[] :
            #print("@293 up")
            if self.y-1 >=B.h1:
                deltas.append((0,-1))
        if self.shui["down"] ==[]: 
            #print("@297 down")
            if self.y+1 <B.h2:
                deltas.append((0,1))
        if self.shui["right"] ==[] :
            #print(f"@301 right {self.x-1} ")
            if self.x-1 <=B.w2:
                deltas.append((1,0))
        if self.shui["left"] ==[] :
            #print(f"@305 left {self.x+1=} {B.mapchip[0]=}")
            if self.x+1 >= B.w1:
                #print(f"@307 left append!")
                deltas.append((-1,0))
        delta = random.choice(deltas)    
        #print(f" @308 {self.shui=} {deltas=} {delta=}")    
        self.x+=delta[0]
        self.y+=delta[1]



    def koteki(self,B):
        pass
        #以下は本格的な向敵
        #"味方チーム"から一番hpの小さいキャラを見つけ出す、そのキャラの座標をjx,jyとする
        #障害物マップを作成する（通路は0、それ以外はすべて1、地形でもキャラでも）
        #自分の位置（self.x,self.y）からjx,jyまでの迷路を幅優先探索（＝最短経路）で解く
        #最初の一歩を踏み出す（）


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
        #実行    nigeDの方向にいる味方のid番号を探知する　→　dmgを与えて引く
        if nigeD=="up":
            self.y-=1
        elif nigeD=="down":
            self.y+=1
        elif nigeD=="right":
            self.x+=1
        elif nigeD=="left":
            self.x-=1

    def calc_jyusin(self,Cs):
        jxsum=0
        jysum=0
        jct=0
        for C in Cs:
            if C.team=="味方":
                jxsum+=C.x
                jysum+=C.y
                jct+=1
        jx=jxsum/jct
        jy=jysum/jct
        print(f"{jx=} {jy=}") 
        return jx,jy
                

    #=================味方周り===========================================
    #モードなしダイレクト入力
    def mikata_update2(self,screen,backGround,characters):    
        #print(f"@463 mikata update2")
        self.check(backGround.mapchip,characters)#索敵
        self.handle(backGround,characters)          #選択肢をチョイス

    def handle(self,B,Cs):#移動モードでの入力
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/100)
                new_y=int(y_pos/100)
                dfs=[(0,-1,"up"),(0,1,"down"),(1,0,"right"),(-1,0,"left")]#udrl上下左右の四方との差分
                for df in dfs:#上下左右の四方のアクションを実行
                    self.handle_action(Cs,B,df,new_x,new_y)

    def handle_action(self,Cs,B,df,new_x,new_y):#移動モードでの入力
        if new_x-self.x== df[0] and new_y-self.y== df[1]  :#方向の特定
            #敵がいるか
            if "c2" in self.shui[df[2]]:
                #敵の同定
                for C1 in Cs:
                    if C1.x-self.x == df[0] and C1.y-self.y == df[1] and C1.team=="敵":
                        dmg=self.dmg_calc(C1)
                        self.make_text(C1,B,dmg)
                        self.energy-=1
            #味方がいるか
            elif "c1" in self.shui[df[2]]:
                #味方の同定
                for C1 in Cs:
                    if C1.x-self.x == df[0] and C1.y-self.y == df[1] and C1.team=="味方":
                        pass
            #移動可能か        
            elif self.shui[df[2]]==[]:
                self.x+=df[0]
                self.y+=df[1]
                self.energy-=1

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

class Judge():
    def __init__(self):
        self.winner=""
        pass

    def judge(self,Cs):
        mnum=0#全体数
        tnum=0
        mdead=0#死んだ数
        tdead=0
        for C in Cs:
            if C.team=="味方":
                mnum+=1
                if C.hp<0:
                    mdead+=1
            elif C.team=="敵":
                tnum+=1
                if C.hp<0:
                    tdead+=1
        #print(f"@438 {mdead=} {tdead=}")
        #print(f"{mnum=} {tnum=}")
        if mnum>0 and mnum==mdead:
            print("味方全滅")
            self.winner="teki"
        if tnum>0 and tnum==tdead:
            print("敵全滅")
            self.winner="mikata"
 

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
        (-1,0,4,"Goutou",Man,"敵","Yakuza Sumiyoshi",fonts,["剣","薬草"],150,60,20,3),
        (1,4,5,"Animal",Cat,"モブ","Cat",fonts,[],100,50,50,2),
    ]

    #データベースからインスタンス化
    Cs = [Character(*Db[i]) for i in range(len(Db))]
    B1 = BackGround(font)
    J1 = Judge()
    #opening
    Character.number=999
    #opening.opening(screen,font,Cs,B1)#本番用
    opening.opening2(screen,font,Cs,B1)#テスト用　オープニング省略バージョン
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
        for ch in Cs:
            ch.new_guide(screen)
        J1.judge(Cs)    
        if J1.winner=="teki" or J1.winner=="mikata":
            break
        pygame.display.update() #こいつは引数がない        
        ck.tick(60) #1秒間で30フレームになるように33msecのwait
main()