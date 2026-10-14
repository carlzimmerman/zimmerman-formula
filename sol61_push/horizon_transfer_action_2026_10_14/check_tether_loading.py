import sys,json,math
from pathlib import Path
import sympy as s
from scipy.optimize import brentq
out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
checks=[]
def ck(n,v):
 checks.append({'name':n,'ok':bool(v)})
 if not bool(v):raise AssertionError(n)
def ze(n,e):ck(n,s.simplify(e)==0)
a,u,K,V,kap,G=s.symbols('a u K V kappa G',positive=True)
x=s.symbols('x',positive=True)
W=(-a*u-a*a*s.log(1-u/a))/K
Wa=s.diff(W,a)
B=x+2*s.log(1-x)+x/(1-x)
ze('full tether vacuum derivative',Wa.subs(u,a*x)+a*B/K)
ze('residual and full same vacuum derivative',s.diff(W-u*u/(2*K),a)-Wa)
ze('loading derivative positive',s.diff(B,x)-x*x/(1-x)**2)
loading=kap*kap*B/(8*s.pi)
ze('scalar effective potential slope',(1+Wa*a/(2*V)).subs(u,a*x).subs(K,4*s.pi*G).subs(a*a,kap*kap*G*V)-(1-loading))
# a(V)=kappa sqrt(GV), fixed physical P/u in the partial variation.
aV=kap*s.sqrt(G*V)
E=V+W.subs({a:aV,K:4*s.pi*G})
ze('positive vacuum-variable curvature',s.diff(E,V,2)-kap**2/(16*s.pi*V)*(u/aV)**3/(1-u/aV)**2)
def BB(z):return z+2*math.log1p(-z)+z/(1-z)
root=brentq(lambda z:BB(z)/(32*math.pi)-1,.98,.9999,xtol=1e-14)
rows=[]
for xx in [.01,.1,.5,.9,.98,.99,root,.999]:
 eta=BB(xx)/(32*math.pi)
 ck('positive loading '+str(xx),eta>0)
 rows.append({'u_over_a0':xx,'loading_fraction':eta,'effective_V_slope_factor':1-eta})
ck('local minimum near saturation',.99<root<.999)
result={'passed':len(checks),'checks':checks,'rows':rows,'critical_u_over_a0':root,'a0_equilibrium_over_fixed_u':1/root,'interpretation':'Partial scalar variation at fixed polarization u and kappa=.5; exact static energy loading, not total coupled Hessian or formation proof. W(a0(V)) changes scalar EOM; omitting it does not define a joined theory. Stiffness/strong-field changes the background u but does not remove this partial derivative.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
