'''
The snake
https://python-scripts.com/kivy-android-ios-exe
'''
import pygame as pg
import sys
from random import randint

pg.init()
W, H = 600, 600
W_, H_ = 1000, 620
WHITE = (255, 255, 255)
MAIN_FONT = (100, 150, 200)

pg.mixer.music.load('Super Mario - 2.mp3')
pg.mixer.music.play(-1)

boom = pg.mixer.Sound('smb_bump.wav')
game_over_music = pg.mixer.Sound('smb_gameover.wav')
coin = pg.mixer.Sound('smb_coin.wav')
pause_mix = pg.mixer.Sound('smb_pause.wav')

clock = pg.time.Clock()
FPS = 30
sc_main = pg.display.set_mode((W_, H_))
sc_main.fill(MAIN_FONT)
sc = pg.Surface((W, H))
sc.fill(WHITE)

RIGHT = "to the right"
LEFT = "to the left"
UP = "to the up"
DOWN = "to the down"

motion = UP
mashroom = None
raund = 0
score = 0


bg = pg.image.load('snake.jpg').convert_alpha()

x, y = W // 2, H // 2

def get_record():
    try:
        with open('record_snake') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record_snake', 'w') as f:
            f.write('0')

def set_record(record, score):
    rec = max(int(record), score)
    with open('record_snake', 'w') as f:
        f.write(str(rec))

def gameover():
    pg.mixer.music.stop()
    boom.play()
    pg.time.wait(1000)
    game_over_music.play()
    pg.time.wait(2000)
    sc_main.blit(game_over, game_over_place)
    pg.display.update()
    pg.time.wait(3000)
    sys.exit()

class Head(pg.sprite.Sprite):
    speed = 2

    def __init__(self, x, y, filename, motion, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(
            filename).convert_alpha()
        self.x = x
        self.y = y
        self.motion = motion
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.add(group)

    def move(self):
        sc.fill(WHITE)
        if self.motion == LEFT:
            rot = pg.transform.rotate(self.image, 90)
            rot_rect = rot.get_rect(center=(self.x, self.y))
            sc.blit(rot, rot_rect)
            self.x -= Head.speed
            if self.x < 0:
                self.x = W
            return self.x, self.y

        elif motion == RIGHT:
            rot = pg.transform.rotate(self.image, -90)
            rot_rect = rot.get_rect(center=(self.x, self.y))
            sc.blit(rot, rot_rect)
            self.x += Head.speed
            if self.x > W:
                self.x = 0
            return self.x, self.y


        elif motion == UP:
            sc.blit(self.image, self.rect)
            self.y -= Head.speed
            if self.y < 0:
                self.y = H
            return self.x, self.y

        elif motion == DOWN:
            rot = pg.transform.rotate(self.image, 180)
            rot_rect = rot.get_rect(center=(self.x, self.y))
            sc.blit(rot, rot_rect)
            self.y += Head.speed
            if self.y > H:
                self.y = 0
            return self.x, self.y


class Body(Head):

    def __init__(self, x, y, filename, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        sc.blit(self.image, self.rect)
        self.add(group)


class Fruit(pg.sprite.Sprite):

    def __init__(self, x, y, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(surf).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)

class Mashroom(pg.sprite.Sprite):

    def __init__(self, x, y, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(surf).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)


class Troubles(pg.sprite.Sprite):
    def __init__(self, pos, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.add(group)

heads = pg.sprite.Group()
head = Head(x, y, 'head_snake.png', motion, heads)

BUSHES = ('bush_1.jpg', 'bush_2.jpg', 'bush_3.jpg')
BUSHES_SURF = []
count_troublse = 3

bushes = pg.sprite.Group()
for i in range(count_troublse):
    BUSHES_SURF.append(pg.image.load(BUSHES[randint(0, 2)]).convert_alpha())

for i in range(count_troublse):
    Troubles((randint(0, W // 2 - 2 * head.image.get_width()), (randint(0, H))),
             BUSHES_SURF[randint(0, 2)], bushes)
    Troubles((randint(W // 2 + 2 * head.image.get_width(), W), (randint(0, H))),
             BUSHES_SURF[randint(0, 2)], bushes)

FRUITS = ('apple.png', 'banana.jpg', 'pineaplle.jpg')
fruits = pg.sprite.Group()
fruit = Fruit((randint(head.image.get_width()//2, W - head.image.get_width()//2)),
              (randint(head.image.get_width()//2, H - head.image.get_width()//2)), FRUITS[randint(0, 2)], fruits)

while pg.sprite.spritecollideany(fruit, bushes):
    fruit.kill()
    fruit = Fruit((randint(0, W)), (randint(0, H)), FRUITS[randint(0, 2)], fruits)

mashrooms = pg.sprite.Group()

bodes = pg.sprite.Group()
body_list = []
lenght = 0

font_name = pg.font.Font('font/font.ttf', 80)
text_name = font_name.render('SNAKE', True, (255, 0, 0))
place = text_name.get_rect(center=(800, 65))

info_font = pg.font.Font('font/font.ttf', 60)
score_show = info_font.render("SCORE", True, pg.Color('darkorange'))
score_place = score_show.get_rect(center=(820, 300))
title_record = info_font.render("Record", True, pg.Color('gold'))
record_place = title_record.get_rect(center=(820, 500))

main_font = pg.font.Font('font/font.ttf', 80)
game_over = main_font.render("GAME OVER", True, pg.Color('blue'))
game_over_place = game_over.get_rect(center=(W_ // 2, H_ // 2))

pause_info = main_font.render("PAUSE", True, pg.Color('pink'))
pause_info_place = pause_info.get_rect(center=(W_ // 2, H_ // 2))

pause = False
while True:
    record = get_record()
    sc_main.blit(bg, (0, 0))
    sc_main.blit(sc, (10, 10))
    sc_main.blit(text_name, place)
    sc_main.blit(score_show, score_place)
    sc_main.blit(title_record, record_place)

    sc_main.blit(info_font.render(str(score), True, pg.Color('red')), (800, 350))
    sc_main.blit(info_font.render(str(record), True, pg.Color('gold')), (800, 550))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_LEFT and motion != RIGHT:
                motion = LEFT
            elif i.key == pg.K_RIGHT and motion != LEFT:
                motion = RIGHT
            elif i.key == pg.K_UP and motion != DOWN:
                motion = UP
            elif i.key == pg.K_DOWN and motion != UP:
                motion = DOWN
            elif i.key == pg.K_SPACE:
                pause = not pause
                pause_mix.play()
    if pause:
        sc_main.blit(pause_info, pause_info_place)
        pg.display.update()
    if not pause:
        sc.fill(WHITE)
        head = Head(x, y, 'head_snake.png', motion, heads)
        x, y = head.move()

        if lenght > 0:
            body = Body(x, y, 'body.png', bodes)
            body_list.append(body)

            for i in body_list[:-lenght]:
                i.kill()

        for col in pg.sprite.groupcollide(heads, bushes, False, False).keys():  # snake eats bushes
            print('snake eats bushes')
            set_record(record, score)
            gameover()

        if pg.sprite.spritecollideany(head, mashrooms):
            print('snake eats mashroom')
            set_record(record, score)
            gameover()

        for col in pg.sprite.groupcollide(mashrooms, bushes, True, False).keys():
            print('mashroom on bushes')
            mashroom = Mashroom((randint(head.image.get_width() // 2, W - head.image.get_width() // 2)),
                                (randint(head.image.get_width() // 2, H - head.image.get_width() // 2)), 'mashroom.jpg',
                                mashrooms)

        for col in pg.sprite.groupcollide(fruits, mashrooms, True, False).keys():
            print('mashroom kills fruit')
            fruit = Fruit((randint(fruit.image.get_width(), W - fruit.image.get_width())),
                          (randint(fruit.image.get_width(), H - fruit.image.get_width())), FRUITS[randint(0, 2)], fruits)

        if pg.sprite.spritecollideany(head, bodes):
            bodes.draw(sc)

            if motion == LEFT:
                rot = pg.transform.rotate(head.image, 90)
                rot_rect = rot.get_rect(center=(x, y))
                sc.blit(rot, rot_rect)
            elif motion == RIGHT:
                rot = pg.transform.rotate(head.image, -90)
                rot_rect = rot.get_rect(center=(x, y))
                sc.blit(rot, rot_rect)
            elif motion == UP:
                sc.blit(head.image, head.rect)
            elif motion == DOWN:
                rot = pg.transform.rotate(head.image, 180)
                rot_rect = rot.get_rect(center=(x, y))
                sc.blit(rot, rot_rect)

        for col in pg.sprite.groupcollide(heads, fruits, False, True).keys():
            coin.play()
            score += 10
            FPS += 1
            if lenght < head.image.get_width():
                lenght += head.image.get_width()//2
            elif head.image.get_width() <= lenght <= head.image.get_width() * 2:
                lenght += head.image.get_width()//4
            elif 2 * head.image.get_width() + 1 <= lenght <= 100 * head.image.get_width():
                lenght += head.image.get_width()//8

            fruit = Fruit((randint(fruit.image.get_width(), W - fruit.image.get_width())),
                          (randint(fruit.image.get_width(), H - fruit.image.get_width())), FRUITS[randint(0, 2)],
                          fruits)

            while pg.sprite.spritecollideany(fruit, bushes):
                fruit.kill()
                fruit = Fruit((randint(fruit.image.get_width(), W - fruit.image.get_width())),
                              (randint(fruit.image.get_width(), H - fruit.image.get_width())), FRUITS[randint(0, 2)],
                              fruits)

        if not mashroom:
            dice = randint(1, 400)
            if dice == 1:
                mashroom = Mashroom((randint(head.image.get_width() // 2, W - head.image.get_width() // 2)),
                                    (randint(head.image.get_width() // 2, H - head.image.get_width() // 2)), 'mashroom.jpg',
                                    mashrooms)
                raund = 0
        if mashroom:
            if raund == 500:
                mashroom.kill()
                mashroom = None

        if len(pg.sprite.spritecollide(head, bodes, False)) > 50:  # snake eats itself
            print('snake eats itself')
            set_record(record, score)
            gameover()

        bushes.draw(sc)
        fruits.draw(sc)
        mashrooms.draw(sc)
        pg.display.update()
        raund += 1
        clock.tick(FPS)