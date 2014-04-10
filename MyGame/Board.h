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
            memset(mArray[i],0,mBoardSize*sizeof(int)); //�����ʼ��Ϊ0
        }
    }

    virtual ~Board()
    {
        for(int i = 0; i < mBoardSize; i++)
            delete [] mArray[i];
        delete [] mArray;
        mArray = nullptr;
    }
    //������Ϸ
    void run()
    {
        //��ʼʱ�����������в�����������
        init();

        printResult();
        while(1)
        {
            char ch = getDirection();
            if(ch == 'Q') break;

            autoUpdate(ch); //���������ƶ������������

            checkFinish(); //�鿴��Ϸ�Ƿ����

            if(bFinished) break;

            //���̸����ϲ����٣���ô��д����һ������
            if(bChanged) generateRandom();

            bChanged = false;

            printResult();
        }
        printResult();
        goodGame();
    }

private:
    //���ڴӼ����л�ȡ������ƶ�����
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

    //��ʼ��ʱ���趨������ʼ����
    void init()
    {
        generateRandom();
        generateRandom();
        mCurrents = 2;
    }

    //���������ǰ����
    void printResult()
    {
        cout << "-------------------------------------" << endl;
        cout << "�÷�Socre => " << mScore << endl;
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

    //�����̵Ŀհ״������������
    void generateRandom()
    {
        srand((unsigned)time(nullptr));
        while(1)
        {
            //����ҵ�һ���հ�λ��
            mWidth = rand()%mBoardSize;
            mHeight = rand()%mBoardSize;

            if(! mArray[mWidth][mHeight])
            {
                mArray[mWidth][mHeight] = (rand()%10==9?4:2); //����4�ĸ���Ϊʮ��֮һ
                mCurrents ++; //��ǰ��ռ�ø���
                break;
            }
        }

    }

    //�����ƶ������������
    void autoUpdate(char key)
    {
        for(int i = 0; i < mBoardSize; i++)
        {
            // i ���� �к�
            for(int j = 0; j < mBoardSize; j++)
            {
                // j ���� �к�
                for(int k = 1; k < mBoardSize - j; k++)
                {
                    // k ���� j ֮��Ŀ��Ե������к�
                    if(!combineAndMove(i, j, k, key))		//��ǰ������û���ƶ�ʱ��Ӧ������ѭ��
                        break;
                }
            }
        }
    }

    //�ƶ��ϲ�����
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
        //�ƶ������ǰ���пո�
        if(!mArray[r1][c1] && mArray[r2][c2])
        {
            mArray[r1][c1] = mArray[r2][c2];
            mArray[r2][c2] = 0;
            bChanged = true;
            bMove = true;
        }

        //�ƶ�������ǰ������������ֵ��ͬ�����кϲ�
        if(mArray[r1][c1] && mArray[r1][c1] == mArray[r2][c2])
        {
            mArray[r1][c1] *= 2;
            mScore += mArray[r1][c1];
            mArray[r2][c2] = 0;
            if(mArray[r1][c1] == mTarget) bFinished = true; //��Ϸ��ɣ�win

            mCurrents--;
            bChanged = true;
            bMove = false;
        }
        return bMove;
    }

    //�鿴��Ϸ�Ƿ����
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

    //�ж���Ϸ�Ƿ�ɹ�
    void goodGame()
    {
        if(bFinished) cout<<"Win"<<endl;
        else cout<<"Fail"<<endl;
    }
private:
    int mBoardSize;     //���̴�С���߳���
    int** mArray;       //��������
    int mCurrents;      //Ŀǰ��ռ�����̸���
    int mTarget;        //���յĺϳ�Ŀ��ֵ
    bool bChanged;      //�ƶ��������Ƿ����䶯�������̱�ռ�õĸ����Ƿ�����ˡ����ǣ�������һ�������������
    bool bFinished;      //��Ϸ�Ƿ����
    int mWidth,mHeight;  //�����ɵ����ӵ�λ��
    int mScore;          //�÷�
};

#endif // BOARD_H_INCLUDED