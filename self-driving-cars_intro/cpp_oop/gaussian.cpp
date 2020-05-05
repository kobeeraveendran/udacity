#include <math.h>

class Gaussian
{
    private:
        float mu, sigma2;

    public:
        Gaussian ();
        Gaussian (float, float);

        void setMu(float);
        void setSigma2(float);

        float getMu();
        float getSigma2();

        float evaluate(float);

        Gaussian mul (Gaussian);
        Gaussian add (Gaussian);
};

Gaussian::Gaussian()
{
    mu = 0;
    sigma2 = 1;
}

void Gaussian::setMu (float average)
{
    mu = average;
}

void Gaussian::setSigma2 (float variance)
{
    sigma2 = variance;
}

float Gaussian::evaluate(float x)
{
    float coefficient, exponential;

    coefficient = 1.0 / sqrt(2.0 * M_PI * sigma2);
    exponential = exp (pow (-0.5 * (x - mu), 2) / sigma2);

    return coefficient * exponential;
}

Gaussian Gaussian::mul (Gaussian other)
{
    float new_mu, new_sigma2;

    new_mu = mu + other.getMu();
    new_sigma2 = sigma2 + other.getSigma2();

    return Gaussian (new_mu, new_sigma2);
}