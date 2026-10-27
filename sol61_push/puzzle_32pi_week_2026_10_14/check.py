import sympy as s
import json
from pathlib import Path
u,a,G,c,C,g,L=s.symbols('u a G c C g L', positive=True)
K=4*s.pi*G
W=a*a/K*(C-u/a-s.log(1-u/a))
rem=W-u*u/(2*K)
checks={}
def eq(name,x,y):
    z=s.simplify(x-y)
    assert z==0,(name,z)
    checks[name]=str(y)
eq('full_force',K*s.diff(W,u),a*u/(a-u))
eq('residual_force',K*s.diff(rem,u),u*u/(a-u))
eq('square_completion',-g*g/(2*K)+u*g/K-W,-(g-u)**2/(2*K)-rem)
eq('simple_mu',(g-u).subs(u,a*g/(a+g)),g*g/(a+g))
eq('offset_force_null',s.diff(W,u,C),0)
W0=W.subs(u,0); W2=s.diff(W,u,2).subs(u,0); W3=s.diff(W,u,3).subs(u,0)
eq('critical_curvature',W2,1/K)
eq('cubic_coefficient',W3,2/(K*a))
eq('amplitude_invariant',W0*W3**2/W2**3,4*C)
Lam=8*s.pi*G*W0/c**4
A=s.pi*c**4/a**2
eq('Lambda_scale_ratio',Lam*c**4/a**2,2*C)
eq('area_Lambda',A*Lam,2*s.pi*C)
eq('target_offset',(A*Lam).subs(C,16*s.pi),32*s.pi**2)
eq('kappa_squared',a*a/(G*W0),4*s.pi/C)
eq('counterexample_kappa_squared',(a*a/(G*W0)).subs(C,8*s.pi),s.Rational(1,2))
q=s.symbols('q',positive=True)
Wq=W.subs(u,q*u)
eq('field_rescaling_invariance',Wq.subs(u,0)*s.diff(Wq,u,3).subs(u,0)**2/s.diff(Wq,u,2).subs(u,0)**3,4*C)
assert s.limit(W,u,a,dir='-')==s.oo
checks['no_finite_saturation_normalization']='W -> +infinity as u -> a from below'
E4=24/L**4; vol=8*s.pi**2*L**4/3
eq('round_S4_Euler_integral',E4*vol,64*s.pi**2)
eq('topological_scale_derivative',s.diff(E4*vol,L),0)
eta=s.diag(-1,1,1,1); eps=s.symbols('eps',positive=True)
Td=s.diag(eps,0,0,0); Tv=-eps*eta
trace=lambda T:s.trace(eta*T)
eq('dust_trace_reversal_00',(Td-s.Rational(1,2)*eta*trace(Td))[0,0],eps/2)
eq('vacuum_trace_reversal_00',(Tv-s.Rational(1,2)*eta*trace(Tv))[0,0],-eps)
print(json.dumps({'checks':checks,'count':len(checks),'scope':'Exact identities for corrected radial potential; not a coefficient derivation.'},indent=2))
