import os
import random

import pygame
from pygame.locals import *

pygame.init()
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)
W, H = 800, 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Tiki Obstacles')

bg = pygame.image.load(os.path.join('assets', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()


class Player(object):
    fall = pygame.image.load(os.path.join("assets", "0.png"))
    run = [pygame.image.load(os.path.join('assets', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('assets', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('assets', 'S1.png')), pygame.image.load(os.path.join('assets', 'S2.png')),
             pygame.image.load(os.path.join('assets', 'S2.png')), pygame.image.load(os.path.join('assets', 'S2.png')),
             pygame.image.load(os.path.join('assets', 'S2.png')), pygame.image.load(os.path.join('assets', 'S2.png')),
             pygame.image.load(os.path.join('assets', 'S2.png')), pygame.image.load(os.path.join('assets', 'S2.png')),
             pygame.image.load(os.path.join('assets', 'S3.png')), pygame.image.load(os.path.join('assets', 'S4.png')),
             pygame.image.load(os.path.join('assets', 'S5.png'))]
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.hitbox = ()
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    def draw(self, screen):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            screen.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif 20 < self.slideCount < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            screen.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            screen.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)


tiki = Player(200, 313, 64, 64)


class Saw(object):
    image = [pygame.image.load(os.path.join('assets', "SAW0.png")),
             pygame.image.load(os.path.join('assets', "SAW1.png")),
             pygame.image.load(os.path.join('assets', "SAW2.png")),
             pygame.image.load(os.path.join('assets', "SAW3.png"))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0

    def draw(self):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.image[self.count // 2], (64, 64)), (self.x, self.y))
        self.count += 1

    def collide(self, rectangle):
        if rectangle[0] + rectangle[2] > self.hitbox[0] and rectangle[0] < self.hitbox[0] + self.hitbox[2]:
            if rectangle[1] + rectangle[3] > self.hitbox[1]:
                return True
        return False


class Spike(Saw):
    image = pygame.image.load(os.path.join("assets", "spike.png"))

    def draw(self):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.image, (self.x, self.y))

    def collide(self, rectangle):
        if rectangle[0] + rectangle[2] > self.hitbox[0] and rectangle[0] < self.hitbox[0] + self.hitbox[2]:
            if rectangle[1] < self.hitbox[3]:
                return True
        return False


spike = Spike(300, 0, 48, 320)
saw = Saw(300, 300, 64, 64)
pause = 0
fall_speed = 0


def updateFile():
    f = open("scores.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open("scores.txt", "w")
        file.write(str(score))
        file.close()
        return str(score)
    return str(last)


def draw():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    tiki.draw(win)
    for items in objects:
        items.draw()

    pygame.display.update()
    score_font = pygame.font.SysFont("comicsans", 30)
    scoring = score_font.render(f"Score: {str(score)}", True, (255, 255, 255))
    win.blit(scoring, (700, 10))
    pygame.display.update()


def endScreen():
    global pause, fall_speed, objects, speed, score
    run = True
    objects = []
    speed = 30
    pause = 0
    while run:
        pygame.time.delay(300)
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                run = False
            if action.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(bg, (0, 0))
        end_font = pygame.font.Font("freesansbold.ttf", 80)
        previous_score = end_font.render("High Score: " + updateFile(), 1, (255, 255, 255))
        win.blit(previous_score, (W / 2 - previous_score.get_width() / 2, 200))
        new_score = end_font.render(f"Score: {str(score)}", 1, (255, 255, 255))
        win.blit(new_score, (W / 2 - previous_score.get_width() / 2, 320))
        pygame.display.update()
    score = 0
    tiki.falling = False
    tiki.sliding = False
    tiki.jumping = False


pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, random.randrange(3000, 4000))
speed = 30
objects = []
while True:
    score = speed // 5 - 6
    if pause > 0:
        pause += 1
        if pause > fall_speed * 2:
            endScreen()
    for item in objects:
        if item.collide(tiki.hitbox):
            tiki.falling = True
            if pause == 0:
                fall_speed = speed
                pause = 1
        item.x -= 1.4
        if item.x < item.width * -1:
            objects.pop(objects.index(item))
    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == USEREVENT + 1:
            speed += 1
        if event.type == USEREVENT + 2:
            r = random.randrange(0, 2)
            if r == 0:
                objects.append(Saw(810, 310, 64, 64))
            else:
                objects.append(Spike(810, 0, 48, 320))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not tiki.jumping:
            tiki.jumping = True

    if keys[pygame.K_DOWN]:
        if not tiki.sliding:
            tiki.sliding = True
    clock.tick(speed)
    draw()
