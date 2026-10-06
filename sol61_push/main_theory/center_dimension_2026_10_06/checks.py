import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--wrong-four-dimensional-coefficient',action='store_true');args=ap.parse_args()
r=s.symbols('r',positive=True);M,c,H,N0=s.symbols('M c H N0',positive=True);n2,b2,x,eps=s.symbols('n2 b2 x eps',real=True)
N,B,V=[s.Function(t)(r) for t in ['N','B','V']];d=lambda z:s.diff(z,r)
def el(L,z):return s.diff(L,z)-d(s.diff(L,d(z)))
rows=[]
for n in range(3,9):
 An=s.Rational(n*(n-1),2);lam=s.Rational(n-1,2*(n-2));used=s.Integer(1) if args.wrong_four_dimensional_coefficient else lam
 ve=An*M*H**2;b=2*c/(n*H);u0=-An*H**2+2*c*s.log(N0)/M
 D=d(V)+d(B)*V/B
 L=M*s.Rational(n-1,2)*((n-2)*N*r**(n-3)*(B+1/B)+2*d(N)*r**(n-2)/B-B/N*(2*r**(n-2)*V*D+(n-2)*r**(n-3)*V**2))+N*B*r**(n-1)*(2*c*s.log(N)-ve)-b*B*r**(n-1)*V*d(N)/N+M*used*d(N)**2*r**(n-1)/(N*B)
 sub={N:N0*(1+n2*r*r),B:1+b2*r*r,V:N0*x*r}
 def coeff(expr,den):return s.simplify(s.limit(expr.subs(sub).doit()/den,r,0))
 eb=coeff(el(L,B),M*N0*r**(n-1));en=coeff(el(L,N),M*r**(n-1))
 wantb=(n-1)*(n-2)*b2-2*(n-1)*n2+An*x*x+u0
 wantn=n*(n-1)*b2-4*n*lam*n2+An*x*x+u0+2*c/M+2*c*x/(M*H)
 assert s.simplify(eb-wantb)==0
 assert s.simplify(en-wantn)==0,'Fourdimensional coefficient incorrectly transplanted'
 combo=s.simplify(en-s.Rational(n,n-2)*eb)
 assert s.simplify(s.diff(combo,n2))==0
 assert s.simplify(combo.subs({N0:1,x:-H,n2:0,b2:0}))==0
 detuned=combo+4*n*lam*eps*n2
 assert s.simplify(detuned*(n-2)/(2*An)).coeff(n2)==2*eps
 rows.append({'n':n,'lambda_n':str(lam),'two_center_Euler_coefficients':True,'critical_cancellation':True,'cosmic_center':True,'detuning_term':True})
Path(args.output).write_text(json.dumps({'checks':rows,'universal_proof':'REPORT.md; finiteEulerchecks n3..8'},indent=2)+'\n');print(json.dumps(rows))
