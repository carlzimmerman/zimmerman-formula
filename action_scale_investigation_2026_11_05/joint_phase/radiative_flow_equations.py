"""Check the steady coupled material/conduction/gravity energy equations."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args()
r,n,u,T,F,m,G,M,J,K,kap,ui,ein,phi,C=s.symbols('r n u T F m G M J K kap ui ein phi C',positive=True)
Tp=-F/kap;q=J/n;phip=G*M/r**2
np=n*(-m*u*(q-K*n-2*u/r)-m*phip+m*q*(ui-u)-Tp)/(T-m*u*u)
up=q-K*n-2*u/r-u*np/n
cv=s.Rational(3,2);cp=cv+1;erel=ein-m*u*ui+m*u*u/2
Fp=J*(erel-cv*T)-n*cv*u*Tp-n*T*(up+2*u/r)-C-2*F/r
checks={}
def eq(name,a,b):checks[name]=bool(s.simplify(a-b)==0)
eq('coupled continuity',u*np+n*up+2*n*u/r,J-K*n*n)
eq('coupled momentum',u*up,-(T*np/n+Tp)/m-phip+q*(ui-u))
eq('coupled internal energy',n*cv*u*Tp+n*T*(up+2*u/r),J*(erel-cv*T)-C-Fp-2*F/r)
B=cv*T+m*u*u/2+m*phi
fluxdiv=(J-K*n*n)*(B+T)+n*u*(cp*Tp+m*u*up+m*phip)+Fp+2*F/r
expected=J*(ein+m*phi)-K*n*n*B-C
eq('coupled conservative total energy',fluxdiv,expected)
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'scope':'Steady equations in a stationary Newtonian potential, checked algebraically; no solved boundary value problem.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values()) else 1)
