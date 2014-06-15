#ifndef AI_INCLUDED
#define AI_INCLUDED

#include <cstdlib>
#include <cstring>
#include <map>
#include <cmath>
#include <ctime>
#include "import.h"
#include <ctype.h>

#ifdef _WIN32
typedef __UINT64_TYPE__  board_t;
typedef __UINT16_TYPE__  row_t;
typedef __UINT8_TYPE__   move_t;
#else
typedef __uint64_t  board_t;
typedef __uint16_t  row_t;
typedef __uint8_t   move_t;
#endif // _WIN32

typedef move_t (*get_move_func_t)(board_t);

#define ROW_MASK 0xFFFFULL
#define COL_MASK 0x000F000F000F000FULL

class Ai
{

    public:
        /* 获得下一步的最优移动方向
            0:上
            1:下
            2:左
            3:右
        */
        int get_move_t(int board[][4]);

        /* autoplay display */
        void start();

        /* 执行一次自动移动并添加新的块 */
        board_t execute_once(board_t board);

        Ai();

    private:
        std::map<int,int> map_int_pow;
        void automatic_play_game();
        void init_move_tables();
        void init_score_tables();
        board_t init_board();
        move_t find_best_move(board_t board);

};



#endif // AI_INCLUDED
