import sys, pygame
import numpy as np
from time import sleep
from pong import Pong
LEFT, RIGHT, UP, DOWN = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN
W, A, S, D = pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d
QUIT, KEYDOWN = pygame.QUIT, pygame.KEYDOWN
class Game():
    def __init__(self, screen_size):

        self.player_color = [255,255,255]
        self.screen_size = (screen_size)
        self.game_size = (x//10 for x in self.screen_size)
        self.speed = .01

        self.inactive = [0,0,0]
        self.border = 0

        screen = pygame.display.set_mode(self.screen_size)
        game = Pong(self.game_size)
        screen.fill([0,0,0])

        x, y, height, width = game.ball.info()
        ball = pygame.Rect(x*10,y*10,height*10,width*10)
        screen.fill(self.player_color, ball)

        x, y, height, width = game.player1.info()
        player1 = pygame.Rect(x*10,y*10,height*10,width*10)
        screen.fill(self.player_color, player1)

        x, y, height, width = game.player2.info()
        player2 = pygame.Rect(x*10,y*10,height*10,width*10)
        screen.fill(self.player_color, player2)

        self.game = game
        self.ball = ball
        self.player1 = player1
        self.player2 = player2
        self.screen = screen
    def run(self, n_life=5, get_action=None, Ai=None):

        while n_life > 0:
            pygame.init()
            actions = pygame.event.get()
            for event in actions:
                if event.type == QUIT:
                    sys.exit()
            if get_action:
                action = get_action(self.game.player1_state())
                self.game.player1_change_dir(action-1)
                action = get_action(self.game.player2_state())
                self.game.player2_change_dir(action-1)
            else:
                keys = pygame.key.get_pressed()
                if keys[W]:
                    self.game.player2_up()
                if keys[S]:
                    self.game.player2_down()
                if keys[UP]:
                    self.game.player1_up()
                if keys[DOWN]:
                    self.game.player1_down()

            state2 = self.game.player2_state()


            if not self.game.tick():
                self.__init__(self.screen_size)
                n_life -= 1
                continue
            reward2 = self.game.player2_reward()
            next_state2 = self.game.player2_state()
            print(self.game.ball.info())

            ball_update, p1_update, p2_update = self.game.info()

            
            self.ball.move_ip(*[x*10 for x in ball_update])
            self.player1.move_ip(*[x*10 for x in p1_update])
            self.player2.move_ip(*[x*10 for x in p2_update])

            self.screen.fill([0,0,0])
            pygame.draw.rect(self.screen, (128,128,128), self.player1, 0)
            pygame.draw.rect(self.screen, (128,128,128), self.ball, 0)
            pygame.draw.rect(self.screen, (128,128,128), self.player2, 0)


            pygame.display.flip()

            sys.stdout.flush()
            sleep(self.speed)

if __name__=="__main__":
    g = Game((400, 200))
    g.run()
