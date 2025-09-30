import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650

LEVEL_UP_INTERVAL = 500
MAX_LEVEL_INDEX = 9
GAMEOVER_ALPHA = 128

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    horintql, vertical = True, True
    if rct.left < 0 or WIDTH < rct.right:
        horintql = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        horintql = False
    return horintql, vertical


def game_over(screen: pg.Surface):

    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(GAMEOVER_ALPHA)
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    left_kk_rect = crying_kk_img.get_rect()
    left_kk_rect.right = text_rect.left - 20
    left_kk_rect.centery = text_rect.centery + 10
    right_kk_rect = crying_kk_img.get_rect()
    right_kk_rect.left = text_rect.right + 20
    right_kk_rect.centery = text_rect.centery + 10

    screen.blit(overlay, [0, 0])
    screen.blit(text, text_rect)
    screen.blit(crying_kk_img, left_kk_rect)
    screen.blit(crying_kk_img, right_kk_rect)

    pg.display.update()
    time.sleep(5)


def prep_bombs() -> tuple[list, list]:

    bb_imgs = []
    for r in range(1, 11):

        bb_img = pg.Surface((20*r, 20*r))

        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs


def main():
    
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = prep_bombs()

    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)

    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        level = min(tmr // LEVEL_UP_INTERVAL, MAX_LEVEL_INDEX)

        avx = vx * bb_accs[level]
        avy = vy * bb_accs[level]

        bb_rct.move_ip(avx, avy)
        beside, vertical = check_bound(bb_rct)

        if not beside:
            vx *= -1
        if not vertical:
            vy *= -1

        current_bb_img = bb_imgs[level]

        screen.blit(current_bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()