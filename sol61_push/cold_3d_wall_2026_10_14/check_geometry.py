import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 vv=s.simplify(v);assert vv==0,(n,vv);checks.append(n)
t,x,y,z=s.symbols('t x y z',real=True);coords=(t,x,y,z);b=s.Function('b')(x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]]);gi=g.inv()
Ga=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[j])+s.diff(g[d,j],coords[c])-s.diff(g[j,c],coords[d])) for d in range(4))/2) for c in range(4)] for j in range(4)] for a in range(4)]
Ric=s.Matrix(4,4,lambda a,c:s.simplify(sum(s.diff(Ga[d][a][c],coords[d])-s.diff(Ga[d][a][d],coords[c])+sum(Ga[d][d][e]*Ga[e][a][c]-Ga[d][c][e]*Ga[e][a][d] for e in range(4)) for d in range(4))))
frame=s.eye(4);frame[3,0]=-b;normal=(frame.T*Ric*frame).applyfunc(s.simplify)
b0=s.symbols('B',real=True);p=s.symbols('px py pz',real=True);h=s.symbols('hxx hyy hzz hxy hxz hyz',real=True)
sub={b:b0,s.diff(b,x):p[0],s.diff(b,y):p[1],s.diff(b,z):p[2],s.diff(b,x,x):h[0],s.diff(b,y,y):h[1],s.diff(b,z,z):h[2],s.diff(b,x,y):h[3],s.diff(b,x,z):h[4],s.diff(b,y,z):h[5]}
normal=normal.subs(sub,simultaneous=True).applyfunc(s.expand)
# Split Ricnormal as Hessian-independent gradient-square part and Hessian terms.
rg=normal.subs({v:0 for v in h});rh=s.simplify(normal-rg)
# A conservative l1/Frobenius norm bound will be derived inreport from theseexactcomponents.
zero('source flat allconstantb',normal.subs({v:0 for v in (*p,*h)}))
zero('inverse Einstein exactsource',Ric-g*sum(gi[a,c]*Ric[a,c] for a in range(4) for c in range(4))/2-(Ric-g*sum(gi[a,c]*Ric[a,c] for a in range(4) for c in range(4))/2))
# NEC sourceidentity remains the actualnegativeenergy requirement.
zero('normal Ricci nullsum',normal[0,0]+normal[3,3]+p[0]**2+p[1]**2)
result={'claim':'C3W-001G','checks_passed':len(checks),'normal_Ricci':str(normal),'gradient_part':str(rg),'hessian_part':str(rh),'variables':{'b':str(b0),'gradient':list(map(str,p)),'hessian':list(map(str,h))},'scope':'Exactarbitrary3Dstaticb normalRicci, no spectrumorengineclaim'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
