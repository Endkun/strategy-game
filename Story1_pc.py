import pygame
from pygame.locals import *
import sys
import random
import time
class Field():
    def __init__(self):
        self.tx = 0
        self.ty = 0
        self.mapWidth = 15 #マスの幅(個数)
        self.mapHeight = 9 #マスの高さ(1マス多い理由は字幕用を稼ぐため)
        self.massSize = 100
        self.pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
        self.pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
        self.pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
        self.door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
        self.door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
        self.mapchip = [
        ["2","2","2","2","2","2","2","2","2","2","2","2","2","2","2"],
        ["0","0","0","0","0","0","0","3","0","0","0","0","0","0","0"],
        ["0","0","1","1","1","1","1","1","1","1","1","1","1","0","0"],
        ["0","0","1","1","1","1","1","1","1","1","1","1","1","0","0"],
        ["0","0","1","1","1","1","1","1","1","1","1","1","1","0","0"],
        ["0","0","1","1","1","1","1","1","1","1","1","1","1","0","0"],
        ["0","0","1","1","1","1","1","1","1","1","1","1","1","0","0"],
        ["0","0","0","0","0","0","0","0","0","0","4","0","0","0","0"],
        ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
        ]
    def draw(self,screen):
        for i in range(self.mapWidth):
            for j in range(self.mapHeight):
                if self.mapchip[j][i] == "1":#床
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
    def __init__(self,x,y,characterType,image,team,name,fonts,id,energy,at,df,hp,personality):#-----------------------------------------------------------初期化
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
        self.pss = personality
        #---------------------包囲用
        self.kat = at+15 #覚醒at
        #---------------------キャラクターのタイプ変数
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム
        self.name = name#名前
        self.characterType = characterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        #--------------------キャラクターエネルギー
        self.energy = energy
        self.tenergy = energy#保存用エナジー
        self.eCount = 0
        #----------------------------------------------設定
        #--------------------フォント
        self.fonts = fonts
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
        #----------------------
        self.chtype = {} #キャラクタータイプのデータ(x,y,体力)
        self.enemyxy = []
        self.ataix = []
        self.ataiy = []
        self.hpl = []
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
        #------------------------情報保存
        """上下左右に敵がいたらキャラクターリストにキャラクターの情報入れる
        　　　　　　　　　　　　　  例:{'左': ['敵', 'Gorotsuki'], '下': ['味方', 'Mikata1']}"""   
        #------------------------enemy
        self.oldx = 0
        self.oldy = 0
        self.wall = []           
    def firstAnimation(self,screen,tick):#-----------------------------------------------------------最初のアニメーション
        self.animaionTick = tick
        if self.characterType == "Slime":   
            if self.name == "BlueSlime":
                if self.animaionTick >= 120:
                    self.x = 7
                    self.y = 2
                if self.animaionTick >= 200:
                    self.y = 3
                if self.animaionTick >= 400:
                    self.x = 8
            if self.name == "YellowSlime":
                if self.animaionTick >= 200:
                    self.x = 7
                    self.y = 2
                if self.animaionTick >= 400:
                    self.y = 3
                if self.animaionTick >= 500:
                    self.x = 6
        if self.characterType == "Goutou":
            if self.name == "Gorotsuki":
                if self.animaionTick >= 400:
                    self.x = 7
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
                    self.x = 8
                if self.animaionTick >= 650:
                    self.y = 9
    def hasamiuti(self,characters):
        for charactera in characters:
            if self.x == charactera.x-1 and charactera.y == self.y:
                for characterb in characters:
                    if self.x == characterb.x-2 and characterb.y == self.y:
                        #if self.team == "味方" and charactera.team == "味方" and characterb.team == "味方" or self.team == "味方" and charactera.team == "敵" and characterb.team == "敵": 
                        if self.team == "敵":
                            if charactera.team == "味方":
                                if characterb.team == "敵":
                                    if self.at != self.kat:
                                        print("味方が包囲された！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                        elif self.team == "味方":
                            if charactera.team == "敵":
                                if characterb.team == "味方":
                                    if self.at != self.kat:
                                        print("敵を包囲した！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                    else:
                        self.at = self.tat
                        charactera.at == charactera.tat
                        characterb.at == characterb.tat
            if self.x == charactera.x+1 and charactera.y == self.y:
                for characterb in characters:
                    if self.x == characterb.x+2 and characterb.y == self.y:
                        #if self.team == "味方" and charactera.team == "味方" and characterb.team == "味方" or self.team == "味方" and charactera.team == "敵" and characterb.team == "敵": 
                        if self.team == "敵":
                            if charactera.team == "味方":
                                if characterb.team == "敵":
                                    if self.at != self.kat:
                                        print("味方が包囲された！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                        elif self.team == "味方":
                            if charactera.team == "敵":
                                if characterb.team == "味方":
                                    if self.at != self.kat:
                                        print("敵を包囲した！")
                                    self.at = self.kat
                                    charactera.at = 0                   
                                    characterb.at = characterb.kat
                    else:
                        self.at = self.tat
                        charactera.at == charactera.tat
                        characterb.at == characterb.tat
            if self.y == charactera.y-1 and charactera.x == self.x:
                for characterb in characters:
                    if self.y == characterb.y-2 and characterb.x == self.x:
                        #if self.team == "敵" and charactera.team == "味方" and characterb.team == "味方" or self.team == "味方" and charactera.team == "敵" and characterb.team == "敵": 
                        if self.team == "敵":
                            if charactera.team == "味方":
                                if characterb.team == "敵":
                                    if self.at != self.kat:
                                        print("味方が包囲された！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                        elif self.team == "味方":
                            if charactera.team == "敵":
                                if characterb.team == "味方":
                                    if self.at != self.kat:
                                        print("敵を包囲した！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                    else:
                        self.at = self.tat
                        charactera.at == charactera.tat
                        characterb.at == characterb.tat
            if self.y == charactera.y+1 and charactera.x == self.x:
                for characterb in characters:
                    if self.y == characterb.y+2 and characterb.x == self.x:
                        #if self.team == "敵" and charactera.team == "味方" and characterb.team == "味方" or self.team == "味方" and charactera.team == "敵" and characterb.team == "敵": 
                        if self.team == "敵":
                            if charactera.team == "味方":
                                if characterb.team == "敵":
                                    if self.at != self.kat:
                                        print("味方が包囲された！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                        elif self.team == "味方":
                            if charactera.team == "敵":
                                if characterb.team == "味方":
                                    if self.at != self.kat:
                                        print("敵を包囲した！")
                                    self.at = self.kat
                                    charactera.at = 0
                                    characterb.at = characterb.kat
                    else:
                        self.at = self.tat
                        charactera.at == charactera.tat
                        characterb.at == characterb.tat
                

    def ctDetection(self,character,direction):
        if self.x+direction[1] == character.x and self.y+direction[2] == character.y:#eチームに差分をたしたところにpチームがいるかを✅
            self.chtype[character.name] = [direction[0],character.hp,direction[1],direction[2]]# ex) {"Player":[上,50,3,7],"Mikata1":[下,30,9,7]}
    def enemyDetection(self,mapchip,character):#eteamがpteamを索敵
        self.ataix = []
        self.ataiy = []
        self.directions = [["上",0,-1],#索敵範囲
                            ["下",0,1],
                            ["右",1,0],
                            ["左",-1,0],
                            ["上2",0,-2],
                            ["下2",0,2],
                            ["右2",2,0],
                            ["左2",-2,0],
                            ["左上",-1,-1],
                            ["左下",-1,1],
                            ["右上",1,-1],
                            ["右下",-1,1],
                            ["上3",0,-3],
                            ["下3",0,3],
                            ["右3",3,0],
                            ["左3",-3,0],
                            ["左左上",-2,-1],
                            ["左左下",-2,1],
                            ["右右上",2,-1],
                            ["右右下",2,1],
                            ["左上上",-1,-2],
                            ["左下下",-1,2],
                            ["右上上",1,-2],
                            ["右下下",1,2]]

        for direction in self.directions:
            self.ctDetection(character,direction)
        #-----------------------キャラクタータイプ
        #for ct in self.chtype:#名前:[hp,x,y] 辞書
        #    #print(character.name)
        #    self.enemyxy = [self.chtype[ct][1],self.chtype[ct][2]]#座標
        #    self.ataix.append(abs(self.x)-abs(character.x))
        #    self.ataiy.append(abs(self.y)-abs(character.y))#距離
    def enemyMove(self,mapchip,character):#敵の動き
        if self.pss == "fierce": #狂暴
            if self.energy <= self.eCount:#エネルギーがなかったら動かない
                pass
            else:
                if self.chtype != {}:
                    if character.name in self.chtype:#chtypeにキャラクターが居たら
                        val = self.chtype[character.name]
                        key = self.chtype.keys()
                        xs = [character.x,self.x]
                        ys = [character.y,self.y]
                        if max(xs)-min(xs) > max(ys)-min(ys):#pチームに行く際に縦横で直線距離が近いほうを取る(この場合は横)
                            if self.x > character.x+1:
                                #print("左")
                                self.x-=1
                            elif self.x < character.x-1:
                                #print("右")
                                self.x+=1
                        else:#縦
                            if self.y > character.y+1:
                                #print("上")
                                self.y-=1
                            elif self.y < character.y-1:
                                #print("下")
                                self.y+=1
                        print(f"@309 {self.x=} {self.y=} {self.name=}" )
                        print(f"@310 {character.x=} {character.y=} {character.name=}" )
                        self.eCount += 1
                        #if character.x == self.x and character.y == self.y:
                        #    break
        if self.pss == "timid": #臆病
            if character.name in self.chtype:
                val = self.chtype[character.name]#[下,30,9,7]等
                x = val[2]#ex)9
                y = val[3]#ex)7
                xs = [character.x,self.x]
                ys = [character.y,self.y]
                self.hpl.append(val[1])
                min_val = 10000000000000000000 #最小値を数えるための限定数
                min_index = 0
                for i in range(len(self.hpl)):#体力が小さいpチームを探す
                    if self.hpl[i] < min_val:
                        min_val = self.hpl[i]
                        min_index = i
                if self.energy <= self.eCount:#エネルギーがなかったら動かない
                    print(self.name,"broke")
                    pass
                else:
                    if val[1] == min_val:
                        if max(xs)-min(xs) > max(ys)-min(ys):#pチームに行く際に縦横で直線距離が近いほうを取る(この場合は横)
                            if self.x > character.x+1:#１歩前は動けないようにする理由はキャラが動いて重ならないようにするため。
                                print(self.name,"左")
                                self.x-=1
                            elif self.x < character.x-1:
                                print(self.name,"右")
                                self.x+=1
                        else:#縦
                            if self.y > character.y+1:
                                print(self.name,"上")
                                self.y-=1
                            elif self.y < character.y-1:
                                print(self.name,"下")
                                self.y+=1
                    #print(f"@346 {self.x=} {self.y=} {self.name=}" )
                    oldx = self.x
                    oldy = self.y 
                self.eCount += 1
        if self.pss == "balance":#バランス
            pass
    def enemyEvent(self,character):
        self.enemyFightCalculation(character)#上下左右で戦えるところを探す 
        if self.hp < self.thp/4:#自身の体力が4割以下になったら薬草を使って回復する
            print(self.name,"は薬草を使った！")
            self.hp += random.randint(10,40)#10~40までのランダムな数を回復  
    def enemyFightCalculation(self,character):#戦えるところを探す
        if self.x == character.x and self.y-1 == character.y: #上方向にpチームがいるか判別
            if self.hp >= 25:#自身の体力が25以上で
                if self.hp+10 >= character.hp:#相手より10体力が高い場合
                    self.findFight.append("ue")
                    self.findFight.append(character.name)#上方向を攻撃するのと、攻撃をするキャラクター
        #else:
        #    if "ue" in self.findFight:
        #        self.findFight.remove("ue")
        #        self.findFight.remove(character.name)

        if self.x == character.x and self.y+1 == character.y: #下方向にpチームがいるか判別
            if self.hp >= 25:#自身の体力が25以上で
                if self.hp+10 >= character.hp:#相手より10体力が高い場合
                    self.findFight.append("sita")
                    self.findFight.append(character.name)#下方向を攻撃するのと、攻撃をするキャラクター
        #else:
        #    if "sita" in self.findFight:
        #        self.findFight.remove("sita")
        #        self.findFight.remove(character.name)

        if self.x+1 == character.x and self.y == character.y: #右方向にpチームがいるか判別
            if self.hp >= 25:#自身の体力が25以上で
                if self.hp+10 >= character.hp:#相手より10体力が高い場合
                    self.findFight.append("migi")  
                    self.findFight.append(character.name)#右方向を攻撃するのと、攻撃をするキャラクター
        #else:
        #    if "migi" in self.findFight:
        #        self.findFight.remove("migi") 
        #        self.findFight.remove(character.name)

        if self.x-1 == character.x and self.y == character.y: #左方向にpチームがいるか判別
            if self.hp >= 25:#自身の体力が25以上で
                if self.hp+10 >= character.hp:#相手より10体力が高い場合
                    self.findFight.append("hidari")
                    self.findFight.append(character.name)#右方向を攻撃するのと、攻撃をするキャラクター
        #else:
        #    if "hidari" in self.findFight:
        #        self.findFight.remove("hidari")
        #        self.findFight.remove(character.name)
        #print(self.findFight)
    def enemyUpdate(self,screen,mapchip,characters,fonts):#敵の処理の核
        #-------------------初期化
        self.findMove.clear()
        self.findFight.clear()
        self.hpl.clear()
        self.chtype = {}
        self.eCount = 0
        #-------------------体力が0以下の時にプログラムから追い出す
        if self.hp <= 0:
            self.x = -10
            self.y = -10
            Character.num += 1
            return
        #----------------------------pチームの索敵、eチームの動きなど
        for character in characters:
            if character.team == "味方":#pチームだけ呼び出す
                self.enemyDetection(mapchip,character)#eチームがpチームを索敵
                self.enemyMove(mapchip,character)#索敵に基づいたeチームの動き
                self.enemyEvent(character)#eチーム細かな設定など(例：アイテムの処理や回復等)
            """findMoveは配列,データにmigi,hidari,sita,ueの４つが入る
               例えば['sita', 'hidari']等"""
        #print(self.findFight)
        if self.findFight == []:
            #-----------------------------旧式の動き
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
            #-----------------------------攻撃
            print(self.name,"が",self.findFight[1],"に攻撃")
            for character in characters:
                if character.name == self.findFight[1]:
                    character.hp -= max(0,self.at-character.df)
            #print(self.addName,"に攻撃")
            Character.num += 1
        self.hasamiuti(characters)
            
                
    def playerUpdate(self,screen,mapchip,characters,fonts):#移動ボタン用
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
        self.hasamiuti(characters)
    def temp(self,characters,sc):
        self.opponent.append(sc[1])
        self.fight(characters)
        self.energy -= 1
        self.fightFalses = True
    def move(self,houkou,dy,dy2,dx,dx2,setnum,setnum2,x,y):
        if houkou in self.findMove: 
            if self.y*100+dy < y < self.y*100+dy2 and self.x*100+dx < x < self.x*100+dx2:
                self.y += setnum
                self.x += setnum2
                self.energy -= 1
    def fightremove(self,houkou):
        if houkou in self.findFight:
            self.findFight.remove(houkou)

            #-----------------------------------------------------------------------------------------イベント処理
    def event(self,screen,characters):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos 
                self.move("ue",-100,0,0,100,-1,0,x,y)
                self.move("sita",100,200,0,100,1,0,x,y)
                self.move("hidari",0,100,-100,0,0,-1,x,y)
                self.move("migi",0,100,100,200,0,1,x,y)  
                if self.isFight == True:
                    x,y = event.pos
                    self.opponent.clear()
                    if "ue" in self.findFight:
                        if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                            sc = self.characterlists['上']
                            self.temp(characters,sc)
                    if "sita" in self.findFight:
                        if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                            sc = self.characterlists['下']
                            self.temp(characters,sc)
                    if "hidari" in self.findFight:
                        if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                            sc = self.characterlists['左']
                            self.temp(characters,sc)
                    if  "migi" in self.findFight:
                        if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                            sc = self.characterlists['右']
                            self.temp(characters,sc)
                    if self.fightFalses == True:
                        self.fightremove("ue")
                        self.fightremove("sita")
                        self.fightremove("migi")
                        self.fightremove("hidari")
    def detection_check(self,character,houkou,dx,dy):
        if self.x + dx == character.x and self.y + dy == character.y: #上
            if houkou in self.findMove:
                self.findMove.remove(houkou)
    def characterlist_check(self,character,houkou,dx,dy):
        if self.x+dx == character.x and self.y+dy == character.y:
            if character.team == "味方":
                self.characterlists[houkou] = ["味方",character.name]
            else:
                self.characterlists[houkou] = ["敵",character.name]
    def wall_check(self,houkou,dx,dy,mapchip):
        if mapchip[self.y+dy][self.x+dx] != "1": #上
            self.wall.append(houkou)
    def move_check(self,houkou,dx,dy,mapchip):
        if mapchip[self.y+dy][self.x+dx] == "1": #上
            self.findMove.append(houkou)
    def detection(self,screen,mapchip,characters):#動くときに周囲をチェックする関数

    #-----------------------------------------------------------------------------------------動ける所の検出
        self.wall = []
        self.characterlists = {}
        for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
            #-----------------------------------------------------------索敵(敵)
            self.characterlist_check(character,"上",0,-1)
            self.characterlist_check(character,"下",0,1)
            self.characterlist_check(character,"右",1,0)
            self.characterlist_check(character,"左",-1,0)
        #------------------------------------------------------------------壁検知
        self.wall_check("ue",0,-1,mapchip)
        self.wall_check("sita",0,1,mapchip)
        self.wall_check("migi",1,0,mapchip)
        self.wall_check("hidari",-1,0,mapchip)
        #--------------------------------------------------------------------------------------動き判定
        self.move_check("ue",0,-1,mapchip)
        self.move_check("sita",0,1,mapchip)
        self.move_check("migi",1,0,mapchip)
        self.move_check("hidari",-1,0,mapchip)
        for character in characters:#他のキャラクターを呼び出して上下左右にキャラクターが居るかを判別する。
            self.detection_check(character,"ue",0,-1)
            self.detection_check(character,"sita",0,1)
            self.detection_check(character,"migi",1,0)
            self.detection_check(character,"hidari",-1,0)

    def fight(self,characters):
        print(self.name,"は",self.opponent,"に攻撃をした！")
        for character in characters:
            if character.name == self.opponent[0]:
                print(self.opponent,"の前hpは",character.hp)
                character.hp -= max(0,self.at-character.df)
                print(self.opponent,"のhpは",character.hp,"になった")
                if character.hp <= 0:
                    character.x = -10
                    character.y = -10

        return
    def place(self):#----------------------------------------------------------------アクション
        if self.characterType == "Goutou":
            if self.name == "Gorotsuki":
                self.y = 3
    def direction_check(self, dx, dy, direction_key, fight_key, mapchip, screen):
        if mapchip[self.y + dy][self.x + dx]== "1":
            if direction_key in self.characterlists.keys():
                cget = self.characterlists.get(direction_key, [])  # キーが存在しない場合は空リストを返す
                if cget[0] == "敵":
                    pygame.draw.circle(screen, (250, 0, 0), ((self.x + dx + 0.5) * 100, (self.y + dy + 0.5) * 100), 10)
                    self.isFight = True
                    self.findFight.append(fight_key)
                elif cget[0] == "味方":
                    pygame.draw.circle(screen, (0, 0, 250), ((self.x + dx + 0.5) * 100, (self.y + dy + 0.5) * 100), 10)
            else:
                pygame.draw.circle(screen, (250, 250, 0), ((self.x + dx + 0.5) * 100, (self.y + dy + 0.5) * 100), 10)
    def circle(self,screen,mapchip):
        self.findMove.clear()
        self.findFight.clear()
        self.direction_check(0, -1, "上", "ue",mapchip,screen)
        self.direction_check(0, 1, "下", "sita",mapchip,screen)
        self.direction_check(1, 0, "右", "migi",mapchip,screen)
        self.direction_check(-1, 0, "左", "hidari",mapchip,screen)
        
    def draw(self,screen,fonts):#-----------------------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))#キャラクターの描画
        hpFont = fonts[2].render(str(self.hp), True, (255,255,255)) # 描画する文字列を画像にする
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
        #print(f"{self.cm=} {self.ct=}")
        
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


def animation(tick,characters,mapchip,screen,fonts,ck,field):
    pt1 = pygame.image.load("img/PlotTile1.png").convert_alpha()   #配置タイル 全て100x100
    pt2 = pygame.image.load("img/PlotTile2.png").convert_alpha()   #モブタイル　
    pt3 = pygame.image.load("img/PlotTile3.png").convert_alpha()   #字幕タイル
    door = pygame.image.load("img/door.png").convert_alpha()   #ドアタイル
    door2 = pygame.image.load("img/door2.png").convert_alpha()   #裏口タイル
    while tick < 800:
        tick += 1
        screen.fill((255,255,255))
        if tick < 500:
            Story = fonts[0].render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = fonts[0].render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        if tick > 500:
            Story = fonts[0].render("強盗だ！金を出せ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = fonts[0].render("打たれたくないなら金だ！", True, (0,0,0)) # 描画する文字列を画像にする
        screen.blit(Story, [70,40])
        screen.blit(Story2,[70,70]) 
        field.draw(screen)
        #---------アニメーション---------
        for character in characters:
            character.firstAnimation(screen,tick)
            character.draw(screen,fonts)
        pygame.display.update()
        ck.tick(160) #1秒間で30フレームになるように33msecのwait      
def main():#-----------------------------------------------------------メイン
    #初期化
    pygame.init()        
    #フォント   
    font = pygame.font.SysFont("yumincho", 30)       
    font2 = pygame.font.SysFont("yumincho", 60) 
    font3 = pygame.font.SysFont("yumincho", 15)
    fonts = [font,font2,font3]                        
    SCREEN_X = 1500
    SCREEN_Y = 800
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # 800
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
    player1 = Character(6,5,"Player",Pl1,"味方","Endo",fonts,0,3,12,12,50,"fierce")#x、y、タイプ、画像、チーム、名前、フォント、id,行動力、攻撃力、防御力、体力
    player2 = Character(7,4,"Player",Pl2,"味方","Sora",fonts,1,2,6,6,30,"fierce")#攻撃力、防御力は6,行動力は1ずつ増えていく。最大30(行動力は最大5)
    #player3 = Character(8,4,"Player",Pl1,"味方","Nao",fonts,2,2,12,12,80,"fierce")
    #player4 = Character(9,5,"Player",Pl2,"味方","Soushi",fonts,3,2,6,12,10,"fierce")#何かあった時の追加用
    slime1 = Character(-1,0,"Slime",Sl1,"敵","BlueSlime",fonts,2,1,12,6,50,"fierce")
    slime2 = Character(-1,0,"Slime",Sl2,"敵","YellowSlime",fonts,3,2,12,3,40,"timid")
    goutou = Character(-1,0,"Goutou",Man,"敵","Gorotsuki",fonts,4,5,30,5,80,"balance")
    cat = Character(1,4,"Animal",Cat,"モブ","Cat",fonts,5,1,0,0,20,"timid")#fierceは無鉄砲,timidは臆病タイプ
    #キャラクター
    characters = [slime1,slime2,goutou,player1,player2]#catは戦わないから入れない,[,player3,player4]追加
    judge = Judge(characters)   
    #敵味方の数
    valMikata = 2
    valTeki = 3
    #死亡カウント
    ck = pygame.time.Clock()
    animation(tick,characters,field.mapchip,screen,fonts,ck,field)                     
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
                    character.enemyUpdate(screen,field.mapchip,characters,fonts)
                    #print(f"@685 {character.at=} {character.name=}")
                if character.team == "味方":
                    character.playerUpdate(screen,field.mapchip,characters,fonts)
            character.draw(screen,fonts)
        for character2 in characters:
            if Character.num == character2.id:
                if character2.team == "味方":
                    character2.circle(screen,field.mapchip)
        judge.hantei(characters)
        #---------描画---------  
        pygame.display.update()         
        ck.tick(60) #1秒間で30フレームになるように33msecのwait   
main()
 