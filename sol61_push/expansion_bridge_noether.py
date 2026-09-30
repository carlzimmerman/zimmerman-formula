"""Exact radial-covariance certificates for the general-radius action."""
import argparse,json
from pathlib import Path
import sympy as s
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
M2,beta,lam,U=s.symbols('M2 beta lam U',positive=True)
N,sg,V,R,P=s.symbols('N sigma V R P',real=True)
Np,sgp,Vp,Rp,Pp,Rpp=s.symbols('Np sigmap Vp Rp Pp Rpp',real=True)
A=s.exp(sg);F=Vp+V*sgp;W=V*Rp/R;T=F+2*W;theta=-T/N
Q=F**2+2*W**2-lam*T**2
curvature=M2*N*(A+Rp**2/A)+2*M2*Np*R*Rp/A
L=M2*A*R**2*Q/(2*N)+curvature+2*M2*R**2*P*Np-N*A*R**2*(M2*P**2+U+beta*M2*P**3/theta)
raw_curvature=M2*N*A-M2*N*Rp**2/A-2*M2*N*R*Rpp/A+2*M2*N*R*Rp*sgp/A
boundary_prime=-2*M2*(Np*R*Rp+N*Rp**2+N*R*Rpp-N*R*Rp*sgp)/A
jets=[N,sg,V,R,P];first=[Np,sgp,Vp,Rp,Pp]
momentum_sum=sum(v*s.diff(L,dv) for v,dv in zip(first,first))
xi_second=s.diff(L,sgp)-V*s.diff(L,Vp)
xi_first=s.diff(L,sg)-V*s.diff(L,V)+Np*s.diff(L,Np)+sgp*s.diff(L,sgp)+Rp*s.diff(L,Rp)+Pp*s.diff(L,Pp)-L
# With xi_second=0 this is the off-shell radial metric combination.
combination=s.diff(L,sg)-V*s.diff(L,V)-Vp*s.diff(L,Vp)
metric=s.Matrix([-N**2+A**2*V**2,A**2*V,A**2,R**2])
radius=s.symbols('r',positive=True)
areal=L.subs({R:radius,Rp:1},simultaneous=True)
Ta=Vp+V*sgp+2*V/radius
expected=M2*A*radius**2*((Vp+V*sgp)**2+2*(V/radius)**2-lam*Ta**2)/(2*N)+M2*N*(A+1/A)+2*M2*Np*radius/A+2*M2*radius**2*P*Np-N*A*radius**2*(M2*P**2+U-beta*M2*N*P**3/Ta)
checks={
 'intrinsic_curvature_boundary':raw_curvature-curvature-boundary_prime,
 'radial_xi_second_coefficient':xi_second,
 'radial_density_weight':xi_first,
 'Euler_combination_certificate':combination-(L-momentum_sum),
 'metric_variable_jacobian':metric.jacobian([N,sg,V,R]).det()-8*N*R*A**4,
 'areal_action_recovery':areal-expected,
}
results={name:s.simplify(expr)==0 for name,expr in checks.items()};assert all(results.values()),results
out={'checks':results,'passed':len(results),'scope':'Exact density/Noether certificates and action recovery; angular and clock implication requires the smooth regular covariant completion stated in EXPANSION_BRIDGE_COMPLETENESS_RESULTS.md. No numerical residual bound, global solution or stability/32pi selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
