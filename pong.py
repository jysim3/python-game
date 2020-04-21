import math, random
UP, STATIONARY, DOWN = -5, 0, 5
BALL_X_V, BALL_Y_V = 1, 1


class Pong():
    def __init__(self, size, pole_size = (1,10)):
        width, height = size
        pole_size = (1,height//5)
        self.width = width
        self.height = height
        self.player1 = self.PongPlayer(5, height//5, pole_size[1], height)
        self.player2 = self.PongPlayer(width-5,height//5, pole_size[1], height)
        self.ball = self.Ball(11, random.randint(0,height))
        self.total_score = 0

    def player1_state(self):
        x, y, _, pole_height = self.player1.info()
        ball_x, ball_y, _, _ = self.ball.info()
        v_x, v_y = self.ball.angle

        higher = 0 if ball_y - y >= 0 else 1
        lower = 0 if y - ball_y + pole_height >= 0 else 1
        x_dist = ball_x - x

        return [higher, lower, x_dist, v_y]

    def player2_state(self):
        x, y, _, pole_height = self.player2.info()
        ball_x, ball_y, _, _ = self.ball.info()
        v_x, v_y = self.ball.angle

        higher = 1 if ball_y - y - 1 > 0 else 0
        lower = 1 if y - ball_y + pole_height - 1 > 0 else 0
        x_dist = -ball_x + x


        return [higher, lower, x_dist, v_y]

    def player2_change_dir(self, dir):
        if dir < 0:
            self.player2_up()
        if dir > 0:
            self.player2_down()
    def player1_change_dir(self, dir):
        if dir < 0:
            self.player1_up()
        if dir > 0:
            self.player1_down()

    def player1_reward(self):
        return self.player1_bounce
    def player2_reward(self):
        return self.player2_bounce

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
        ball_move = self.ball.tick(0, self.height)
        p1_move = self.player1.move()
        p2_move = self.player2.move()
        self.update = [ball_move,p1_move,p2_move]

        self.player2_bounce = self.ball.check_and_bounce(self.player2.x, self.player2.y,self.player2.height)
        self.player1_bounce = self.ball.check_and_bounce(self.player1.x, self.player1.y,self.player1.height)
        if self.player2_bounce > 0 or self.player1_bounce > 0:
            self.total_score += 1

        return 0 <= self.ball.x < self.width



    class Ball() :
        def __init__(self, x, y, v=5):
            self.x = x
            self.y = y
            self.angle = [BALL_X_V,BALL_Y_V]
        def check_and_bounce(self,x, y, height):
            if self.x == x:
                if 0 <= self.y - y < height//2:
                    self.angle[0] *= -1
                    self.angle[1] = BALL_Y_V
                    return 1000
                if height//2 <= self.y - y < height:
                    self.angle[0] *= -1
                    self.angle[1] = -BALL_Y_V
                    return 1000
                return -1000
            return 0

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
            self.height = height
            self.direction = STATIONARY
        def set_direction(self, direction):
            self.direction = direction 
        def info(self):
            return self.x, self.y, 1, self.height
        def move(self):
            update = STATIONARY
            if 0 <= self.y + self.direction and self.y + self.direction + self.height <= self.screen_height:
                self.y += self.direction
                update = self.direction
            self.direction = STATIONARY
            return (0, update)