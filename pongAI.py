import random 
import sys
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
from pong import Pong
from windowsInhibitor import WindowsInhibitor as wi
from collections import deque


print(tf.__version__)
class PongAI():
    def __init__(self, action_dim):
        self.action_dim = action_dim
        self.size = (60, 40)
        self.state_dim = len(Pong(self.size).player1_state())

        model = Sequential([
            #Dense(self.action_dim),
            Dense(5,activation='relu',input_dim=self.state_dim),
            Dense(self.action_dim),
            # Dense(self.action_dim, input_dim = self.state_dim),
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), 
                        loss=tf.keras.losses.MSE)
        model.summary()
        self.model = model
        self.batch_size = 50
        self.stored_batch = 2000
        self.epsilon = 1
        self.epsilon_decay = 1.0005
        self.memory = deque()
        self.n_games = 300
        self.n_frames = 300
        self.model_name = 'ponglayer.h5'
        #self.q = np.zeros((*self.size,*self.size,self.action_dim,self.action_dim), dtype=float)
    def explore(self, state, r=True, verbose = False):
        #state = np.array([state])
        state = np.reshape(state, [1,self.state_dim])
        Q_estimates = self.model.predict(state)
        # Q_estimates = [self.q[ (*state), ]]
        d = ["U","N","D"]
        if r and random.random() < self.epsilon:
            '''
            explore
            '''
            action = random.randint(0,  self.action_dim - 1)
        else:
            '''
            select action
            '''
            action = np.argmax(Q_estimates)
        if verbose:
            print(f"{state} {Q_estimates} {d[action]}")
        return action, Q_estimates

    def add_memory(self,state,direction,reward, next_state):
        state = list(state)
        next_state = list(next_state)
        if reward != 0:
            self.memory.append([state,direction,reward,next_state])
        else:
            self.memory.appendleft([state,direction,reward,next_state])


    def train_batch(self, state=None, direction=None, reward=None, next_state=None):

        if len(self.memory) < self.batch_size:
            return 
        elif len(self.memory) > self.stored_batch:
            self.memory.popleft()
        batch = random.sample(self.memory,self.batch_size)
        batch = list(zip(*batch))
        state, direction, reward, next_state = batch
        next_state = self.model.predict(next_state)
        next_reward = np.argmax(next_state,axis=1)
        reward += 0.9 * next_reward

        target_f = self.model.predict(state)
        target_f[np.arange(self.batch_size),np.array(direction)] = reward

        self.model.fit(np.array(state), target_f, epochs=1, verbose=0)
        self.epsilon /= self.epsilon_decay
        self.epsilon = max(self.epsilon, 0.05)
    def run(self):
        max_score = 0
        max_size = 0
        scores = [0]
        osSleep = wi()
        try:
            osSleep.inhibit()
            for n_game in range(self.n_games):
                pong = Pong(self.size)    
                for j in range(self.n_frames):
                    # PLAYER 1
                    state1 = pong.player1_state()
                    direction1, prediction1 = self.explore(state1)
                    pong.player1_change_dir(direction1-1)
                    # PLAYER 1
                    state2 = pong.player2_state()
                    direction2, prediction2 = self.explore(state2)
                    pong.player2_change_dir(direction2-1)


                    m = pong.tick()

                    reward1 = pong.player1_reward()
                    next_state1 = pong.player1_state()
                    self.add_memory(state1,direction1,reward1, next_state1)


                    next_state2 = pong.player2_state()
                    reward2 = pong.player2_reward()
                    self.add_memory(state2,direction2,reward2, next_state2)


                    self.train_batch()
                    if not m:
                        scores.append(pong.total_score)
                        if len(scores) > 10:
                            scores.pop()
                        break
                    max_score = max(max_score,*scores)
                    sys.stdout.write(f"\r"
                                f"r: {n_game:6} "
                                f"r: {sum(scores)/len(scores):6} "
                                f"ball : {pong.ball.info()}"
                                f"state : {pong.player2_state()}"
                                f"player1: {pong.player2.info()}"
                                f'direction : {["U  ", " N ", "  D"][direction2]}'
                                f"epsilon: {self.epsilon:.5f}, max: {max_score}")
                    sys.stdout.flush()
                if n_game % 5000 == 0 and n_game != 0:
                    total_reward = 0
                    for x in range(10):
                        snake = Pong(self.size)    
                        reward = 0
                        for y in range(self.n_frames):
                            # PLAYER 1
                            state1 = pong.player1_state()
                            direction1, prediction1 = self.explore(state1)
                            # PLAYER 1
                            state2 = pong.player2_state()
                            direction2, prediction2 = self.explore(state2)

                            pong.player1_change_dir(direction1-1)
                            pong.player2_change_dir(direction2-1)

                            if not pong.tick():
                                reward = max(reward, pong.total_score)
                                break
                        total_reward += reward
                    print(f' ave: {total_reward/10}')


            #break
        except KeyboardInterrupt:
            pass
        osSleep.uninhibit()
        if input("Save? (y/n)") != "n":
            self.model.save(self.model_name)
    def show(self):
        from pongInterface import Game 
        g = Game([ x *10 for x in self.size])
        get_action = lambda x: self.explore(x, False, verbose=True)[0]
        g.run(1,get_action=get_action)
    def load(self):
        self.model.load_weights(self.model_name)
        self.epsilon = .62515




if __name__ == "__main__":
    s = PongAI(action_dim=3)
    if input("Load? (y/n)") != "n":
        s.load()
    s.run()
    s.show()
        
