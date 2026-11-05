"""FRW two-scalar constrained kinetic block, not full action-health proof."""
import argparse
import itertools
import json
from pathlib import Path
import sys
import sympy as s
import mpmath as mp

ap=argparse.ArgumentParser()
ap.add_argument('--out',required=True)
ap.add_argument('--mutate',action='store_true')
args=ap.parse_args()
checks={}
def check(name,ok):
    checks[name]=bool(ok)
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)

e,Z,Zd,C,Cd,al,sh,cs,sn=s.symbols('e Z Zd C Cd alpha shift cs sn',real=True)
a,H,k,ep,cY,m2,v,F1,Rm=s.symbols('a H k epsilon cY M2 v F1 Rm',positive=True)
F0,F2=s.symbols('F0 F2',real=True)
z=e*Z*cs;zd=e*Zd*cs;zx=-e*k*Z*sn;zxx=-e*k*k*Z*cs
bx=-e*k*sh*sn;bxx=-e*k*k*sh*cs;N=1+e*al*cs
Lgrav=m2*a**3*s.exp(3*z)*(-3*(H+zd)**2/N+2*(H+zd)*s.exp(-2*z)*(bxx+zx*bx)/(a*a*N)-N*s.exp(-2*z)*(2*zxx+zx*zx)/(a*a))
Q=ep*m2*H*H
V=3*m2*H*H-Q-v*v*F1+F0
Lclock=a**3*s.exp(3*z)*(Q/N-N*V)
# Y expanded directly from inverse ADM metric, including shift cross term.
psi_x=-e*k*C*sn
psi_dot=v+e*Cd*cs
shift_contraction=s.exp(-2*z)/a**2*bx*psi_x
Y=(psi_dot-shift_contraction)**2/(2*N*N)-s.exp(-2*z)*psi_x**2/(2*a*a)
dY=s.series(Y-v*v/2,e,0,3).removeO()
Lmatter=a**3*s.exp(3*z)*N*(F0+F1*dY+F2*dY**2/2)
Lraw=s.series(Lgrav+Lclock+Lmatter,e,0,3).removeO().expand().coeff(e,2)
Lavg=s.expand(Lraw).subs({cs**2:s.Rational(1,2),sn**2:s.Rational(1,2)})
check('spatial average has no residual phase',not Lavg.has(cs,sn))
sign=-1 if args.mutate else 1
Lavg+=sign*m2*a*cY*k*k*al*al/2
constraints=s.solve([s.diff(Lavg,al),s.diff(Lavg,sh)],[al,sh],dict=True)[0]
alpha_expected=Zd/H+F1*v*C/(2*m2*H)
check('momentum constraint includes matter',s.simplify(constraints[al]-alpha_expected)==0)
Lred=s.expand(Lavg.subs(constraints)).subs(F2,(Rm-F1)/v**2)
Kmat=s.simplify(s.hessian(Lred,(Zd,Cd)))
E=ep+sign*cY*k*k/(a*a*H*H)
expected=a**3*s.Matrix([[m2*E+Rm*v*v/(2*H*H),-Rm*v/(2*H)],[-Rm*v/(2*H),Rm/2]])
check('exact constrained kinetic matrix',all(s.simplify(x)==0 for x in Kmat-expected))
det=s.factor(Kmat.det())
check('exact determinant',s.simplify(det-a**6*m2*Rm*E/2)==0)
check('P-decoupled determinant',s.simplify(det.subs(cY,0)-a**6*m2*Rm*ep/2)==0)
check('symmetric matrix',Kmat==Kmat.T)

# Independent constraint Hessian Schur elimination from the raw density.
Kfull=s.hessian(Lavg,(Zd,Cd,al,sh)).subs(F2,(Rm-F1)/v**2)
Schur=s.simplify(Kfull[:2,:2]-Kfull[:2,2:]*Kfull[2:,2:].inv()*Kfull[2:,:2])
check('direct raw Hessian Schur elimination',all(s.simplify(x)==0 for x in Schur-Kmat))
fn=s.lambdify((a,H,k,ep,cY,m2,v,F1,Rm),Schur,'mpmath')
rows=[]
for es,vs,cs2,cy,kk in itertools.product(['.05','.5'],['.1','1'],['1','1/3','1/10000'],['0','.5','1'],[1,100]):
    vals=[]
    def number(x):
        if '/' in x:
            num,den=x.split('/')
            return mp.mpf(num)/mp.mpf(den)
        return mp.mpf(x)
    for dps in [40,80]:
        with mp.workdps(dps):
            ee,vv,cc,yy=map(number,(es,vs,cs2,cy))
            matrix=fn(1,1,kk,ee,yy,1,vv,1,1/cc)
            dm=mp.det(matrix)
            dt=(ee+sign*yy*kk*kk)/(2*cc)
            vals.append([matrix[0,0],matrix[0,1],matrix[1,1],dm,dt])
    with mp.workdps(80):
        err=max(abs(x-y)/max(1,abs(y)) for x,y in zip(vals[0],vals[1]))
        err=max(err,abs(vals[1][3]-vals[1][4])/max(1,abs(vals[1][4])))
        rows.append({'epsilon_clock':es,'v':vs,'matter_cs2':cs2,'cY':cy,'k':kk,
                     'det':mp.nstr(vals[1][3],35),'normalized_error':mp.nstr(err,8),
                     'positive':bool(vals[1][2]>0 and vals[1][3]>0)})
check('72 frozen fixtures',len(rows)==72)
check('40/80 digit matrix agreement',all(mp.mpf(x['normalized_error'])<mp.mpf('1e-30') for x in rows))
check('positive kinetic on all fixtures',all(x['positive'] for x in rows))
out={'mode':'reversed_polarization' if args.mutate else 'main','checks':checks,
     'passed':all(checks.values()),'matrix':str(Kmat),'determinant':str(det),
     'lapse':str(constraints[al]),'rows':rows,
     'scope':'FRW finite-sound-speed matter and canonical single-clock kinetic block only; b is not selected.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True)
Path(args.out).write_text(json.dumps(out,indent=2)+'\n')
sys.exit(0 if out['passed'] else 1)
