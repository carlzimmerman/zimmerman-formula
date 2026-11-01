"""Bounded master checks, including independent convergent parameter integral."""
import argparse
import itertools
import json
import math
from pathlib import Path
import resource
import time

import mpmath as mp
from scipy.integrate import quad

from master_integrals import I,J,J2,I_mp,J_mp,cache_info

mp.mp.dps=60


def mixed_parameter(x,y,z):
    # -d_x d_y d_z I=integral_simplex abc/[U^2 M^2].
    def outer(a):
        def inner(v):
            b=(1-a)*v;c=(1-a)*(1-v);U=a*b+b*c+c*a;M=a*x+b*y+c*z
            return a*b*c*(1-a)/(U*U*M*M) if U else 0.
        return quad(inner,0,1,epsabs=2e-12,epsrel=2e-12,limit=150)[0]
    value,error=quad(outer,0,1,epsabs=2e-11,epsrel=2e-11,limit=150)
    return -value,error


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();start=time.monotonic()
    triples=[(0,0,0),(0,0,1),(0,1,1),(0,1,2),(0,1e-12,1),(1,1,1),(1,2,2),(1,2,9),
             (1,1,4),(1,1,4*(1-1e-8)),(1,1,4*(1+1e-8)),(1e-10,1,2),
             (1e-8,1e-8,1),(1e-20,1e-3,10),(3,7,13),(1e3,1e3,1e3)]
    rows=[];perms=0;worst=0.
    for masses in triples:
        for q in [.2,1.,5.]:
            ref=I_mp(*masses,q);val=I(*masses,q);scale=max(1.,sum(masses),abs(float(ref)))
            err=abs(val-float(ref))/scale;worst=max(worst,err);assert err<3e-11,(masses,q,ref,val)
            for p in set(itertools.permutations(masses)):
                assert I(*p,q)==val;perms+=1
            rows.append({'masses':masses,'Q2':q,'I':val,'mp60':str(ref),'normalized_abs_error':err})
    equal=[]
    for x,q in [(1.,1.),(3.,.2),(.001,5.)]:
        lx=mp.log(mp.mpf(x)/q);cl=mp.im(mp.polylog(2,mp.exp(mp.j*mp.pi/3)))
        ref=mp.mpf(x)*(-mp.mpf('1.5')*lx**2+6*lx-mp.mpf('7.5')+2*mp.sqrt(3)*cl)
        err=abs(I_mp(x,x,x,q)-ref);assert err<mp.mpf('1e-50')*max(1,abs(ref))
        equal.append({'x':x,'Q2':q,'absolute_error':str(err)})
    scale_rows=[]
    for masses in [(0,1,2),(1,1,1),(1,2,9)]:
        for k in [1e-9,1e9]:
            lhs=I(*(k*x for x in masses),k*.7);rhs=k*I(*masses,.7)
            err=abs(lhs-rhs)/max(abs(rhs),k);assert err<1e-11
            scale_rows.append({'masses':masses,'scale':k,'normalized_error':err})
    qder=[]
    for masses in [(0,0,1),(0,1,1),(0,1,2),(1,1,1),(1,2,9)]:
        q=mp.mpf('.7');d=mp.diff(lambda t:I_mp(*masses,q*mp.exp(2*t)),0)
        expected=2*sum(J_mp(x,q) for x in masses)-2*sum(masses)
        err=abs(d-expected);assert err<mp.mpf('1e-45')*max(1,abs(expected))
        qder.append({'masses':masses,'error':str(err)})
    limits=[]
    for y,z in [(1,1),(1,2),(0,1)]:
        delta=mp.mpf('1e-18');v=I_mp(delta,y,z);ref=I_mp(0,y,z)
        err=abs(v-ref);assert err<mp.mpf('1e-14')
        limits.append({'target':[0,y,z],'delta':str(delta),'difference':str(err)})
    mixed=[]
    for masses in [(1,1,1),(1,2,2),(1,2,9)]:
        ref,qe=mixed_parameter(*masses)
        deriv=mp.diff(lambda x,y,z:I_mp(x,y,z),tuple(mp.mpf(x) for x in masses),(1,1,1))
        err=abs(float(deriv)-ref)/max(1e-12,abs(ref));assert err<3e-8,(masses,deriv,ref,err)
        mixed.append({'masses':masses,'analytic_mixed_derivative':str(deriv),'independent_real_parameter_integral':ref,'quad_error_estimate':qe,'relative_difference':err})
    rejected=0
    for fn in [lambda:I(-1,1,1),lambda:I(1,1,1,0),lambda:J(-1),lambda:J(1,-1)]:
        try:fn()
        except ValueError:rejected+=1
    assert rejected==4
    out={'claim_id':'TP03-MASTER-INTEGRALS','checks':{'48float_mp_cases':len(rows)==48,'permutation_symmetry':True,'equalmass_specials':len(equal)==3,'scale_homogeneity':len(scale_rows)==6,'Q_derivative':len(qder)==5,'massless_continuity':len(limits)==3,'independent_mixed_derivative_quadrature':len(mixed)==3,'invalid_domain_rejected':rejected==4},
         'cases':rows,'permutation_evaluations':perms,'max_normalized_float_error':worst,'equalmass':equal,'scale':scale_rows,'Q_derivatives':qder,'limits':limits,'independent_mixed_derivative':mixed,
         'runtime_seconds':time.monotonic()-start,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'cache_info':{k:str(v) for k,v in cache_info().items()},
         'non_claims':['Finite validation,notintervalcertificate orallinputaccuracyproof','Positive squaredmassesonly;no tachyonicbranch continuation','No diagramvertexnormalization inferred frommasterchecks']}
    assert out['peak_RSS_bytes']<1073741824
    Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['checks','max_normalized_float_error','runtime_seconds','peak_RSS_bytes']}))

if __name__=='__main__':main()
