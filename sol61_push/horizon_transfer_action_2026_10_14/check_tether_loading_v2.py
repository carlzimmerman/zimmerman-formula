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
# Joint relaxation with the correctly reduced carrier energy.
Erem=E-u*u/(8*s.pi*G)
Huu=s.diff(Erem,u,2); Huv=s.diff(Erem,u,V); Hvv=s.diff(Erem,V,2)
det=s.simplify(Huu*Hvv-Huv**2)
ze('joint residual Hessian determinant',det-aV*aV*(u/aV)**4/(4*(4*s.pi*G)**2*V**2*(1-u/aV)**3))
ze('joint u curvature',Huu-(1/(1-u/aV)**2-1)/(4*s.pi*G))
mu=root;solutions=[]
for gN in [1e-4,1,1e4]:
 aa=gN*(1-mu)/(mu*mu); uu=aa*mu
 ck('joint stationary source '+str(gN),abs(uu*uu/(aa-uu)/gN-1)<1e-12)
 ck('constant force enhancement '+str(gN),abs((gN+uu)/gN-1/mu)<1e-12)
 solutions.append({'gN':gN,'a0_relaxed':aa,'u_relaxed':uu,'g_total_over_gN':(gN+uu)/gN})
# K=1 units for direct bounded energy comparisons, kappa=.5.
aa=(1-mu)/(mu*mu)
def energy(aval,xx):
 uu=aval*xx
 return 16*math.pi*aval*aval-aval*uu-aval*aval*math.log1p(-xx)-uu*uu/2-uu
emin=energy(aa,mu)
for mult in [.2,.5,1,2,5]:
 for xx in [.1,.5,.9,.98,.999]:
  ck('joint energy comparison '+str((mult,xx)),energy(aa*mult,xx)>emin)
result={'passed':len(checks),'checks':checks,'rows':rows,'critical_u_over_a0':root,'joint_relaxed_solutions':solutions,'joint_relaxed_force_enhancement':1/root,'a0_equilibrium_over_fixed_u':1/root,'interpretation':'Partial scalar variation at fixed polarization u and kappa=.5; exact static energy loading, not total coupled Hessian or formation proof. W(a0(V)) changes scalar EOM; omitting it does not define a joined theory. Stiffness/strong-field changes the background u but does not remove this partial derivative.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
