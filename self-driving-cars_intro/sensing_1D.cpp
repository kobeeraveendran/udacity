#include <iostream>
#include <vector>

using namespace std;


vector<string> world = {"green", "red", "red", "green", "green"};


float pHit = 0.6;
float pMiss = 0.2;
float pExact = 0.8;
float pOvershoot = 0.1;
float pUndershoot = 0.1;

void print_vector(vector<float> input)
{
    cout << "\n[ ";
    for (int i = 0; i < input.size(); i++)
    {
        cout << input[i] << " ";
    }
    cout << "]" << endl;
}

vector<float> sense(vector<float> p, string Z)
{
    vector<float> q = {};
    int hit;
    float sum = 0.0;

    for (int i = 0; i < p.size(); i++)
    {
        hit = (Z == world[i]) ? 1 : 0;

        q.push_back(p[i] * (hit * pHit + (1 - hit) * pMiss));
        sum += q[i];
    }

    for (int i = 0; i < q.size(); i++)
    {
        q[i] = q[i] / sum;
    }

    return q;
}

vector<float> move(vector<float> p, int U)
{
    vector<float> q = {};
    float s;

    /*
    for (int i = 0; i < p.size(); i++)
    {
        s = pExact * p[(i - U) % p.size()];
        s = s + pOvershoot * p[(i - U - 1) % p.size()];
        s = s + pUndershoot * p[(i - U + 1) % p.size()];

        q.push_back(s);
    }
    */

   for (int i = 0; i < p.size(); i++)
   {
       if (i-U < 0) {
            s = pExact * p[(i-U) + p.size()];
        }
        else {
            s = pExact * p[(i-U) % p.size()];
        }
        if (i-U-1 < 0) {
            s = s + pOvershoot * p[(i-U-1) + p.size()];
        }
        else {
            s = s + pOvershoot * p[(i-U-1) % p.size()];
        }
        if (i-U+1 < 0) {
            s = s + pUndershoot * p[(i-U+1) + p.size()];
        }
        else {
            s = s + pUndershoot * p[(i-U+1) % p.size()];
        }

        q.push_back(s);
   }

    return q;
}



int main()
{
    
    vector<float> p = {0.2, 0.2, 0.2, 0.2, 0.2};
    vector<string> measurements = {"red", "green"};
    vector<int> motions = {1, 1};

    for (int i = 0; i < measurements.size(); i++)
    {
        p = sense(p, measurements[i]);
        p = move(p, motions[i]);
    }
    
    print_vector(p);

    return 0;
}