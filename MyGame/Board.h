#ifndef BOARD_H_INCLUDED
#define BOARD_H_INCLUDED
#include <iostream>
#include <iomanip>
#include <cstring>
#include<stdlib.h>
#include<time.h>

using namespace std;

class Board
{
public:
    Board(int aSize,int aTarget):mBoardSize(aSize),mCurrents(0),mTarget(aTarget),bChanged(false),bFinished(false),mWidth(-1),mHeight(-1),mScore(0)
    {
        mArray = new int*[mBoardSize];
        for(int i = 0; i < mBoardSize; i++)
        {
            mArray[i] = new int [mBoardSize];
            memset(mArray[i],0,mBoardSize*sizeof(int)); //数组初始化为0
        }
    }

    virtual ~Board()
    {
        for(int i = 0; i < mBoardSize; i++)
            delete [] mArray[i];
        delete [] mArray;
        mArray = nullptr;
    }
    //运行游戏
    void run()
    {
        //开始时，现在棋盘中产生两个棋子
        init();

        printResult();
        while(1)
        {
            char ch = getDirection();
            if(ch == 'Q') break;

            autoUpdate(ch); //根据输入移动方向调整棋盘

            checkFinish(); //查看游戏是否结束

            if(bFinished) break;

            //棋盘格数合并减少，那么重写生成一个棋子
            if(bChanged) generateRandom();

            bChanged = false;

            printResult();
        }
        printResult();
        goodGame();
    }

private:
    //用于从键盘中获取输入的移动方向
    char getDirection()
    {
        char ch;
        cin>>ch;
        switch(ch)
        {
        case 'w':
        case 'W':
            return 'U';					//Up
        case 's':
        case 'S':
            return 'D';					//Down
        case 'd':
        case 'D':
            return 'R';					//Right
        case 'A':
        case 'a':
            return 'L';					//Left
        case 'Q':
        case 'q':
            return 'Q';					//Quit
        default:
            return '\0';				//Nothing
        }
    }

    //初始化时，设定两个初始格子
    void init()
    {
        generateRandom();
        generateRandom();
        mCurrents = 2;
    }

    //用于输出当前棋盘
    void printResult()
    {
        cout << "-------------------------------------" << endl;
        cout << "得分Socre => " << mScore << endl;
        cout << "-------------------------------------" << endl;
        for (int i = 0; i < mBoardSize; i++)
        {
            for (int j = 0; j < mBoardSize; j++)
            {
                if (mArray[i][j])
                    cout << setw(5) << mArray[i][j] << " |";
                else
                    cout << setw(7) << " |";
            }
            cout << endl;
        }
        cout << "-------------------------------------" << endl << endl;;

    }

    //在棋盘的空白处随机产生棋子
    void generateRandom()
    {
        srand((unsigned)time(nullptr));
        while(1)
        {
            //随机找到一个空白位置
            mWidth = rand()%mBoardSize;
            mHeight = rand()%mBoardSize;

            if(! mArray[mWidth][mHeight])
            {
                mArray[mWidth][mHeight] = (rand()%10==9?4:2); //产生4的概率为十分之一
                mCurrents ++; //当前已占用格数
                break;
            }
        }

    }

    //根据移动方向调整棋盘
    void autoUpdate(char key)
    {
        for(int i = 0; i < mBoardSize; i++)
        {
            // i 代表 行号
            for(int j = 0; j < mBoardSize; j++)
            {
                // j 代表 列号
                for(int k = 1; k < mBoardSize - j; k++)
                {
                    // k 代表 j 之后的可以递增的列号
                    if(!combineAndMove(i, j, k, key))		//当前的棋子没有移动时，应该跳出循环
                        break;
                }
            }
        }
    }

    //移动合并棋盘
    bool combineAndMove(int i, int j, int k, char key)
    {
        int r1 = 0,c1 = 0,r2 = 0,c2 = 0;
        switch(key)
        {
        case 'U':
            r1 = j, r2 = j + k;
            c1 = c2 = i;
            break;
        case 'D':
            r1 = (mBoardSize - 1 - j), r2 = (mBoardSize - 1 - j - k);
            c1 = c2 =  i;
            break;
        case 'L':
            r1 = r2 = i;
            c1 = j, c2 = j + k;
            break;
        case 'R':
            r1 = r2 = i;
            c1 = (mBoardSize - 1 - j), c2 = (mBoardSize - 1 - j - k);
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
        }

        //移动方向上前后两个格子数值相同，进行合并
        if(mArray[r1][c1] && mArray[r1][c1] == mArray[r2][c2])
        {
            mArray[r1][c1] *= 2;
            mScore += mArray[r1][c1];
            mArray[r2][c2] = 0;
            if(mArray[r1][c1] == mTarget) bFinished = true; //游戏完成，win

            mCurrents--;
            bChanged = true;
            bMove = false;
        }
        return bMove;
    }

    //查看游戏是否结束
    void checkFinish()
    {
        bFinished = true;
        for(int r = 0; r < mBoardSize; r++)
            for(int c = 0; c < mBoardSize; c++)
            {
                if(mArray[r][c] == mTarget)
                {
                    bFinished = true;
                    return;
                }
            }

        for(int r = 0; r < mBoardSize-1; r++)
            for(int c = 0; c < mBoardSize-1; c++)
            {
                if(mArray[r][c] == mArray[r][c+1] || mArray[r][c] == mArray[r+1][c] || mArray[r][c] == 0)
                {
                    bFinished = false;
                    return;
                }
            }
    }

    //判断游戏是否成功
    void goodGame()
    {
        if(bFinished) cout<<"Win"<<endl;
        else cout<<"Fail"<<endl;
    }
private:
    int mBoardSize;     //棋盘大小（边长）
    int** mArray;       //棋盘数组
    int mCurrents;      //目前已占用棋盘格数
    int mTarget;        //最终的合成目标值
    bool bChanged;      //移动后，棋盘是否发生变动，即棋盘被占用的个数是否减少了。若是，则生成一个棋子填充棋盘
    bool bFinished;      //游戏是否结束
    int mWidth,mHeight;  //新生成的棋子的位置
    int mScore;          //得分
};

#endif // BOARD_H_INCLUDED
