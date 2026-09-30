"""Scaled critical-point identities and finite roots; not a global solution."""
import argparse,json
import sympy as s
from pathlib import Path
import numpy as np
from scipy.optimize import root
ns={}
src=Path('sol61_push/expansion_bridge_radial_ivp.py').read_text().split('\nparser=argparse.ArgumentParser();')[0]
exec(compile(src,'reviewed_radial','exec'),ns)
body=src[src.index('def parts('):src.index('\ndef rhs_r(')]
body=body[:body.index(' pp=-constant/denom')]+' return np.array([C,denom,constant])\n'
body=body.replace('def parts(', 'def algebra(')
exec(compile(body,'reviewed_algebra','exec'),ns)
fn=ns['algebra']
parser=__import__('argparse').ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
H,B,be=s.symbols('H B beta',positive=True);S=3*B+2
k,d,p=s.symbols('k d p',real=True)
normal=s.Matrix([2*(k-p),2*H**2*S/B-2*be*p/H,-2*be*p**2/H+4*H**2*S*p/B+2*H*S*d])
pstar=S*H**3/(be*B);dstar=-S*H**4/(be*B**2)
sub={k:pstar,d:dstar,p:pstar}
jac=normal.jacobian([k,d,p])
z,rr=s.symbols('z r',real=True)
qscale=pstar*rr
poly=z**2-4*qscale*z-7*qscale**2
checks={
 'normal_form_root_C':normal[0].subs(sub),
 'normal_form_root_D':normal[1].subs(sub),
 'normal_form_root_R':normal[2].subs(sub),
 'nonzero_scaled_jacobian':jac.det().subs(sub)-8*be*S,
 'negative_slope_root':poly.subs(z,qscale*(2-s.sqrt(11))),
 'positive_slope_root':poly.subs(z,qscale*(2+s.sqrt(11))),
 'slope_discriminant':(-4*qscale)**2-4*(-7*qscale**2)-44*qscale**2,
}
exact={key:s.simplify(value)==0 for key,value in checks.items()};assert all(exact.values()),exact
cases=[]
for betaval in [2.,10.,20.]:
 ns['beta']=betaval
 for radius in [.001,.002]:
  initial=np.array([5/betaval,-5/betaval,5/betaval])
  def state(x):return np.array([0,x[0]*radius**3,0,x[1]*radius**3,x[2]*radius**2])
  def residual(x):return fn(radius,state(x))/np.array([radius,radius,radius**2])
  sol=root(residual,initial,tol=1e-10);y=state(sol.x)
  assert sol.success and np.max(np.abs(residual(sol.x)))<1e-10
  sig,dW,dt,pp=y[1:];E=np.exp(sig);W=-1+dW;th=3+dt;ct=1+2*betaval*pp**3/th**3
  base=np.array([E*(pp-1.5*betaval*pp*pp/th),-(dt+3*dW)/radius-2*E*W*pp,-4*W*E*pp/ct,0])
  direction=np.array([radius*E,-radius*E*W,(3*betaval*pp*pp/th**2-2*radius*W*E)/ct,1])
  gradients=[]
  for i in range(1,5):
   yy=y.astype(complex);yy[i]+=1e-30j;gradients.append(np.imag(fn(radius,yy))/1e-30)
  gradients=np.array(gradients).T
  dr=np.imag(fn(radius+1e-30j,y.astype(complex)))/1e-30
  D0=dr[1]+gradients[1]@base;D1=gradients[1]@direction
  R0=dr[2]+gradients[2]@base;R1=gradients[2]@direction
  coefficients=np.array([D1,D0+R1,R0]);slopes=np.sort(np.roots(coefficients))
  discriminant=coefficients[1]**2-4*coefficients[0]*coefficients[2]
  assert discriminant>0 and slopes[0]<0<slopes[1]
  expected=(5/betaval)*radius*np.array([2-np.sqrt(11),2+np.sqrt(11)])
  assert np.max(np.abs(slopes/expected-1))<1e-6
  assert th>0 and pp>0
  cases.append({'beta':betaval,'r':radius,'scaled_sigma_dTheta_P':sol.x.tolist(),
   'max_scaled_residual':float(np.max(np.abs(residual(sol.x)))),
   'Pprime_candidates':slopes.tolist(),'slope_polynomial':coefficients.tolist(),
   'discriminant':float(discriminant),'max_relative_leading_slope_difference':float(np.max(np.abs(slopes/expected-1))),
   'Lambda_over_conditional_a0_squared':3*betaval**2/4})
out={'symbolic_checks':exact,'passed_symbolic':len(exact),'critical_cases':cases,
 'scope':'Exact scaled normal-form algebra plus six finite critical-point roots and slope candidates; analyticity and IFT argument are in the report. No actual smooth trajectory, source/cosmology matching, full health or 32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed_symbolic':len(exact),'cases':cases},indent=2))
