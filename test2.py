import time
class Player():#味方クラス(1人)
    def __init__(self,hp,at,df,name,speed):
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name
        self.speed = speed
class Enemy():#敵のクラス(1人)
    def __init__(self,hp,at,df,name,speed): 
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name
        self.speed = speed

def sort(enys):
    n = len(enys)
    for i in range(n):
        for j in range(0, n-i-1):
            if enys[j].speed < enys[j+1].speed:
                enys[j], enys[j+1] = enys[j+1], enys[j]

        
def turn(iCount,enys,plys):
    switchFlag = 0
    #--------敵のターン------------------
    time.sleep(0.5)
    print("---相手のターン-------------")
    print(enys[iCount].name,"の攻撃")
    damage = max(enys[iCount].at-plys[0].df,0)
    plys[0].hp -= damage
    print(enys[iCount].name,"は",plys[0].name,"に",damage,"ダメージを負わせた！")
    print("残りの",plys[0].name,"のhpは",plys[0].hp)
    #print(iCount)
    if iCount == 3:
        switchFlag = 1
        iCount = 0
    #---------------------------------------------------------------------------
    if switchFlag == 1:
        switchFlag = 0
        if plys[0].hp >= 1:
            time.sleep(1)
            #--------味方のターン---------------
            print("---味方のターン-------------")
            print(plys[0].name,"の攻撃")
            damage = max(plys[0].at-enys[iCount].df,0)
            enys[iCount].hp -= damage
            print(plys[0].name,"は",enys[iCount].name,"に",damage,"ダメージを負わせた！")
            print("残りの",enys[iCount].name,"のhpは",enys[iCount].hp)
    return enys,plys
def main():
    plys = []#プレイヤーをまとめた配列
    ply1 = Player(1000,50,0,"自分",15)
    ply2 = Player(80,40,10,"猫",20)
    ply3 = Player(200,50,40,"巨人",5)
    ply4 = Player(100,50,20,"自分のクローン",10)
    plys.append(ply1)
    plys.append(ply2)
    plys.append(ply3)
    plys.append(ply4)
    enys = []#敵をまとめた配列
    eny1 = Enemy(150,30,30,"鬼",5)
    eny2 = Enemy(100,50,10,"青鬼",10)
    eny3 = Enemy(80,50,0,"ネズミ",20)
    eny4 = Enemy(30,50,40,"チビ",15)
    enys.append(eny1)
    enys.append(eny2)
    enys.append(eny3)
    enys.append(eny4)
    while True:
        sort(enys)
        print("ターンの境目--------------------------------------------")
        for i in range(len(enys)):
            enys,plys = turn(i,enys,plys)
            if enys[i].hp <= 0:
                plys.pop(0)
        if plys[0].hp <= 0:
            print("敵チームの勝利")
            break
        if enys ==  "":
            print("味方チームの勝利")
main()

        
        

