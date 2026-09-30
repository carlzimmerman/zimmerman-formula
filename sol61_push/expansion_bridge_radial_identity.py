"""Exact checks of radial closure used by the separate numerical IVP."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
r,M2,beta,lam,U=s.symbols('r M2 beta lam U',positive=True)
N=s.Function('N')(r);sig=s.Function('sigma')(r);V=s.Function('V')(r);P=s.Function('P')(r)
E=s.exp(sig);Fk=s.diff(V,r)+V*s.diff(sig,r);W=V/r;T=Fk+2*W;th=-T/N
Q=Fk**2+2*W**2-lam*T**2
R3=2*(1-s.exp(-2*sig))/r**2+4*s.exp(-2*sig)*s.diff(sig,r)/r
L=M2*r**2*E*Q/(2*N)+M2*r**2*N*E*R3/2+2*M2*r**2*P*s.diff(N,r)-r**2*N*E*(M2*P**2+U+beta*M2*P**3/th)
def EL(f):return s.diff(L,f)-s.diff(s.diff(L,s.diff(f,r)),r)
rad=(EL(sig)-V*EL(V))/(r**2*N*E)
expected=-M2*Q/(2*N**2)+M2*(1-s.exp(-2*sig))/r**2-2*M2*s.exp(-2*sig)*s.diff(N,r)/(N*r)-M2*P**2-U-2*beta*M2*P**3/th
identity=2*M2*s.exp(-2*sig)/r*(s.diff(sig,r)+s.diff(N,r)/N-r*E*(s.diff(P,r)+2*P/r))
checks={'radial_metric_combination':rad-expected,'gradient_identity':EL(N)/(r**2*E)-rad-identity}
ss,ww,tt,pp,dp,u=s.symbols('sigma W theta P Pprime u',real=True)
ee=s.exp(ss);t=1/ee;B=lam-1;aa=pp+3*beta*pp**2/(2*tt);ct=B+2*beta*pp**3/tt**3
rest=B*tt**2/2-2*tt*ww-3*ww**2-pp**2-u-2*beta*pp**3/tt
C=rest+(1-t*t)/r**2-2*t*aa/r
n=ee*aa;sk=r*ee;s0=2*ee*pp-n;wk=-r*ee*ww;w0=-tt/r-ww*(2*ee*pp+3/r)
tk=(3*beta*pp**2/tt**2-2*r*ww*ee)/ct;t0=-4*ww*ee*pp/ct
D=-6*beta*t*pp/(tt*r)-3*beta*pp**2/tt+2*r*ee*ww*(tt+3*ww)+s.diff(C,tt)*tk
R=-6*beta*t*pp**2/(tt*r*r)+2*aa*(pp-3*beta*pp**2/(2*tt))/r+2*rest/r+s.diff(C,ww)*w0+s.diff(C,tt)*t0
Cprime=s.diff(C,r)+s.diff(C,ss)*(sk*dp+s0)+s.diff(C,ww)*(wk*dp+w0)+s.diff(C,tt)*(tk*dp+t0)+s.diff(C,pp)*dp
checks['constraint_derivative_closure']=Cprime-(D*dp+R-2*C/r)
results={name:s.simplify(expr)==0 for name,expr in checks.items()}
assert all(results.values()),results
out={'checks':results,'passed':len(results),'scope':'Exact reduced radial combination and algebraic closure; no full covariant equation completeness or global existence.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
