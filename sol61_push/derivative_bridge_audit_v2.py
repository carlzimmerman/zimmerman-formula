"""Exact local derivative-bridge identities and illustrative sign checks.

Fixed metric/clock acceleration, timelike scalar background, algebraically
relaxed outward polarization. Not a full gravity characteristic analysis.
"""
import argparse
import json
from pathlib import Path
import sympy as s

parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
X, Xref, P, Kc, M2, Z, n = s.symbols('X Xref P Kc M2 Z n', positive=True)
omega, velocity, gradient, accel = s.symbols('omega velocity gradient accel', real=True)
f=s.Function('f')(X)
fp=s.diff(f,X)
fpp=s.diff(f,X,2)
L=Z*X+2*M2*P*accel-M2*P**2-Kc*f*P**3
Xpert=((omega+velocity)**2-gradient**2)/2
Lpert=L.subs(X,Xpert)
sub={velocity:0,gradient:0,omega:s.sqrt(2*X)}
Hvv=s.diff(Lpert,velocity,2).subs(sub)
Hvp=s.diff(Lpert,velocity,P).subs(sub)
Hpp=s.diff(L,P,2)
Hgg=s.diff(Lpert,gradient,2).subs(sub)
expected_time=Z-Kc*P**3*(fp+2*X*fpp)+18*Kc**2*X*fp**2*P**4/(2*M2+6*Kc*f*P)
expected_space=Z-Kc*fp*P**3
N, omegaN=s.symbols('N omegaN',positive=True)
Xn=omegaN**2/(2*N**2)
Ln=-N*Kc*s.Function('f')(Xn)*P**3
lapse_expected=-Kc*P**3*(s.Function('f')(Xn)-2*Xn*s.diff(s.Function('f')(X),X).subs(X,Xn))
Ns, Es, V, psi, w=s.symbols('Ns Es V psi w',nonzero=True,real=True)
F=Ns**2-Es*V**2
Xrad=((w-V*psi)**2/Ns**2-psi**2/Es)/2
psi0=-w*Es*V/F
fpower=(X/Xref)**n
z=3*Kc*fpower*P/M2
power_time=Z+Kc*fpower*P**3/X*(n*(n+1)-3*n**2/(1+z))
checks={
 'polarization_equation':s.diff(L,P)-2*M2*(accel-P-3*Kc*f*P**2/(2*M2)),
 'frozen_time_hessian':Hvv-(Z-Kc*P**3*(fp+2*X*fpp)),
 'relaxed_time_hessian':Hvv-Hvp**2/Hpp-expected_time,
 'space_hessian':-Hgg-expected_space,
 'lapse_cubic_variation':s.diff(Ln,N)-lapse_expected,
 'zero_flux_scalar_gradient':(V*w/Ns**2+(1/Es-V**2/Ns**2)*psi).subs(psi,psi0),
 'zero_flux_X':Xrad.subs(psi,psi0)-w**2/(2*F),
 'power_time':expected_time.subs({f:fpower,fp:s.diff(fpower,X),fpp:s.diff(fpower,X,2)},simultaneous=True)-power_time,
}
results={key:s.simplify(value)==0 for key,value in checks.items()}
assert all(results.values()),results
samples=[]
for exponent,pval in [(1,1),(-s.Rational(1,2),10),(-2,s.Rational(6,5)),(-2,2),(0,10)]:
 vals={X:1,Xref:1,M2:1,Kc:1,Z:1,n:exponent,P:pval}
 samples.append({'n':str(exponent),'P':str(pval),'time_relaxed':float(power_time.subs(vals)),
                 'space':float((Z-Kc*n*fpower*P**3/X).subs(vals))})
assert samples[0]['space']<0
assert samples[1]['time_relaxed']<0
assert samples[2]['time_relaxed']<0 and samples[3]['time_relaxed']>0
assert samples[4]['time_relaxed']==1 and samples[4]['space']==1
out={'symbolic_checks':results,'passed_symbolic':len(results),'sign_assertions':4,'samples':samples,
     'scope':'Fixed metric, canonical scalar kinetic term, positive outward polarization, auxiliary P relaxed at quadratic order. No full Horndeski or gravitational stability claim.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
