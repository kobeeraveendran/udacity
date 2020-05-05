#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

int main()
{
    vector < vector <int> > matrix (5, vector<int> (3, 2));
    vector <int> row;

    ofstream outputfile;
    outputfile.open("matrixoutput.txt");

    if (outputfile.is_open())
    {

        for (int row = 0; row < matrix.size(); row++)
        {
            for (int col = 0; col < matrix[row].size(); col++)
            {
                if (col != matrix[row].size() - 1)
                {
                    outputfile << matrix[row][col] << ", ";
                }

                else
                {
                    outputfile << matrix[row][col] << endl;
                }
                
            }
        }
    }

    outputfile.close();

    return 0;
}