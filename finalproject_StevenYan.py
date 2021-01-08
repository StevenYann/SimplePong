'''
finalproject_StevenYan.py
Steven Yan
21/12/2017 11:32:21
v1.2
pong
'''

import pygame
import random
import time

pygame.init()
width = 1100
height = 500
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
done = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.mouse.set_visible(0)

font = pygame.font.Font(None, 90)

clock = pygame.time.Clock()
sprites_list = pygame.sprite.Group()

#collision sound
bump = pygame.mixer.Sound('bump.wav')
death = pygame.mixer.Sound('death.wav')

p1_score = 0
p2_score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, colour, yacc):
        super(Player, self).__init__()
        self.image = pygame.Surface((5, 110))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = height/2

        self.colour = colour
        self.y = 110
        self.yvel = 0
        self.yacc = yacc
    def move_up(self):
        self.yvel -= self.yacc
    def move_down(self):
        self.yvel += self.yacc
    def stop(self):
        self.yvel = 0
    def update(self):
        self.rect.y += self.yvel
    def teleport(self):
        if self.rect.y >= height - 1:
            self.rect.y -= height + 220
        elif self.rect.y <= -300:
            self.rect.y += height + 220


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, xmove, ymove, colour):
        super(Cube, self).__init__()

        cubec = WHITE
        self.image = pygame.Surface((20, 20))
        self.image.fill(cubec)
        self.rect = self.image.get_rect()
        self.rect.x = width/2
        self.rect.y = height/2

        self.xmove = xmove
        self.ymove = ymove
        self.colour = colour

    def move(self):
        self.rect.x += self.xmove
        self.rect.y += self.ymove

    def bounce(self):
        if self.rect.y + self.ymove >= height - 20 or self.rect.y + self.ymove < 0:
            self.ymove *= -1
            bump.play()

    def reset(self):
        global p1_score
        global p2_score
        if self.rect.x < -10:
            p1_score += 1
            self.rect.x = width/2
            self.rect.y = height/2
            death.play()
            time.sleep(3)
        elif self.rect.x + self.xmove > width:
            p2_score += 1
            self.rect.x = width/2
            self.rect.y = height/2
            death.play()
            time.sleep(3)

    def score_print(self):
        self.sc1 = WHITE
        self.sc2 = WHITE
        if p1_score > p2_score:
            self.sc1 = GREEN
            self.sc2 = RED
        elif p2_score > p1_score:
            self.sc2 = GREEN
            self.sc1 = RED
        else:
            self.sc1 = WHITE
            self.sc2 = WHITE
        self.scoreprint = str(p1_score)
        self.text = font.render(self.scoreprint, 1, self.sc1)
        self.textpos = (width/2 + 30, height/2 - 22.5)
        screen.blit(self.text, self.textpos)
        self.scoreprint = str(p2_score)
        self.text = font.render(self.scoreprint, 1, self.sc2)
        self.textpos = (width/2 - 65, height/2 - 22.5)
        screen.blit(self.text, self.textpos)

    def collide(self):
        if pygame.sprite.collide_rect(cube, player1):
            self.xmove *= -1
            bump.play()
        if pygame.sprite.collide_rect(cube, player2):
            self.xmove *= -1
            bump.play()


#cube initialisation
cube = Cube(width/2, height/2, 10, 10, WHITE)
sprites_list.add(cube)

#player initialisation
player_list = []
player1 = Player(50, WHITE, 10)
sprites_list.add(player1)
player_list.append(player1)
player2 = Player(width - 50, WHITE, 10)
sprites_list.add(player2)
player_list.append(player2)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # player 1 controls (ws)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.move_up()
            elif event.key == pygame.K_s:
                player1.move_down()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1.stop()
            elif event.key == pygame.K_s:
                player1.stop()

        # player 2 controls (arrow keys)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2.move_up()
            elif event.key == pygame.K_DOWN:
                player2.move_down()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2.stop()
            elif event.key == pygame.K_DOWN:
                player2.stop()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (width/2, 0), (width/2, height), 1)

    if p2_score == 9:
        scoreprint = str('Winner!')
        text = font.render(scoreprint, 1, WHITE)
        textpos = (30, height/2 - 22.5)
        screen.blit(text, textpos)
        scoreprint = str('Loser!')
        text = font.render(scoreprint, 1, WHITE)
        textpos = (width/2 + 30, height/2 - 22.5)
        screen.blit(text, textpos)
    elif p1_score == 9:
        scoreprint = str('Winner!')
        text = font.render(scoreprint, 1, WHITE)
        textpos = (width/2 + 30, height/2 - 22.5)
        screen.blit(text, textpos)
        scoreprint = str('Loser!')
        text = font.render(scoreprint, 1, WHITE)
        textpos = (30, height/2 - 22.5)
        screen.blit(text, textpos)
    else:
        pygame.draw.circle(screen, WHITE, (width/2, height/2), 100, 1)
        sprites_list.draw(screen)
        cube.move()
        cube.bounce()
        cube.reset()
        cube.score_print()
        cube.collide()

    for player in player_list:
        player.update()
        player.teleport()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
