"""8/18 1
   「Goutouのstepsが5のはずなのに、2マス程度しか見えてない。」解決。
   数える変数が、敵ではなくキャラクターだった。C.steps -> self.steps
   8/18 2
   症状
   ・オーバーキル(味方が敵npc倒されてもまだ攻撃判定になる。)
   仮説
   ・攻撃して倒した後も、攻撃判定になっているかも
   検証
   ・倒したら倒した判定にして次に進ませる
   8/17 1
   ブランチをsarからmainに変更
       青木さんが作ったsarから共同用のmainに反映させた。
       sarでやった変更をmainに反映させるときの手順
        1branchをmainに入れ替えた。 git checkout main
        2sarブランチをマージする git merge sar
        (マージをすると競合が起こる)
        3競合が起きたとき、古いほう(選んで良いほう)の競合プログラムを削除する
        4リモートリポジトリの変更をローカルに取り込む git pull origin main
        (pullすると競合が起こる)
        5再度コミットする git status -> git add . -> gid status -> git commit -m "入れたい奴"
        6プッシュする git push
   昔のコードをoldfileに入れて本来のコードを分かりやすくした。
   8/17 2
   Goutouのsteps(視認距離)が変数で指定した値より見えてないところを修正
   症状
   Goutouのstepsが5のはずなのに、2マス程度しか見えてない。
   仮説
   キャラクターx,キャラクターyの範囲がGoutouの視認距離と連動していない

   8/10
   仮説(miss)
   t_hp>c_hpで

   t_hp>c_hpで一番hpの低い奴が選ばれる
   しかし、一番hpの低い奴が自分の範囲に居ないときに「相手が見つからず」になる
   本当は範囲内でt_hp>c_hpをやって範囲内で一番体力が少ないやつを追いかけるようにする
   来週やる事
   ・検証
     t_hp>c_hpで体力が一番低いキャラクターをprintで調べる
     その一番低いキャラクターが範囲内にいるか調べる
     範囲内に居なかった場合この仮説は合ってることになる
    結果---------
    仮説は間違いである
    なぜなら、範囲内にいても体力の低いキャラクターが追いかけれること

"""


import pygame
from pygame.locals import *
import sys
import random
import time
import opening
from decimal import *
class BackGround():
    def __init__(self,font,level):
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
        chair1 = pygame.image.load("img/PlotChair1.png").convert_alpha()   #裏口タイル
        chair1 = pygame.transform.scale(chair1, (SIZE, SIZE))
        chair2 = pygame.image.load("img/PlotChair2.png").convert_alpha()   #裏口タイル
        chair2 = pygame.transform.scale(chair2, (SIZE, SIZE))
        table = pygame.image.load("img/PlotTable.png").convert_alpha()   #裏口タイル
        table = pygame.transform.scale(table, (SIZE, SIZE))
        pt4 = pygame.image.load("img/PlotTile4.png").convert_alpha()   #モブタイル　
        pt4 = pygame.transform.scale(pt4, (SIZE, SIZE)) 
        pt5 = pygame.image.load("img/PlotTile5.png").convert_alpha()   #字幕タイル
        pt5 = pygame.transform.scale(pt5, (SIZE, SIZE)) 
        pt6 = pygame.image.load("img/PlotStone1.png").convert_alpha()   #字幕タイル
        pt6 = pygame.transform.scale(pt6, (SIZE, SIZE)) 
        pt7 = pygame.image.load("img/PlotTree1.png").convert_alpha()   #字幕タイル
        pt7 = pygame.transform.scale(pt7, (SIZE, SIZE)) 
        pt8 = pygame.image.load("img/PlotOcean1.png").convert_alpha()   #字幕タイル
        pt8 = pygame.transform.scale(pt8, (SIZE, SIZE)) 
        self.scrollx = 2
        self.scrolly = 2
        self.width = 10
        self.height = 9

        self.tiles=[pt2,pt1,pt3,door,door2,pt1,chair1,chair2,table,pt4,pt5,pt6,pt7,pt8]
        self.mapchips = [[
            ["0","0","0","0","0","0","0","3","0","0"],#チュートリアル気質
            ["0","7","1","1","1","1","1","1","1","0"],
            ["0","8","1","1","1","1","1","1","1","0"],
            ["0","6","1","6","8","7","1","1","1","0"],
            ["0","1","1","7","1","1","1","1","1","0"],
            ["0","1","1","1","1","0","0","1","0","0"],
            ["0","1","7","1","1","0","1","1","1","0"],
            ["0","1","1","7","1","0","1","1","1","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ],
            [
            ["9","9","9","9","9","1","1","9","9","9"],#こっからマップが広がる
            ["9","1","1","1","9","1","1","9","1","9"],
            ["9","1","1","1","9","1","1","9","1","9"],
            ["9","9","1","9","9","1","1","1","1","1"],
            ["1","1","1","1","1","1","1","1","1","1"],
            ["1","1","1","1","1","1","10","10","1","10"],
            ["1","1","1","1","1","1","10","1","1","10"],
            ["1","1","1","1","1","1","10","1","1","10"],
            ["1","1","1","1","1","1","10","10","10","10"],
            ],
            [
            ["1","1","12","12","1","1","1","12","12","1"],
            ["1","1","1","1","1","1","1","12","1","1"],
            ["11","1","1","1","11","1","1","1","1","12"],
            ["1","1","12","1","1","1","1","11","1","12"],
            ["1","1","1","1","1","12","1","1","1","12"],
            ["1","12","1","1","1","12","1","12","1","12"],
            ["1","1","1","1","12","11","1","11","1","1"],
            ["1","1","11","1","1","1","1","12","12","1"],
            ["1","11","1","1","1","1","1","1","1","1"],
            ],
            [
            ["13","13","13","13","13","13","13","13","13","13"],
            ["13","13","13","1","13","13","13","13","13","13"],
            ["1","1","13","1","13","13","1","13","13","13"],
            ["1","1","1","1","13","13","1","1","1","13"],
            ["1","1","8","1","8","1","1","1","1","1"],
            ["1","1","1","1","1","1","1","1","1","1"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ],
            [
            ["10","10","10","10","10","1","1","10","10","10"],#こっからマップが広がる
            ["10","1","1","1","10","1","1","10","1","10"],
            ["10","1","1","1","10","1","10","10","1","10"],
            ["10","1","1","1","1","1","1","1","1","1"],
            ["10","1","1","1","1","1","1","1","1","1"],
            ["10","1","1","1","10","10","10","10","1","10"],
            ["10","1","1","1","1","1","10","1","1","10"],
            ["10","1","1","1","1","1","10","1","1","10"],
            ["10","1","1","10","10","10","10","10","10","10"],
            ]]
        self.mapchip = self.mapchips[level-1]
        self.font2=font
        self.w1 = 0 #マップの左端
        self.w2 = 10 #右端(実際の取る値は-1まで)
        self.h1 = 0 #上
        self.h2 = 9 #下(実際の取る値は-1まで)

    def draw_tile(self,screen):
        screen.fill((255,255,255))
        for i in range(self.width):
            for j in range(self.height):
                mapnum = int(self.mapchip[j][i])            
                screen.blit(self.tiles[mapnum] ,Rect(self.scrollx+i*SIZE,self.scrolly+j*SIZE,50,50))            
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
    def draw_scroll(self):
        pass



class Character():
    number=0#リアルタイムでキャラの切り替えができるようにするためのid番号、numberと一致したidを持つインスタンスだけが更新される
    def __init__(self,x,y,id,type,image,team,name,fonts,pocket,hp,ap,dp,energy,steps,level):#-----------------------------------------------------------初期化
        self.id = id
        self.lv = level
        self.name = name#名前
        self.x = x      #キャラの座標
        self.y = y
        self.hp = int(hp*(self.lv*0.2))
        self.hpOrg = self.hp
        self.ap = int(ap*(self.lv*0.2))
        if "剣" in pocket:
            self.ap += 50
        if "拳" in pocket:
            self.ap += 50
            #～拳である拳は対人戦にて強い性質を持つようにする
        self.dp = int(dp*(self.lv*0.15))
        self.dpOrg = dp
        self.steps = steps
        self.shui={"up":[],"down":[], "right":[],"left":[]}   #各方向になにがあるか　敵や岩、なにもないときは[]のまま、
        self.directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]     #indexで使いたいのであえて辞書型にしていない   
        self.pocket=pocket#持ち物
        self.type = type#キャラクタータイプ Player、Slime,Animal,Goutouなどキャラクタータイプ)
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム、モブチームOnly
        self.font = fonts[0]
        self.fontb = fonts[1]
        self.fontm = fonts[2]
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.tick = 0#アニメ用 タイミング調節用
        self.energyOrg = energy #1ターンでどれだけ動けるか　移動１歩や攻撃１回で１energy消費
        self.energy=self.energyOrg#実際のエネルギー量のカウンタ
    def death_check(self,deathplayers):
        if self.name in deathplayers:
            pass
        else:
            if self.hp <= 0:
                if self.team == "味方":
                    deathplayers.append(self.name)
        if self.name in deathplayers:
            self.hp = -50


    #-------------------------------　敵味方共通----------

    def draw(self,screen,B):#--------描画（１次）
        if self.hp>0:
            #画像表示    
            screen.blit(self.image,Rect(B.scrollx+self.x*SIZE,B.scrolly+self.y*SIZE,50,50))
            #hp表示
            self.draw_point(screen, self.hp,5,8,B)
            #energy表示
            self.draw_point(screen, self.energy,75,8,B)

            #ap表示
            self.draw_point(screen, self.ap,5,38,B)

            #dp表示
            self.draw_point(screen, self.dp,75,48,B)

            #level表示
            self.draw_point(screen, self.lv,5,70,B)

            #黄色いガイドの表示
            if Character.number==self.id :
                pygame.draw.circle(screen,(250,250,0),(B.scrollx+(self.x+0.5)*SIZE,B.scrolly+(self.y+0.5)*SIZE),50,2)

    def draw_point(self, screen, point, pos_x, pos_y,B):#（２次）
            txt = str(point)
            txtg = self.fontm.render(txt, True, (0,0,0))  
            screen.blit(txtg, [B.scrollx+self.x*SIZE+pos_x,B.scrolly+self.y*SIZE+pos_y])
            txtg = self.fontm.render(txt, True, (255,255,255))  
            screen.blit(txtg, [B.scrollx+self.x*SIZE+pos_x+2,B.scrolly+self.y*SIZE+pos_y+2])


    def update(self,B,Cs,E,M,screen):#更新（１次受け）#敵味方共通
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
            self.mikata_update(B,Cs,E,M,screen)  
        elif self.team=="敵":
            self.teki_update(B,Cs,M)    
        elif self.team=="モブ":
            self.energy -=1

        if self.energy<=0:#キャラクターの交代
            Character.number=(Character.number+1)%len(Cs)
            #ここで次のキャラを初期化するべし！
            Cs[Character.number].energy = Cs[Character.number].energyOrg
            Cs[Character.number].tick = 0
            self.energy=self.energyOrg#自分も戻しておく

    def check_4directions(self, B, Cs, M):#敵味方共通、四方周囲に何があるか探索
        #上下左右の周囲を見渡して以下のようなデータを作成する
        # self.shui= {'up': ['敵'], 'down': ['壁'], 'right': ['モブ'], 'left': []}
        #壁:地形:味方:敵:モブ

        self.shui = {"up": [], "down": [], "right": [], "left": []}  # リセット
        for directionSet in self.directions:#上下左右をスキャン self.directions = [("up", 0, -1), ("down", 0, 1), ("right", 1, 0), ("left", -1, 0)]   
            self.check_1direction(directionSet, B, Cs, M)#directionSetはこんな形("up", 0, -1)
        #if self.team=="敵":
            #print(f"@150 self.team==敵のとき、{self.name=}  {self.shui=}")    

    def check_1direction(self, directionSet, B, Cs, M):#敵味方共通　#directionSetはこんな形("up", 0, -1)
        direction = directionSet[0]#directionSetはこんな形("up", 0, -1)
        dx = directionSet[1]    
        dy = directionSet[2]
        new_x = self.x + dx#新しい位置＝着目点
        new_y = self.y + dy

        if not (B.w1 <= new_x < B.w2 and B.h1 <= new_y < B.h2):  # 範囲外のチェック
            self.shui[direction].append("壁")
        elif int(B.mapchip[new_y][new_x]) > 1:  # 壁や建造物があるかチェック
            self.shui[direction].append("地形")
        else:
            if self.team=="味方":#味敵味
                for C in Cs:  # キャラクタースキャン
                    if new_x == C.x and new_y == C.y and C.hp>0:#着目点にキャラが居るなら、以下でそいつが何者か調べる
                        if C.team == "敵":
                            C.dp=C.dpOrg#いったんdpを初期状態に戻しておく、dpは挟まれると1/3になるので
                            code = "敵"
                            self.shui[direction].append(code)#ここで目的のself.shui[direction]を作成　
                            # こんなやつ　self.shui= {'up': ['敵'], 'down': ['壁'], 'right': ['モブ'], 'left': []}

                            #挟み撃ち攻撃のチェック（味方ー敵ー味方）
                            hasami_x = new_x + dx
                            hasami_y = new_y + dy
                            if (B.w1 <= hasami_x < B.w2 and B.h1 <= hasami_y < B.h2):
                                for Ch in Cs:  # キャラクタースキャン
                                    if hasami_x == Ch.x and hasami_y == Ch.y and Ch.id!=C.id and Ch.id!=self.id:
                                        if Ch.team=="味方":
                                            C.dp=int(C.dp/3)
                                            mes1=f"挟み撃ち!!{C.name}の防御が{C.dp}に"
                                            M.append_tail_line([mes1])#メッセージ追加
                                            #print(mes1)
                        elif C.team == "味方":
                            code = "味方"
                            self.shui[direction].append(code)#ここで目的のself.shui[direction]を作成　
                        else: #"モブ"はあとまわし
                            pass
            elif self.team=="敵":#敵味敵
                for C in Cs:  # キャラクタースキャン
                    if new_x == C.x and new_y == C.y and C.hp>0:#着目点にキャラが居るなら
                        if C.team == "味方" :#そいつが味方なら
                            C.dp=C.dpOrg#いったんdpを初期状態に戻しておく、dpは挟まれると1/3になるので
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
                                            M.append_tail_line([mes])#メッセージ追加
                        elif C.team == "敵":
                            code = "敵"
                            self.shui[direction].append(code)#ここで目的のself.shui[direction]を作成　

    #全キャラ用、新ガイドを描画するだけ　#敵味方共通
    def new_guide(self,screen,B):
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
                pygame.draw.circle(screen,(250,0,0),(B.scrollx+(px+0.5)*SIZE,B.scrolly+(py+.5)*SIZE),10)
            #味方がいるなら黄ガイド
            elif "味方" in v:
                pygame.draw.circle(screen,(250,255,0),(B.scrollx+(px+0.5)*SIZE,B.scrolly+(py+.5)*SIZE),10)
            #何もないなら青ガイド
            elif v==[]:
                pygame.draw.circle(screen,(0,0,255),(B.scrollx+(px+0.5)*SIZE,B.scrolly+(py+.5)*SIZE),10)
                #移動可能表示

    def useYakusou(self,B,M):#薬草を使う(3次)　#敵味方共通
        self.hp+=30
        if self.hp>self.hpOrg:
            self.hp=self.hpOrg
        self.pocket.remove("薬草")   
        mes1=f"{self.name}は薬草使用！hpは{self.hp}に"
        M.append_tail_line([mes1]) 

    def dmg_calc_show(self,C,M):#ダメージ計算と表示（4次）敵味方共通
        dmg=self.dmg_calc(C)
        #print(f"@239ー{dmg=}")
        mes1=f"{self.name}は{C.name}を攻撃→{dmg}のダメージ"
        if C.hp<=0:
            print(f"@311ー{C.hp=}")
            mes1=mes1+"死んだ"
            time.sleep(1)
        M.append_tail_line([mes1]) 

    def dmg_calc(self,C):#ダメージの計算（５次）敵味方共通
        dmg=self.ap-C.dp
        if dmg <0:
            dmg=0
        C.hp-=dmg  
        return dmg  


    #-----------------------------敵----------------------------------
    def teki_update(self, B, Cs, M): 
        #updateから呼ばれる　（２次受け）
        #B:バック　Cs:キャラクターズ（敵、味方）
        self.tick+=1
        if self.tick % 60 == 30:#早く動きすぎないよう60フレーム中１回動かす
            self.check_4directions(B, Cs, M)        #上下左右の周囲を見渡して以下のようなデータを作成する
            # self.shui= {'up': [], 'down': ['壁'], 'right': ['モブ'], 'left': []}
            if self.hp/self.hpOrg < 0.5:#hpが50%を切ったら
                if "薬草" in self.pocket:#薬草を持っていたら
                    self.useYakusou(B,M)#薬草を使う
                else:        #もってなかったら    
                    self.teki_nigeru(B) #逃げるを実行
            else:#hpが50%以上なら
                self.teki_kougeki(B,Cs,M)#攻撃する
            self.energy -=1#エネルギーをマイナス１

    def teki_kougeki(self,B,Cs,M):#B:バック　Cs:キャラクターズ（敵、味方）
        #敵の攻撃　teki_updateから呼ばれる（３次受け）
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
            #txt="" 
            for d in self.directions:#hpが0になったらshuiから消す
                if kogekiD==d[0]:
                    dx=d[1]
                    dy=d[2]
                    for C in Cs:
                        if C.x==self.x+dx and C.y == self.y+dy and C.team=="味方":
                            self.dmg_calc_show(C,M)

        else:#接敵がないときの向敵アルゴリズム
            self.easy_koteki(B,Cs)#とりあえずランダムで動く簡易化されたやつ
            #self.koteki(B)#本格的なやつ

    def easy_koteki(self,B,Cs):
        #teki_kougekiから呼ばれる　（４次受け）
        #向敵の最初の一歩を計算

        deltas=[]#動ける場所の集合（＝x,yの移動分(dx,dy)）を集めたもの deltas=[(0, -1),  (1, 0), (-1, 0)]だったら上、右、左みたいな感じ

        #まずは１歩だけ（上下左右）
        #動ける方向を収集する
        if self.shui["up"] ==[] :
            if self.y-1 >=B.h1:
                deltas.append((0,-1))#上への移動分（デルタ＝(0,1)）を追加
        if self.shui["down"] ==[]: 
            if self.y+1 <B.h2:
                deltas.append((0,1))
        if self.shui["right"] ==[] :
            if self.x-1 <=B.w2:
                deltas.append((1,0))
        if self.shui["left"] ==[] :
            if self.x+1 >= B.w1:
                deltas.append((-1,0))
        #print(f"@333 {deltas=}")#deltas=[(0, -1),  (1, 0), (-1, 0)]
    
        d = self.calc_target_delta(Cs)#ターゲットのdeltaを計算

        if d in deltas:#動ける方向に入っていればそこに向かう
            delta=d
        else:#なければランダムで選ぶ
            delta = random.choice(deltas)    
        self.x+=delta[0]#移動する
        self.y+=delta[1]

    def calc_target_delta(self,Cs):   #easy_koteki　から呼ばれる（５次受け）戻り値はデルタ
        t_x,t_y,t_id = self.search_target(Cs)#盤面上にいる一番弱いやつを狙う
        if t_id==-1:#該当がない時
            print("@382　相手が見つからず")
            return (-999,-999)
        else:
            dx = t_x-self.x#盤面上にいる最弱の味方キャラとの座標の差分を取る
            dy = t_y-self.y
            #傾き計算の前にdx=0の場合をやっておく
            if dx==0:
                if dy<0:
                    delta=(0,-1) #上に行く
                else:
                    delta=(0,1)  #下に行く   
                return  delta                

            a=dy/dx#傾きを計算
            if -1<a<1:#傾きが-1から+1の範囲内（45度未満）なら
                if dx>0:# t_x-self.x 
                    delta=(1,0)#右
                else:
                    delta=(-1,0)#左
            else:#傾きが45度以上なら
                if dy<0:
                    delta=(0,-1) #下
                else:
                    delta=(0,1) #上                  
            return delta     
            """
        selfが敵(e)、t_xは味方(p)の座標だとして、この位置関係
        ..p.....  p(2,0)
        ...e....  e(3,1)
        ........
        なら
        dx=-1 dy=-1
        de
        """

    def search_target(self,Cs):  #calc_target_deltaから呼ばれる（６次受け）
        #Csの味方の中で一番弱い、生きているキャラを探す
        #目的：敵が味方の一番弱いキャラを狙うため
        t_hp=9999
        t_id=-1#該当がない時
        for C in Cs:
            if C.team=="味方":#味方, C.hp>0は今の非追尾バグには入っていない
                if C.hp>0: 
                    if t_hp>C.hp:  
                        if (abs(C.x - self.x) + abs(C.y - self.y) <= self.steps):#(生きている)かつ(味方チーム)かつ（これまででたCの中で一番弱いよりも小さい）かつ（マンハッタン距離以内）か
                            t_hp=C.hp                                     
                            t_x=C.x
                            t_y=C.y
                            t_id=C.id       
        if t_id==-1:
            return -999,-999,t_id
        else:
            return t_x,t_y ,t_id       

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
               
    #=================味方==========================================
    #モードなしダイレクト入力
    def mikata_update(self,B,Cs,E,M,screen):    
        self.check_4directions(B,Cs,M)#索敵
        self.handle(B,Cs,E,M)          #選択肢をチョイス
        self.Button(screen,B)

    def handle(self,B,Cs,E,M):#移動モードでの入力
        for event in E.getEvent:  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x_pos, y_pos = event.pos
                self.dragging = True  # ドラッグ状態にする
                self.offset_x = B.scrollx - x_pos
                self.offset_y = B.scrolly - y_pos
                new_x=int(x_pos/SIZE)
                new_y=int(y_pos/SIZE)
                if B.scrollx+self.x*100+70< x_pos and B.scrollx+self.x*100+100 > x_pos:
                    if B.scrolly+self.y*100+70 < y_pos and B.scrolly+self.y*100+100 > y_pos:
                        Character.number=(Character.number+1)%len(Cs)
                        self.energy=self.energyOrg
                #dfs=[(0,-1,"up"),(0,1,"down"),(1,0,"right"),(-1,0,"left")]#udrl上下左右の四方との差分
                for directionSet in self.directions:#上下左右の四方のアクションを実行
                    self.handle_action(Cs,B,directionSet,new_x,new_y,M)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False  # ドラッグを終了
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:  # ドラッグ中なら
                    x_pos, y_pos = event.pos
                    B.scrollx = x_pos + self.offset_x
                    B.scrolly = y_pos + self.offset_y 
                    #print(B.scrollx,B.scrolly)

    def handle_action(self,Cs,B,directionSet,new_x,new_y,M):#移動モードでの入力
        direction=directionSet[0]
        dx=directionSet[1]    
        dy=directionSet[2]
        dec = Decimal(str(B.scrollx/SIZE))
        ans = dec.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        dec2 = Decimal(str(B.scrolly/SIZE))
        ans2 = dec2.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        print(f"A{B.scrollx=} {B.scrolly=} {int(ans)=} {int(ans2)=}")
        if new_x-self.x== int(ans)+dx and new_y-self.y == int(ans2)+dy:#方向の特定
            #敵がいるなら
            if "敵" in self.shui[direction]:
                #敵の同定
                for C1 in Cs:
                    if C1.x-self.x == dx and C1.y-self.y == dy and C1.team=="敵":
                        self.dmg_calc_show(C1,M)
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
    def Button(self,screen,B):
        self.Button1 = pygame.image.load("img/pass.png").convert_alpha()   #配置タイル 
        self.Button1 = pygame.transform.scale(self.Button1, (30, 30)) 
        screen.blit(self.Button1,Rect(B.scrollx+self.x*100+70,B.scrolly+self.y*100+70,50,50))#x,yは70から100
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

class Messenger():#draw()は毎フレーム呼ばれ、self.tail_txtをスクロール表示
    def __init__(self,fonts):
        self.font30 = fonts[0]
        self.font60 = fonts[1]
        self.font20 = fonts[2]        

        #ヘッドライン
        self.head_x=5
        self.head_y=20
        self.head_txt=""

        #スクロール画面
        self.tail_x=5   
        self.tail_y=650
        self.max_line=7
        self.tail_txt=["" for i in range(self.max_line)]


    #スクロール用の文字列の追加（ロジックのみで描画しない）
    def append_tail_line(self,txts):
        #前回と同じならスクロールを実行しない
        if txts[0] == self.tail_txt[self.max_line-1]:
                return
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

    #実際の描画
    def draw(self,screen):
        self.draw_head_line(screen)
        self.draw_tail_line(screen)
        
    def draw_head_line(self,screen):
        g_txt = self.font30.render(self.head_txt, True, (0,0,0))   # 描画する文字列の設定
        screen.blit(g_txt, [self.head_x, self.head_y])# 文字列の表示位置

    def draw_tail_line(self,screen):
        #描画
        dy=0
        for t in self.tail_txt:
            g_txt = self.font20.render(t, True, (0,0,0))   # 描画する文字列の設定
            screen.blit(g_txt, [self.tail_x, self.tail_y+dy])# 文字列の表示位置
            dy+=30

class Event():#毎フレーム呼ばれ、取得したeventをself.getEventに入れる
    def __init__(self):
        self.getEvent = pygame.event.get() 
    def update(self):#毎フレーム呼ばれる
        self.getEvent = pygame.event.get()    

def mainInit(level): 
    print (f"{level=}")
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
    TMan = pygame.image.load("img/goutou1.png").convert_alpha()       #強盗、スライムの支配主
    TMan = pygame.transform.scale(TMan, (SIZE, SIZE)) 
    Man = pygame.image.load("img/goutou1m.png").convert_alpha()       #強盗、スライムの支配主
    Man = pygame.transform.scale(Man, (SIZE, SIZE)) 
    TMan2 = pygame.image.load("img/goutou2.png").convert_alpha()       #強盗、スライムの支配主
    TMan2 = pygame.transform.scale(TMan2, (SIZE, SIZE)) 
    Man2 = pygame.image.load("img/goutou2m.png").convert_alpha()       #強盗、スライムの支配主
    Man2 = pygame.transform.scale(Man2, (SIZE, SIZE)) 
    Man3 = pygame.image.load("img/goutou3.png").convert_alpha()       #強盗、スライムの支配主
    Man3 = pygame.transform.scale(Man3, (SIZE, SIZE)) 
    Man4 = pygame.image.load("img/YankeeSlime.png").convert_alpha()       #強盗、スライムの支配主
    Man4 = pygame.transform.scale(Man4, (SIZE, SIZE)) 
    Man5 = pygame.image.load("img/YankeeSlime3.png").convert_alpha()       #強盗、スライムの支配主
    Man5 = pygame.transform.scale(Man5, (SIZE, SIZE)) 
    Man6 = pygame.image.load("img/YankeeSlime2.png").convert_alpha()       #強盗、スライムの支配主
    Man6 = pygame.transform.scale(Man6, (SIZE, SIZE)) 
    Man7 = pygame.image.load("img/goutou4.png").convert_alpha()       #強盗、スライムの支配主
    Man7 = pygame.transform.scale(Man7, (SIZE, SIZE)) 
    level_Max=7
    #死んだキャラクターリストを作ってキャラクターリストに次の出る人が入ってた場合消す
    """例えばgirlが死んだら死んだキャラクターリストに入れて、次のステージからは死んだキャラクターリストで判別して消す"""
    if level==5:
        Db=[
            (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],150,50,80,4,7,5), 
            (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,30,30,5,3,4),
            (1,3,2,"Goutou",Man,"味方","Goutou",fonts,["剣","薬草"],80,80,50,5,5,5),
            (3,2,3,"Goutou2",Man2,"味方","Ramen",fonts,["拳"],300,40,80,8,4,5),
            (3,1,4,"Yankee",Man4,"敵","Yankee1",fonts,["拳"],200,50,120,2,2,2),
            (5,2,5,"Yankee",Man5,"敵","Yankee2",fonts,["拳,スプレー"],150,50,120,3,4,4),#スプレーは敵が前面又は背面に来た場合敵の残りの行動力を0にする
            (8,4,6,"Yankee",Man6,"敵","Yankee3",fonts,["拳","剣"],150,50,120,3,3,3),
            (3,4,7,"Yankeeboss",Man7,"敵","Yankee4",fonts,["拳","スプレー"],180,80,120,3,4,5),
        ]
    if level==4:
         Db=[
            (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],150,50,80,4,7,4), 
            (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,30,30,5,3,4),
            (1,3,2,"Goutou",Man,"味方","Goutou",fonts,["剣","薬草"],80,80,50,5,5),
            (3,2,3,"Goutou2",Man2,"味方","Ramen",fonts,["拳"],300,40,80,8,4,4),
            (3,1,4,"Goutou3",Man3,"敵","Joruno",fonts,["拳","剣"],250,100,120,5,5,5),
        ]       
    if level==3:
        Db=[
            (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],150,50,80,5,7,3),
            (1,3,2,"Goutou",Man,"味方","Goutou",fonts,["剣","薬草"],80,80,50,5,5,3),
            (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,50,30,5,3,3),
            (3,3,3,"Animal",Cat,"味方","Cat",fonts,["拳"],20,80,50,5,2,2),
            (3,2,4,"Goutou2",TMan2,"敵","Ramen",fonts,["拳"],300,60,80,8,4,3),
        ]
    elif level==2:
        Db=[#キャラのデータベース
            #(初期位置x,y、id、タイプ、画像、チーム、名前、フォント、持ち物,hp,ap,dp,energy,steps,level)
            (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],120,50,50,4,3,2),
            (3,5,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,30,30,5,3,2),
            (3,5,2,"Goutou4",Sl1,"敵","BlueSlime",fonts,["薬草"],120,50,30,3,2,1),
            (8,4,3,"Goutou5",Sl2,"敵","YelloSlime",fonts,["薬草"],120,30,40,4,2,1),
            (4,3,4,"Goutou",TMan,"敵","Yakuza",fonts,["剣","薬草"],80,80,50,5,5,2),
            (3,3,5,"Animal",Cat,"味方","Cat",fonts,["拳"],20,50,50,3,2,1),
        ]
    elif level==1:
        Db=[#キャラのデータベース
            #(初期位置x,y、id、タイプ、画像、チーム、名前、フォント、持ち物,hp,ap,dp,energy,steps,level)
            (2,5,0,"Player",Pl1,"味方","Player",fonts,["剣","薬草"],100,50,50,4,3,1),
            (3,4,1,"Player",Pl2,"味方","girl",fonts,["薬草"],50,30,30,5,3,1),
            (5,1,2,"Goutou4",Sl1,"敵","BlueSlime",fonts,["薬草"],120,50,30,2,1,1),
            (4,2,3,"Goutou5",Sl2,"敵","YelloSlime",fonts,["薬草"],120,50,40,2,2,1)
        ]
    if level == level_Max:
        print("コンプリート")
        quit()
    Cs = [Character(*Db[i]) for i in range(len(Db))]    #データベースからインスタンス化
    B1 = BackGround(fonts[0],level)
    J1 = Judge()
    E1 = Event()
    M1 = Messenger(fonts)
    return Cs, B1, J1, ck, E1, M1

def main():#-----------------------------------------------------------メイン
    #init
    pygame.init()        
    screen = pygame.display.set_mode((500, 500))  # 800
    ck = pygame.time.Clock()
    level=1
    #opening.opening(screen,Cs,B1,M1)#本番用
    depl = []
    while True:
        Cs,B1,J1,ck,E1,M1 = mainInit(level)
        #print(f"{len(Cs)=}")
        opening.opening2(Cs)#初期配置
        Character.number=0#現在選択されているキャラ、クラス変数
        #battle 　
        while True:
            E1.update()#1フレームに１回だけeventを取得し、getEventにいれる
            B1.draw_tile(screen)#壁面
            B1.draw_text(screen)#メイン文字
            B1.draw_tail(screen)#補足説明用の文字
            #---------更新と描画---------
            for ch in Cs:#キャラ全員の更新と描画
                ch.death_check(depl) 
                ch.update(B1,Cs,E1,M1,screen)#ただし現在選択されているキャラ以外は即return
                ch.draw(screen,B1)
            for ch in Cs:#ガイドの表示（一旦すべて描画したあとじゃないと埋もれてしまうので）
                ch.new_guide(screen,B1)
            M1.draw(screen)    #メッセージくん
            J1.judge(Cs,M1)    #判定くん
            if J1.winner=="teki" or J1.winner=="mikata":
                break
            pygame.display.update() #画面更新、こいつは引数がない        
            ck.tick(60) #1秒間で60フレームになるように16msecのwait
        if J1.winner=="mikata":
            level+=1 
        else:
            break           
SIZE=100#画面での１マスの大きさ

main()
