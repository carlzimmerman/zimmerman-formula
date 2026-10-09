# One-loop QED: MSbar running mass m(mu) = M [1 - (alpha/pi)(1 + (3/4) ln(mu^2/M^2))] (pole M).
# Ask: is there ONE scale mu where both Q = 2/3 and delta = 2/9 hold? Two conditions, one parameter.
from mpmath import mp, mpf, sqrt, acos, log, pi, findroot
mp.dps=30
a=1/mpf('137.035999084')
M=[mpf('0.51099895000'),mpf('105.6583755'),None]
def inv(mt,mu,mode):
    ms=[x*(1-(a/pi)*(1+mpf(3)/4*log(mu**2/x**2))) for x in (M[0],M[1],mt)] if mode=='msbar' else [M[0],M[1],mt]
    v=[sqrt(x) for x in ms]; A=sum(v)/3; Q=sum(ms)/sum(v)**2; r=sqrt(6*Q-2)
    d=acos((v[2]/A-1)/r); return Q,d
for mt,lab in [(mpf('1776.93'),'PDG/wiki 1776.93'),(mpf('1777.09'),'Belle II 1777.09')]:
    print(lab, " pole: Q-2/3=%.2e  delta-2/9=%.2e"%tuple([x-y for x,y in zip(inv(mt,1,'pole'),(mpf(2)/3,mpf(2)/9))]))
    for mu in [mpf('0.511'),mpf(1),mpf(10),mpf('105.66'),mpf(1000),mpf('1777'),mpf('91187.6'),mpf(10)**6]:
        Q,d=inv(mt,mu,'msbar'); print("   mu=%10.3f MeV  Q-2/3=%+.3e  delta-2/9=%+.3e"%(mu,Q-mpf(2)/3,d-mpf(2)/9))
