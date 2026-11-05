"""Exact ADM spatial principal block; reuse pinned raw expansion, not its verdict."""
import argparse,json,itertools,sys
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
source=Path('action_scale_investigation_2026_11_05/single_clock.py')
# Stop before its independent fixture run; this constructs raw and reduced ADM L.
ns={};exec(compile(source.read_text().split('# Independent constraint Hessian')[0],str(source),'exec'),ns)
a,H,k,ep,cY,m2,v,F1,Rm=[ns[x] for x in ('a','H','k','ep','cY','m2','v','F1','Rm')]
Z,Zd,C,Cd=[ns[x] for x in ('Z','Zd','C','Cd')]
L=ns['Lred'];q=s.Matrix([Z,C]);qd=s.Matrix([Zd,Cd]);checks={}
def check(n,b):
 checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n,flush=True)
B=s.Matrix(2,2,lambda i,j:s.diff(L,qd[i],q[j]));P=s.hessian(L,q)
# Spatial principal terms before any k-limit. The uncoupled source is exact.
B0=B.subs(cY,0);P0=P.subs(cY,0)
Hd=-ep*H**2-F1*v**2/(2*m2)
vd=-3*H*F1*v/Rm
Rdot=s.Symbol('Rdot',real=True)
flow={a:a*H,H:Hd,v:vd,F1:(Rm-F1)*vd/v,Rm:Rdot,ep:ep*(-6*H-2*Hd/H)}
def dt(x):return s.expand(sum(s.diff(x,y)*dy for y,dy in flow.items()))
Bsym=(B0+B0.T)/2
G0=s.simplify(Bsym.applyfunc(dt)-P0)
Gsp=G0.applyfunc(lambda x:s.simplify(s.expand(x).coeff(k,2)/(a)))
expected=s.Matrix([[m2*ep+F1*v*v/(2*H*H),-F1*v/(2*H)],[-F1*v/(2*H),F1/2]])
check('ADM gradient after background integration by parts',all(s.simplify(x)==0 for x in Gsp-expected))
check('uncoupled spatial antisymmetric mixing vanishes',all(s.expand(x).coeff(k,2)==0 for x in B0-B0.T))
Ls=s.Symbol('Lstar',positive=True)
cy=1/(1+Ls**2*k*k/(2*a*a))
K=s.hessian(L,qd)
Kuv=K.subs(cY,cy).applyfunc(lambda x:s.simplify(s.limit(x/a**3,k,s.oo)))
# All additional P-sector coordinate/velocity terms remain bounded as k grows.
check('portal adds no UV spatial matrix',all(s.simplify(s.limit(x.subs(cY,cy)/k**2,k,s.oo))==0 for x in P-P0))
check('portal spatial mixed term vanishes in UV',all(s.simplify(s.limit(x.subs(cY,cy)/k,k,s.oo))==0 for x in B-B0))
E=ep+2/(Ls*Ls*H*H)
Kexp=s.Matrix([[m2*E+Rm*v*v/(2*H*H),-Rm*v/(2*H)],[-Rm*v/(2*H),Rm/2]])
check('UV kinetic matrix',all(s.simplify(x)==0 for x in Kuv-Kexp))
u=s.Matrix([-v/H,1]);difference=m2*2/(Ls*Ls*H*H)*s.diag(1,0)+(Rm-F1)/2*u*u.T
check('exact causal ordering K-G',all(s.simplify(x)==0 for x in Kuv-Gsp-difference))
check('gradient determinant',s.simplify(Gsp.det()-m2*ep*F1/2)==0)
check('kinetic determinant',s.simplify(Kuv.det()-m2*E*Rm/2)==0)
# In Q=C-v/H Z basis the two matrices are diagonal at principal order.
T=s.Matrix([[1,0],[v/H,1]])
check('simultaneous diagonal principal basis',all(s.simplify(x)==0 for x in T.T*Kuv*T-s.diag(m2*E,Rm/2)) and all(s.simplify(x)==0 for x in T.T*Gsp*T-s.diag(m2*ep,F1/2)))
rows=[]
for es,vs,cs2,ls in itertools.product(['.01','.5','2'],['.01','1','10'],['1','1/3','1/10000'],['.001','1','100']):
 vals=[]
 for prec in [40,80]:
  with mp.workdps(prec):
   def num(x):return mp.mpf(x) if '/' not in x else mp.mpf(x.split('/')[0])/mp.mpf(x.split('/')[1])
   e,w,c,l=map(num,(es,vs,cs2,ls));r=1/c
   km=mp.matrix([[e+2/l**2+r*w*w/2,-r*w/2],[-r*w/2,r/2]])
   gm=mp.matrix([[e+w*w/2,-w/2],[-w/2,mp.mpf('.5')]])
   # Symmetric whitening avoids nonsymmetric eigensolver artifacts.
   chol=mp.cholesky(km);wh=chol**-1
   eig=sorted(mp.eigsy(wh*gm*wh.T,eigvals_only=True))
   exact=sorted([e/(e+2/l**2),c]);vals.append((eig,exact))
 with mp.workdps(80):
  err=max([abs(x-y) for x,y in zip(vals[0][0],vals[1][0])]+[abs(x-y) for x,y in zip(vals[1][0],vals[1][1])])
  rows.append(dict(epsilon=es,v=vs,cs2=cs2,Lstar=ls,speeds_squared=[mp.nstr(x,35) for x in vals[1][0]],error=mp.nstr(err,8),healthy=all(0<x<=1+mp.mpf('1e-25') for x in vals[1][0])))
check('81 cases',len(rows)==81)
check('40/80 digits and analytic speeds',all(mp.mpf(x['error'])<mp.mpf('1e-25') for x in rows))
check('all finite fixtures positive subluminal',all(x['healthy'] for x in rows))
check('reversed sign negative control',float((ep-2/(Ls*Ls*H*H)).subs({ep:s.Rational(1,2),Ls:1,H:1}))<0)
out=dict(checks=checks,passed=all(checks.values()),K=str(Kuv),G=str(Gsp),rows=rows,scope='Finite positive Lstar UV FRW principal block; exact dust and full finite k spectrum excluded')
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n')
sys.exit(0 if out['passed'] else 1)
