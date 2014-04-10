#include "Logic.h"
#include <time.h>
#include <cstring>
#include <iomanip>
#include <stdlib.h>

Logic::Logic(int aTarget):mTarget(aTarget),mCurrents(0),
    bChanged(false),bFinished(false),bWin(false),
    mWidth(-1),mHeight(-1),mScore(0)
{
    mArray = new int*[kSideLength];
    for(int i = 0; i < kSideLength; i++)
    {
        mArray[i] = new int [kSideLength];
        memset(mArray[i],0,kSideLength*sizeof(int)); //数组初始化为0
    }
}

Logic::Logic(const Logic& src)
{
    mTarget = src.mTarget;
    mCurrents = src.mCurrents;
    bChanged = src.bChanged;
    bFinished = src.bFinished;
    bWin = src.bWin;
    mWidth = src.mWidth;
    mHeight = src.mHeight;
    mScore = src.mScore;

    // alloc
    mArray = new int*[kSideLength];
    for(int i = 0; i < kSideLength; i++)
    {
        mArray[i] = new int [kSideLength];
        memset(mArray[i],0,kSideLength*sizeof(int));
    }
    // init
    for(int i = 0; i < kSideLength; i++)
        for(int j = 0; j < kSideLength; j++)
            mArray[i][j] = src.mArray[i][j];
}

Logic::~Logic()
{
    for(int i = 0; i < kSideLength; i++)
        delete [] mArray[i];
    delete [] mArray;
    mArray = nullptr;
}

MoveDirection Logic::userInput()
{
    cout<<"输入 WASD 表示上左下右的移动：";
    char ch;
    cin>>ch;
    switch(ch)
    {
    case 'w':
    case 'W':
        return Move_Up;                    //Up
    case 's':
    case 'S':
        return Move_Down;                    //Down
    case 'd':
    case 'D':
        return Move_Right;                    //Right
    case 'A':
    case 'a':
        return Move_Left;                    //Left
    default:
        return Move_Nothing;                //Nothing
    }
}

void Logic::setMoveDirection(MoveDirection aDirection)
{
    if(aDirection != Move_Nothing)
        autoUpdate(aDirection);
}

void Logic::printResult()
{
    cout << "-------------------------------------" << endl;
    cout << "得分Socre => " << mScore << endl;
    cout << "-------------------------------------" << endl;
    for (int i = 0; i < kSideLength; i++)
    {
        for (int j = 0; j < kSideLength; j++)
        {
            if (mArray[i][j])
                cout << setw(5) << mArray[i][j] << " |";
            else
                cout << setw(7) << " |";
        }
        cout << endl;
    }
    cout << "-------------------------------------" << endl << endl;
}

void Logic::generateRandom()
{
    srand((unsigned)time(nullptr));
    while(1)
    {
        //随机找到一个空白位置
        mWidth = rand()%kSideLength;
        mHeight = rand()%kSideLength;

        if(! mArray[mWidth][mHeight])
        {
            mArray[mWidth][mHeight] = (rand()%10==9?4:2); //产生4的概率为十分之一
            mCurrents ++; //当前已占用格数
            break;
        }
    }
}

void Logic::autoUpdate(MoveDirection myDirection)
{
    if (myDirection != Move_Nothing)
    {
        for(int i = 0; i < kSideLength; i++)
        {
            // i 代表 行号
            for(int j = 0; j < kSideLength; j++)
            {
                // j 代表 列号
                for(int k = 1; k < kSideLength - j; k++)
                {
                    // k 代表 j 之后的可以递增的列号
                    if(!combineAndMove(i, j, k,myDirection))		//当前的棋子没有移动时，应该跳出循环
                        break;
                }
            }
        }
    }
}

bool Logic::combineAndMove(int i, int j, int k, MoveDirection pDirection)
{
    int r1 = 0,c1 = 0,r2 = 0,c2 = 0;
    switch(pDirection)
    {
    case Move_Up:
        r1 = j, r2 = j + k; //不同行
        c1 = c2 = i; //同一列
        break;
    case Move_Down:
        r1 = (kSideLength - 1 - j), r2 = (kSideLength - 1 - j - k);
        c1 = c2 =  i;
        break;
    case Move_Left:
        r1 = r2 = i;
        c1 = j, c2 = j + k;
        break;
    case Move_Right:
        r1 = r2 = i;
        c1 = (kSideLength - 1 - j), c2 = (kSideLength - 1 - j - k);
        break;
    default:
        break;
    }

    bool bMove = true;
    //移动方向的前方有空格
    if(!mArray[r1][c1] && mArray[r2][c2])
    {
        mArray[r1][c1] = mArray[r2][c2];
        mArray[r2][c2] = 0;
        bChanged = true;
        bMove = true;

        //move
    }

    //移动方向上前后两个格子数值相同，进行合并
    if(mArray[r1][c1] && mArray[r1][c1] == mArray[r2][c2])
    {
        //check
        bool flag = true;
        // left or right move
        if(r1 == r2)
        {
            int from = 0,to = 0;
            if(c1 > c2)
            {
                from = c2+1;
                to = c1;
            }
            else
            {
                from = c1+1;
                to = c2;
            }

            while(from < to)
            {
                if(mArray[r1][from] != 0)
                {
                    flag = false;
                    break;
                }
                from++;
            }
        }
        else if(c1 == c2) // up or down move
        {
            if(abs(r1 - r2) != 1)
            {
                int from = 0,to = 0;
                if(r1 > r2)
                {
                    from = r2+1;
                    to = r1;
                }
                else
                {
                    from = r1+1;
                    to = r2;
                }

                while(from < to)
                {
                    if(mArray[from][c1] != 0)
                    {
                        flag = false;
                        break;
                    }
                    from++;
                }
            }
        }
        if (flag)
        {
            mArray[r1][c1] *= 2;
            mScore += mArray[r1][c1];
            mArray[r2][c2] = 0;
            if(mArray[r1][c1] == mTarget) bFinished = true; //游戏完成，win

            mCurrents--;
            bChanged = true;
            bMove = false;

            // merge
        }
    }
    return bMove;
}

void Logic::checkFinish()
{
    bFinished = true;
    bWin = true;

    //检查棋盘中是否出现目标数字
    for(int r = 0; r < kSideLength; r++)
        for(int c = 0; c < kSideLength; c++)
        {
            if(mArray[r][c] == mTarget)
            {
                bFinished = true;
                bWin = true;
                return;
            }
        }

    if(mCurrents < kSideLength*kSideLength) //棋盘中还有空位
    {
        bFinished = false;
        bWin = false;
        return;
    }

    else if(mCurrents == kSideLength*kSideLength) //棋盘中所有格子已经被占满
    {
        for(int r = 0; r < kSideLength-1; r++)
            for(int c = 0; c < kSideLength-1; c++)
            {
                if(mArray[r][c] == mArray[r][c+1] || mArray[r][c] == mArray[r+1][c])
                {
                    bFinished = false;
                    bWin = false;
                    return;
                }
            }
    }
}

//
void Logic::gameInit()
{
    generateRandom();
    generateRandom();
}

void Logic::gameRun()
{
    gameInit();
    printResult();

    while(1)
    {
        setMoveDirection(userInput());

        checkFinish();

        if(bFinished || bWin) break;

        if(bChanged) generateRandom();
        else cout<<"invalid move!"<<endl;

        bChanged = false;

        printResult();
    }
    printResult();
    goodGame();
}

void Logic::goodGame()
{
    if(bFinished && bWin) cout<<"Win"<<endl;
    if(bFinished && !bWin) cout<<"Fail"<<endl;
}
