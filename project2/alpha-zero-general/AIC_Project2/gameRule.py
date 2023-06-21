import copy
import numpy as np
import random

'''
mapStat: border=-1, free field=0, player_occupied=player_number(1~2)
gameStat: sheepStat
playerStat: position of player
'''


def initialMap(node_num, seed):
    initGameStat = np.zeros((12, 12), dtype=np.int32)

    # create border
    temp_map = np.ones((14, 14), dtype=np.int32)
    temp_map[1:13, 1:13] = np.zeros([12, 12])

    while True:
        n_free = 0
        t = [[7, 7]]
        prob = 0.7
        random.seed(seed)
        seed += 1
        rand = random.random()
        if rand < prob:
            # as free
            n_free += 1
            temp_map[7][7] = -1
        else:
            n_free = 2
            temp_map[7][7] = 1

        while n_free < node_num:
            if len(t) == 0 & n_free != node_num:
                # recreate
                print("recreate")
                n_free = 0
                temp_map[1:13, 1:13] = np.zeros([12, 12])
                t = [[7, 7]]
                prob = 0.7
                random.seed(seed)
                seed += 1
                rand = random.random()
                if rand < prob:
                    # as free
                    n_free += 1
                    temp_map[7][7] = -1
                else:
                    temp_map[7][7] = 1
                continue
            random.seed(seed)
            seed += 1
            random.shuffle(t)
            x, y = t.pop()
            window = temp_map[x - 1:x + 2, y - 1:y + 2]

            neighbor = []
            # 3
            if window[0][1] == 0:
                neighbor.append([x - 1, y])
            # 4
            if window[2][1] == 0:
                neighbor.append([x + 1, y])

            if y % 2 == 1:
                # 1
                if window[0][0] == 0:
                    neighbor.append([x - 1, y - 1])

                # 2
                if window[1][0] == 0:
                    neighbor.append([x, y - 1])

                # 5
                if window[0][2] == 0:
                    neighbor.append([x - 1, y + 1])

                # 6
                if window[1][2] == 0:
                    neighbor.append([x, y + 1])

            elif y % 2 == 0:
                # 1
                if window[1][0] == 0:
                    neighbor.append([x, y - 1])
                # 2
                if window[2][0] == 0:
                    neighbor.append([x + 1, y - 1])

                # 5
                if window[1][2] == 0:
                    neighbor.append([x, y + 1])
                # 6
                if window[2][2] == 0:
                    neighbor.append([x + 1, y + 1])

            np.random.seed(seed)
            seed += 1
            rand = np.random.random(len(neighbor))
            rand = rand < prob

            for i in range(len(neighbor)):
                m, n = neighbor[i]
                if rand[i]:
                    # as free
                    n_free += 1
                    t.append([m, n])
                    temp_map[m][n] = 1
                else:
                    temp_map[m][n] = -1
                if n_free == node_num: break

        n_component, _, _ = getConnectRegion(1, temp_map[1:13, 1:13])
        if n_component != 1:
            # print('recreate because not 1-component')
            temp_map[1:13, 1:13] = np.zeros([12, 12])
        else:
            break

    # fill all hole
    temp_map[temp_map == 0] = -1

    initMapStat = temp_map[1:13, 1:13]
    initMapStat[initMapStat == 1] = 0

    return initMapStat, initGameStat


def getConnectRegion(targetLabel, mapStat):
    '''

    :param targetLabel:
    :param mapStat:
    :return: numbers of connect region, total occupied area, max connect region
    '''
    # turn into boolean array
    mask = mapStat == targetLabel
    n_field = np.count_nonzero(mask)

    # print(flagArr)

    n_components = 0
    # connection region

    ind = np.where(mask == 1)
    labels = np.zeros((14, 14), dtype=np.int32)
    for k in range(len(ind[0])):
        m, n = ind[0][k], ind[1][k]
        if labels[m + 1][n + 1] != 0:
            continue
        else:
            # haven't have mark
            l_window = labels[m:m + 3, n:n + 3]
            if (l_window == 0).all():
                n_components += 1
                labels[m + 1][n + 1] = n_components
            else:
                mark_pos = np.where(l_window != 0)
                neighbor = np.zeros(1, dtype=np.uint8)

                # connect region
                if n % 2 == 0:
                    for l in range(len(mark_pos[0])):
                        i, j = mark_pos[0][l], mark_pos[1][l]
                        if i == 0:
                            if j == 0:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 1:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 2:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue
                        elif i == 1:
                            if j == 0:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 2:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue
                        elif i == 2:
                            if j == 1:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue
                elif n % 2 == 1:
                    for l in range(len(mark_pos[0])):
                        i, j = mark_pos[0][l], mark_pos[1][l]
                        if i == 0:
                            if j == 1:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue
                        elif i == 1:
                            if j == 0:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 2:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue
                        elif i == 2:
                            if j == 0:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 1:
                                neighbor = np.append(neighbor, l_window[i][j])
                            elif j == 2:
                                neighbor = np.append(neighbor, l_window[i][j])
                            else:
                                continue

                neighbor = np.delete(neighbor, 0)
                # mark m,n as min class in the neighborhood
                if neighbor.size == 0:

                    n_components += 1
                    labels[m + 1][n + 1] = n_components
                else:
                    labels[m + 1][n + 1] = min(neighbor)
                    for i in np.unique(neighbor):
                        if i != min(neighbor):
                            # print(f'{i} -> {min(neighbor)}')
                            labels[labels == i] = min(neighbor)

    n_components = len(np.unique(labels)) - 1
    counts = []
    for k in np.unique(labels):
        if k == 0: continue
        c = np.count_nonzero(labels == k)
        counts = np.append(counts, c)
    return n_components, n_field, max(counts)
    
    
def play(player, mapStat, gameStat, move, step):
    new_mapStat = copy.deepcopy(mapStat)
    new_gameStat = copy.deepcopy(gameStat)

    [move_pos_x, move_pos_y] = move[0]  # expected [x,y]
    steps = move[1]  # how many step
    move_dir = move[2]  # 1~6

    next_x = move_pos_x
    next_y = move_pos_y
    new_mapStat[next_x][next_y] = player
    new_gameStat[next_x][next_y] = step
    for i in range(steps - 1): 
        [next_x, next_y]=Next_Node(next_x,next_y,move_dir)
        new_mapStat[next_x][next_y] = player
        new_gameStat[next_x][next_y] = step

    return new_mapStat, new_gameStat
    
    
def Next_Node(pos_x,pos_y,direction):
    if pos_y%2==1:
        if direction==1:
            return pos_x,pos_y-1
        elif direction==2:
            return pos_x+1,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x,pos_y+1
        elif direction==6:
            return pos_x+1,pos_y+1
    else:
        if direction==1:
            return pos_x-1,pos_y-1
        elif direction==2:
            return pos_x,pos_y-1
        elif direction==3:
            return pos_x-1,pos_y
        elif direction==4:
            return pos_x+1,pos_y
        elif direction==5:
            return pos_x-1,pos_y+1
        elif direction==6:
            return pos_x,pos_y+1

def checkMoveValidation(player, mapStat, move):
    # move =[move position, move # of step, move direction]
    [pos_x, pos_y] = move[0]  # expected [x,y]
    if (move[1] < 1 or move[1] > 3):
        print(f"player {player} illegal length.")
        return False
    if mapStat[pos_x][pos_y] != 0:
        print(f"player {player} illegal place.")
        return False
    next_x, next_y=pos_x,pos_y
    for i in range(move[1] - 1): 
        [next_x, next_y]=Next_Node(next_x,next_y,move[2])
        print("NEW POS {i}: ", next_x, "----", next_y)
        if(next_x < 0 or next_x > 11 or next_y < 0 or next_y > 11 or mapStat[next_x][next_y]!=0):
            print(f"player {player} illegal move.")
            return False
    return True

def checkRemainMove(mapStat):
    free_region = (mapStat == 0)
    temp = []
    for i in range(len(free_region)):
        for j in range(len(free_region[0])):
            if(free_region[i][j] == True):
                temp.append([i,j])
    return temp

def Getstep(mapStat):
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
    return ([steps,dictance_choice,dir_choice])
    #please write your code here

def end_game_check(mapStat):

    return not (mapStat==0).any()