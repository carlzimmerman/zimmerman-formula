import sympy as s
from pathlib import Path
import json
M,U,E,p,r,b1,b2,b3,p1,p2,r1,N,N1,N2,w,w1,w2,L,P,P1,F,FD,FD1,d=s.symbols('M U E p r b1 b2 b3 p1 p2 r1 N N1 N2 w w1 w2 L P P1 F FD FD1 d',nonzero=True)
jet={E:2*E*b1,b1:b2,b2:b3,p:p1,p1:p2,r:r1,N:N1,N1:N2,w:w1,w1:w2,P:P1,FD:FD1}
def dx(expr):return sum(s.diff(expr,a)*da for a,da in jet.items())
vol=U*E;C=2*M*M*E*E/p;S=2*b2+3*b1*b1;pb=r+C*S
hk=(p*p-2*p*pb)/(4*M*vol);rate=N*(p-pb)/(2*M*vol)
bdot=-N*p/(2*M*vol)+w*b1
Lsp=M*E/U*(2*N1*b1+N*b1*b1)
pdot=N*hk+N*vol*(F-FD*d)-Lsp+dx(w*p)
pbdot=2*N*hk+2*N*vol*F+2*Lsp-dx(2*M*E/U*(N1+N*b1)+2*N*E*P*FD)+dx(w*pb)
expr=pbdot-C*(4*bdot-pdot/p)*S-C*(2*dx(dx(bdot))+6*b1*dx(bdot))
expr=expr.subs({w2:-dx(rate),w1:L-rate},simultaneous=True)
expr=expr.subs(p2,b2*pb+b1*dx(pb)).subs(p1,b1*pb)
expr=s.factor(s.cancel(expr))
checks={str(x)+'_absent':not expr.has(x)for x in [N2,b3,p1,p2,w1,w2]}
checks['advection_r']=s.simplify(s.diff(expr,r1)-w)==0
replacements,reduced=s.cse(expr,optimizations='basic')
args=[M,U,E,p,r,b1,b2,N,N1,w,L,P,P1,F,FD,FD1,d,r1]
code='"""Generated exact constrained adapted momentum RHS; see derive_expanded.py."""\n'
code+='def rate('+','.join(map(str,args))+'):\n'
for key,val in replacements:code+='    '+str(key)+' = '+s.pycode(val)+'\n'
code+='    return '+s.pycode(reduced[0])+'\n'
pth=Path(__file__).resolve().parent
(pth/'expanded_rate.py').write_text(code)
(pth/'expanded_algebra.json').write_text(json.dumps(dict(checks=checks,all_pass=all(checks.values()),expression=str(expr)),indent=2)+'\n')
print(json.dumps(checks,indent=2));print('operations',s.count_ops(expr));assert all(checks.values())
