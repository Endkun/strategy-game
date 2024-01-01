
import pygame
pygame.init() 

def opening2(screen,font,Cs,backGround):#--------------------
    for C1 in Cs:
        if C1.type == "Slime":   
            if C1.name == "BlueSlime":
                C1.y = 4
                C1.x = 1
            if C1.name == "GreenSlime":
                C1.y = 4
                C1.x = 3
        if C1.type == "Goutou" and C1.name == "Yakuza Sumiyoshi":
                C1.x = 2
                C1.y = 2
        if C1.type == "Player" and C1.name == "girl":
                C1.y += 1
                C1.y += 0
        if C1.type == "Animal" and C1.name == "Cat":
                C1.x = 0
                C1.y = 4

def opening(screen,font,Cs,B):#--------------------
    ##オープニング
    ck = pygame.time.Clock()
    tick=0
    while True:
        tick += 1
        if tick>800:
            break
        B.draw_tile(screen)
        if tick <= 500:
            Story = font.render("喫茶店でくつろいでいたら", True, (0,0,255)) # 描画する文字列を画像にする
            Story2 = font.render("突然強盗が入ってきた！", True, (0,0,255)) # 描画する文字列を画像にする
        elif 500 < tick <= 700:
            Story = font.render("強盗だ！金を出せ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("56されたくないなら金だ！", True, (0,0,0)) # 描画する文字列を画像にする
        if tick > 700:
            Story = font.render("こいつ、逆らう気だぞ！", True, (0,0,0)) # 描画する文字列を画像にする
            Story2 = font.render("野郎ども　やっちまえ", True, (0,0,0)) # 描画する文字列を画像にする
        screen.blit(Story, [70,40])
        screen.blit(Story2,[70,70])   
        #---------アニメーション---------
        for C1 in Cs:
            C1.firstAnimation()

        #---------描画---------
        for C1 in Cs:
            C1.draw(screen)
                          
        pygame.display.update()         
        ck.tick(60) #1秒間で30フレームになるように33msecのwait   