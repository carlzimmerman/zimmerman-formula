"""Local symbolic identities; periodic component proof is in REPORT, not check count."""
import sympy as s,json,sys
from pathlib import Path
x=s.symbols('x',real=True);c=s.symbols('c',real=True);u=s.Function('u')(x);f=-s.diff(u,x,2);v=s.diff(u,x)+c/2

def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);ctl=sys.argv[2] if len(sys.argv)>2 else 'none';checks={}
 def check(n,b):checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n)
 eq=f*s.diff(f,x)-2*s.diff(f,x,2)*s.diff(u,x)-c*s.diff(f,x,2)
 rhs=2*v*s.diff(v,x,3)+s.diff(v,x)*s.diff(v,x,2)
 check('integrated actual equation has PLUS sign',s.expand(eq-rhs)==0)
 a,b,d,e=s.symbols('a b d e',real=True); vp=s.symbols('vp',positive=True);vm=s.symbols('vm',negative=True)
 for z,label in [(vp,'positive'),(vm,'negative')]:
  # d(sqrt(|v|)v'') = sqrt(|v|)/(2v)*(2v v'''+v'v'').
  root=s.sqrt(z if label=='positive' else -z)
  derivative=(1 if label=='positive' else -1)*b*d/(2*root)+root*e
  claimed=root/(2*z)*(2*z*e+( -1 if ctl=='minus_sign' else 1)*b*d)
  check('integrating factor '+label,s.simplify(derivative-claimed)==0)
 # exact mean integration by parts: <f''u'> = -<f'u''> = <f'f> =0.
 check('mean integration constant vanishes',s.expand(-s.diff(f,x)*s.diff(u,x,2)-f*s.diff(f,x))==0)
 check('shift c does not affect derivatives',s.diff(v,x)==s.diff(u,x,2))
 if ctl=='longitudinal':check('candidate transverse averaged shift constant',s.diff(s.cos(x),x)==0)
 (out/'results.json').write_text(json.dumps({'checks':checks,'scope':'Exact identities; uniform proof uses periodic nonzero-set components and bounded v second derivative','arithmetic':'SymPy exact symbols'},indent=2)+'\n')
 return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(main())
