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
        self.job = job#1が魔法使い(ランダムでn体を同時攻撃),2が格闘家(１発ダメージ２倍),
                      #3がヒーラー(ランダムで味方を回復する人),4はスカウト(攻撃した相手を困惑させて攻撃できなくする)
        if self.job == 2:
            self.at*=2
class Enemy():#敵のクラス(1人)
    def __init__(self,hp,at,df,name,speed,job): 
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name
        self.speed = speed
        self.job = job#1が魔法使い(ランダムでn体を同時攻撃),2が格闘家(１発ダメージ２倍),
                      #3がヒーラー(ランダムで味方n人を回復する人),4はスカウト(攻撃した相手を困惑させて攻撃できなくする)
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
        time.sleep(0.2)
        print("---相手のターン-------------")
        #print("i",i,len(enys)-1)
        print(eny.name,"の攻撃")#←攻撃↓
        damage = max(eny.at-plys[0].df,0)
        plys[0].hp -= damage
        print("残りの",plys[0].name,"のhpは",plys[0].hp)
        print(eny.name,"は",plys[0].name,"に",damage,"ダメージを負わせた！")
        if plys[0].hp <= 0:
            plys.pop(0)
        if len(plys) == 0:
            print("敵チームの勝利")
            end = 1
            break
    return enys,plys,end
#==============================================================================
def plyTurn(enys,plys,end):#味方ターン関数
    enyHpSort(enys)
    for ply in plys:
        if ply.hp >= 1:
            time.sleep(0.5)
            #--------味方のターン---------------
            print("---味方のターン-------------")
            print(ply.name,"の攻撃")
            damage = max(ply.at-enys[0].df,0)
            enys[0].hp -= damage
            print(ply.name,"は",enys[0].name,"に",damage,"ダメージを負わせた！")
            print("残りの",enys[0].name,"のhpは",enys[0].hp)
            if enys[0].hp <= 0:
                enys.pop(0)
            if len(enys) == 0:
                print("味方チームの勝利")
                end = 1
                break
    return enys,plys,end
#========================================================================================================   メイン関数 
def main():
    end = 0#Whileの強制終了
    turnCount = 0#ターン数
    plys = []#プレイヤーをまとめた配列
    ply1 = Player(150,60,30,"自分",15,1)
    ply2 = Player(90,70,30,"猫",20,4)
    ply3 = Player(200,50,40,"巨人",5,2)
    ply4 = Player(120,40,20,"自分のクローン",10,3)
    plys.append(ply1)
    plys.append(ply2)
    plys.append(ply3)
    plys.append(ply4)
    enys = []#敵をまとめた配列
    eny1 = Enemy(200,50,30,"鬼",5,3)
    eny2 = Enemy(200,70,10,"青鬼",10,1)
    eny3 = Enemy(50,30,40,"ネズミ",20,2)
    eny4 = Enemy(80,20,10,"チビ",15,4)
    enys.append(eny1)
    enys.append(eny2)
    enys.append(eny3)
    enys.append(eny4)
    while end == 0:
        plyHeal = random.randint(0,len(plys))
        turnCount += 1
        time.sleep(0.25)
        print("ターンの境目--------------------------------------------",turnCount,"ターン目")
        #for eny in enys:
        for eny in enys:
            print("eny",eny.name,eny.hp,eny.at)#見える化用
        for ply in plys:
            print("ply",ply.name,ply.hp,ply.at)#見える化用
            if ply.job == 2:#Job用,3は回復
                plys[plyHeal].hp += 50
                print(plys[plyHeal].name,"が50Hp回復した")


        #敵ターン-----
        enySort(enys)
        enys,plys,end = enyTurn(enys,plys,end)
        #味方ターン---
        plySort(plys)
        enys,plys,end = plyTurn(enys,plys,end)



            
main()

        
        
 
