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

eps,beta=s.symbols('epsilon beta',real=True)
ph,phd,sg,sgd,ww,wwd,tt,ttd,pp,ppd=s.symbols('phi phip sigma sigmap W Wprime theta thetap P Pprime',real=True)
EE=s.exp(eps*sg);TH=3*H+eps*tt;WW=-H+eps*ww;PP=eps*pp
nn=eps*phd/(1+eps*ph);aa=PP+3*beta*PP**2/(2*TH)
exact={
 'linearize_polarization':(nn-EE*aa,phd-pp),
 'linearize_gradient':(eps*sgd+nn-r*EE*(eps*ppd+2*PP/r),sgd+phd-r*ppd-2*pp),
 'linearize_momentum':((B+2*beta*PP**3/TH**3)*eps*ttd-(3*beta*PP**2/TH**2-2*r*WW*EE)*eps*ppd+4*WW*EE*PP,B*ttd-2*H*r*ppd-4*H*pp),
 'linearize_trace':(eps*wwd+TH/r+WW*(nn+eps*sgd+3/r),wwd+(tt+3*ww)/r-H*(phd+sgd)),
 'linearize_constraint':(B*TH**2/2-2*TH*WW-3*WW**2+(1-s.exp(-2*eps*sg))/r**2-2*s.exp(-eps*sg)*aa/r-PP**2-3*S*H**2/2-2*beta*PP**3/TH,H*S*tt+2*sg/r**2-2*pp/r),
}
for key,(expression,expected) in exact.items():checks[key]=s.diff(expression,eps).subs(eps,0)-expected

result={key:s.simplify(value)==0 for key,value in checks.items()};assert all(result.values()),result
out={'passed':len(result),'checks':result,'scope':'Exact solutions of specified linearized necessary radial equations; fixed normalized flat-spatial de Sitter boundary sets Ctheta=0, not beta. No global nonlinear or physical horizon match.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
