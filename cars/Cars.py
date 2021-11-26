'''
Cars
'''
from random import randint
import pygame as pg
import sys

pg.init()
mach = 500
pg.time.set_timer(pg.USEREVENT, mach)

RIGHT = "to the right"
LEFT = "to the left"
UP = "to the up"
DOWN = "to the down"
STOP = "stop"

motion = None
W = 500
H = 639
W_, H_ = 1100, 659
WHITE = (255, 255, 255)
MAIN_FONT = (100, 150, 200)

CARS = ('car1.png', 'car2.png', 'car3.png')

CARS_SURF = []

sc_main = pg.display.set_mode((W_, H_))
sc = pg.Surface((W, H))
sc_main.fill(MAIN_FONT)

pg.mixer.music.load('Super Mario - 1.mp3')
pg.mixer.music.play(-1)

boom = pg.mixer.Sound('smb_bump.wav')
game_over_music = pg.mixer.Sound('smb_gameover.wav')
fire_shot = pg.mixer.Sound('smb_fireworks.wav')
demage_animy = pg.mixer.Sound('smb_breakblock.wav')

info_font = pg.font.Font('font/font.ttf', 50)
font_name = pg.font.Font('font/font.ttf', 80)
text_name = font_name.render('ТАЧКИ', True, (255, 0, 0))
place = text_name.get_rect(center=(850, 60))

score_show = info_font.render("SCORE", True, pg.Color('darkorange'))
score_place = score_show.get_rect(center=(850, 200))
title_record = info_font.render("Record", True, pg.Color('gold'))
record_place = title_record.get_rect(center=(850, 400))

main_font = pg.font.Font('font/font.ttf', 80)
game_over = main_font.render("GAME OVER", True, pg.Color('green'))
game_over_place = game_over.get_rect(center=(W_ // 2, H_ // 2))

bg = pg.image.load('FONT.jpg').convert_alpha()
score = 0


def get_record():
    try:
        with open('record_cars') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record_cars', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record_cars', 'w') as f:
        f.write(str(rec))


for i in range(len(CARS)):
    CARS_SURF.append(
        pg.image.load(CARS[i]).convert_alpha())


class Demage(pg.sprite.Sprite):
    def __init__(self, pos, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Bomb(pg.sprite.Sprite):
    def __init__(self, pos, group):
        pos[0] = pos[0] - 20
        pos[1] = pos[1] - 20
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('bomb.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.add(group)

    def update(self):
        self.rect.y -= 5
        if self.rect.y <= 0:
            self.kill()


class Car(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(
            center=(x, 0))
        self.add(group)
        self.speed = randint(1, 3)

    def update(self):
        if self.rect.y < H:
            self.rect.y += self.speed
        else:
            self.kill()
            global score
            score += -1


class My_Car(pg.sprite.Sprite):

    def __init__(self, x, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(
            filename).convert_alpha()
        self.rect = self.image.get_rect(
            center=(x, H - self.image.get_height() // 2))

    def movie(self, motion):
        if motion == LEFT:
            self.rect.x -= 3
        elif motion == RIGHT:
            self.rect.x += 3
        elif motion == UP:
            self.rect.y -= 3
        elif motion == DOWN:
            self.rect.y += 3
        if self.rect.x <= 0:  # ограничения
            self.rect.x = 0
        if self.rect.x >= W - self.rect.width:  # ограничения
            self.rect.x = W - self.rect.width
        if self.rect.y >= H - self.rect.height:  # ограничения
            self.rect.y = H - self.rect.height
        if self.rect.y <= 0:  # ограничения
            self.rect.y = 0

    def fire(self):
        pg.draw.circle(sc_main, pg.Color('orange'), (self.rect.x + self.rect.width, self.rect.y + self.rect.width // 2),
                       self.rect.width // 4)
        return [self.rect.x + self.rect.width, self.rect.y + self.rect.width // 2]


cars = pg.sprite.Group()
bombs = pg.sprite.Group()
my_car = My_Car(W // 2, 'car.jpg')
pause = False

while 1:
    record = get_record()
    sc_main.blit(bg, (0, 0))
    sc_main.blit(text_name, place)
    sc_main.blit(sc, (20, 20))
    sc_main.blit(score_show, score_place)
    sc_main.blit(title_record, record_place)

    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.USEREVENT and not pause:
            Car(randint(15, W - 15), CARS_SURF[randint(0, 2)], cars)
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_LEFT:
                motion = LEFT
            elif i.key == pg.K_RIGHT:
                motion = RIGHT
            elif i.key == pg.K_UP:
                motion = UP
            elif i.key == pg.K_DOWN:
                motion = DOWN
            elif i.key == pg.K_LCTRL:
                pos = my_car.fire()
                fire_shot.play()
                Bomb(pos, bombs)
            elif i.key == pg.K_SPACE:
                pause = not pause

        elif i.type == pg.KEYUP:
            if i.key in [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN]:
                motion = STOP

    if not pause:
        sc.fill(WHITE)
        sc.blit(my_car.image, my_car.rect)  # тут должна быть моя машинка
        cars.draw(sc)
        bombs.draw(sc)

        if pg.sprite.spritecollideany(my_car, cars): #спрайт и группа
            pg.mixer.music.stop()
            sc_main.blit(info_font.render(str(score), True, pg.Color('red')), (840, 250))
            sc_main.blit(info_font.render(str(record), True, pg.Color('gold')), (840, 450))

            pos = my_car.fire()
            bump = Demage(pos, 'demage_1.jpg')
            sc_main.blit(bump.image, bump.rect)
            pg.display.update()
            boom.play()
            pg.time.wait(1000)
            game_over_music.play()
            pg.time.wait(2000)
            sc_main.blit(game_over, game_over_place)
            pg.display.update()
            pg.time.wait(2000)
            set_record(record, score)
            sys.exit()


        for bom in pg.sprite.groupcollide(bombs, cars, True, True).keys(): #спрайты из разных групп
            demage_animy.play()
            score += 10

        sc_main.blit(info_font.render(str(score), True, pg.Color('red')), (840, 250))
        sc_main.blit(info_font.render(str(record), True, pg.Color('gold')), (840, 450))
        pg.display.update()
        pg.time.delay(20)
        cars.update()
        bombs.update()
        my_car.movie(motion)