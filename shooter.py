import pygame
from random import randint

pygame.init()
pygame.mixer.init()

win_width = 700
win_height = 500
FPS = 60

clock = pygame.time.Clock()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Shooter')

def imgfromtext(text, size, color = (0, 0, 0)):
    return pygame.font.SysFont('Arial', size).render(text, False, color)

class Sprite:
    def __init__(self, window : pygame.display.set_mode, width : int, height : int, images : list() = [], sounds : list() = [], speed : int = 1):
        self.images = list()
        self.sounds = list()
        self.speed = speed
        self.width = width
        self.height = height
        for image in images:
            if type(image) == type(''):
                self.images.append(pygame.transform.scale(pygame.image.load(image), (width, height)))
            else:
                self.images.append(pygame.transform.scale(image, (width, height)))
        self.image = 0
        self.rect = pygame.rect.Rect(0, 0, width, height)
        if self.images:
            self.__upimg__()
        for sound in sounds:
            self.sounds.append(pygame.mixer.Sound(sound))
        self.window = window

    def __upimg__(self):
        self.img = self.images[self.image]
        self.rect = self.img.get_rect()

    def draw(self):
        self.window.blit(self.img, (self.rect.x, self.rect.y))

    def goto(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_img(self, num):
        self.__upimg__()
        if type(num) == type(0):
            self.image = num
        else:
            self.img = num

    def add_img(self, img):
        self.images.append(pygame.transform.scale(img, (width, height)))
        self.__upimg__()

    def collide(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def play(self, num):
        if self.sounds:
            self.sounds[num].play()

    def controls(self, *args):
        keys = pygame.key.get_pressed()
        if keys[args[0]]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[args[1]]:
            if (self.rect.x + self.rect.width) < win_width:
                self.rect.x += self.speed
        if keys[args[2]]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
        if keys[args[3]]:
            if (self.rect.y + self.rect.height) < win_height:
                self.rect.y += self.speed

background = Sprite(win, win_width, win_height, ['galaxy.jpg'], ['space.ogg'])
rocket = Sprite(win, 75, 75, ['rocket.png'], ['fire.ogg'], 5)
bullet = Sprite(win, 50, 50, ['bullet.png'], [], 20)
label = Sprite(win, 200, 50, [imgfromtext('', 50, (255, 255, 255))], [], 20)
ufos = list()
for i in range(5):
    ufos.append(Sprite(win, 75, 50, ['ufo.png'], [], 2.5))
for ufo in ufos:
    ufo.rect.y = 0
    ufo.rect.x = randint(0, win_width - ufo.width)

rocket.goto(300, 425)

skip = 0
scale = 0

background.play(0)
while True:
    background.draw()
    rocket.draw()
    bullet.draw()
    label.draw()
    for ufo in ufos:
        if ufo.rect.y > win_height-ufo.height:
            ufo.rect.y = 0
            ufo.rect.x = randint(0, win_width-ufo.width)
            skip += 1
        else:
            ufo.goto(ufo.rect.x, ufo.rect.y+ufo.speed)
        if ufo.collide(bullet):
            ufo.rect.y = 0
            ufo.rect.x = randint(0, win_width-ufo.width)
            scale += 1
        # ufo.rect.x += randint(0, 1)-1
        ufo.draw()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and bullet.rect.y < 0:
        rocket.play(0)
        bullet.goto(rocket.rect.x+(rocket.width/2), rocket.rect.y+(rocket.height/2))
    if scale >= 150:
        lbl = Sprite(win, 100, 10, [], [])
        lbl.images.append(imgfromtext('!YOU WIN!', 72, (255, 255, 255)))
        lbl.set_img(0)
        lbl.goto(200, 200)
        lbl.draw()
        pygame.display.update()
        while not keys[pygame.K_SPACE]:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        rocket.goto(300, 425)
        skip = 0
        scale = 0
        background.play(0)
    if skip >= 10:
        lbl = Sprite(win, 100, 10, [], [])
        lbl.images.append(imgfromtext('!YOU LOSE!', 72, (255, 255, 255)))
        lbl.set_img(0)
        lbl.goto(200, 200)
        lbl.draw()
        pygame.display.update()
        while not keys[pygame.K_SPACE]:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        rocket.goto(300, 425)
        skip = 0
        scale = 0
        background.play(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    rocket.controls(pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_w)
    bullet.goto(bullet.rect.x, bullet.rect.y-bullet.speed)
    label.set_img(imgfromtext(f'{scale} : {skip}', 50, (255, 255, 255)))
    pygame.display.update()
    clock.tick(FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()