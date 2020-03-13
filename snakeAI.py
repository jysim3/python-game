import random 
import sys
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import numpy as np
from snake import Snake 


print(tf.__version__)
class SnakeAI():
    def __init__(self, action_dim):
        self.action_dim = action_dim
        self.size = (15,15)
        self.state_dim = len(Snake(self.size).state())

        model = Sequential([
            #Dense(5,input_dim=self.state_dim),
            #Dense(self.action_dim),
            Dense(self.action_dim,input_dim=self.state_dim),
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001), 
                        loss=tf.keras.losses.MSE)
        model.summary()
        self.model = model
        self.batch_size = 20
        self.epsilon = 1
        self.epsilon_decay = 1.0005
        self.memory = []
        self.n_games = 200000
        self.n_frames = 10
        #self.q = np.zeros((*self.size,*self.size,self.action_dim,self.action_dim), dtype=float)
    def explore(self, state, r=True, verbose = False):
        #state = np.array([state])
        state = np.reshape(state, [1,self.state_dim])
        Q_estimates = self.model.predict(state)
        # Q_estimates = [self.q[ (*state), ]]
        d = ["U","D","R","L"]
        if verbose:
            print(f"{d[np.argmax(Q_estimates)]} {state}")
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
        self.memory.append((state,direction,reward,next_state))

        if len(self.memory) < self.batch_size:
            return 
        elif len(self.memory) > 5000:
            self.memory.pop(0)
        batch = np.array(random.sample(self.memory,self.batch_size))
        state = list(batch[:,0])
        state = np.array(state,np.int32)
        direction = list(batch[:,1])
        reward = batch[:,2]
        next_state = batch[:,3]
        next_state = self.model.predict(np.array(list(next_state)))
        next_reward = np.argmax(next_state,axis=1)
        reward += 0.8 * next_reward


        target_f = self.model.predict(state)
        target_f[np.arange(self.batch_size),np.array(direction)] = reward
        self.model.fit(state, target_f, epochs=1, verbose=0)
        self.epsilon /= self.epsilon_decay
        self.epsilon = max(self.epsilon, 0.05)
    def run(self):
        max_score = 0
        max_size = 0
        scores = [0]
        try:
            for n_game in range(self.n_games):
                snake = Snake(self.size)    
                for j in range(self.n_frames):
                    state = snake.state()
                    direction, prediction = self.explore(state)
                    snake.change_direction(direction+273)
                    m = snake.move()

                    if m:
                        reward = snake.score()

                    else:
                        reward = -3

                    next_state = snake.state()


                    self.train_batch(state,direction,reward, next_state)



                    if not m:
                        scores.append(snake.total_score())
                        scores = scores[-10:]
                        break
                max_score = max(max_score, snake.total_score())
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
        self.model.save('snakeModel.h5')
    def show(self):
        from snakeInterface import Game 
        g = Game(self.size)
        get_action = lambda x: self.explore(x.state(),False, verbose=True)[0]
        g.run(0.5,1,get_action)
    def load(self):
        self.model.load_weights('snakeModel.h5')
        self.epsilon = .62515




if __name__ == "__main__":
    s = SnakeAI(action_dim=4)
    s.load()
    #s.run()
    s.show()
        
