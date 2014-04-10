#ifndef LOGIC_H
#define LOGIC_H
#include <iostream>
using namespace std;

typedef enum _MoveDirection_
{
    Move_Up,
    Move_Down,
    Move_Left,
    Move_Right,
    Move_Nothing
} MoveDirection;

class Logic
{
public:
    Logic(int aTarget);
    Logic(const Logic& src);
    virtual ~Logic();

    int** getArray()
    {
        return mArray;
    }
    // set user move direction
    void setMoveDirection(MoveDirection aDirection);

    // input
    MoveDirection userInput();

    void gameRun();

protected:
    //pirnt array
    void printResult();

    //randomly create
    void generateRandom();

    //
    void autoUpdate(MoveDirection myDirection);
    bool combineAndMove(int i, int j, int k, MoveDirection pDirection);

    //
    void checkFinish();

    void gameInit();

    void goodGame();
private:
    const static int kSideLength = 4; //边长4

    int mTarget;	     //最终的合成目标值
    int **mArray;	     //数组
    int mCurrents;       //目前已占用格数
    bool bChanged;       //移动后，棋盘是否发生变动，若是，则生成一个棋子填充棋盘，否则，就是无效的操作
    bool bFinished;      //游戏是否结束（当无法继续进行，或者游戏完成时，finish）
    bool bWin;           //游戏是否胜利，即达到目标值
    int mWidth,mHeight;  //新生成的棋子的位置
    int mScore;          //得分
};

#endif // LOGIC_H
