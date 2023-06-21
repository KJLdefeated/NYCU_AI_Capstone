#include "STcpClient_1.h"
#include <stdlib.h>
#include <iostream>
#include <vector>

using namespace std;


/*
    input position (x,y) and direction
    output next node position on this direction
*/
vector<int> Next_Node(int pos_x, int pos_y, int direction) {
    vector<int> result;  //建立一個大小為 2 的 vector，用來儲存座標
    result.resize(2);
    if (pos_y % 2 == 1) {
        if (direction == 1) {
            result[0] = pos_x;
            result[1] = pos_y - 1;
        }
        else if (direction == 2) {
            result[0] = pos_x + 1;
            result[1] = pos_y - 1;
        }
        else if (direction == 3) {
            result[0] = pos_x - 1;
            result[1] = pos_y;
        }
        else if (direction == 4) {
            result[0] = pos_x + 1;
            result[1] = pos_y;
        }
        else if (direction == 5) {
            result[0] = pos_x;
            result[1] = pos_y + 1;
        }
        else if (direction == 6) {
            result[0] = pos_x + 1;
            result[1] = pos_y + 1;
        }
    }
    else {
        if (direction == 1) {
            result[0] = pos_x - 1;
            result[1] = pos_y - 1;
        }
        else if (direction == 2) {
            result[0] = pos_x;
            result[1] = pos_y - 1;
        }
        else if (direction == 3) {
            result[0] = pos_x - 1;
            result[1] = pos_y;
        }
        else if (direction == 4) {
            result[0] = pos_x + 1;
            result[1] = pos_y;
        }
        else if (direction == 5) {
            result[0] = pos_x - 1;
            result[1] = pos_y + 1;
        }
        else if (direction == 6) {
            result[0] = pos_x;
            result[1] = pos_y + 1;
        }
    }
    return result;
}


/*
    輪到此程式移動棋子
    mapStat : 棋盤狀態為 12*12矩陣, 0=可移動區域, -1=障礙, 1~2為玩家1~2佔領區域
    gameStat : 棋盤歷史順序
    return Step
    Step : 4 elements, [x, y, l, dir]
            x, y 表示要畫線起始座標
            l = 線條長度(1~3)
            dir = 方向(1~6),對應方向如下圖所示
              1  2
            3  x  4
              5  6
*/
vector<int> GetStep(int mapStat[12][12], int gameStat[12][12])
{
    vector<int> step;
    step.resize(4);
    /*Please write your code here*/
    //TODO

    /*Please write your code here*/
    return step;
}

int main()
{
    int id_package;
    int mapStat[12][12];
    int gameStat[12][12];


    while (true)
    {
        if (GetBoard(id_package, mapStat, gameStat))
            break;

        std::vector<int> step = GetStep(mapStat, gameStat);
        SendStep(id_package, step);
    }
}
