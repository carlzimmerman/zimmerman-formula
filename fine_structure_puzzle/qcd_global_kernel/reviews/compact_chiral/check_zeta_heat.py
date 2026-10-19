"""Independent heat-Mellin check of the new prime S4 zeta finite part."""
import json,sys,math
from fractions import Fraction as Q
from pathlib import Path
import mpmath as m
import sympy as s
m.mp.dps=45
def halfz(n):
 b=s.bernoulli(n+1)
 return (Q(1,2**n)-1)*(-Q(int(b.p),int(b.q))/(n+1))
raw={-2:Q(1,6),-1:Q(-1,24)}
for j in range(12): raw[j]=Q((-1)**j,math.factorial(j))*(halfz(3+2*j)/3-halfz(1+2*j)/12)
co={j:sum(v*Q(9,4)**(j-k)/math.factorial(j-k) for k,v in raw.items() if k<=j) for j in range(11)}
def mq(v): return m.mpf(v.numerator)/v.denominator
split=m.mpf('.04')
low=(mq(co[0])-1)*split+m.fsum(mq(co[j])*split**(j+1)/(j+1) for j in range(1,11))
def prime_trace(t):
 n=int(m.ceil(m.sqrt(155/t)))+3
 assert n<200
 return m.fsum(m.mpf((l+1)*(l+2)*(2*l+3))/6*m.exp(-t*l*(l+3)) for l in range(1,n+1))
mid=m.quad(lambda t:prime_trace(t)-1/(6*t*t)-1/(3*t),[split,m.mpf('.2'),1])
high=m.quad(prime_trace,[1,4,16,m.inf])
# 1/Gamma(1+eps)=1+gamma eps; a0/(s-2) contributes -a0.
fp=low+mid+high-m.mpf(1)/6+m.euler/3
target=2*m.euler/3-m.mpf(8)/9
err=abs(fp-target)
assert err<m.mpf('2e-18')
result={'status':'completed','method':'Mellin prime heat trace with local a0/a1 subtraction at t=1; distinct from target Hurwitz Laurent series',
 'residue':'1/3','finite_part_heat':m.nstr(fp,35),'finite_part_closed':m.nstr(target,35),'absolute_difference':m.nstr(err,35),
 'bounds':{'precision':45,'heat_split':str(split),'heat_small_segment_order':10,'maximum_harmonics':200},
 'non_claims':['No interval certification','No k15 RG identification','No full NLO partition']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
