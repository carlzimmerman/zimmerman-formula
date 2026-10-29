"""Independent elimination of the gauge coupling and tree-modulus test."""
import json
import math
import sys
from pathlib import Path

import sympy as S

L,alpha,g,h,lam,f,k=S.symbols('L alpha g h lam f k',positive=True)
R=S.Rational
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    if not checks[name]:
        raise AssertionError(name)

check('gauge_integration_constant',S.simplify(S.diff(1/(10*k*L),L)+10*k/(10*k*L)**2)==0)
original=R(29,12)*k**2*h**2*lam**2*(16*h**2+13*lam**2)/(lam**2+30*h**2)
reduced=S.simplify(original.subs(h**2,alpha*lam**2).subs(lam**2,20/(29*k*L)))
C=100*alpha*(16*alpha+13)/(87*(1+30*alpha))
check('general_hierarchy_coefficient',S.simplify(reduced-C/L**2)==0)
check('unified_rational_coefficient',S.simplify(C.subs(alpha,R(1,30)))==R(7,27))
check('lambda_in_pi_convention',S.simplify((20/(29*k*L)).subs(k,1/(16*S.pi**2))-320*S.pi**2/(29*L))==0)
drift=2*k*(12*alpha*lam**2+R(2,5)*lam**2)
check('normalization_is_not_invariant',S.simplify(drift.subs(alpha,R(1,30)).subs(lam**2,20/(29*k*L))-32/(29*L))==0)
U=f**2*lam**2/(lam**2+30*h**2)
hslope=S.simplify(h*S.diff(U,h)/U)
lslope=S.simplify(lam*S.diff(U,lam)/U)
check('tree_modulus_h_slope',S.simplify(hslope.subs(h**2,alpha*lam**2)+60*alpha/(1+30*alpha))==0)
check('tree_modulus_lambda_slope',S.simplify(lslope.subs(h**2,alpha*lam**2)-60*alpha/(1+30*alpha))==0)
check('unified_tree_slopes',hslope.subs(h**2,lam**2/30)==-1 and lslope.subs(h**2,lam**2/30)==1)
scale=S.symbols('scale',positive=True)
check('coupling_rescaling_requires_free_hierarchy',S.simplify((C/L**2).subs(L,L/scale**2)-scale**4*C/L**2)==0)
rows=[]
for Ln in (100.,300.,1000.):
    kn=1/(16*math.pi**2)
    vn=20/(29*kn*Ln)
    wn=1/(10*kn*Ln)
    for an in (.01,1/30,.1,1.):
        un=an*vn
        direct=29/12*kn*kn*un*vn*(16*un+13*vn)/(vn+30*un)
        via=100*an*(16*an+13)/(87*(1+30*an)*Ln**2)
        assert abs(direct-via)<=2e-15*via
        assert abs(wn/vn-29/200)<1e-15
        rows.append({'L':Ln,'alpha':an,'h':math.sqrt(un),'lambda':math.sqrt(vn),
                     'g':math.sqrt(wn),'B_over_V':direct})
check('twelve_direct_numeric_comparisons',len(rows)==12)
result={'status':'passed','checks':checks,'case_count':len(rows),'cases':rows,
        'coefficient_at_alpha_1_over_30':'7/27',
        'non_claim':'L and alpha are not dynamically selected; no numerical B/V prediction.'}
text=json.dumps(result,indent=2)+'\n'
Path(sys.argv[1]).write_text(text)
print(text,end='')
