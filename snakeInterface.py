import sys, pygame
import numpy as np
from time import sleep
from snake import Snake
from snakeAI import SnakeAI 
LEFT, RIGHT, UP, DOWN = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN
QUIT, KEYDOWN = pygame.QUIT, pygame.KEYDOWN
class Game():
    def __init__(self, game_size):
        screen_size = (700, 700)
        speed = .05
        inactive = [0,0,0]
        snake = [255,0,0]
        food = [0,255,0]
        border = 0
        self.screen_size = (700, 700)
        self.game_size = game_size
        self.speed = 1
        self.inactive = [0,0,0]
        self.snake = [255,0,0]
        self.food = [0,255,0]
        self.border = 0
        screen = pygame.display.set_mode(screen_size)
        game = Snake(game_size)
        boxes = [[None for x in range(game_size[0])] for y in range(game_size[1])]
        screen.fill([0,0,0])
        for i in range(game_size[0]):
            for j in range(game_size[1]):
                coor = screen_size[0]/game_size[0] * i + border, screen_size[1]/game_size[1] * j  + border
                boxes[i][j] = pygame.Rect(coor, (screen_size[0]/game_size[0] - border*2, screen_size[1]/game_size[1] - border*2))
                screen.fill(inactive, boxes[i][j])
        self.game = game
        self.boxes = boxes
        self.screen = screen
    def run(self, speed, n_life=50, get_action=None, Ai=None):
        if Ai:
            s = SnakeAI(4,4)
            s.load()
        while n_life > 0:
            pygame.init()
            actions = pygame.event.get()
            for event in actions:
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    self.game.change_direction(event.key)
            if get_action:
                d = get_action(self.game)
                self.game.change_direction(d+273)
            if not self.game.move():
                self.__init__(self.game_size)
                n_life -= 1
                continue
            renders = []
            i,j = self.game.last_move
            renders.append((self.inactive, self.boxes[i][j]))
            i,j = self.game.food
            renders.append((self.food, self.boxes[i][j]))
            i,j = self.game.new_move()
            renders.append((self.snake, self.boxes[i][j]))

            for r in renders:
                self.screen.fill(r[0], r[1])

            pygame.display.flip()
            if Ai:
                o = s.model.predict(np.array([[*self.game.food,*self.game.new_move()]]))
                print(f"{self.game.score()} {o}\n")
            sys.stdout.flush()
            sleep(speed)

if __name__=="__main__":
    g = Game((7,7))
    g.run(1)
