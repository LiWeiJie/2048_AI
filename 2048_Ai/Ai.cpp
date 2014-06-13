#include <cstdio>
#include "Ai.h"
//#define DEBUG


/* local function */
int bina_weight[]={0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384};
static inline void print_board(board_t board) {
    int i,j;
    for(i=0; i<4; i++) {
        for(j=0; j<4; j++) {
            printf("%d ", bina_weight[(board)&0xf]);
            board >>= 4;
        }
        printf("\n");
    }
    printf("\n");
}

/* initial */
static board_t row_left_table[65536];
static board_t row_right_table[65536];
static board_t col_up_table[65536];
static board_t col_down_table[65536];

 static inline row_t pack_col(board_t col) {
    return (row_t)(col | (col >> 12) | (col >> 24) | (col >> 36));
}

static inline board_t unpack_col(row_t row) {
    board_t tmp = row;
    return (tmp | (tmp << 12ULL) | (tmp << 24ULL) | (tmp << 36ULL)) & COL_MASK;
}

static inline row_t reverse_row(row_t row) {
    return (row >> 12) | ((row >> 4) & 0x00F0)  | ((row << 4) & 0x0F00) | (row << 12);
}

void Ai::init_move_tables(void) {
    unsigned row;

    memset(row_left_table, 0, sizeof(row_left_table));
    memset(row_right_table, 0, sizeof(row_right_table));
    memset(col_up_table, 0, sizeof(col_up_table));
    memset(col_down_table, 0, sizeof(col_down_table));

    for(row = 0; row < 65536; row++) {
        unsigned int line[4] = {row & 0xf, (row >> 4) & 0xf, (row >> 8) & 0xf, (row >> 12) & 0xf};
        row_t result;
        int i, j;

        /* execute a move to the left */
        for(i=0; i<3; i++) {
            for(j=i+1; j<4; j++) {
                if(line[j] != 0)
                    break;
            }
            if(j == 4)
                break; // no more tiles to the right

            if(line[i] == 0) {
                line[i] = line[j];
                line[j] = 0;
                i--; // retry this entry
            } else if(line[i] == line[j] && line[i] != 0xf) {
                line[i]++;
                line[j] = 0;
            }
        }

        result = (line[0]) | (line[1] << 4) | (line[2] << 8) | (line[3] << 12);

        row_left_table[row] = row ^ result;
        row_right_table[reverse_row(row)] = reverse_row(row) ^ reverse_row(result);
        col_up_table[row] = unpack_col(row) ^ unpack_col(result);
        col_down_table[reverse_row(row)] = unpack_col(reverse_row(row)) ^ unpack_col(reverse_row(result));
    }
}



#define DO_LINE(tbl,i,lookup,xv) do { \
        tmp = tbl[lookup]; \
        ret ^= xv; \
    } while(0)

#define DO_ROW(tbl,i) DO_LINE(tbl,i, (board >> (16*i)) & ROW_MASK,          tmp << (16*i))
#define DO_COL(tbl,i) DO_LINE(tbl,i, pack_col((board >> (4*i)) & COL_MASK), tmp << (4*i))

/*
    0,1,2,3分别是上下左右移动
*/
static inline board_t execute_move_0(board_t board) {
    board_t tmp;
    board_t ret = board;

    DO_COL(col_up_table, 0);
    DO_COL(col_up_table, 1);
    DO_COL(col_up_table, 2);
    DO_COL(col_up_table, 3);

    return ret;
}

static inline board_t execute_move_1(board_t board) {
    board_t tmp;
    board_t ret = board;

    DO_COL(col_down_table, 0);
    DO_COL(col_down_table, 1);
    DO_COL(col_down_table, 2);
    DO_COL(col_down_table, 3);

    return ret;
}

static inline board_t execute_move_2(board_t board) {
    board_t tmp;
    board_t ret = board;

    DO_ROW(row_left_table, 0);
    DO_ROW(row_left_table, 1);
    DO_ROW(row_left_table, 2);
    DO_ROW(row_left_table, 3);

    return ret;
}

static inline board_t execute_move_3(board_t board) {
    board_t tmp;
    board_t ret = board;

    DO_ROW(row_right_table, 0);
    DO_ROW(row_right_table, 1);
    DO_ROW(row_right_table, 2);
    DO_ROW(row_right_table, 3);

    return ret;
}
#undef DO_ROW
#undef DO_COL
#undef DO_LINE

/* Execute a move. */
static inline board_t execute_move(move_t move, board_t board) {
    switch(move) {
    case 0: // up
        return execute_move_0(board);
    case 1: // down
        return execute_move_1(board);
    case 2: // left
        return execute_move_2(board);
    case 3: // right
        return execute_move_3(board);
    default:
        return board;
    }
}

static inline int get_max_rank(board_t board) {
    int maxrank = 0;
    while(board) {
        int k = board & 0xf;
        if(k > maxrank) maxrank = k;
        board >>= 4;
    }
    return maxrank;
}

/* Optimizing the game */
static float line_heur_score_table[65536];
static float row_score_table[65536];

struct eval_state {
    typedef std::map<board_t, float> trans_table_t;
    trans_table_t trans_table; // transposition table, to cache previously-seen moves
    float cprob_thresh;
    int maxdepth;
    int curdepth;
    int cachehits;
    int moves_evaled;

    eval_state() : cprob_thresh(0), maxdepth(0), curdepth(0), cachehits(0), moves_evaled(0) {
    }
};

// score a single board heuristically
static float score_heur_board(board_t board);
#ifdef DEBUG
// score a single board actually (adding in the score from spawned 4 tiles)
static float score_board(board_t board);
#endif
// score over all possible moves
static float score_move_node(eval_state &state, board_t board, float cprob);
// score over all possible tile choices and placements
static float score_tilechoose_node(eval_state &state, board_t board, float cprob);

void Ai::init_score_tables(void) {
    unsigned row;

    memset(line_heur_score_table, 0, sizeof(line_heur_score_table));
    memset(row_score_table, 0, sizeof(row_score_table));

    for(row = 0; row < 65536; row++) {
        unsigned int line[4] = {row & 0xf, (row >> 4) & 0xf, (row >> 8) & 0xf, (row >> 12) & 0xf};
        int i;
        float heur_score = 0;
        float score = 0;

        for(i=0; i<4; i++) {
            int rank = line[i];

            if(rank == 0) {
                heur_score += 10000;
            } else if(rank >= 2) {
                // the score is the total sum of the tile and all intermediate merged tiles
                score += (rank-1) * powf(2, rank);
            }
        }

        int maxi = 0;
        int maxrank = 0;
        for(i=0; i<4; i++) {
            int rank = line[i];

            if(rank > maxrank) {
                maxrank = rank;
                maxi = i;
            }
        }

        if(maxi == 0 || maxi == 3)
            heur_score += 20000;

        // Check if maxis are close to eachother, and of diff ranks (eg 128 256)
        for(i=1; i<4; i++) {
            if ((line[i] == line[i-1] + 1) || (line[i] == line[i-1] - 1)) {
                heur_score += 1000;
            }
        }

        // Check if the values are ordered:
        if ((line[0] < line[1]) && (line[1] < line[2]) && (line[2] < line[3])) heur_score += 10000;
        if ((line[0] > line[1]) && (line[1] > line[2]) && (line[2] > line[3])) heur_score += 10000;

        row_score_table[row] = score;
        line_heur_score_table[row] = heur_score;
    }
}

#define SCORE_BOARD(board,tbl) ((tbl)[(board) & ROW_MASK] + \
    (tbl)[((board) >> 16) & ROW_MASK] + \
    (tbl)[((board) >> 32) & ROW_MASK] + \
    (tbl)[((board) >> 48) & ROW_MASK])

#define SCORE_COL_BOARD(board,tbl) ((tbl)[pack_col((board) & COL_MASK)] + \
    (tbl)[pack_col(((board) >> 4) & COL_MASK)] + \
    (tbl)[pack_col(((board) >> 8) & COL_MASK)] + \
    (tbl)[pack_col(((board) >> 12) & COL_MASK)])

static float score_heur_board(board_t board) {
    return SCORE_BOARD(board, line_heur_score_table) + SCORE_COL_BOARD(board, line_heur_score_table) + 100000;
}

#ifdef DEBUG
static float score_board(board_t board) {
    return SCORE_BOARD(board, row_score_table);
}
#endif

static float score_tilechoose_node(eval_state &state, board_t board, float cprob) {
    float res = 0;
    int num_open = 0;

    for(int i=0; i<16; i++) {
        if(((board >> (4*i)) & 0xf) == 0)
            num_open++;
    }

    cprob /= num_open;

    for(int i=0; i<16; i++) {
        if(((board >> (4*i)) & 0xf) == 0) {
            res += score_move_node(state, board | (((board_t)1) << (4*i)), cprob * 0.9f) * 0.9f;
            res += score_move_node(state, board | (((board_t)2) << (4*i)), cprob * 0.1f) * 0.1f;
        }
    }

    return res / num_open;
}

/* Statistics and controls */
// cprob: cumulative probability
/* don't recurse into a node with a cprob less than this threshold */
#define CPROB_THRESH_BASE (0.0001f)
#define CACHE_DEPTH_LIMIT 6
#define SEARCH_DEPTH_LIMIT 8

static float score_move_node(eval_state &state, board_t board, float cprob) {
    if(cprob < state.cprob_thresh || state.curdepth >= SEARCH_DEPTH_LIMIT) {
        if(state.curdepth > state.maxdepth)
            state.maxdepth = state.curdepth;
        return score_heur_board(board);
    }

    if(state.curdepth < CACHE_DEPTH_LIMIT) {
        const eval_state::trans_table_t::iterator &i = state.trans_table.find(board);
        if(i != state.trans_table.end()) {
            state.cachehits++;
            return i->second;
        }
    }

    int move;
    float best = 0;

    state.curdepth++;
    for(move=0; move<4; move++) {
        board_t newboard = execute_move(move, board);
        state.moves_evaled++;
        if(board == newboard)
            continue;

        float res = score_tilechoose_node(state, newboard, cprob);
        if(res > best)
            best = res;
    }
    state.curdepth--;

    if(state.curdepth < CACHE_DEPTH_LIMIT) {
        state.trans_table[board] = best;
    }

    return best;
}

static float _score_toplevel_move(eval_state &state, board_t board, int move) {
    //int maxrank = get_max_rank(board);
    board_t newboard = execute_move(move, board);

    if(board == newboard)
        return 0;

    state.cprob_thresh = CPROB_THRESH_BASE;

    return score_tilechoose_node(state, newboard, 1.0f) + 1e-6;
}

float score_toplevel_move(board_t board, move_t move) {
    float res;
    struct timeval start, finish;
    double elapsed;
    eval_state state;

    gettimeofday(&start, NULL);
    res = _score_toplevel_move(state, board, move);
    gettimeofday(&finish, NULL);

    elapsed = (finish.tv_sec - start.tv_sec);
    elapsed += (finish.tv_usec - start.tv_usec) / 1000000.0;

    #ifdef DEBUG
    printf("Move %d: result %f: eval'd %d moves (%d cache hits, %zd cache size) in %.2f seconds (maxdepth=%d)\n", move, res,
        state.moves_evaled, state.cachehits, state.trans_table.size(), elapsed, state.maxdepth);
    #endif

    return res;
}


/* Find the best move for a given board. */
move_t Ai::find_best_move(board_t board) {
    move_t move;
    float best = 0;
    int bestmove = -1;

    #ifdef DEBUG
    print_board(board);
    printf("Current scores: heur %.0f, actual %.0f\n", score_heur_board(board), score_board(board));
    #endif

    for(move=0; move<4; move++) {
        float res = score_toplevel_move(board, move);

        if(res > best) {
            best = res;
            bestmove = move;
        }
    }

    return bestmove;
}

int ask_for_move(board_t board) {
    int move;
    char validstr[5];
    char *validpos = validstr;

    print_board(board);

    for(move=0; move<4; move++) {
        if(execute_move(move, board) != board)
            *validpos++ = "UDLR"[move];
    }
    *validpos = 0;
    if(validpos == validstr)
        return -1;

    while(1) {
        char movestr[64];
        const char *allmoves = "UDLR";

        printf("Move [%s]? ", validstr);

        if(!fgets(movestr, sizeof(movestr)-1, stdin))
            return -1;

        if(!strchr(validstr, toupper(movestr[0]))) {
            printf("Invalid move.\n");
            continue;
        }

        return strchr(allmoves, toupper(movestr[0])) - allmoves;
    }
}

/* unif_random is defined as a random number generator returning a value in [0..n-1]. */
static inline unsigned unif_random(unsigned n) {
    static int seeded = 0;

    if(!seeded) {
        srand(time(NULL));
        seeded = 1;
    }

    return rand() % n;
}

/* 随机生成权重为1或者2的方块
    比例是80%为1，20%为2
*/
static int gen_tile() {
    return (unif_random(10) < 9) ? 1 : 2;
}


/*
    TODO：自动演示

*/
void Ai::start()
{
    automatic_play_game();

}

static board_t insert_tile_rand(board_t board, int tile) {
    int num_blank = 0;
    for(int i=0; i<16; i++) {
        if(((board >> (4*i)) & 0xf) == 0)
            num_blank++;
    }

    if(num_blank == 0) {
        printf("insert_tile_rand: no blank !\n");
        return board;
    }

    int index = unif_random(num_blank);
    for(int i=0; i<16; i++) {
        if(((board >> (4*i)) & 0xf) != 0)
            continue;
        if(index == 0) {
            board |= ((board_t)tile) << (4*i);
            break;
        }
        index--;
    }
    return board;
}


/* 初始化棋盘，随机添加两个块 */
board_t Ai::init_board()
{
    //随机添加两个块
    int ct = 2,i;
    board_t board = 0;
    for (i=0; i<ct; i++)
    {
        board = insert_tile_rand(board,gen_tile());
    }
    return board;
}

/* 执行一次自动移动并添加新的块 */
board_t Ai::execute_once(board_t board)
{
    move_t mt = find_best_move(board);
    board = execute_move(mt,board);
    board = insert_tile_rand(board,gen_tile());
    return board;
}


//TODO:自动演示,现只执行两次
void Ai::automatic_play_game()
{
    board_t board = init_board();
    print_board(board);
    board = execute_once(board);
    print_board(board);
    board = execute_once(board);
    print_board(board);
}

int Ai::get_move_t(int board[][4])
{
    board_t local_board = 0;
    for (int i=3;i>=0;i--)
    {
        for (int j=3;j>=0;j--)
        {
            local_board <<= 4;
            local_board += map_int_pow[board[i][j]];
        }
    }
//    print_board(local_board);
    move_t mt = find_best_move(local_board);
//    local_board = execute_move(mt,local_board);
//    print_board(local_board);
    return mt;
}

Ai::Ai()
{
    init_move_tables();
    init_score_tables();
    map_int_pow.clear();
    int ret = 2;
    map_int_pow[0] = 0;
    for (int i=1;i<16;i++){
        map_int_pow[ret] = i;
//        printf("%d %d\n",ret,i);
        ret <<=1;
    }
}

