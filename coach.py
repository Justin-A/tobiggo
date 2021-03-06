import numpy as np
from mcts import mcts
from tqdm import trange


class coaching():
    def __init__(self, game, nnet, mcts1):
        self.game = game
        self.nnet = nnet
        self.mcts = mcts1
        self.prints = False

    def executeepisode(self):
        trainexample = []
        board = self.game.startphan()
        new_board = self.game.dim_board()
        self.curplayer = 1
        episodestep = 0

        while True:
            episodestep += 1
            oneminusone = self.game.oneminusone(board, self.curplayer)
            pi = self.mcts.getactionprob(oneminusone, new_board)
            sym = self.game.symme(new_board, pi)
            for b, p in sym:
                trainexample.append([b, self.curplayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            board, self.curplayer, new_board = self.game.nextstate(board, new_board, self.curplayer, action)
            if self.prints == True:
                print("episode :", episodestep, "\n", board)
            r = self.game.ggeutnam(board, self.curplayer)

            if r != 0:
                return [(x[0], x[2], r * ((-1) ** (x[1] != self.curplayer))) for x in trainexample]

    def learn(self):

        for iter in range(10000):
            print("iter : ",iter+1)
            iterationtrainexample = []
            finalexample = []
            self.prints = False
            if iter % 30:
                self.nnet.saving("~/", "model1.ckpt")
            try:
                for i in trange(1):
                    self.prints = False
                    #print("game:", i)
                    if iter % 10 == 9 and i == 49:
                        self.prints = True
                    iterationtrainexample += self.executeepisode()
                for e in iterationtrainexample:
                    finalexample.append(e)
                self.nnet.train(finalexample)
                self.mcts = mcts(self.game, self.nnet)

            except Exception as err:
                print(err)
                self.nnet.saving("~/", "model_err.ckpt")

        self.nnet.saving("~/", "model1.ckpt")








