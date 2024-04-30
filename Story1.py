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
        self.dpOrg = dp
        self.shui={"up":[],"down":[], "right":[],"left":[]}   #各方向になにがあるか　敵や岩、なにもないときは[]のまま、
        self.directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]     #indexで使いたいのであえて辞書型にしていない   
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
    def draw_point(self, screen, point, pos_x, pos_y):
            txt = str(point)
            txtg = self.fontm.render(txt, True, (0,0,0))  
            screen.blit(txtg, [self.x*SIZE+pos_x,self.y*SIZE+pos_y])
            txtg = self.fontm.render(txt, True, (255,255,255))  
            screen.blit(txtg, [self.x*SIZE+pos_x+2,self.y*SIZE+pos_y+2])

    def draw(self,screen):#----------------------------描画
        if self.hp>0:
            #画像表示    
            screen.blit(self.image,Rect(self.x*SIZE,self.y*SIZE,50,50))
            #hp表示
            self.draw_point(screen, self.hp,5,8)
            #energy表示
            self.draw_point(screen, self.energy,48,8)

            #ap表示
            self.draw_point(screen, self.ap,5,48)

            #dp表示
            self.draw_point(screen, self.dp,48,48)

            #黄色いガイドの表示
            if Character.number==self.id :
                pygame.draw.circle(screen,(250,250,0),((self.x+0.5)*SIZE,(self.y+0.5)*SIZE),50,2)
        
    def update(self,B,Cs,E,M):#更新（最初に呼ばれるところ）
        if self.id != Character.number:#Character.numberと一致したインスタンスだけupdateする
            return
        if self.hp<=0:#死んでいたら何もしないで次に送る
            self.x=-10#どかしておかないと死んだあとでも残っているので
            self.y=-10
            Character.number=(Character.number+1)%len(Cs)#つぎのキャラに送る
            return

        mes=f"{self.name}のターン 行動残：{self.energy}"
        M.head_txt=mes

        if self.team=="味方":
            self.mikata_update(B,Cs,E,M)  
        elif self.team=="敵":
            self.teki_update(B,Cs,M)    
        elif self.team=="モブ":
            self.energy -=1
            pass

        if self.energy<=0:#キャラクターの交代
            Character.number=(Character.number+1)%len(Cs)
            #ここで次のキャラを初期化するべし！
            Cs[Character.number].energy = Cs[Character.number].energyOrg
            Cs[Character.number].tick = 0
            #Cs[Character.number].dp = Cs[Character.number].dpOrg
            self.energy=self.energyOrg#自分も戻しておく

    #-------------周囲のチェック------------
    def check(self, B, Cs, M):#敵味方共通、四方周囲に何があるか探索
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': ['敵'], 'down': ['壁'], 'right': ['モブ'], 'left': ["敵ハサミ"]}
        #壁:地形:味方:敵:モブ

        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        for directionSet in self.directions:#上下左右をスキャン
            self.check_direction(directionSet, B, Cs, M)

    def check_direction(self, directionSet, B, Cs, M):#BはBackGround
        direction = directionSet[0]
        dx = directionSet[1]    
        dy = directionSet[2]
        new_x = self.x + dx#新しい位置＝着目点
        new_y = self.y + dy

        if not (B.w1 <= new_x < B.w2 and B.h1 <= new_y < B.h2):  # 範囲外のチェック
            self.shui[direction].append("壁")
        elif int(B.mapchip[new_y][new_x]) > 1:  # 壁や建造物があるかチェック
            self.shui[direction].append("地形")
        else:
            if self.team=="味方":
                for C in Cs:  # キャラクタースキャン
                    if new_x == C.x and new_y == C.y:#着目点にキャラが居るなら
                        if C.team == "敵":
                            C.dp=C.dpOrg#いったん戻しておく
                            code = "敵"
                            self.shui[direction].append(code)
                            #挟み撃ち攻撃のチェック（味方ー敵ー味方）
                            hasami_x = new_x + dx
                            hasami_y = new_y + dy
                            if (B.w1 <= hasami_x < B.w2 and B.h1 <= hasami_y < B.h2):
                                for Ch in Cs:  # キャラクタースキャン
                                    if hasami_x == Ch.x and hasami_y == Ch.y and Ch.id!=C.id and Ch.id!=self.id:
                                        if Ch.team=="味方":
                                            C.dp=int(C.dp/3)
                                            mes1=f"挟み撃ち!!{C.name}の防御が{C.dp}に"
                                            M.append_tail_line([mes1])
                                            print(mes1)
                        else:
                            "モブ"
            elif self.team=="敵":
                for C in Cs:  # キャラクタースキャン
                    if new_x == C.x and new_y == C.y:#着目点にキャラが居るなら
                        if C.team == "味方" :#そいつが味方なら
                            C.dp=C.dpOrg#いったん戻しておく
                            code = "味方"
                            self.shui[direction].append(code)
                            #挟み撃ち攻撃のチェック（敵ー味方ー敵）
                            hasami_x = new_x + dx
                            hasami_y = new_y + dy
                            if (B.w1 <= hasami_x < B.w2 and B.h1 <= hasami_y < B.h2):
                                for Ch in Cs:  # キャラクターがいるかチェック
                                    if hasami_x == Ch.x and hasami_y == Ch.y and Ch.id!=C.id and Ch.id!=self.id:
                                        if Ch.team=="敵":
                                            mes=f"やばい！！敵に挟まれた "
                                            M.append_tail_line([mes])
                                            print(mes)                                            


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
            if "敵" in v:
                pygame.draw.circle(screen,(250,0,0),((px+0.5)*SIZE,(py+.5)*SIZE),10)
            #味方がいるなら黄ガイド
            elif "味方" in v:
                pygame.draw.circle(screen,(250,255,0),((px+0.5)*SIZE,(py+.5)*SIZE),10)
            #何もないなら青ガイド
            elif v==[]:
                pygame.draw.circle(screen,(0,0,255),((px+0.5)*SIZE,(py+.5)*SIZE),10)
                #移動可能表示

    def useYakusou(self,B,M):#薬草を使う
        self.hp+=30
        if self.hp>self.hpOrg:
            self.hp=self.hpOrg
        self.pocket.remove("薬草")   
        mes1=f"{self.name}は薬草使用！hpは{self.hp}に"
        M.append_tail_line([mes1]) 

    def dmg_calc_show(self,C,M):
        dmg=self.dmg_calc(C)
        mes1=f"{self.name}は{C.name}を攻撃→{dmg}のダメージ"
        M.append_tail_line([mes1]) 

    def dmg_calc(self,C):#ダメージの計算
        dmg=self.ap-C.dp
        if dmg <0:
            dmg=0
        C.hp-=dmg  
        return dmg  

    def make_text(self, C,B,dmg,M):
        B.mess=[]                
        mes1=f"{self.name}は{C.name}を攻撃→{dmg}のダメージ"
        M.append_tail_line([mes1]) 

    #---------------------------------敵周り-----------------------------------
    def teki_update(self, B, Cs, M): #B:バック　Cs:キャラクターズ（敵、味方）
        self.tick+=1
        if self.tick % 60 == 30:#早く動きすぎないよう60フレーム中１回動かす
            self.check(B, Cs, M)        #上下左右の周囲を見渡して以下のようなデータを作成する
            # self.shui= {'up': [], 'down': ['壁'], 'right': ['モブ'], 'left': []}
            if self.hp/self.hpOrg < 0.5:#hpが50%を切ったら
                if "薬草" in self.pocket:#薬草を持っていたら
                    self.useYakusou(B,M)#薬草を使う
                else:        #もってなかったら    
                    self.teki_nigeru(B) #逃げるを実行
            else:#hpが50%以上なら
                self.teki_kougeki(B,Cs,M)#攻撃する
            self.energy -=1#エネルギーをマイナス１

    def teki_kougeki(self,B,Cs,M):#敵の攻撃
        #接敵状況を把握する
        kogekiDir=[]    
        if "味方" in self.shui["up"] and self.y-1 >=0:
            kogekiDir.append("up")
        elif "味方" in self.shui["down"] and self.y+1 <len(B.mapchip):
            kogekiDir.append("down")
        elif "味方" in self.shui["left"] and self.x-1 >=0:
            kogekiDir.append("left")
        elif "味方" in self.shui["right"] and self.y-1 < len(B.mapchip[0]):
            kogekiDir.append("right")

        if len(kogekiDir)>0:    #接敵数が１つ以上あるならランダムで選ぶ
            kogekiD=random.choice(kogekiDir)
            #実行    
            txt=""
            if kogekiD=="up":
                for C1 in Cs:
                    if C1.x==self.x and C1.y == self.y-1 and C1.team=="味方":
                        self.dmg_calc_show(C1,M)
            elif kogekiD=="down":
                for C1 in Cs:
                    if C1.x==self.x and C1.y == self.y+1 and C1.team=="味方":
                        self.dmg_calc_show(C1,M)
            elif kogekiD=="right":
                for C1 in Cs:
                    if C1.x ==self.x+1 and C1.y == self.y and C1.team=="味方":
                        self.dmg_calc_show(C1,M)
            elif kogekiD=="left":
                for C1 in Cs:
                    if C1.x ==self.x-1 and C1.y == self.y and C1.team=="味方":
                        self.dmg_calc_show(C1,M)
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
        #print(f"@274 {t_x=}  {t_y=} {t_id=}")       
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
               
    #=================味方周り===========================================
    #モードなしダイレクト入力
    def mikata_update(self,B,Cs,E,M):    
        self.check(B,Cs,M)#索敵
        self.handle(B,Cs,E,M)          #選択肢をチョイス

    def handle(self,B,Cs,E,M):#移動モードでの入力
        for event in E.getEvent:  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                new_x=int(x_pos/SIZE)
                new_y=int(y_pos/SIZE)
                #dfs=[(0,-1,"up"),(0,1,"down"),(1,0,"right"),(-1,0,"left")]#udrl上下左右の四方との差分
                for directionSet in self.directions:#上下左右の四方のアクションを実行
                    self.handle_action(Cs,B,directionSet,new_x,new_y,M)

    def handle_action(self,Cs,B,directionSet,new_x,new_y,M):#移動モードでの入力
        direction=directionSet[0]
        dx=directionSet[1]    
        dy=directionSet[2]
        if new_x-self.x== dx and new_y-self.y== dy  :#方向の特定
            #敵がいるなら
            if "敵" in self.shui[direction]:
                #敵の同定
                for C1 in Cs:
                    if C1.x-self.x == dx and C1.y-self.y == dy and C1.team=="敵":
                        dmg=self.dmg_calc(C1)
                        self.make_text(C1,B,dmg,M)
                        self.energy-=1
            #味方がいるなら
            elif "味方" in self.shui[direction]:
                #味方の同定
                for C1 in Cs:
                    if C1.x-self.x == dx and C1.y-self.y == dy and C1.team=="味方":
                        pass
            #移動可能なら        
            elif self.shui[direction]==[]:
                self.x += dx
                self.y += dy
                self.energy -= 1

class Judge():
    def __init__(self):
        self.winner=""

    def judge(self,Cs,M):
        mikata_num=0#味方の総数
        teki_num=0#敵の総数
        mikata_dead=0#死んだ数(味方)
        teki_dead=0
        for C in Cs:
            if C.team=="味方":
                mikata_num+=1
                if C.hp<=0:
                    mikata_dead+=1
            elif C.team=="敵":
                teki_num+=1
                if C.hp<=0:
                    teki_dead+=1
        #print(f"@503:judge {mikata_dead=} {teki_dead=}")                    
        if mikata_num>0 and mikata_num==mikata_dead:
            mes = "味方全滅"
            print(mes)
            M.append_tail_line([mes])
            self.winner="teki"
        if teki_num>0 and teki_num==teki_dead:
            mes="敵全滅"
            print(mes)
            M.append_tail_line([mes])
            self.winner="mikata"

class Messenger():
    def __init__(self,fonts):
        self.font30 = fonts[0]
        self.font60 = fonts[1]
        self.font20 = fonts[2]        

        self.head_x=5
        self.head_y=20
        self.head_txt=""

        self.tail_x=5
        self.tail_y=650
        self.max_line=7
        self.tail_txt=["" for i in range(self.max_line)]

        self.old_txt=[]

    def draw(self,screen):
        self.draw_head_line(screen)
        self.draw_tail_line(screen)

    def draw_head_line(self,screen):
        g_txt = self.font30.render(self.head_txt, True, (0,0,0))   # 描画する文字列の設定
        screen.blit(g_txt, [self.head_x, self.head_y])# 文字列の表示位置

    def append_tail_line(self,txts):
        #前回と同じならスクロールを実行しない
        if txts[0] == self.tail_txt[self.max_line-1]:
                return
        #self.old_txt=txts

        #スクロール動作　
        linput=len(txts)    #行数　例えばtxtsは２行で ["x","y"]とする
        tmp=self.tail_txt   #一時置場 ex.["a","b","c","d","e","f","g"]
        if linput>self.max_line:        #7行までで制限
            print("err")
            import pdb;pdb.set_trace()
        il = self.max_line-linput           #linput=2ならil=7-2=5
        for i in range(il):                 #i=0,1,2
            tmp[i]=self.tail_txt[i+linput]  #上に詰める
            #["c","d","e","f","g","",""]
        for i,t in enumerate(txts) :   #空いたところに入力行を挿入
            tmp[i+il]=t  
            #["c","d","e","f","g","x","y"]
        self.tal_txt=tmp

    def draw_tail_line(self,screen):
        #描画
        dy=0
        for t in self.tail_txt:
            g_txt = self.font20.render(t, True, (0,0,0))   # 描画する文字列の設定
            screen.blit(g_txt, [self.tail_x, self.tail_y+dy])# 文字列の表示位置
            dy+=30

class Event():
    def __init__(self):
        self.getEvent = pygame.event.get() 
    def update(self):
        self.getEvent = pygame.event.get()    

def mainInit(): 
    pygame.init()        
    screen = pygame.display.set_mode((500, 900))  # 800
    font30 = pygame.font.SysFont("yumincho", 30)       
    font60 = pygame.font.SysFont("yumincho", 60)                      
    font20 = pygame.font.SysFont("yumincho", 20)                      
    fonts=[font30,font60,font20] 
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
        (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,30,30,5),
        (-1,0,2,"Slime",Sl1,"敵","BlueSlime",fonts,["薬草"],90,50,30,3),
        (-1,0,3,"Slime",Sl2,"敵","YelloSlime",fonts,["薬草"],60,30,40,4),
        (-1,0,4,"Goutou",Man,"敵","Yakuza",fonts,["剣","薬草"],250,60,50,3),
        (3,3,5,"Animal",Cat,"味方","Cat",fonts,[],20,50,50,2),
    ]
    Cs = [Character(*Db[i]) for i in range(len(Db))]    #データベースからインスタンス化
    B1 = BackGround(fonts[0])
    J1 = Judge()
    E1 = Event()
    M1 = Messenger(fonts)
    return screen,fonts,Cs,B1,J1,ck,E1,M1

def main():#-----------------------------------------------------------メイン
    #init
    screen,fonts,Cs,B1,J1,ck,E1,M1 = mainInit()
    #opening
    opening.opening(screen,Cs,B1,M1)#本番用
    #opening.opening2(Cs)#テスト用　オープニング省略バージョン
    Character.number=0#現在選択されているキャラ、クラス変数
    #battle 　
    while True:
        E1.update()#1フレームに１回だけeventを取得し、getEventにいれる
        B1.draw_tile(screen)#壁面
        B1.draw_text(screen)#メイン文字
        B1.draw_tail(screen)#補足説明用の文字
        #---------更新と描画---------
        for ch in Cs:#キャラ全員の更新と描画
            ch.update(B1,Cs,E1,M1)#ただし現在選択されているキャラ以外は即return
            ch.draw(screen)
        for ch in Cs:#ガイドの表示（一旦すべて描画したあとじゃないと埋もれてしまうので）
            ch.new_guide(screen)
        M1.draw(screen)    
        J1.judge(Cs,M1)    #判定
        if J1.winner=="teki" or J1.winner=="mikata":
            break
        pygame.display.update() #画面更新、こいつは引数がない        
        ck.tick(60) #1秒間で60フレームになるように16msecのwait

SIZE=70#画面での１マスの大きさ
main()
