"""
playerから３step（マンハッタン距離で３歩）以内に敵がいたら、リストに放り込んで
    敵リストを返す関数

前提としてplayerが自動的に弱い敵を見つけ出してその方向に一歩踏み出すまで    を　敵位置と一致するまで繰り返す

"""

SIZE = 18  #フィールドの大きさ8x8


class Characters():  #ダミーのクラス

    def __init__(self, id, x, y, hp, team):
        self.id = id
        self.x = x
        self.y = y
        self.hp = hp
        self.team = team


def search_area(grid, start_x, start_y, Cs, steps=3):
    # フィールドのサイズ
    grid_size = len(grid)
    E_list = []  #これが最終結果を収めるリスト

    # 索敵範囲内のマスを調べる
    for ix in range(max(0, start_x - steps), min(grid_size,
                                                 start_x + steps + 1)):
        for jy in range(max(0, start_y - steps),
                        min(grid_size, start_y + steps + 1)):
            # プレイヤーの位置からの距離がsteps以内かどうかをチェック
            if abs(start_x - ix) + abs(start_y - jy) <= steps:
                for C in Cs:
                    if C.x == ix and C.y == jy and C.team == "enemy":
                        print(f"Found {C.team} at ({ix}, {jy}) HP= {C.hp}")
                        E_list.append(C)
    print(f"{E_list=}")                      
    return E_list

#ここから
# フィールドを作成 (0で初期化)
grid = [[0] * SIZE for _ in range(SIZE)]

#キャラクタ初期位置データ
Clist = [
    [2, 1, 100, "enemy"],#あx,y,hp、チーム
    [2, 4, 200, "player"],#い
    [5, 7, 300, "enemy"],#う
    [2, 5, 400, "enemy"],#え
]
"""
敵は３人、味方pが一人（pは自動運転）
索敵範囲の敵は　あとえ、あが最弱なので、この条件だとp（い）は2,1のE（あ）に近づくはず
    01234567
0   ........
1   ..E.....
2   ........
3   ........
4   ..P.....
5   ..E.....
6   ........
7   .....E..

"""


Cs = []#キャラクタ全員（味方チームだけじゃない）
Es = []#索敵エリアに居た敵（敵チーム全員じゃない！）


#全員をインスタンスか
for i, C in enumerate(Clist):
    C1 = Characters(i, *C)  #インスタンス化、idも追加
    Cs.append(C1)

for C in Cs:
    if C.team == "player":#味方チームなら索敵 (味方は1人だけという前提、敵は複数の可能性)
        P=C
        Es = search_area(grid, C.x, C.y, Cs)# 索敵関数を呼出
print(f"@79 {P.x=}  {P.y=}")
#一旦表示
print(f"{Es=}")
#見つかった敵が１匹以上なら、一番弱いやつを探す
if len(Es) > 0:
    hpmin=9999
    idmin=0
    for E in Es:
        if E.hp < hpmin:
            hpmin=E.hp
            idmin=E.id
print(f"{idmin=}")
E=Cs[idmin]

while True:
    print("---------------")
    print(f"{E.x=}  {E.y=}  {P.x=} {P.y=}")
    dx=abs(E.x-P.x)
    dy=abs(E.y-P.y)
    if dx==0 and dy==0:
        break
    print(f"{dx=},{dy=}")
    if dx>dy:#差分の絶対値がｙよりｘが大きいならx方向に動かす
        if E.x-P.x>0:#敵が自分より大きいなら
            print("→")#→
            P.x+=1
        else:
            print("←")
            P.x-=1
    else:
        if E.y-P.y>0:
            print("↓")
            P.y+=1
        else:
            print("↑")
            P.y-=1
    print(f"{P.x=}  {P.y=}")
print("end")
