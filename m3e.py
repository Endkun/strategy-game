import pygame
import random
W=2000#全サイズ（仮想画面の範囲）
H=2000
CW=600#カメラ　サイズ（見えている範囲）
CH=800
class Enemy():
    # 敵キャラの設定
    def __init__(self):
        self.enemy_size = 30
        self.enemy_color = (0, 255, 0)  # 初期の青色
        self.x = random.randint(0, W - self.enemy_size)
        self.y = random.randint(0, H - self.enemy_size)  # ランダム位置
        self.sx = random.choice([-2, 2])
        self.sy = random.choice([-2, 2])  # ランダムな初期速度
    def chk(self,P):   # 敵キャラがクリックされたかチェック
        if self.x <= P.px <= self.x + self.enemy_size and self.y <= P.py <= self.y + self.enemy_size:
            # 敵キャラの色を変える（ランダムに変更）
            r1 = random.randint(1, 255)
            g1 = random.randint(1, 255)
            b1 = random.randint(1, 255)
            self.enemy_color = (r1, g1, b1)
            P.point += 1
    def update(self):
        # 敵キャラの移動
        self.x += self.sx
        self.y += self.sy
        # 敵キャラがマップの端に到達したら方向をランダムに変える
        if self.x <= 0 or self.x >= W - self.enemy_size:
            self.sx = -self.sx
        if self.y <= 0 or self.y >= H - self.enemy_size:
            self.sy = -self.sy
        # 敵キャラが少しの確率で方向を変える
        if random.random() < 0.01:
            self.sx = random.choice([-2, 2])
            self.sy = random.choice([-2, 2])
    def draw(self,scr):
        pygame.draw.rect(scr, self.enemy_color, (self.x, self.y, self.enemy_size, self.enemy_size))  # 敵キャラを描画
class Player():
    def __init__(self):
        # カメラ（表示領域）の位置
        self.camera_x, self.camera_y = 0, 0
        # ドラッグ状態管理
        self.dragging = False
        self.start_x = 0
        self.start_y = 0
        self.px =0
        self.py =0
        self.point = 0  #得点
    def update(self):
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # マウスボタンが押されたとき、ドラッグ開始
            if event.type == pygame.MOUSEBUTTONDOWN:
            #if event.button == 1:  # 左クリック
                self.dragging = True
                self.start_x, self.start_y = event.pos  #最初のスタート位置,これは差分じゃないので注意！
                # 画面上のクリック位置をマップ上の位置に変換
                self.px = event.pos[0] + self.camera_x  #見えない部分も含めた全画面上における絶対座標を計算
                self.py = event.pos[1] + self.camera_y
            # マウスボタンが離されたとき、ドラッグ終了
            if event.type == pygame.MOUSEBUTTONUP:
                #if event.button == 1:  # 左クリック
                    self.dragging = False
            # ドラッグ中の動作
            if event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.dx = event.pos[0] - self.start_x  # マウス位置とスタート位置の差分を計算
                    self.dy = event.pos[1] - self.start_y
                    self.camera_x -= self.dx  # カメラを差分だけ動かす
                    self.camera_y -= self.dy
                    self.start_x, self.start_y = event.pos  # 現在の位置を新たにスタート位置とする
                    # カメラ位置の制限（画面外にはみ出さないようにする）
                    self.camera_x = max(0, min(W - CW, self.camera_x))
                    self.camera_y = max(0, min(H - CH-200, self.camera_y))
#=====================================
#start
pygame.init()
running = True
FPS = 60  # フレームレート
screen = pygame.display.set_mode((CW, CH))  #実画面サイズ
scr = pygame.Surface((H, W))                  #仮想画面サイズ
scr.fill((128,0, 0))                          #マップの背景色（緑）
# フォントの初期化（デフォルトフォント、サイズ36）
font = pygame.font.Font(None, 36)
#インスタンス化
Es=[]
for i in range(30):
    E=Enemy()
    Es.append(E)
P=Player()
clock = pygame.time.Clock()
# メインループ
while running:
    scr.fill((100, 0, 0))  # 背景を再描画
    #敵の更新、描画
    for E in Es:
        E.update()
        if P.dragging:
            E.chk(P)
        E.draw(scr)
    P.update()
    #背景を描画　とりあえず全体の分
    w_size=50
    num=int(W/w_size)
    for i in range(num):
        pygame.draw.rect(scr, (255, i, 0), (i * 50, i * 50, 40, 40))  # 赤四角を再描画
    for i in range(num+20):
        pygame.draw.rect(scr, (0, 0, 255), (i * 50, i * 50 + 500, 40, 40))  # 青四角を再描画
    # ◆全ての仮想画面（scr）からカメラで見える範囲を切り取って表示
    print(f"{P.camera_x=} {P.camera_y=}")
    screen.blit(scr, (0, 0), (P.camera_x, P.camera_y, CW, CH))
    # スコアテキストを描画
    score_text = font.render(f"Points: {P.point}", True, (255, 255, 255))  # スコアを描画
    screen.blit(score_text, (10, 10))  # 固定位置(10, 10)に描画
    # 画面更新
    pygame.display.flip()
    # フレームレートを維持
    clock.tick(FPS)
pygame.quit()














