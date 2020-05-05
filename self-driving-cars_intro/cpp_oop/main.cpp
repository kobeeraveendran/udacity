#include <iostream>

using namespace std;

class Gaussian
{
    private:
        float mu, sigma2;

    public:

        //constructor fns
        Gaussian ();
        Gaussian (float, float);

        // setter functions
        void setMu(float);
        void setSigma2(float);

        float getMu();
        float getSigma2();

        float evaluate (float);
        Gaussian mul (Gaussian);
        Gaussian add (Gaussian);
};

int main ()
{
    Gaussian mygaussian (30.0, 100.0);
    Gaussian othergaussian (10.0, 25.0);

    cout << "Average: " << mygaussian.getMu() << endl;
    cout << "Evaluation: " << mygaussian.evaluate(15.0) << endl;

    cout << "mul results variance: " << mygaussian.mul(othergaussian).getSigma2() << endl;
    cout << "mul results average: " << mygaussian.mul(othergaussian).getMu() << endl;

    cout << "add results variance: " << mygaussian.add(othergaussian).getSigma2() << endl;
    cout << "add results average: " << mygaussian.add(othergaussian).getMu() << endl;

    return 0;
}