import time
import random

import pygame
from pygame.locals import *
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:

    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):

        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE
        self.draw()


class Snake:

    def __init__(self, parent_screen, length):
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.screen = parent_screen
        self.direction = 'down'

    def draw(self):

        #self.screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        if self.x[0] - SIZE > 1000:
            self.x[0] = 0
            self.direction = 'right'
        elif self.x[0] < 0:
            self.x[0] = 24 * SIZE
            self.direction = 'left'
        elif self.y[0] - SIZE > 800:
            self.y[0] = 0
            self.direction = 'down'
        elif self.y[0] < 0:
            self.y[0] = 19*SIZE
            self.direction = 'up'

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':

            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()


class Game:




    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.render_background()
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.sleep_time = .2
        self.level = 1

    def is_collission(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < (x2 + SIZE):
            if y1 >= y2 and y1 < (y2 + SIZE):
                return True
        return False


    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))
        pygame.display.flip()
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"SCORE: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))
    def display_level(self):
        font = pygame.font.SysFont('arial', 30)
        level = font.render(f"LEVEL: {self.level}", True, (255, 255, 255))
        self.surface.blit(level, (800, 40))
    def show_gameover(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"GAME OVER! Your SCORE is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play game again press ENTER. To EXIT press ESC", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def play_sound(self, s):
        sound = pygame.mixer.Sound(f"resources/{s}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.display_level()
        pygame.display.flip()

        if self.is_collission(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.apple.move()
            pygame.display.flip()
            self.snake.increase_length()
        for i in range(3,self.snake.length - 1):
            if self.is_collission(self.snake.x[0], self.snake.y[0],self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"
                self.show_gameover()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.sleep_time = .2
        self.level = 1


    def run(self):
        running = True
        pause = False


        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        self.play_background_music()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_gameover()
                pygame.mixer.music.pause()
                pause = True
                self.reset()

            if self.snake.length == 10:
                self.sleep_time = .1
                self.level = 2
            time.sleep(self.sleep_time)


if __name__=="__main__":

    game = Game()
    game.run()
