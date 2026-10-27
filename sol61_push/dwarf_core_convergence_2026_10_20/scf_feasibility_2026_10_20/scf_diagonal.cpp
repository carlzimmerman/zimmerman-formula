// Complete-m Zhao-basis diagonal, matching pinned Agama's normalization.
// No force approximation beyond the declared finite basis; no self pair remains.
#include <cmath>
#include <cstddef>
#include <vector>
#ifdef __FAST_MATH__
#error "No fast-math admitted"
#endif

extern "C" int scf_diagonal(const double* radius, std::size_t count,
    int nmax, int lmax, double eta, double r0, double* kernel, double* derivative) {
    if(nmax<0 || nmax>256 || lmax<0 || lmax>64 || !(eta>=.5) || !(r0>0)) return 1;
    const double pi=std::acos(-1.0);
    std::vector<double> norms((lmax+1)*(nmax+1));
    for(int l=0;l<=lmax;l++) {
        const double w=.5+eta*(2*l+1);
        double pref=-std::exp(std::log(pi/(2*eta))-w*std::log(16.)+std::lgamma(2*w)-2*std::lgamma(w));
        for(int n=0;n<=nmax;n++) {
            if(n) pref*= (2*w+n-1)/n;
            norms[l*(nmax+1)+n]=pref/(n+w)*(4*(n+w)*(n+w)-1);
        }
    }
    int invalid=0;
    #pragma omp parallel for num_threads(2) schedule(static) reduction(|:invalid)
    for(std::size_t i=0;i<count;i++) {
        const double r=radius[i];
        if(!(r>0) || !std::isfinite(r)) {invalid=1;continue;}
        const double s=r/r0,u=std::pow(s,1/eta),xi=(u-1)/(u+1),zi=std::pow(u+1,-eta);
        const double mul=s*zi*zi,dxi=(1-xi*xi)/(2*eta*r);
        double base=-zi,k=0,dk=0;
        for(int l=0;l<=lmax;l++) {
            if(l)base*=mul;
            const double w=.5+eta*(2*l+1),dbase=-base*((2*l+1)*xi+1)/(2*r);
            double previous=0,current=1,dprevious=0,dcurrent=0;
            for(int n=0;n<=nmax;n++) {
                const double f=base*current,df=dbase*current+base*dcurrent*dxi;
                const double scale=(2*l+1)/(r0*norms[l*(nmax+1)+n]);
                k+=scale*f*f;dk+=2*scale*f*df;
                const double next=(2*(n+w)*xi*current-(n+2*w-1)*previous)/(n+1);
                const double dnext=(2*(n+w)*(current+xi*dcurrent)-(n+2*w-1)*dprevious)/(n+1);
                previous=current;current=next;dprevious=dcurrent;dcurrent=dnext;
            }
        }
        kernel[i]=k;derivative[i]=dk;
        if(!std::isfinite(k) || !std::isfinite(dk))invalid=1;
    }
    return invalid;
}
