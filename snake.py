from random import randrange

LEFT, RIGHT, UP, DOWN = 276, 275, 273, 274
QUIT, KEYDOWN = 12, 2
class Snake:
    def __init__(self, size):
        self.r_size, self.c_size = size
        self.row, self.col = (self.r_size//2, self.c_size//2)
        self.direction = LEFT
        self.last_move = 0,0
        self.moves = [(self.r_size//2, self.c_size//2)]
        self.history = (self.r_size//2+1, self.c_size//2)
        self.new_food()
        self.just_ate = False
        self.life = 0
        self._total_score = 0
        self.move()
        self.moves = [(self.r_size//2, self.c_size//2)] + self.moves
    def state(self):
        move = [0,0,0,0]
        move[self.direction - 273] = 1
        danger = [0,0,0,0]
        if self.moves[-1][0] == 0:
            danger[0] = 1
        if self.moves[-1][1] == 0:
            danger[1] = 1
        if self.moves[-1][0] == self.r_size-1:
            danger[2] = 1
        if self.moves[-1][1] == self.c_size-1:
            danger[3] = 1

        food = [0,0,0,0]
        if self.food[0] > self.moves[-1][0]:
            food[0] = 1
        if self.food[0] < self.moves[-1][0]:
            food[1] = 1
        if self.food[1] > self.moves[-1][1]:
            food[2] = 1
        if self.food[1] < self.moves[-1][1]:
            food[3] = 1
        return (*move, *danger, *food)
    def score(self):
        if self.just_ate:
            return self.r_size * self.c_size 
        else:
            return 0
    def total_score(self):
        return self._total_score
    def new_food(self):
        r = randrange(self.r_size)
        c = randrange(self.c_size)
        while (r,c) in self.moves:
            r = randrange(self.r_size)
            c = randrange(self.c_size)
        self.food = (r,c)
    def eat(self):
        self._total_score += 1
        self.just_ate = True
        self.new_food()
    def new_move(self):
        return self.moves[-1]
    def change_direction(self, direction):
        if direction in [LEFT, RIGHT, UP, DOWN]:
            self.direction = direction
    def move(self):
        self.just_ate = False
        result = False
        self.life += 1
        self.history = self.row,self.col
        if self.direction == LEFT:
            result = self.move_left()
        elif self.direction == RIGHT:
            result = self.move_right()
        elif self.direction == UP:
            result = self.move_up()
        elif self.direction == DOWN:
            result = self.move_down()
        if (self.row, self.col) in self.moves:
            return False
        self.moves.append((self.row,self.col))
        # if len(self.moves) > 3:
        #     self.moves.pop(0)
        if (self.row, self.col) == self.food:
            self.eat()
        else:
            self.last_move = self.moves.pop(0)
        #self.moves = [(self.row,self.col)]
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
