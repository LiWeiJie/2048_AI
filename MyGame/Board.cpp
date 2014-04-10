#include "Board.h"


char Board::getDirection()
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

void Board::printResult()
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

void Board::generateRandom()
{
    srand((unsigned)time(nullptr));
    while(1)
    {
        //����ҵ�һ���հ�λ��
        mWidth = rand()%mBoardSize;
        mHeight = rand()%mBoardSize;

        if(! mArray[mWidth][mHeight])
        {
            mArray[mWidth][mHeight] = 2;
            mCurrents ++; //��ǰ��ռ�ø���
            break;
        }
    }

}

//void Board::run()
//{
//
//}


















