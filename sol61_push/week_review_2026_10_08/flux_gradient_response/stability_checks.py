"""Cartesian Hessian and sharp coercivity constant at aligned spherical states."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)
x,y,z=s.symbols('x y z',real=True)
F,a,S=s.symbols('F a S',positive=True)
R=s.sqrt(x*x+y*y+z*z)
A=s.Function('A')
B=s.Function('B')
sign=-1 if args.mutate else 1
V=A(R)-sign*S*B(R)*z/R
H=s.hessian(V,(x,y,z)).subs({x:0,y:0,z:F})
g=s.sqrt(F)*s.sqrt(F+a)
gp=s.diff(g,F); gpp=s.diff(g,F,2)
H=H.subs({s.diff(A(F),F,2):gp+F*gpp,s.diff(A(F),F):F*gp,
          s.diff(B(F),F,2):gpp,s.diff(B(F),F):gp,B(F):g})
H=H.applyfunc(s.simplify)
Hr=(4*F**3+6*a*F**2+a*a*F+a*a*S)/(4*F**s.Rational(3,2)*(F+a)**s.Rational(3,2))
Ht=(2*F+a)/(2*g)+S*a/(2*F*g)
check('Cartesian mixed Hessian vanishes',all(H[i,j]==0 for i in range(3) for j in range(3) if i!=j))
check('Cartesian radial Hessian',s.simplify(H[2,2]-Hr)==0,H[2,2])
check('Cartesian transverse Hessian',s.simplify(H[0,0]-Ht)==0 and s.simplify(H[1,1]-Ht)==0,H[0,0])
check('Density increases radial stiffness',s.diff(H[2,2],S).is_positive is True,s.diff(H[2,2],S))
check('Density increases transverse stiffness',s.diff(H[0,0],S).is_positive is True,s.diff(H[0,0],S))
base=Hr.subs(S,0)
expected=a*a*(2*F-a)/(8*F**s.Rational(3,2)*(F+a)**s.Rational(5,2))
check('Unique minimum derivative factor',s.simplify(s.diff(base,F)-expected)==0,expected)
check('Sharp coercivity constant',s.simplify(base.subs(F,a/2)-5/(3*s.sqrt(3)))==0)
check('Transverse base at least one certificate',s.simplify(gp*gp-1-a*a/(4*F*(F+a)))==0)
for ff in [s.Rational(1,100),s.Rational(1,2),s.Integer(1),s.Integer(100)]:
    for ss in [0,1,100]:
        diag=[v.subs({F:ff,a:1,S:ss}).evalf() for v in H.diagonal()]
        check('Sample Cartesian positivity '+str((ff,ss)),all(v>0 for v in diag),diag)
Path(args.output).write_text(json.dumps(dict(checks=checks,radial=str(Hr),transverse=str(Ht),mutation=args.mutate),indent=2)+'\n')
print(str(sum(x['passed'] for x in checks))+'/'+str(len(checks))+' passed',flush=True)
raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
