"""Exact linear outer radial modes; no nonlinear connection asserted."""
import argparse,json
from pathlib import Path
import sympy as s
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
r,H,B=s.symbols('r H B',positive=True)
cp,ct,cw,cn=s.symbols('Cp Ctheta Cw Cn',real=True)
lam=B+1;S=3*lam-1
theta=ct/r**2
P=cp/r**2+B*ct/(H*r**3)
W=-lam*ct/r**2+cw/r**3
sigma=-H*S*ct/2+cp/r+B*ct/(H*r**2)
phi=cn-cp/r-B*ct/(2*H*r**2)
checks={
 'linear_lapse_gradient':s.diff(phi,r)-P,
 'linear_metric_gradient':s.diff(sigma,r)-r*s.diff(P,r)-P,
 'linear_momentum':B*s.diff(theta,r)-2*H*r*s.diff(P,r)-4*H*P,
 'linear_trace':s.diff(W,r)+(theta+3*W)/r-H*(s.diff(phi,r)+s.diff(sigma,r)),
 'linear_radial_constraint':H*S*theta+2*sigma/r**2-2*P/r,
 'trace_constant':r**2*theta-ct,
 'spatial_boundary_constant':s.limit(sigma,r,s.oo)+H*S*ct/2,
 'flat_boundary_P':P.subs(ct,0)-cp/r**2,
}
result={key:s.simplify(value)==0 for key,value in checks.items()};assert all(result.values()),result
out={'passed':len(result),'checks':result,'scope':'Exact solutions of specified linearized necessary radial equations; fixed normalized flat-spatial de Sitter boundary sets Ctheta=0, not beta. No global nonlinear or physical horizon match.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
