import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import argparse,json,itertools,time
from pathlib import Path
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();t0=time.time();checks={}
e,Z,Zd,al,sh,cs,sn=s.symbols('e Z Zd alpha shift cs sn',real=True)
a,H,k,ep,cY=s.symbols('a H k epsilon cY',positive=True)
z=e*Z*cs;zd=e*Zd*cs;zx=-e*k*Z*sn;zxx=-e*k*k*Z*cs
bx=-e*k*sh*sn;bxx=-e*k*k*sh*cs;N=1+e*al*cs
# ADM extrinsic trace combination through quadratic order in planar perturbations.
Lgrav=a**3*s.exp(3*z)*(-3*(H+zd)**2/N+2*(H+zd)*s.exp(-2*z)*(bxx+zx*bx)/(a*a*N)-N*s.exp(-2*z)*(2*zxx+zx*zx)/(a*a))
Lscalar=a**3*s.exp(3*z)*(ep*H*H/N-N*(3-ep)*H*H)
Lraw=s.series(Lgrav+Lscalar,e,0,3).removeO().expand().coeff(e,2)
Lavg=s.expand(Lraw).subs({cs**2:s.Rational(1,2),sn**2:s.Rational(1,2)})+a*cY*k*k*al*al/2
checks['no_remaining_spatial_phase']=not Lavg.has(cs,sn)
constraints=s.solve([s.diff(Lavg,al),s.diff(Lavg,sh)],[al,sh],dict=True)[0]
checks['shift_lapse_relation']=s.simplify(constraints[al]-Zd/H)==0
Lr=s.expand(Lavg.subs(constraints));cross=s.diff(Lr,Z,Zd)
# Integrate the symmetric Z*Zd term by parts using adot=aH,Hdot=-epsilon H².
dcross=s.diff(cross,a)*a*H+s.diff(cross,H)*(-ep*H*H)
Lfinal=s.expand(Lr-cross*Z*Zd-dcross*Z*Z/2)
expected=a**3*(ep+cY*k*k/(a*a*H*H))*Zd*Zd/2-a*ep*k*k*Z*Z/2
checks['ADM_reduced_action']=s.simplify(Lfinal-expected)==0
checks['decoupled_canonical']=s.simplify(Lfinal.subs(cY,0)-(a**3*ep*Zd*Zd-a*ep*k*k*Z*Z)/2)==0
P,A,KK,gamma=s.symbols('P A K gamma',positive=True)
Lp=P*A-(KK+gamma*k*k)*P*P/2
solP=s.solve(s.diff(Lp,P),P)[0]
checks['P_completing_square']=s.simplify(Lp.subs(P,solP)-A*A/(2*(KK+gamma*k*k)))==0
R={'checks':checks,'reduced_action':str(s.factor(Lfinal)),'rows':[],'scope':'Single canonical-clock, smooth stiffness, scalar-only FRW quadratic sector; no complete-action or observational PASS.'}
for es,ls,xs in itertools.product(['.05','.5','1'],['1e-8','1e-4','1'],['.01','1','1e4','1e8']):
 vals=[]
 for prec in [40,80]:
  with mp.workdps(prec):
   eps=mp.mpf(es);ell=mp.mpf(ls);x=mp.mpf(xs);den=eps+(1+eps*ell*ell)*x*x
   phase=mp.sqrt(eps*(1+ell*ell*x*x)/den)
   group=phase-eps*x*x/(phase*den*den)
   om=lambda xx:mp.sqrt(eps)*xx*mp.sqrt(1+ell*ell*xx*xx)/mp.sqrt(eps+(1+eps*ell*ell)*xx*xx)
   independent=mp.diff(om,x);coef=eps+x*x/(1+ell*ell*x*x)
   vals.append([phase,group,coef])
   if prec==80:
    R['rows'].append(dict(epsilon=float(eps),HL_over_sqrt2=float(ell),k_over_H=float(x),phase=float(phase),group=float(group),kinetic=float(coef),derivative_error=float(abs(group-independent)/(1+abs(group))),precision_error=float(max(abs(a-b)/(1+abs(a)) for a,b in zip(vals[1],vals[0]))),positive=bool(coef>0 and 0<group<=phase<=1),mutant_kinetic=float(eps-x*x/(1+ell*ell*x*x))))
checks.update(count=len(R['rows'])==48,positive_kinetic_and_speeds=all(r['positive'] for r in R['rows']),derivative=all(r['derivative_error']<1e-25 for r in R['rows']),precision=all(r['precision_error']<1e-25 for r in R['rows']),negative_control=any(r['mutant_kinetic']<0 for r in R['rows']))
R['seconds']=time.time()-t0
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(R,indent=2));print(json.dumps(dict(checks=checks,seconds=R['seconds']),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
