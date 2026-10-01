"""AFG-002: test the actual transition, not just the deep-limit approximation."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erfc


def phantom(y, kernel):
    t = np.sqrt(y)
    if kernel == 'Q':
        return t/(np.sqrt(1+y)+t)  # stable sqrt(y²+y)-y
    return y*np.exp(-t)/(-np.expm1(-t))


def averages(q, E, s2, kernel, extent=12.):
    # q is mean B/a0(0); response in units a0(0); mean B is held fixed.
    def values(n):
        B = q*np.exp(-s2/2+np.sqrt(s2)*n)
        h = E*phantom(B/E, kernel)
        return B, h
    def integrate(func):
        return quad(lambda n: func(*values(n))*np.exp(-n*n/2)/np.sqrt(2*np.pi),
                    -extent, extent, epsabs=1e-12, epsrel=1e-10, limit=200)[0]
    mean = q+integrate(lambda B,h:h)
    second = q*q*np.exp(s2)+integrate(lambda B,h:2*B*h+h*h)
    if kernel == 'Q':
        exact_second = q*q*np.exp(s2)+E*q
        assert abs(second/exact_second-1)<1e-8
    return mean, second


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    rows=[]
    for z in [1.,3.,5.]:
        E=float(np.sqrt(.315*(1+z)**3+.685))
        for q in [1e-4,.01,.1,1.]:
            for kernel in ['Q','R']:
                target=q+phantom(q,kernel)
                s2=brentq(lambda v:averages(q,E,v,kernel)[0]-target,0.,100.,xtol=1e-10)
                mean,second=averages(q,E,s2,kernel)
                mean_wide,second_wide=averages(q,E,s2,kernel,14.)
                assert abs(mean/target-1)<1e-8
                assert abs(mean_wide/mean-1)<1e-8 and abs(second_wide/second-1)<1e-8
                # Fraction of baryonic-acceleration first moment in B/a0(z)>.1.
                tail=.5*erfc((np.log(.1*E/q)-s2/2)/np.sqrt(2*s2))
                rows.append(dict(z=z,E=E,mean_B_over_a0_today=q,kernel=kernel,
                    exact_log_variance=float(s2),deep_log_variance=float(4*np.log(E)),
                    source_cv=float(np.sqrt(np.expm1(s2))),
                    intrinsic_line_m4_over_m2_squared=float(second/mean**2),
                    source_first_moment_fraction_outside_deep=float(tail),
                    recovered_mean_over_target=float(mean/target)))
    report=dict(checkpoint='AFG-002',rows=rows,checks='Q second moment exact identity; inverse roots; Gaussian integration extent 12 versus 14.',
                non_claims=['Lognormal source heterogeneity is a test family, not a derived physical distribution.',
                            'Common radius, common projection, identical weights, circular motion and independent Gaussian broadening remain assumptions.',
                            'No measured high-z spectra or instrument response are fitted.'])
    (args.out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=='__main__':
    main()
