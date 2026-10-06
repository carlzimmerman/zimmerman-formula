#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--mutate-invariant',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
r,eta,kap,q=S.symbols('r eta kap q',positive=True);N=S.Function('N')(r);B=S.Function('B')(r);V=S.Function('V')(r);lf=S.Function('ell')(r);bf=S.Function('b')(r);uf=S.Function('u')(r)
a=S.diff(N,r)/(N*B);U=-3+6*eta*S.log(N)
L=N*(B+1/B)+2*r*S.diff(N,r)/B-r*V**2*(S.diff(B,r)/N+B*S.diff(N,r)/N**2)+N*B*r*r*U-2*eta*B*r*r*V*S.diff(N,r)/N+N*B*r*r*kap*a*a
EL=lambda f:S.diff(L,f)-S.diff(S.diff(L,S.diff(f,r)),r)
l,b,u,k,kp,bp,up=S.symbols('l b u k kp bp up');subs={N:1+q*lf,B:1+q*bf,V:-r*(1+q*(lf+uf))}
linear=[]
for f in [N,B,V]:
 z=S.diff(EL(f).subs(subs).doit(),q).subs(q,0).doit()
 z=z.subs({S.diff(lf,r,2):(kp-k)/r**2,S.diff(lf,r):k/r,S.diff(bf,r):bp/r,S.diff(uf,r):up/r,lf:l,bf:b,uf:u});linear.append(S.simplify(z))
sol=S.solve(linear,[bp,up,kp],dict=True)[0]
checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});print(n,v)
expected={bp:(eta-1)*k,up:-3*eta*l-b/r**2-3*u+(r**-2-eta)*k,kp:3*eta**2*r**2*l/kap+eta*b/kap-k}
for key in [bp,up,kp]:ck('varied_linear_'+str(key),S.simplify(sol[key]-expected[key])==0)
C=b+(0 if args.mutate_invariant else 1-eta)*l
ck('linear_conserved_offset',S.simplify(S.diff(C,l)*k+S.diff(C,b)*sol[bp])==0)
J=S.Matrix([k,sol[bp],sol[up],sol[kp]]).jacobian([l,b,u,k]);lam=S.symbols('lambda')
ck('frozen_characteristic_polynomial',S.simplify(J.charpoly(lam).as_expr()-lam*(lam+3)*(lam**2+lam+eta*(1-eta)/kap-3*eta**2*r*r/kap))==0)
ck('mass_type_mode',all(S.simplify(expr.subs({l:0,b:0,k:0}))==val for expr,val in [(sol[bp],0),(sol[kp],0),(sol[up],-3*u)]))
ck('small_radius_clock_pair',S.simplify(((-1+S.sqrt(1-4*eta*(1-eta)/kap))/2)**2+(-1+S.sqrt(1-4*eta*(1-eta)/kap))/2+eta*(1-eta)/kap)==0)
(out/'results.json').write_text(json.dumps({'checks':checks,'linear_system':{str(key):str(value) for key,value in sol.items()},'scope':'Exact first variation about deSitter H1; frozen eigenvalues not exact variable-coefficient modes; r<<1 exponents neglect r²term'},indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
