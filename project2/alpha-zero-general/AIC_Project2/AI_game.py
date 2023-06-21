# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:07 2023

@author: LAB639
"""
import copy
import STcpServer
import gameUI
import os, time
import numpy as np
import random
from gameRule import checkMoveValidation, end_game_check, checkRemainMove, Getstep
from gameRule import initialMap, play

def battle(teamID, node_num, seed):
    '''

    :param teamID: 2 teams in this game
    :return:
    '''

    initMapStat, initGameStat = initialMap(node_num, seed)

    map_current = copy.deepcopy(initMapStat)
    game_current = copy.deepcopy(initGameStat)

    count_dis = [0, 0]  # to save whether disconnect
    for i in range(2):
        print(f'player {i + 1} = team {teamID[i]}')

    print("\n----------START GAME----------\n")

    replay = []
    action_record = {}
    action_record['text'] = '(initial state)'
    action_record['map'] = initMapStat
    action_record['game'] = initGameStat
    replay.append(action_record)

    # record for UI
    action_record['movement'] = None
    action_record['map'] = map_current
    action_record['game'] = game_current

    replay.append(action_record)

    # start game
    print('initial success.\n')
    

    print("\n----------while----------\n")
    
    item = -1
    step = 0
    lose_player = 0
    while not end_game_check(map_current):
        action_record = {}
        action_record['text'] = ''
        item = (item + 1) % 2
        player = item + 1
        (connect, movement) = STcpServer.SendBoard(item, map_current, game_current)
        print(f"player {player}:", movement)
        if connect == 1:
            # time out
            print(f"player {player} no response.")
            action_record['text'] = action_record['text'] + "player " + str(player) + " no response.\n\n"
            movement = Getstep(map_current)
            step += 1
            t_mapStat, t_gameStat = play(player, map_current, game_current, movement, step)
            map_current = copy.deepcopy(t_mapStat)
            game_current = copy.deepcopy(t_gameStat)
            
        elif connect == 2:
            count_dis[item] += 1
            print(f"player {player} disconnected.")
            action_record['text'] = action_record['text'] + "player " + str(player) + " disconnected.\n\n"
        else:
            print('movement: {}\n'.format(movement))
            print(f"map\n", map_current.T)
            action_record['text'] = action_record['text'] + 'movement: ' + str(movement) + '\n\n'

            legality_tag = checkMoveValidation(player, map_current, movement)
            if not legality_tag:
                print(f"player {player}: movement illegal.")
                action_record['text'] = action_record['text'] + "player " + str(player) + " : movement illegal.\n"
                lose_player = player
            else:
                # move player
                step += 1
                t_mapStat, t_gameStat = play(player, map_current, game_current, movement, step)
                map_current = copy.deepcopy(t_mapStat)
                game_current = copy.deepcopy(t_gameStat)
            #vaild, map_current, move = play(player, map_current, map_current, move)
        time.sleep(0.1)
        
        action_record['movement'] = movement
        action_record['map'] = map_current
        action_record['game'] = game_current
        replay.append(action_record)
        #print(action_record)
        if lose_player: break

    print("\n----------END GAME----------\n")

    for item in range(2):
        STcpServer.SendBoard(item, map_current, game_current, gameFlag=0)

    if not lose_player:
        z = np.where(game_current==np.max(game_current))
        x = z[0][0]
        y = z[1][0]
        lose_player = map_current[x][y]

    winner = (lose_player % 2) + 1

    UI = gameUI.gameUI(replay, initMapStat, initGameStat, teamID, winner, node_num, seed)

    # UI.show_result(replay)
    UI.window.mainloop()  # 運行視窗程式

    return


def main():
    teams = [0, 0]
    path = ['', '']

    # use cmd input
    '''for i in range(2):
        teamID = input(f'input Team{i + 1} team number(int): ')
        teams[i] = int(teamID)
        path[i] = input(f'input Path to Team{i + 1}exe(example: C:\\yourpath\\Team_number.exe): ')'''

    # use input.txt
    with open('input.txt', 'r') as file:
        lines = file.readlines()

    for l in range(2):
        i=l*2
        teams[l] = int(lines[i])
        path[l] =lines[i+1][:-1]
    node_num = int(lines[4]) + 1
    seed = int(lines[5])

    if (node_num - 1) == 0:
        node_num = random.randint(13,34)
    if seed == 0:
        seed = random.randint(1,1001)

    print(teams)
    print(path)
    print(node_num - 1)
    print(seed)

    (success, failId) = STcpServer.StartMatch(teams, path)

    if (not success):
        print("connection fail, teamId:", failId)
    else:
        battle(teams, node_num, seed)

    STcpServer.StopMatch()


if __name__ == "__main__":
    main()
    os.system('pause')




