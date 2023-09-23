class Player():#味方クラス(1人)
    def __init__(self,hp,at,df,name):
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name
class Enemy():#敵のクラス(1人)
    def __init__(self,hp,at,df,name):
        self.hp = hp
        self.at = at
        self.df = df
        self.name = name

def sort():
    pass

def turn(enys,plys):
    #--------敵のターン------------------
    print("---相手のターン-------------")
    print(enys[0].name,"の攻撃")
    if enys[0].at <= plys[0].df:
        print(enys[0].name,"は",plys[0].name,"に 0 ダメージを負わせた！")
    else:
        plys[0].hp -= (enys[0].at-plys[0].df)
        print(enys[0].name,"は",plys[0].name,"に",enys[0].at-plys[0].df,"ダメージを負わせた！")
    print("残りの",plys[0].name,"のhpは",plys[0].hp)
    #--------味方のターン---------------
    print("---味方のターン-------------")
    print(plys[0].name,"の攻撃")
    if plys[0].at <= enys[0].df:
        print(plys[0].name,"は",enys[0].name,"に 0 ダメージを負わせた！")
    else:
        enys[0].hp -= (plys[0].at-enys[0].df)
        print(plys[0].name,"は",enys[0].name,"に",plys[0].at-enys[0].df,"ダメージを負わせた！")
    print("残りの",enys[0].name,"のhpは",enys[0].hp)
    
    return enys,plys


def main():
    plys = []#プレイヤーをまとめた配列
    ply1 = Player(100,50,20,"自分")
    ply2 = Player(80,40,10,"猫")
    ply3 = Player(200,50,40,"巨人")
    ply4 = Player(100,50,20,"自分のクローン")
    plys.append(ply1)
    plys.append(ply2)
    plys.append(ply3)
    plys.append(ply4)
    enys = []#敵をまとめた配列
    eny1 = Enemy(150,30,30,"鬼")
    eny2 = Enemy(100,50,10,"青鬼")
    eny3 = Enemy(80,50,0,"ネズミ")
    eny4 = Enemy(30,50,40,"チビ")
    enys.append(eny1)
    enys.append(eny2)
    enys.append(eny3)
    enys.append(eny4)
    while True:
        #enys,plys = sort()
        print("関数外")
        enys,plys = turn(enys,plys)
        if enys[0].hp <= 0:
            print("プレイヤーの勝利")
            break
        if plys[0].hp <= 0:
            print("敵チームの勝利")
            break

main()

        
        

