#!/usr/bin/env python3
"""General local-action reciprocity: symbolic PDE and bounded numeric checks."""
import json
import math
from pathlib import Path
import subprocess
import sys
import numpy as np
import sympy as S
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE/'run'
OUT.mkdir(exist_ok=True)
checks=[]
def zero(name,expr):
    residual=S.simplify(expr)
    assert residual==0,(name,residual)
    checks.append(name)

# Generic constitutive Jacobian, no response function inserted.
u,v,w=S.symbols('u v w',real=True)
e=S.symbols('e',positive=True)
mu=S.Function('mu')
norm=S.sqrt(u*u+v*v+w*w)
flux=S.Matrix([mu(norm)*t for t in (u,v,w)])
J=flux.jacobian([u,v,w]).subs({u:0,v:0,w:e}).applyfunc(S.simplify)
expected=S.diag(mu(e),mu(e),mu(e)+e*S.diff(mu(e),e))
for i in range(3):
    for j in range(3): zero('constitutive_J_%d%d'%(i,j),J[i,j]-expected[i,j])

# Independently verify the anisotropic exterior Green function and source flux.
x,y,z=S.symbols('x y z',real=True)
Gamma,C,r=S.symbols('Gamma C r',positive=True)
D=Gamma*(x*x+y*y)+z*z
phi=-C/S.sqrt(D)
lap=S.diff(phi,x,2)+S.diff(phi,y,2)+S.diff(phi,z,2)
zero('green_equation_off_source',S.diff(phi,x,2)+S.diff(phi,y,2)+Gamma*S.diff(phi,z,2))
zero('effective_density_numerator',lap-C*(Gamma-1)*(2*z*z-Gamma*(x*x+y*y))/D**S.Rational(5,2))
parallel=S.diff(phi,z).subs({x:0,y:0,z:r})
perpendicular=S.diff(phi,x).subs({x:r,y:0,z:0})
zero('force_ratio_from_green',parallel/perpendicular-S.sqrt(Gamma))
t=S.symbols('t',real=True)
primitive=t/S.sqrt(Gamma+(1-Gamma)*t*t)
zero('source_flux_primitive',S.diff(primitive,t)-Gamma/(Gamma+(1-Gamma)*t*t)**S.Rational(3,2))
zero('source_flux_normalization',primitive.subs(t,1)-primitive.subs(t,-1)-2)

# Eliminate the unknown response derivative, not just its amplitude.
L=S.symbols('L',positive=True)
beta=S.Rational(1,2)-1/(1+L)
zero('AQUAL_reciprocity',(1+L)*(1-2*beta)-2)
K=-L/(1+L)
Eq=1/(1+K/2)
zero('QUMOND_reciprocity',Eq*(3-2*beta)-4)
zero('nodal_cone_vs_orbit',2/(1+L)-(1-2*beta))
assert S.Rational(4,3)**2 != 2

# Numerical chain: independent implicit orbit solves -> log slope; finite
# differences of constitutive flux -> Gamma; finite differences of Green
# potential -> internal force ratio. This is not a nonlinear global EFE solve.
kernels={
 'rational':lambda a:a*(a+2)/(1+a)**2,
 'simple':lambda a:a/(1+a),
 'standard':lambda a:a/math.sqrt(1+a*a),
 'exponential':lambda a:-math.expm1(-2*a)}
rows=[]
for name,muf in kernels.items():
  for acc in np.geomspace(.01,100,21):
    acc=float(acc)
    muv=muf(acc)
    radius=math.sqrt(1/(acc*muv))
    def vc(rad):
      root=brentq(lambda lg:2*math.log(rad)+lg+math.log(muf(math.exp(lg))),-60,60,xtol=1e-13)
      return math.sqrt(rad*math.exp(root))
    h=1e-4
    bv=(math.log(vc(radius*math.exp(h)))-math.log(vc(radius*math.exp(-h))))/(2*h)
    eps=acc*h
    Jlong=((acc+eps)*muf(acc+eps)-(acc-eps)*muf(acc-eps))/(2*eps)
    gam=Jlong/muv
    assert gam>0
    # Probe sufficiently far away for the external-dominated interpretation.
    R=100*radius
    def pot(a,b,c):return -1/(muv*math.sqrt(gam*(a*a+b*b)+c*c))
    dr=R*h
    gp=(pot(0,0,R+dr)-pot(0,0,R-dr))/(2*dr)
    gt=(pot(R+dr,0,0)-pot(R-dr,0,0))/(2*dr)
    E=gp/gt
    residual=E*E*(1-2*bv)-2
    assert abs(residual)<2e-6,(name,acc,residual)
    rows.append({'kernel':name,'acceleration':acc,'beta':bv,'E':E,'residual':residual})

nodes,weights=np.polynomial.legendre.leggauss(80)
flux_errors=[]
for gam in [1,4/3,2,3]:
    val=float(np.dot(weights,gam/(gam+(1-gam)*nodes*nodes)**1.5))
    flux_errors.append(abs(val-2))
    assert abs(val-2)<1e-12

lean=subprocess.run(['lake','env','lean',str(HERE/'Reciprocity.lean')],
    cwd=ROOT/'fable_independent_2026/lean_2026',capture_output=True,text=True)
(OUT/'lean.txt').write_text(lean.stdout+lean.stderr)
assert lean.returncode==0,lean.stdout+lean.stderr
assert 'sorryAx' not in lean.stdout and 'warning:' not in lean.stdout
assert lean.stdout.count('depends on axioms:')==11
result={'status':'conditional action-class compatibility verified',
 'exact_checks':checks,'exact_check_count':len(checks),'numerical_cases':rows,
 'numerical_case_count':len(rows),'max_reciprocity_residual':max(abs(r['residual']) for r in rows),
 'max_flux_normalization_error':max(flux_errors),'lean_theorems':11,'lean_exit_code':lean.returncode,
 'deep_AQUAL_ratio':math.sqrt(2),'deep_QUMOND_ratio':4/3,
 'relative_deep_force_ratio_separation':math.sqrt(2)/(4/3)-1,
 'scope':'linear external-field-dominated limit; isolated spherical exterior orbit; same physical acceleration; ordinary test-body inertia',
 'non_claims':['No empirical detection','No global novelty established',
 'Not universal across all particle-free gravity theories',
 'Not an exact finite-internal-field formula','No projected-velocity estimator supplied',
 '3D linearization and Green-function bridge checked symbolically, not in Lean']}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='numerical_cases'},indent=2))
