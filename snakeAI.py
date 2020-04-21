import random 
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
from snake import Snake 
from windowsInhibitor import WindowsInhibitor as wi


print(tf.__version__)
class SnakeAI():
    def __init__(self, action_dim):
        self.action_dim = action_dim
        self.size = (30,30)
        self.state_dim = len(Snake(self.size).state())

        model = Sequential([
            #Dense(self.action_dim),
            Dense(5,input_dim=self.state_dim),
            Dense(self.action_dim),
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), 
                        loss=tf.keras.losses.MSE)
        model.summary()
        self.model = model
        self.batch_size = 500
        self.stored_batch = 2000
        self.epsilon = 1
        self.epsilon_decay = 1.0005
        self.memory = []
        self.n_games = 50
        self.n_frames = 1000
        self.model_name = 'snake2layers.h5'
        #self.q = np.zeros((*self.size,*self.size,self.action_dim,self.action_dim), dtype=float)
    def explore(self, state, r=False, verbose = False):
        #state = np.array([state])
        state = np.reshape(state, [1,self.state_dim])
        Q_estimates = self.model.predict(state)
        # Q_estimates = [self.q[ (*state), ]]
        d = ["U","D","R","L"]
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
            print(f"{state} {d[action]} {Q_estimates}")
        return action, Q_estimates
    def train_one(self,state,direction,reward, next_state):
        # a,b,c,d = self.q[(*state),]
        _, next_r = self.explore(next_state,False)
        reward += 0.8 * np.amax(next_r)

        _, target_f = self.explore(state,False)
        target_f[0][direction] = reward
        state = np.reshape(state, [1,self.state_dim])
        self.model.fit(state, target_f, epochs=1, verbose=0)

        # self.q[(*state),direction] = reward
    def train_batch(self,state,direction,reward, next_state):
        state = list(state)
        next_state = list(next_state)
        self.memory.append([state,direction,reward,next_state])

        if len(self.memory) < self.batch_size:
            return 
        elif len(self.memory) > self.stored_batch:
            self.memory.pop(0)
        batch = random.sample(self.memory,self.batch_size)
        batch = list(zip(*batch))
        state, direction, reward, next_state = batch


        next_state = self.model.predict(next_state)
        next_reward = np.argmax(next_state,axis=1)
        reward += 0.8 * next_reward


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
                snake = Snake(self.size)    
                for _ in range(self.n_frames):
                    state = snake.state()
                    direction, prediction = self.explore(state)
                    snake.change_direction(direction+273)
                    m = snake.move()

                    reward = snake.score()


                    next_state = snake.state()


                    self.train_batch(state,direction,reward, next_state)



                    max_score = max(max_score, snake.total_score())
                    if not m:
                        scores.append(snake.total_score())
                        scores = scores[-10:]
                        break
                    sys.stdout.write(f"\rr: {n_game:6} "
                                f"size: {sum(scores)/len(scores)}"
                                f"score: {snake.total_score():3} "
                                f'chose:{["U   ", " D  ", "  R ", "   L"][direction]:5} '
                                f"epsilon: {self.epsilon:.5f}, max: {max_score}")
                    sys.stdout.flush()
                if n_game % 5000 == 0 and n_game != 0:
                    total_reward = 0
                    for x in range(10):
                        snake = Snake(self.size)    
                        reward = 0
                        for y in range(self.n_frames):
                            state = snake.state()
                            direction, prediction = self.explore(state, False)
                            snake.change_direction(direction+273)
                            reward = snake.total_score()
                            if not snake.move():
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
        from snakeInterface import Game 
        g = Game(self.size)
        get_action = lambda x: self.explore(x.state(), 0, verbose=False)[0]
        g.run(0,5,get_action)
    def load(self):
        self.model.load_weights(self.model_name)
        self.epsilon = .62515




if __name__ == "__main__":
    s = SnakeAI(action_dim=4)
    if input("Load? (y/n)") != "n":
        s.load()
    s.run()
    s.show()
        
