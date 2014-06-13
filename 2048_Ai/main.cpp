#include <iostream>
#include "Ai.h"
//#define DEBUG
using namespace std;

#include <map>

int main()
{
    #ifdef DEBUG
        cout << "debuging" << endl;
    #endif

    Ai ai;
    int board[4][4] =  {{ 0, 2, 2, 4 },
                            { 2, 2, 4, 8 },
                            { 2, 2, 4, 8 },
                            { 2, 2, 4, 8 }};
    cout << ai.get_move_t(board) << endl;
    return 0;
}
