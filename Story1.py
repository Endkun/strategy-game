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
        pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 
        pt1 = pygame.transform.scale(pt1, (SIZE, SIZE)) 
        pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
        pt2 = pygame.transform.scale(pt2, (SIZE, SIZE)) 
        pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
        pt3 = pygame.transform.scale(pt3, (SIZE, SIZE)) 
        door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
        door = pygame.transform.scale(door, (SIZE, SIZE)) 
        door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
        door2 = pygame.transform.scale(door2, (SIZE, SIZE)) 
        self.tiles=[pt2,pt1,pt3,door,door2,pt1]
        self.mapchip = [
            ["2","2","2","2","2"],
            ["1","1","1","1","1"],
            ["1","1","3","1","1"],
            ["1","1","1","1","1"],
            ["1","1","1","1","1"],
            ["1","1","1","1","1"],
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
                screen.blit(self.tiles[mapnum] ,Rect(tx+i*SIZE,ty+j*SIZE,50,50))            
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
        self.energyOrg = energy #1ターンでどれだけ動けるか　移動１歩や攻撃１回で１energy消費
        self.energy=self.energyOrg#実際のエネルギー量のカウンタ

    #-------------------------------基本のやつ-----------
    def draw(self,screen):#----------------------------描画
        if self.hp>=0:
            #画像表示    
            screen.blit(self.image,Rect(self.x*SIZE,self.y*SIZE,50,50))
            #hp表示
            txt = str(self.hp)
            txtg = self.fontm.render(txt, True, (0,0,0))  
            screen.blit(txtg, [self.x*SIZE+10,self.y*SIZE+10])
            txtg = self.fontm.render(txt, True, (255,255,255))  
            screen.blit(txtg, [self.x*SIZE+12,self.y*SIZE+12])
            #ガイドの表示
            if Character.number==self.id :
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*SIZE,(self.y+0.5)*SIZE),50,2)
        
    def update(self,screen,B,Cs):#更新（最初に呼ばれるところ）
        if self.id != Character.number:#Character.numberと一致したインスタンスだけupdateする
            return
        if self.hp<0:#死んでいたら何もしないで次に送る
            self.x=-10
            self.y=-10
            Character.number=(Character.number+1)%len(Cs)#つぎのキャラに送る
            return

        txt=f"{self.name}のターン {self.energy=}"
        B.mes_tail=txt

        if self.team=="味方":
            #self.mikata_update(screen,backGround,characters)  
            self.mikata_update2(B,Cs)  
  
        elif self.team=="敵":
            self.teki_update(screen,B,Cs)    
        elif self.team=="モブ":
            self.energy -=1
            pass
        if self.energy<=0:#キャラクターの交代
            Character.number=(Character.number+1)%len(Cs)
            #ここで次のキャラを初期化するべし！
            Cs[Character.number].energy = Cs[Character.number].energyOrg
            Cs[Character.number].tick = 0
            self.energy=self.energyOrg#自分も戻しておく


    #----------------------------敵味方共通-------------周囲のチェック------------

    def check(self, B, Cs):
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
        #w1:壁　w2:地形　c1:味方　c2:敵　c3:モブ

        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]

        for direction, dx, dy in directions:
            self.check_direction(direction, dx, dy, B, Cs)

    def check_direction(self, direction, delta_x, delta_y, B, Cs):
        new_x = self.x + delta_x#新しい位置＝着目点
        new_y = self.y + delta_y

        if not (B.w1 <= new_x < B.w2 and B.h1 <= new_y < B.h2):  # 範囲外のチェック
            self.shui[direction].append("w1")
        elif int(B.mapchip[new_y][new_x]) > 1:  # 壁や建造物があるかチェック
            self.shui[direction].append("w2")
        else:
            for C in Cs:  # キャラクターがいるかチェック
                if new_x == C.x and new_y == C.y:
                    code = "c1" if C.team == "味方" else "c2" if C.team == "敵" else "c3"
                    self.shui[direction].append(code)

    #全キャラ用、新ガイドを描画するだけ
    def new_guide(self,screen):
        if self.id != Character.number:#Character.numberと一致したインスタンスだけupdateする
            return
        for k,v in self.shui.items():
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
                pygame.draw.circle(screen,(250,0,0),((px+0.5)*SIZE,(py+.5)*SIZE),10)
            #味方がいるなら黄ガイド
            elif "c1" in v:
                pygame.draw.circle(screen,(250,255,0),((px+0.5)*SIZE,(py+.5)*SIZE),10)
            #何もないなら青ガイド
            elif v==[]:
                pygame.draw.circle(screen,(0,0,255),((px+0.5)*SIZE,(py+.5)*SIZE),10)
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
        # print(txt1)
        # print(txt2)

    def dmg_calc(self,C):#ダメージの計算
        dmg=self.ap-C.dp
        if dmg <0:
            dmg=0
        C.hp-=dmg  
        return dmg  

    def make_text(self, C,B,dmg):
        B.mess=[]                
        txt1=f"{self.name}は{C.name}に"
        txt2=f"{dmg}のダメージを与えた"
        B.mess.append(txt1)                
        B.mess.append(txt2)                

    #---------------------------------敵周り-----------------------------------
    def teki_update(self,screen,B,Cs):    
        self.tick+=1
        if self.tick % 60 == 30:
            #print(f"------@172 {self.name=}-----")
            self.check(B,Cs)        #上下左右の周囲を見渡して以下のようなデータを作成する
            # self.shui= {'up': [], 'down': ['w1'], 'right': ['c3'], 'left': []}
            #self.calc_jyusin(characters)
            if self.hp/self.hpOrg < 0.5:
                if "薬草" in self.pocket:
                    self.useYakusou(B)#薬草を使う
                else:        #逃げるを実行    
                    self.teki_nigeru(B) 
            else:
                self.teki_kougeki(B,Cs)
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
            self.easy_koteki(B,Cs)#とりあえずランダムで動く簡易化されたやつ
            #self.koteki(B)#本格的なやつ

    def search_target(self,Cs):#一番弱い、生きているキャラを狙う,
        t_hp=9999
        for C in Cs:
            if C.hp>0 and C.team=="味方" and t_hp>C.hp:#生きているかつ一番弱いか
                t_hp=C.hp
                t_x=C.x
                t_y=C.y
                t_id=C.id
        print(f"@274 {t_x=}  {t_y=} {t_id=}")       
        return t_x,t_y ,t_id       

    def calc_target_delta(self,Cs):
        t_x,t_y,t_id = self.search_target(Cs)#一番弱いやつを狙う
        dx = t_x-self.x#差分を取る
        dy = t_y-self.y
        if dx==0:
            if dy<0:
                delta=(0,-1) 
            else:
                delta=(0,1)     
            return  delta                

        a=dy/dx#傾きを計算
        if -1<a<1:
            if dx>0:
                delta=(1,0)
            else:
                delta=(-1,0)
        else:
            if dy<0:
                delta=(0,-1) 
            else:
                delta=(0,1)                   
        return delta        


    def easy_koteki(self,B,Cs):#向敵の最初の一歩を計算
        deltas=[]
        #動ける方向を収集する
        if self.shui["up"] ==[] :
            if self.y-1 >=B.h1:
                deltas.append((0,-1))
        if self.shui["down"] ==[]: 
            if self.y+1 <B.h2:
                deltas.append((0,1))
        if self.shui["right"] ==[] :
            if self.x-1 <=B.w2:
                deltas.append((1,0))
        if self.shui["left"] ==[] :
            if self.x+1 >= B.w1:
                deltas.append((-1,0))
    
        d = self.calc_target_delta(Cs)#ターゲットのdeltaを計算
        if d in deltas:#動ける方向に入っていればそこに向かう
            delta=d
        else:#なければランダムで選ぶ
            delta = random.choice(deltas)    
        self.x+=delta[0]#移動する
        self.y+=delta[1]

    def koteki(self,B):
        pass
        #以下は本格的な向敵
        #"味方チーム"から一番hpの小さいキャラを見つけ出す、そのキャラの座標をjx,jyとする
        #障害物マップを作成する（通路は0、それ以外はすべて1、地形でもキャラでも）
        #自分の位置（self.x,self.y）からjx,jyまでの迷路を幅優先探索（＝最短経路）で解く
        #最初の一歩を踏み出す（）


    def teki_nigeru(self,B):
        nigeDir=[]    
        if self.shui["up"]==[] and self.y-1 >=B.h1:
            nigeDir.append("up")
        elif self.shui["down"]==[] and self.y+1 <B.h2:
            nigeDir.append("down")
        elif self.shui["left"]==[] and self.x-1 >= B.w1:
            nigeDir.append("left")
        elif self.shui["right"]==[] and self.x+1 < B.w2:
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
    def mikata_update2(self,B,Cs):    
        self.check(B,Cs)#索敵
        self.handle(B,Cs)          #選択肢をチョイス

    def handle(self,B,Cs):#移動モードでの入力
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/SIZE)
                new_y=int(y_pos/SIZE)
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
        if mnum>0 and mnum==mdead:
            print("味方全滅")
            self.winner="teki"
        if tnum>0 and tnum==tdead:
            print("敵全滅")
            self.winner="mikata"

def mainInit(): 
    pygame.init()        
    screen = pygame.display.set_mode((500, 900))  # 800
    font = pygame.font.SysFont("yumincho", 30)       
    fontb = pygame.font.SysFont("yumincho", 60)                      
    fontm = pygame.font.SysFont("yumincho", 20)                      
    fonts=[font,fontb,fontm] 
    ck = pygame.time.Clock()

    #image load
    Pl1 = pygame.image.load("img/player1.png").convert_alpha()       #プレイヤー
    Pl1 = pygame.transform.scale(Pl1, (SIZE, SIZE)) 
    Pl2 = pygame.image.load("img/player2.png").convert_alpha()       #プレイヤー
    Pl2 = pygame.transform.scale(Pl2, (SIZE, SIZE)) 
    Cat = pygame.image.load("img/cat.png").convert_alpha()       #プレイヤー
    Cat = pygame.transform.scale(Cat, (SIZE, SIZE)) 
    Sl1 = pygame.image.load("img/Slime1.png").convert_alpha()       #雑魚スライム
    Sl1 = pygame.transform.scale(Sl1, (SIZE, SIZE)) 
    Sl2 = pygame.image.load("img/Slime2.png").convert_alpha()       #雑魚スライム
    Sl2 = pygame.transform.scale(Sl2, (SIZE, SIZE)) 
    Man = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主
    Man = pygame.transform.scale(Man, (SIZE, SIZE)) 

    Db=[#キャラのデータベース
        #(初期位置x,y、id、タイプ、画像、チーム、名前、フォント、持ち物,hp,ap,dp,energy)
        (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],100,50,50,3),
        (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,10,10,2),
        (-1,0,2,"Slime",Sl1,"敵","BlueSlime",fonts,["薬草"],90,10,20,3),
        (-1,0,3,"Slime",Sl2,"敵","GreenSlime",fonts,["薬草"],60,30,30,4),
        (-1,0,4,"Goutou",Man,"敵","Yakuza Sumiyoshi",fonts,["剣","薬草"],150,60,20,3),
        (3,3,5,"Animal",Cat,"味方","Cat",fonts,[],10,50,50,2),
    ]
    Cs = [Character(*Db[i]) for i in range(len(Db))]    #データベースからインスタンス化
    B1 = BackGround(font)
    J1 = Judge()
    return screen,fonts,Cs,B1,J1,ck

def main():#-----------------------------------------------------------メイン
    #init
    screen,fonts,Cs,B1,J1,ck=mainInit()
    #opening
    #opening.opening(screen,fonts[0],Cs,B1)#本番用
    opening.opening2(screen,fonts[0],Cs,B1)#テスト用　オープニング省略バージョン
    Character.number=0#現在選択されているキャラ、クラス変数
    #battle 　
    while True:
        B1.draw_tile(screen)#壁面
        B1.draw_text(screen)#メイン文字
        B1.draw_tail(screen)#補足説明用の文字
        #---------更新と描画---------
        for ch in Cs:#キャラ全員の更新と描画
            ch.update(screen,B1,Cs)#ただし現在選択されているキャラ以外は即return
            ch.draw(screen)
        for ch in Cs:#ガイドの表示（一旦すべて描画したあとじゃないと埋もれてしまうので）
            ch.new_guide(screen)
        J1.judge(Cs)    #判定
        if J1.winner=="teki" or J1.winner=="mikata":
            break
        pygame.display.update() #画面更新、こいつは引数がない        
        ck.tick(60) #1秒間で60フレームになるように16msecのwait

SIZE=70#画面での１マスの大きさ
main()