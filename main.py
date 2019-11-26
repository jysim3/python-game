import sys, pygame
from time import sleep
from random import randrange
LEFT, RIGHT, UP, DOWN = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN

class Game:
    def __init__(self, size):
        self.r_size, self.c_size = size
        self.row, self.col = (self.r_size//2, self.c_size//2)
        self.direction = pygame.K_LEFT
        self.moves = [(self.r_size//2, self.c_size//2)]
        self.new_food()
    def new_food(self):
        r = randrange(self.r_size)
        c = randrange(self.c_size)
        while (r,c) in self.moves:
            r = randrange(self.r_size)
            c = randrange(self.c_size)
        self.food = (r,c)
    def eat(self):
        self.new_food()
    def new_move(self):
        return self.moves[-1]
    def change_direction(self, direction):
        if self.direction in [LEFT, RIGHT] and direction in [LEFT, RIGHT]:
            return
        if self.direction in [UP, DOWN] and direction in [UP, DOWN]:
            return
        if direction in [LEFT, RIGHT, UP, DOWN]:
            self.direction = direction
    def move(self):
        result = False
        if self.direction == LEFT:
            result = self.move_left()
        elif self.direction == RIGHT:
            result = self.move_right()
        elif self.direction == UP:
            result = self.move_up()
        elif self.direction == DOWN:
            result = self.move_down()
        if (self.row, self.col) == self.food:
            self.eat()
        else:
            self.last_move = self.moves.pop(0)
        if (self.row, self.col) in self.moves:
            return False
        self.moves.append((self.row,self.col))
        return result
    def move_left(self):
        if self.row != 0:
            self.row -= 1
            return True
    def move_right(self):
        if self.row != self.r_size - 1:
            self.row += 1
            return True
    def move_up(self):
        if self.col != 0:
            self.col -= 1
            return True
    def move_down(self):
        if self.col != self.c_size - 1:
            self.col += 1
            return True
def main():
    screen_size = (700, 700)
    game_size = 30,30
    speed = .05
    inactive = [0,0,0]
    snake = [255,0,0]
    food = [0,255,0]
    border = 0


    def init():
        screen = pygame.display.set_mode(screen_size)
        game = Game(game_size)
        boxes = [[None for x in range(game_size[0])] for y in range(game_size[1])]
        screen.fill([0,0,0])
        for i in range(game_size[0]):
            for j in range(game_size[1]):
                coor = screen_size[0]/game_size[0] * i + border, screen_size[1]/game_size[1] * j  + border
                boxes[i][j] = pygame.Rect(coor, (screen_size[0]/game_size[0] - border*2, screen_size[1]/game_size[1] - border*2))
                screen.fill(inactive, boxes[i][j])
        return game, boxes, screen
    game, boxes, screen = init()



    while 1:
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                game.change_direction(event.key)
        if not game.move():
            game, boxes, screen = init()
            continue
        i,j = game.last_move
        screen.fill(inactive, boxes[i][j])
        i,j = game.food
        screen.fill(food, boxes[i][j])

        i,j = game.new_move()
        screen.fill(snake, boxes[i][j])
        pygame.display.flip()
        sleep(speed)

if __name__=="__main__":
    main()
