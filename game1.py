import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面の幅と高さ
WIDTH, HEIGHT = 800, 600

# 画面の設定
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("横スクロールアクションゲーム")

# プレイヤーのキャラクター
player = pygame.Rect(50, 300, 40, 40)
player_color = (255, 0, 0)

# プレイヤーの速度
player_speed = 1

# メインゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力の処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_s]:
        player.y += player_speed
    if keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_d]:
        player.x += player_speed

    # 描画
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player_color, player)

    pygame.display.update()

# Pygameの終了
pygame.quit()
sys.exit()
