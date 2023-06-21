import numpy as np
import random
import time
from AIC_Project2.Server_Source_Code.gameRule import checkMoveValidation, end_game_check, checkRemainMove, initialMap, play, Next_Node

from MCTS import MCTS
from AICHw.gamerule import AIGame
from AICHw.NNet import NNetWrapper as nn
from utils import *
from MyCode0405_ import Getstep as mcts_
from a109550165 import Getstep as minmax

'''
    input position (x,y) and direction
    output next node position on this direction

    輪到此程式移動棋子
    mapStat : 棋盤狀態(list of list), 為 12*12矩陣, 0=可移動區域, -1=障礙, 1~2為玩家1~2佔領區域
    gameStat : 棋盤歷史順序
    return Step
    Step : 3 elements, [(x,y), l, dir]
            x, y 表示要畫線起始座標
            l = 線條長度(1~3)
            dir = 方向(1~6),對應方向如下圖所示
              1  2
            3  x  4
              5  6
'''

def randomstep(mapStat, Stat):
    #please write your code here
    Step = checkRemainMove(mapStat)
    steps = random.choice(Step)
    temp_steps = steps
    legel_dir = [1, 2, 3, 4, 5, 6]
    legel_distance = [1]
    dir_choice = random.choice(legel_dir)
    next_x,next_y = temp_steps[0],temp_steps[1]
    for i in range(2,4):
        [next_x,next_y] = Next_Node(next_x,next_y,dir_choice)
        if(next_x >= 0 and next_x < 12 and next_y >= 0 and next_y < 12 and mapStat[next_x][next_y]==0):
            legel_distance.append(i)
        else:
            break
    dictance_choice = random.choice(legel_distance)
    return [steps,dictance_choice,dir_choice]
    #please write your code here

args = dotdict({
    'numIters': 100,
    'numEps': 50,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.55,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 125,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 2,

    'checkpoint': './temp/',
    'load_model': True,
    'load_folder_file': ('./temp/','best_2.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

#game = AIGame(33)
#nnet = nn(game)
#nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
#nmcts = MCTS(game, args)

class Agent:
    def __init__(self, game, mcts):
        self.game = game
        self.mcts = mcts

    def Getstep(self, mapStat, gameStat):
        #Please write your code here
        action = np.argmax(self.mcts.getActionProb(mapStat, temp=0))
        idx = 0
        for x in range(12):
            for y in range(12):
                if mapStat[x][y] == -1:
                    continue
                pos = [x,y]
                act = [pos ,1, 1]
                if idx == action:
                    move = act
                idx += 1
                for l in range(2, 4):
                    for dir in range(1, 7):
                        act = [pos, l, dir]
                        if idx == action:
                            move = act
                        idx += 1
        return move
    #Please write your code here

# start game

print('start game')
matches = 20
a1 = 0
a2 = 0
for i in range(matches):
    print("Running match {}...".format(i+1))
    node_num = random.randint(13, 33)
    seed = random.randint(0, 1000)
    board, Stat = initialMap(node_num, seed)
    episode = 0
    a = Agent(game=AIGame(node_num), mcts=MCTS(AIGame(node_num), args))
    player = [a.Getstep, mcts_]
    while not end_game_check(board):
        #print("Episode:{}".format(episode))
        st_time = time.time()
        act = player[episode%2](board, Stat)
        ed_time = time.time()
        print(episode%2, act)
        print("cost {} sec".format(ed_time-st_time))
        #print(board)
        board, Stat= play(episode%2+1, board, Stat, act, 0)
        episode+=1
    if episode%2 == 0:
        a1+=1
    else:
        a2+=1
    print(a1, a2)
for i in range(matches):
    print("Running match {}...".format(i+1))
    node_num = random.randint(13, 33)
    seed = random.randint(0, 1000)
    board, Stat = initialMap(node_num, seed)
    episode = 0
    a = Agent(game=AIGame(node_num), mcts=MCTS(AIGame(node_num), args))
    player = [mcts_, a.Getstep]
    while not end_game_check(board):
        #print("Episode:{}".format(episode))
        st_time = time.time()
        act = player[episode%2](board, Stat)
        ed_time = time.time()
        print(episode%2, act)
        print("cost {} sec".format(ed_time-st_time))
        #print(board)
        board, Stat= play(episode%2+1, board, Stat, act, 0)
        episode+=1
    if episode%2 == 0:
        a2+=1
    else:
        a1+=1
    print(a1, a2)
