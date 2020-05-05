#include <iostream>
#include <vector>

using namespace std;

vector < vector <int> > matrix_multiply(vector < vector <int> > matrixA, vector < vector <int> > matrixB)
{

    if (matrixA[0].size() != matrixB.size())
    {
        cout << "Invalid matrix sizes for matrix multiplication" << endl;
        exit(0);
    }

    vector < vector <int> > result (matrixA.size(), (vector <int> (matrixB[0].size(), 0)));

    for (int i = 0; i < matrixA.size(); i++)
    {
        for (int j = 0; j < matrixB[0].size(); j++)
        {
            for (int k = 0; k < matrixA[0].size(); k++)
            {
                result[i][j] += matrixA[i][k] * matrixB[k][j];
            }
        }
    }

    return result;
}

int main()
{

    vector<vector<int> > matrixA {
        {1, 2, 3}, 
        {4, 5, 6}
    };

    vector<vector<int> > matrixB {
        {1, 2}, 
        {3, 4}, 
        {5, 6}
    };

    vector<vector<int> > product;

    product = matrix_multiply(matrixA, matrixB);

    for (int i = 0; i < product.size(); i++)
    {
        for (int j = 0; j < product[0].size(); j++)
        {
            cout << product[i][j] << " ";
        }

        cout << endl;
    }

    return 0;
}