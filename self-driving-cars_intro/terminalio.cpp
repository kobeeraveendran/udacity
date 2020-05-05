#include <iostream>
#include <vector>

using namespace std;

int main()
{
    int num1, num2;

    cout << "Enter an integer between 1 and 100" << endl;
    cin >> num1;

    cout << "Enter another integer between 1 and 100" << endl;
    cin >> num2;

    cout << "The sum of your two numbers is " << num1 + num2 << endl;
    cout << "The difference between the two numbers is " << num1 - num2 << endl;

    return 0;
}