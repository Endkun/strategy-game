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
        self.cafe = pygame.image.load("img/CafeTile.png").convert_alpha()   #ドアタイル
        self.barrier = pygame.image.load("img/shopTile.png").convert_alpha()   #ドアタイル
        self.mapchip = [
        ["2","2","2","2","2"],
        ["0","0","0","0","0"],
        ["0","1","1","1","0"],
        ["0","3","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
        ["0","1","1","1","0"],
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
                elif self.mapchip[j][i] == "3":#喫茶店
                    screen.blit(self.cafe ,Rect(self.tx+i*100,self.ty+j*100,50,50))
class Character():
    num = 0#クラス変数
    def __init__(self,x,y,characterType,image,team,name,font2,id):#-----------------------------------------------------------初期化
        #-------------------------------キャラクター
        #------------------キャラクターID
        self.id = id#id番号 
        #------------------キャラクターの基本変数
        self.x = x
        self.y = y
        #---------------------キャラクターのタイプ変数
        self.image = image#イメージ画像
        self.team = team#チーム   味方チーム、敵チーム
        self.name = name#名前
        self.characterType = characterType#キャラクタータイプ プレイヤー、動物、モブ人、敵(スライム、ゾンビなどといったキャラクタータイプ)
        #--------------------キャラクターエネルギー
        #----------------------------------------------設定
        #--------------------フォント
        self.font2 = font2
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
    def playerUpdate(self,screen,mapchip,characters,font2):#移動ボタン用
        self.event(screen,characters)
            #-----------------------------------------------------------------------------------------イベント処理
    def event(self,screen,characters):
        for event in pygame.event.get():  # イベントキューからキーボードやマウスの動きを取得
            if event.type == QUIT:        # 閉じるボタンが押されたら終了
                pygame.quit()             # Pygameの終了(ないと終われない)
                sys.exit()                # 終了（ないとエラーで終了することになる）
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos 
                if self.y*100-100 < y < self.y*100 and self.x*100 < x < self.x*100+100:
                    self.y -= 1  
                if self.y*100+100 < y < self.y*100+200 and self.x*100 < x < self.x*100+100:
                    self.y += 1 
                if self.x*100-100 < x < self.x*100 and self.y*100 < y < self.y*100+100:
                    self.x -= 1
                if self.x*100+100 < x < self.x*100+200 and self.y*100 < y < self.y*100+100:
                    self.x += 1     
    def draw(self,screen,font):#-----------------------------------------------------------描画
        screen.blit(self.image,Rect(self.x*100,self.y*100,50,50))#キャラクターの描画

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
    #tick
    tick = 700
    #フィールド読み込み
    field = Field()
    #キャラクターインスタンス化
    player1 = Character(2,5,"Player",Pl1,"味方","Player",font2,0)#x、y、タイプ、画像、チーム、名前、フォント、id,行動力、攻撃力、防御力、体力
    #キャラクター
    characters = [player1]#catは戦わないから入れない
    #敵味方の数
    valMikata = 1
    valTeki = 0
    ck = pygame.time.Clock()                   
    while True:
        screen.fill((0,0,255))
        field.draw(screen)
        if Character.num >= len(characters):
            Character.num = 0
        #---------プレイヤー-------------------
        for character in characters:
            if character.team == "味方":
                character.playerUpdate(screen,field.mapchip,characters,font2)
            character.draw(screen,font3)
            
        #---------描画---------  
        pygame.display.update()         
        ck.tick(33) #1秒間で30フレームになるように33msecのwait   
main()
