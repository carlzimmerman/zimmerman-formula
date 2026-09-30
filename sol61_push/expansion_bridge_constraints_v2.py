"""Symbolic necessary ADM constraints and a kinematic CMC control."""
import argparse
import json
from pathlib import Path
import sympy as s

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
r=s.symbols('r',positive=True)
M2,beta,lam,U,H,m,C=s.symbols('M2 beta lam U H m C',positive=True)
N=s.Function('N')(r);sigma=s.Function('sigma')(r);V=s.Function('V')(r);P=s.Function('P')(r)
E=s.exp(sigma);Fk=s.diff(V,r)+V*s.diff(sigma,r);W=V/r;T=Fk+2*W
Theta=-T/N;Q=Fk**2+2*W**2-lam*T**2
R3=2*(1-s.exp(-2*sigma))/r**2+4*s.exp(-2*sigma)*s.diff(sigma,r)/r
L=M2*r**2*E*Q/(2*N)+M2*r**2*N*E*R3/2+2*M2*r**2*P*s.diff(N,r)-r**2*N*E*(M2*P**2+U+beta*M2*P**3/Theta)
def EL(f):return s.diff(L,f)-s.diff(s.diff(L,s.diff(f,r)),r)
B=beta*N**3*P**3/T**2;J=Fk-lam*T-B
shift_expected=s.diff(J,r)+(2/r-s.diff(N,r)/N)*J-2*(W-lam*T-B)/r
lapse_expected=-M2*Q/(2*N**2)+M2*R3/2-2*M2/E*(s.diff(P,r)+2*P/r)-M2*P**2-U-2*beta*M2*P**3/Theta
pol_expected=2*M2*r**2*N*E*(s.diff(N,r)/(N*E)-P-3*beta*P**2/(2*Theta))
F=1-2*m/r-H**2*r**2
flow=H*r+C/r**2;A2=F+flow**2
checks={
 'shift_equation':EL(V)+M2*r**2*E*shift_expected/N,
 'lapse_equation':EL(N)/(r**2*E)-lapse_expected,
 'polarization_equation':EL(P)-pol_expected,
 'constant_expansion':s.diff(flow,r)+2*flow/r-3*H,
 'slice_metric':1/F-F*(flow/(F*s.sqrt(A2)))**2-1/A2,
 'CMC_zero_C_lapse':A2.subs(C,0)-(1-2*m/r),
 'CMC_zero_C_spatial_curvature':(2*(1-(1-2*m/r))/r**2-2*s.diff(1-2*m/r,r)/r),
 'CMC_clock_acceleration_squared':s.diff(s.sqrt(1-2*m/r),r)**2-m**2/(r**4*(1-2*m/r)),
}
values={name:s.simplify(value)==0 for name,value in checks.items()}
assert all(values.values()),values
y=s.symbols('y',positive=True)
pg=-s.sqrt(H**2*r**2+2*m/r)
theta_pg=-(s.diff(pg,r)+2*pg/r)
assert s.simplify(theta_pg-3*(H**2*r**3+m)/(r**s.Rational(3,2)*s.sqrt(H**2*r**3+2*m)))==0
assert s.simplify((1+y)**2/(1+2*y)-1-y**2/(1+2*y))==0
Ac=s.sqrt(1-2*m/r)
cmc_map={N:Ac,sigma:-s.log(Ac),V:-Ac*H*r}
cmc_shift=s.simplify(shift_expected.subs(cmc_map,simultaneous=True).doit())
assert s.simplify(cmc_shift+beta*Ac*P**2*s.diff(P,r)/(3*H**2))==0
out={'checks':values,'passed':len(values)+3,'CMC_shift_identity':True,
 'scope':'Exact necessary lapse, shift and polarization equations on Theta>0; CMC control is kinematic and not an interacting solution. No beta selection or full constraints/stability proof.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
