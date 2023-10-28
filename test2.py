#一人から始まって、順々増えていく
#味方を手に入れるには、普段より小し強い敵を倒すと手に入れられる。
import time
import random
#========================================================================================================    敵味方クラス
class Player():#味方クラス(1人)
    def __init__(self,hp,at,df,name,speed,job):
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name
        self.speed = speed
        self.defend = 0
        #--------------------------------------------------------------------ジョブ
        self.job = job#1が魔法使い(選択肢による),2が格闘家(１発ダメージ２倍),
                      #3がヒーラー(味方を回復する人),4はスカウト(攻撃した相手を困惑させて攻撃できなくする)
                      #5はジョーカー(強化アイテムを盗め、弱体化させることができる)
        #---------------------------------------------------------------------アイテム 1つめは武器 2つめ+はその他アイテム
        if job == 1:#勇者の杖は魔法を使えて、無くすと魔法が使えなくなる。20攻撃力上昇 
            self.items = ["勇者の杖","強化石"]
        
        elif job == 2:#ロングソードは攻撃力2倍、プロテインはスカウトの攻撃を無効化&30回復
            self.items = ["ロングソード","プロテイン"]#プロテインは２回のみ
        
        elif job == 3:#剣はアタックポイントが上昇する。薬草は50回復する
            self.items = ["剣","薬草"]
        elif job == 4:#透明薬は相手に攻撃されなくなる＆攻撃したら反撃ができなくなる
            self.items = ["剣","透明薬"]#透明薬は２回のみ
        elif job == 5:
            self.items = ["ナイフ","姿隠しのマスク"]#姿隠しのマスクを使えば敵のアイテムを盗める(が盗まれたら使えなくなる)
        #-----------------------------------------------------------------is錯乱
        self.confusion = False#錯乱(Trueの場合ターンが終わるまで攻撃ができなくなる)
        if self.job == 2:
            self.at*=2
class Enemy():#敵のクラス(1人)
    def __init__(self,hp,at,df,name,speed,job): 
        self.hp = hp
        self.oldhp = hp
        self.at = at
        self.df = df
        self.name = name
        self.speed = speed
        self.job = job#1が魔法使い(ランダムでn体を同時攻撃),2が格闘家(１発ダメージ２倍),
                         #魔法使いの新要素
                         #魔法使いにも選択ができるように
                         #1.n体への同時攻撃
                         #2.全員を少量回復
                         #3.１人を回復
                         #4.自分又は味方の誰かを防御して無効化
        self.confusion = False#錯乱(Trueの場合ターンが終わるまで攻撃ができなくなる)
        if self.job == 2:
            self.at*=2
#========================================================================================================    ソート
def enySort(enys):
    n = len(enys)
    for i in range(n):
        for j in range(0, n-i-1):
            if enys[j].speed < enys[j+1].speed:
                enys[j], enys[j+1] = enys[j+1], enys[j]
def plySort(plys):
    n = len(plys)
    for i in range(n):
        for j in range(0, n-i-1):
            if plys[j].speed < plys[j+1].speed:
                plys[j], plys[j+1] = plys[j+1], plys[j]
def enyHpSort(enys):
    n = len(enys)#敵ソート用
    for i in range(n):
        for j in range(0, n-i-1):
            if enys[j].hp > enys[j+1].hp:
                enys[j], enys[j+1] = enys[j+1], enys[j]
def plyHpSort(plys):
    n = len(plys)#味方ソート用
    for i in range(n):
        for j in range(0, n-i-1):
            if plys[j].hp > plys[j+1].hp:
                plys[j], plys[j+1] = plys[j+1], plys[j]
#========================================================================================================    ターン攻撃
def enyTurn(enys,plys,end):#敵ターン関数
    plyHpSort(plys)
    for eny in enys:
        if eny.confusion == False:#錯乱中か
            time.sleep(0.2)
            print("---相手のターン-------------")
            #print("i",i,len(enys)-1)
            print(eny.name,"の攻撃")#←攻撃↓
            if plys[0].defend == 1:
                plys[0].defend = 0
                print(plys[0].name,"には攻撃は聞かなかったようだ...")
            else:
                damage = max(eny.at-plys[0].df,0)
                plys[0].hp -= damage
                print("残りの",plys[0].name,"のhpは",plys[0].hp)
                print(eny.name,"は",plys[0].name,"に",damage,"ダメージを負わせた！")
                if eny.job == 4:#錯乱用
                    print(eny.name,"は",plys[0].name,"を錯乱させた！")
                    plys[0].confusion = True
                if eny.job == 5:#盗む用
                    rob = random.randint(0,1)
                    if plys[0].items[0] == "" and plys[0].items[1] == "":
                        print(plys[0].name,"は何も持っていなかった...")
                    elif plys[0].items[rob] == "":
                        print(plys[0].name,"のアイテムはもう取ってしまった..")
                    else:                    
                        print(eny.name,"は",plys[0].name,"の",plys[0].items[rob],"を盗んだ！")
                        plys[0].items[rob] = ""
                if plys[0].hp <= 0:#死亡用
                    print(plys[0].name,"は死んでしまった！")
                    plys.pop(0)
                if len(plys) == 0:
                    print("敵チームの勝利")
                    end = 1
                    break
    return enys,plys,end
#==============================================================================#↑敵関数　↓味方関数
def plyTurn(enys,plys,end):#味方ターン関数
    enyHpSort(enys)
    for ply in plys:
        if ply.hp >= 1:
            if ply.confusion == False:#錯乱中か
                oldat = ply.at
                oldsp = ply.speed
                time.sleep(0.2)
                #--------味方のターン------------------------
                #-プレイヤー操作--------------------
                print("---味方のターン-------------")
                print("操作:",ply.name)
                #---------------------------------------------魔法使い
                if ply.job == 1:
                    if ply.items[1] == "強化石":
                        oldat = ply.at
                        ply.at += 20
                    if ply.items[0] == "勇者の杖" :
                        print("複数攻撃","番号:",1)#ランダムで1~全員の敵へ攻撃(但し攻撃力は半分になる)
                        print("全員回復","番号:",2)#全員を20ずつ回復
                        print("味方回復","番号:",3)#選択された味方を50回復
                        print("防御陣形","番号:",4)#自分又は選択された味方の被ダメージを無効化する
                        choice = input("何の魔法を使いますか？")
                        #print(choice)
                        choice = int(choice)
                        if choice == 1:#複数攻撃
                            for eny in enys:
                                damage = max(ply.at-eny.df,0)
                                eny.hp -= damage
                                print(ply.name,"は",eny.name,"に",damage,"ダメージを負わせた！")
                                print("残りの",eny.name,"のhpは",eny.hp)
                                if eny.hp <= 0:
                                    enys.remove(eny)
                        if choice == 2:#全員回復
                            for ply in plys:
                                ply.hp += 20
                                print(ply.name,"は20HP回復した")
                        if choice == 3:#特定回復or個人回復
                            for plyi in range(len(plys)):
                                print("味方:",plys[plyi].name,"番号:",plyi)
                            players = input("誰を回復しますか")
                            print(plys[int(players)].name,"は50HP回復した")
                            plys[int(players)].hp += 50
                        if choice == 4:
                            for plyi in range(len(plys)):
                                print("味方:",plys[plyi].name,"番号:",plyi)
                            players = input("誰を防御しますか")
                            plys[int(players)].defend = 1
                    else:
                        print("魔法使いは自分の杖を失ったようだ...")
                    ply.at = oldat

                #---------------------------------------------その他味方
                else:#役職ごとにアイテム効果編成
                    oldat = ply.at
                    oldsp = ply.speed
                    if ply.job == 2:
                        if ply.items[0] == "ロングソード":
                            ply.at *= 2
                    if ply.job == 3 or ply.job == 4:
                        if ply.items[0] == "剣":
                            ply.at += 10
                    if ply.job == 4:
                        if ply.items[0] == "ナイフ":
                            ply.at += 5
                            ply.speed += 10

                    for i in range(len(enys)):
                        print("敵",enys[i].name,"番号:",i)
                    choice = input("どの敵を倒しますか？")
                    #print(choice)
                    choice = int(choice)
                    #-攻撃-----------------------------
                    print(" ")
                    print(ply.name,"の攻撃")
                    damage = max(ply.at-enys[choice].df,0)
                    enys[choice].hp -= damage
                    print(ply.name,"は",enys[choice].name,"に",damage,"ダメージを負わせた！")
                    print("残りの",enys[choice].name,"のhpは",enys[choice].hp)
                    if ply.job == 4:#錯乱用
                        print(ply.name,"は",enys[choice].name,"を錯乱させた！")
                        enys[choice].confusion = True
                    #if ply.job == 5:#盗む用
                    #    rob = random.randint(0,2)                        
                    #    print(ply.name,"は",enys[choice].name,"の",enys[choice].items[rob],"を盗んだ！")
                    if enys[choice].hp <= 0:
                        print(enys[choice].name,"を倒した！")
                        enys.pop(choice)
                    if len(enys) == 0:#死亡用
                        print("味方チームの勝利")
                        end = 1
                        break
                    ply.at = oldat
                    ply.speed = oldsp
    return enys,plys,end
"""def plyMagicTurn(enys,ply,end):
    print("---味方のターン-------------")
    if ply.hp >= 1:
        if ply.confusion == False:#錯乱中か
            for eny in enys:
                time.sleep(0.5)"""
            #    damage = max(ply.at*0.4-eny.df,0)
            #    eny.hp -= damage
            #    print(ply.name,"は",eny.name,"に",damage,"ダメージを負わせた！")
            #    print("残りの",eny.name,"のhpは",eny.hp)
            #    if eny.hp <= 0:
            #        enys.remove(eny)
            #    if len(enys) == 0:#死亡用
            #        print("味方チームの勝利")
            #        end = 1
            #        break
            #return enys,ply,end
    
#---------------------------------------------------------------------------------------1バトル

def battleseen(enys,plys):
    end = 0#Whileの強制終了
    turnCount = 0#ターン数
    for eny in enys:
        print(eny.name,"が現れた！")
    while end == 0:
        turnCount += 1
        time.sleep(0.25)
        print("ターンの境目--------------------------------------------",turnCount,"ターン目")
        #for eny in enys:
        for eny in enys:
            print("eny",eny.name,eny.hp,eny.at)#見える化用
        for ply in plys:
            print("ply",ply.name,ply.hp,ply.at)#見える化用
            if ply.job == 3:#Job用,3は回復
                plyHeal = random.randint(0,len(plys)-1)
                plys[plyHeal].hp += 50
                print(plys[plyHeal].name,"が50Hp回復した")

        #敵ターン-----
        enySort(enys)
        enys,plys,end = enyTurn(enys,plys,end)
        #味方ターン---
        for ply in plys:
            plySort(plys)
            enys,plys,end = plyTurn(enys,plys,end)
            break
#========================================================================================================   メイン関数 
def main():

    #---------------------------------------↓味方
    plys = []#プレイヤーをまとめた配列
    ply1 = Player(150,60,30,"自分",15,0)#1(0にしてもいい)
    ply2 = Player(90,70,30,"猫",20,4)#4
    ply3 = Player(200,50,40,"巨人",5,2)#2
    ply4 = Player(120,40,20,"自分のクローン",10,5)#3
    plys.append(ply1)
    #plys.append(ply2)
    #plys.append(ply3)
    #plys.append(ply4)
    plys = [ply1]
    #---------------------------------------↓敵

    #eny1 = Enemy(200,50,30,"鬼",5,3)#3
    #eny2 = Enemy(200,70,10,"青鬼",10,4)#4
    #eny3 = Enemy(50,30,40,"ネズミ",20,2)#2
    #eny4 = Enemy(80,20,10,"チビ",15,1)#1
    eny1 = Enemy(60,30,20,"スライム",15,0)#0(0は特殊スキルなし)
    eny2 = Enemy(100,40,0,"スケルトン",20,0)
    eny3 = Enemy(80,40,30,"ニワトリ",40,0)
    eny4 = Enemy(50,40,10,"リチウムスライム",10,0)
    eny5 = Enemy(60,50,20,"純金スライム",30,0)
    eny6 = Enemy(80,40,0,"ゾンビ",20,0)
    eny7 = Enemy(100,40,0,"スケルトンチーフ",40,2)#小小ボス
    eny8 = Enemy(50,50,20,"スケルトンガード",20,3)
    kouho = [[eny1],
              [eny3],
              [eny6],
              [eny2,eny6],
              [eny2,eny8],
              [eny1,eny4],
              [eny7,eny8],#小小ボス,味方が１人手に入る
              [eny1,eny4,eny5],
              [eny6,eny8,eny2]]
    for i in kouho:
        for j in i:
            j.hp = j.oldhp
        enys = i
        battleseen(enys,plys)


            
main()

        
        
 
