#include <cmath>
#include <vector>
#include <algorithm>
extern "C" void collapse_rhs(int N, double eps, const double* y, double* out) {
    const double dm=1.0/N, B=y[N], V=y[2*N+1];
    std::vector<double> pressure(N);
    double previous=0, sum_derivative=0;
    for(int j=0;j<N;j++) {
        const double r=y[j], cube=std::pow(r,3);
        const double volume=std::max((cube-previous)/3,1e-20);
        const double density=dm/volume;
        pressure[j]=.005*density*density; previous=cube;
    }
    for(int j=0;j<N;j++) {
        const double r=y[j], m=(j+1)*dm, w=j==N-1?dm/2:dm;
        const double q=std::min(m/(r*r),1-eps/2);
        const double gb=r<B?r/(B*B*B):1/(r*r);
        const double deriv=r<B?1.5*(B*B-r*r)/(B*B*B*B):0;
        const double next=j==N-1?0:pressure[j+1];
        out[j]=y[N+1+j];
        out[N+1+j]=r*r*(pressure[j]-next)/w+q*q/(1-q)-gb;
        sum_derivative+=w*deriv;
    }
    out[N]=V;
    out[2*N+1]=(.6/(B*B*B)-.6/(B*B)-sum_derivative-.75*dm/(B*B))/.6;
}
