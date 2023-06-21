from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import numpy as np
from AICHw.gamelogic import *

class AIGame(Game):
    '''
    mapStat: border=-1, free field=0, player_occupied=player_number(1~2)
    gameStat: sheepStat
    playerStat: position of player
    '''
    def __init__(self, node_num):
        self.idx_action_pair = {}
        self.node_num = node_num

    def getInitBoard(self):
        # return initial board (numpy board)
        seed = random.randint(1, 1000)
        n = random.randint(13, 33)
        board = initialMap(node_num=n, seed=seed)
        return np.array(board)

    def getBoardSize(self):
        # (a,b) tuple
        return (12, 12)

    def getActionSize(self):
        # return number of actions
        return 33 * (6 * 2 + 1)

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        idx = 0
        for x in range(12):
            for y in range(12):
                if board[x][y] == -1:
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
        new_board = play(player=(1 if player == 1 else 2), mapStat=board, move = move)
        return (new_board, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valid_move = [0]*self.getActionSize()
        idx = 0
        for x in range(12):
            for y in range(12):
                if board[x][y] == -1:
                    continue
                pos = [x,y]
                act = [pos ,1, 1]
                if checkMoveValidation(player=player, mapStat=board, move=act):
                    valid_move[idx] = 1            
                idx += 1
                for l in range(2, 4):
                    for dir in range(1, 7):
                        act = [pos, l, dir]
                        if checkMoveValidation(player=player, mapStat=board, move=act):
                            valid_move[idx] = 1
                        idx += 1
        return np.array(valid_move)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        if not (board == 0).any():
            if player == 1:
                return 1
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        b = np.copy(board)
        if player == -1:
            for i in range(12):
                for j in range(12):
                    if b[i][j] == 1:
                        b[i][j] = 2
                    elif b[i][j] == 2:
                        b[i][j] = 1
        return board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.getActionSize(board))  # 1 for pass
        #pi_board = np.reshape(pi, (12, 12, 13))
        l = [(board, pi)]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(square for row in board for square in row)
        return board_s