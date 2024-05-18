"""
playerから３step（マンハッタン距離で３歩）以内に敵がいたら、リストに放り込んで
    敵リストを返す関数
"""

SIZE = 8  #フィールドの大きさ8x8


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
    return E_list


# フィールドを作成 (0で初期化)
grid = [[0] * SIZE for _ in range(SIZE)]

Clist = [
    [2, 1, 100, "enemy"],
    [2, 4, 200, "player"],
    [5, 7, 300, "enemy"],
    [2, 5, 400, "enemy"],
]
Cs = []
Es = []
for i, C in enumerate(Clist):
    C1 = Characters(i, *C)  #インスタンス化
    Cs.append(C1)

for C in Cs:
    if C.team == "player":
        Es = search_area(grid, C.x, C.y, Cs)
        player_id = C.id
        player_hp = C.hp

# 索敵関数を呼び出す
if len(Es) > 0:
    for E in Es:
        print(f"{E.id=} {E.hp=}")
