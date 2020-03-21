import math
UP, STATIONARY, DOWN = -1, 0, 1


class Pong():
    def __init__(self, size, pole_size = (1,10)):
        width, height = size
        self.width = width
        self.height = height
        self.player1 = self.PongPlayer(10, height//2, pole_size[1], height)
        self.player2 = self.PongPlayer(width-10,height//2, pole_size[1], height)
        self.ball = self.Ball(10, height//2)

    def player1_state(self):
        ball_dir = self.ball.angle
        x, y, _, pole_height = self.player1.info()
        ball_x, ball_y, _, _ = self.ball.info()
        x_distance = abs(ball_x - x)
        y_distance = ball_y - (y + pole_height) // 2
        return [ball_dir, x_distance, y_distance]

    def player2_state(self):
        ball_dir = -self.ball.angle
        x, y, _, pole_height = self.player1.info()
        ball_x, ball_y, _, _ = self.ball.info()
        x_distance = abs(ball_x - x)
        y_distance = ball_y - (y + pole_height) // 2
        return [ball_dir, x_distance, y_distance]


    def player2_up(self):
        self.player2.set_direction(UP)
    def player2_down(self):
        self.player2.set_direction(DOWN)
    def player1_up(self):
        self.player1.set_direction(UP)
    def player1_down(self):
        self.player1.set_direction(DOWN)

    def info(self):
        update = self.update
        self.update = []
        return update

    def tick(self):
        #self.ball.tick()
        self.ball.check_and_bounce(self.player2.x, self.player2.y,self.player2.height)
        self.ball.check_and_bounce(self.player1.x, self.player1.y,self.player1.height)
        ball_move = self.ball.tick(0, self.height)
        p1_move = self.player1.move()
        p2_move = self.player2.move()
        self.update = [ball_move,p1_move,p2_move]
        return 0 <= self.ball.x < self.width



    class Ball() :
        def __init__(self, x, y, v=5):
            self.x = x
            self.y = y
            self.angle = [UP,UP]
        def check_and_bounce(self,x, y, height):
            if self.x == x:
                if 0 <= self.y - y < height//2:
                    self.angle[0] *= -1
                    self.angle[1] = UP
                if height//2 <= self.y - y < height:
                    self.angle[0] *= -1
                    self.angle[1] = DOWN

        def tick(self, top, bottom):
            self.x += self.angle[0]
            if top >= self.y + self.angle[1] or self.y + self.angle[1] >= bottom:
                self.angle[1] *= -1
            self.y += self.angle[1]
            return self.angle
        def info(self):
            return self.x, self.y, 1, 1

    class PongPlayer():
        def __init__(self, x,y, height, screen_height = 100):
            self.x = x
            self.y = y
            self.screen_height = screen_height
            self.height = 10
            self.direction = STATIONARY
        def set_direction(self, direction):
            self.direction = direction 
        def info(self):
            return self.x, self.y, 1, self.height
        def move(self):
            m = STATIONARY
            if 0 < self.y + self.direction and self.y + self.direction + self.height < self.screen_height:
                self.y += self.direction
                m = self.direction
            self.direction = STATIONARY
            return (0, m)