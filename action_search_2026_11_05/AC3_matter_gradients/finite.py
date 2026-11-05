"""Full frozen two-field frequencies on an explicit on-shell background."""
import argparse,json,itertools,sys
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
source=Path('action_scale_investigation_2026_11_05/single_clock.py')
ns={};exec(compile(source.read_text().split('# Independent constraint Hessian')[0],str(source),'exec'),ns)
a,H,k,ep,cY,m2,v,F1,Rm=[ns[x] for x in ('a','H','k','ep','cY','m2','v','F1','Rm')]
Z,Zd,C,Cd=[ns[x] for x in ('Z','Zd','C','Cd')]
Ls=s.Symbol('Lstar',positive=True);cy=1/(1+Ls**2*k*k/(2*a*a))
L=s.expand(ns['Lred'].subs({F1:1,Rm:1,ns['F0']:v*v/2,cY:cy}))
qd=s.Matrix([Zd,Cd]);q=s.Matrix([Z,C]);K=s.simplify(s.hessian(L,qd))
B=s.Matrix(2,2,lambda i,j:s.diff(L,qd[i],q[j]));P=s.hessian(L,q)
Hd=-ep*H**2-v**2/(2*m2)
flow={a:a*H,H:Hd,v:-3*H*v,ep:ep*(-6*H-2*Hd/H)}
def dt(x):return sum(s.diff(x,y)*dy for y,dy in flow.items())
G=s.simplify(((B+B.T)/2).applyfunc(dt)-P);A=s.simplify(B-B.T)
w=s.Symbol('omega',real=True);x=s.Symbol('x',real=True)
poly=K.det()*x*x-(K[0,0]*G[1,1]+K[1,1]*G[0,0]-2*K[0,1]*G[0,1]+A[0,1]**2)*x+G.det()
checks={}
def check(n,b):checks[n]=bool(b);print(('PASS ' if b else 'FAIL ')+n,flush=True)
check('exact mixed frequency determinant',s.simplify((-w*w*K+s.I*w*A+G).det()-poly.subs(x,w*w))==0)
fn=s.lambdify((a,H,k,ep,m2,v,Ls),(K,G,A),'mpmath')
rows=[]
for es,ms,ls,ks in itertools.product(['.05','.5','2'],['.01','.3','.9'],['.001','1','100'],['10','100','10000']):
 vals=[]
 for prec in [40,80]:
  with mp.workdps(prec):
   e,em,l,kk=map(mp.mpf,(es,ms,ls));vv=mp.sqrt(2*em)
   km,gm,am=fn(1,1,kk,e,1,vv,l)
   c2=mp.det(km);c1=-(km[0,0]*gm[1,1]+km[1,1]*gm[0,0]-2*km[0,1]*gm[0,1]+am[0,1]**2);c0=mp.det(gm)
   disc=c1*c1-4*c2*c0
   # Stable quadratic roots, including negative or complex cases.
   big=(-c1+mp.sqrt(disc))/(2*c2);small=c0/(c2*big)
   errors=[]
   for om in map(mp.mpf,['.1','1','10','100']):
    direct=mp.det(gm-om*om*km+1j*om*am);expanded=c2*om**4+c1*om**2+c0
    errors.append(abs(direct-expanded)/max(1,abs(expanded)))
   vals.append([small,big,c2,c1,c0,max(errors)])
 with mp.workdps(80):
  err=max(abs(z-y)/max(1,abs(y)) for z,y in zip(vals[0],vals[1]))
  roots=vals[1][:2]
  rows.append(dict(epsilon_phi=es,epsilon_m=ms,Lstar=ls,k=ks,omega2=[mp.nstr(z,35) for z in roots],negative_roots=sum(mp.im(z)==0 and mp.re(z)<0 for z in roots),complex_roots=any(mp.im(z)!=0 for z in roots),error=mp.nstr(err,8),direct_error=mp.nstr(vals[1][-1],8)))
check('81 cases',len(rows)==81)
check('40/80 digit agreement',all(mp.mpf(r['error'])<mp.mpf('1e-25') for r in rows))
check('direct determinant numerical agreement',all(mp.mpf(r['direct_error'])<mp.mpf('1e-25') for r in rows))
out=dict(checks=checks,passed=all(checks.values()),K=str(K),G=str(G),A=str(A),rows=rows,negative_cases=sum(r['negative_roots']>0 for r in rows),complex_cases=sum(r['complex_roots'] for r in rows))
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2)+'\n')
print('Negative cases:',out['negative_cases'],'Complex cases:',out['complex_cases'],flush=True)
sys.exit(0 if out['passed'] else 1)
