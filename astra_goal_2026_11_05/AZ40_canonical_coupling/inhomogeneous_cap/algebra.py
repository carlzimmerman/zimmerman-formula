"""Exact independent Legendre and auxiliary-variation checks (SymPy)."""
import json
import sympy as s
from pathlib import Path
import argparse
pa,pb,v,M,kx,ky,la,star,U=s.symbols('pa pb v M kx ky la star U', nonzero=True)
L=M**2*v*(-2*kx*ky-ky**2-la*(kx+2*ky-star)+U)
vel={kx:(pa-pb)/(2*M**2*v)-la/2,ky:-pa/(2*M**2*v)-la/2}
H=(pa*kx+pb*ky-L).subs(vel)
expected=(M**2*v*(-2*kx*ky-ky**2-la*star-U)).subs(vel)
checks={}
def ck(n,e):checks[n]=s.simplify(e)==0
ck('momentum_A',s.diff(L,kx)-M**2*v*(-2*ky-la))
ck('momentum_B',s.diff(L,ky)-M**2*v*(-2*(kx+ky)-2*la))
ck('Legendre_transform',H-expected)
ck('velocity_A',s.diff(H,pa)-vel[kx]);ck('velocity_B',s.diff(H,pb)-vel[ky])
ck('lambda_envelope',s.diff(H,la)-M**2*v*((kx+2*ky).subs(vel)-star))
th,delta,b,T=s.symbols('theta delta b T',positive=True)
ck('shear_decomposition',(-2*kx*ky-ky**2).subs({kx:(th+2*delta)/3,ky:(th-delta)/3})-(-th**2/3+delta**2/3))
# For constant zero target and scalar/matter absent, lambda=-? No: lambda has
# the sign of Theta, lambda=b Theta/sqrt(1-Theta^2/T^2).
r=s.symbols('r',positive=True)
# Parametrize lambda=b*T*sinh(r): Theta=T*tanh(r), U=b*T^2*(cosh(r)-1).
Uexact=T*s.sqrt((b*T*s.sinh(r))**2+b**2*T**2)-b*T**2
ck('cap_hyperbolic_potential',s.trigsimp(Uexact)-b*T**2*(s.cosh(r)-1))
ck('cap_hyperbolic_derivative',s.diff(Uexact,r)/s.diff(b*T*s.sinh(r),r)-T*s.tanh(r))
# Polarization EL: L_P = v P e^-A N_x - N v (W+gamma Dp^2/2).
# d_x(v e^-A)=2 B_x v e^-A, so all B_x terms cancel after integration by parts.
N,Nx,A,Bx,Dp,Dpx,Wp,gam=s.symbols('N Nx A Bx Dp Dpx Wp gamma')
el=v*s.exp(-A)*Nx-N*v*Wp-2*N*v*gam*Dp*s.exp(-A)*Bx+gam*v*s.exp(-A)*(Nx*Dp+2*N*Bx*Dp+N*Dpx)
ck('polarization_EL',el-N*v*((1+gam*Dp)*s.exp(-A)*Nx/N-Wp+gam*s.exp(-A)*Dpx))
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();p=Path(a.out);p.mkdir(parents=True,exist_ok=True)
r={'checks':checks,'passed':sum(checks.values()),'total':len(checks)};(p/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(not all(checks.values()))
