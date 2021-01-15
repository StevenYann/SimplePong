'''
SimplePong.py
Steven Yan
15/01/2021
v1.3
pong
'''

import pygame
import time

pygame.init()
width = 1100
height = 500
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Simple Pong by Steven Yan")
done = False
pygame.mouse.set_visible(0)
font = pygame.font.Font(None, 90)
clock = pygame.time.Clock()
sprites_list = pygame.sprite.Group()

# collision sounds
bump = pygame.mixer.Sound('bump.wav')
death = pygame.mixer.Sound('death.wav')

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# score count initialisation
left_collision_count = 0
right_collision_count = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, x_position, colour, y_acceleration):
        super(Player, self).__init__()

        self.colour = colour
        self.y = 110
        self.y_velocity = 0
        self.y_acceleration = y_acceleration

        self.image = pygame.Surface((5, self.y))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = height / 2 - self.y / 2

    def move_up(self):
        self.y_velocity -= self.y_acceleration

    def move_down(self):
        self.y_velocity += self.y_acceleration

    def stop(self):
        self.y_velocity = 0

    def update(self):
        self.rect.y += self.y_velocity
        self.__teleport()

    def __teleport(self):
        if self.rect.y >= height - 1:
            self.rect.y -= height + self.y * 2
        elif self.rect.y <= -300:
            self.rect.y += height + self.y * 2


class Cube(pygame.sprite.Sprite):
    def __init__(self, speed, size, colour):
        super(Cube, self).__init__()
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)
        self.rect = self.image.get_rect()

        self.rect.x = width / 2
        self.rect.y = height / 2

        self.x_move = speed
        self.y_move = speed

    def move(self):
        self.rect.x += self.x_move
        self.rect.y += self.y_move

    def bounce(self):
        if self.rect.y + self.y_move >= height - self.size or self.rect.y + self.y_move < 0:
            self.y_move *= -1
            bump.play()

    def reset(self):
        global left_collision_count
        global right_collision_count
        if self.rect.x < -10:
            left_collision_count += 1
            self.__die()
        elif self.rect.x + self.x_move > width:
            right_collision_count += 1
            self.__die()

    def score_print(self):
        if left_collision_count > right_collision_count:
            left_colour = GREEN
            right_colour = RED
        elif right_collision_count > left_collision_count:
            left_colour = RED
            right_colour = GREEN
        else:
            left_colour = WHITE
            right_colour = WHITE
        self.__score_render(left_collision_count, left_colour, 30)
        self.__score_render(right_collision_count, right_colour, -65)

    def collide(self):
        if pygame.sprite.collide_rect(cube, player1) or pygame.sprite.collide_rect(cube, player2):
            self.x_move *= -1
            bump.play()

    def __die(self):
        self.rect.x = width / 2
        self.rect.y = height / 2
        death.play()
        time.sleep(3)

    def __score_render(self, p_score, colour, center_offset):
        self.scoreprint = str(p_score)
        self.text = font.render(self.scoreprint, 1, colour)
        self.textpos = (width / 2 + center_offset, height / 2 - 22.5)
        screen.blit(self.text, self.textpos)


# cube initialisation
cube = Cube(10, 20, WHITE)
sprites_list.add(cube)

# player initialisation
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

        if event.type == pygame.KEYDOWN:
            # player 1 controls (w and s)
            if event.key == pygame.K_w:
                player1.move_up()
            elif event.key == pygame.K_s:
                player1.move_down()
            # player 2 controls (arrow keys)
            elif event.key == pygame.K_UP:
                player2.move_up()
            elif event.key == pygame.K_DOWN:
                player2.move_down()
        elif event.type == pygame.KEYUP:
            # player 1 controls (w and s)
            if event.key == pygame.K_w:
                player1.stop()
            elif event.key == pygame.K_s:
                player1.stop()
            # player 2 controls (arrow keys)
            elif event.key == pygame.K_UP:
                player2.stop()
            elif event.key == pygame.K_DOWN:
                player2.stop()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (width / 2, 0), (width / 2, height), 1)

    if right_collision_count == 9:
        result_print("Winner!")
        result_print("Loser!", width / 2)
    elif left_collision_count == 9:
        result_print("Winner!", width / 2)
        result_print("Loser!")
    else:
        sprites_list.draw(screen)
        cube.move()
        cube.bounce()
        cube.reset()
        cube.score_print()
        cube.collide()

    def result_print(string, offset = 0):
        scoreprint = str(string)
        text = font.render(scoreprint, 1, WHITE)
        text_position = (offset + 30, height / 2 - 22.5)
        screen.blit(text, text_position)

    for player in player_list:
        player.update()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
