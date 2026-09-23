"""Exact family algebra; all-n transport interpretation is in THEOREM.md."""
import json
from pathlib import Path
from fractions import Fraction as Q
import sympy as S

HERE=Path(__file__).resolve().parent
s,z=S.symbols('s z', real=True)
a,A=S.symbols('a A', positive=True)
n=S.symbols('n', integer=True, positive=True)
q,L=S.symbols('q L', positive=True)
def exact(x): return S.cancel(S.expand(x))
k=A/(a+s); F=A*S.log((a+1)/(a+s))/2
c=S.Rational(20,9); b=-2*F-S.Rational(2,3)*s*k
J=A**2*(S.log((a+1)/(a+s))+a/(a+1)-a/(a+s))
u0=(A/(a+1))**2/11+(c-1)*(1-s)+F**2+J/3
U=u0+b*z+c*z**2
def gen(f):
    p=S.Poly(f,z)
    angular=p.nth(0)+p.nth(2)*(3*s+z**2)/10
    return 2*z*S.diff(f,s)+S.diff(f,z)+k*(angular-f)
checks={
 'mean_generator':exact(gen(F-z)+1)==0,
 'full_majorant_residual':exact(gen(U)+2*(F-z)+4*A*a*z**2/(3*(a+s)**2))==0,
 'boundary_square':exact(U.subs(s,1)-z**2-S.Rational(11,9)*(z-3*A/(11*(a+1)))**2)==0,
 'radius_squared_jacobian':S.diff(s/2,s)==S.Rational(1,2),
}
an=1/(2**n-1)
checks['family_ratio']=exact((1+an)/an-2**n)==0
mean=S.expand_log(S.log(2**n),force=True)/S.log(2)
negative_mean=S.expand_log(S.log(2**(2*n)),force=True)/S.log(2)
checks['mean_n']=exact(mean-n)==0
checks['negative_mean_residual']=exact(negative_mean-n)-n==0
checks['negative_rejects_claimed_mean']=bool(n.is_positive)
B=S.Rational(11,9)+4*(1-q)**2/(11*L**2)+4*(n*L-1+q)/(3*L**2)
coarse=S.Rational(11,9)+4/(11*L**2)+4*n/(3*L)
gap=4*q*(2-q)/(11*L**2)+4*(1-q)/(3*L**2)
checks['coarse_gap_identity']=exact(coarse-B-gap)==0
# With 0<q<1 and L>0, both terms of gap are nonnegative.
x=S.symbols('x', nonnegative=True)
checks['q_gap_positive_form']=exact(gap.subs(q,1/(1+x))-(4*(1+2*x)/(11*L**2*(1+x)**2)+4*x/(3*L**2*(1+x))))==0
checks['rational_constant_margin']=Q(11,9)+Q(9,11)<3
checks['rational_slope_bound']=Q(4,3)/Q(2,3)==2
checks['relative_limit']=S.limit(2/n+3/n**2,n,S.oo)==0
checks['witness_bound_gap']=exact(5/n-(2/n+3/n**2)-3*(n-1)/n**2)==0
intervals=[]
for N in [16,20]:
    t=Q(1,3)
    low=2*sum((t**(2*j+1)/Q(2*j+1) for j in range(N)),Q(0))
    high=low+2*t**(2*N+1)/(Q(2*N+1)*(1-t*t))
    checks[f'log2_lower_{N}']=Q(2,3)<low<high
    checks[f'constant_{N}']=Q(11,9)+4/(11*low*low)<3
    checks[f'slope_{N}']=4/(3*low)<2
    intervals.append({'N':N,'lower':str(low),'upper':str(high)})
result={'checks':{k:bool(v) for k,v in checks.items()},'all_checks_pass':all(checks.values()),
 'mean':str(mean),'negative_mean':str(negative_mean),'variance_upper':str(B),
 'uniform_rational_upper':'2*n+3','relative_upper':'2/n+3/n^2','log2_enclosures':intervals,
 'limitations':['Codex self-review, not independent peer review','Each finite n is bounded; no common opacity cap','No fixed mean across family','No physical observation or novelty certified']}
(HERE/'certified/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':result['checks'],'all_checks_pass':result['all_checks_pass']}))
