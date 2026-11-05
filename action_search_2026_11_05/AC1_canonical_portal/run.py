#!/usr/bin/env python3
"""Frozen AC1 diagnostics; not the full constrained action spectrum."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
import argparse,json,hashlib,platform,time
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();t0=time.time()
checks={};out={'checks':checks,'histories':[],'mass_fixtures':[],'non_claim':'Not full constrained spectrum or action health; kappa fitted.'}
b,z,v,O=s.symbols('beta z v Omega',positive=True)
B=2*s.sqrt(3*(1-b))/(3*b);lam=s.sqrt(3*(1-b))*z
F=s.Matrix([-(z*z-1)*v/B,-(3-v*v/2-3*O/2)*v+lam*(3-v*v/2-3*O),O*(-3+v*v+3*O)])
ve=B*3*b/(2*z);oe=1-z**-2
sub={v:ve,O:oe};fz=s.simplify(F[0].subs(sub))
checks['exact_branch_tangent']=all(s.simplify(x)==0 for x in [F[1].subs(sub)-s.diff(ve,z)*fz,F[2].subs(sub)-s.diff(oe,z)*fz])
mut=oe/(1+b/z**2)
checks['wrong_density_mutant_rejected']=s.simplify((F[2].subs({v:ve,O:mut})-s.diff(mut,z)*F[0].subs({v:ve,O:mut})))!=0
J=s.simplify(F.jacobian([z,v,O]).subs({z:1,v:s.sqrt(3*(1-b)),O:0}))
out['late_jacobian']=str(J);out['late_eigenvalues']={str(k):n for k,n in J.eigenvals().items()}
expected=(-3*b,-3*(1+b)/2,-3*b)
x=s.symbols('x');checks['late_eigen_polynomial']=s.simplify(J.charpoly(x).as_expr()-s.prod(x-e for e in expected))==0
for beta in (1/3,2/3,.9):
 BB=float(B.subs(b,beta));ll=np.sqrt(3*(1-beta))
 def rhs(N,U):
  zz,vv,oo=U
  return [-(zz*zz-1)*vv/BB,-(3-vv*vv/2-1.5*oo)*vv+ll*zz*(3-vv*vv/2-3*oo),oo*(-3+vv*vv+3*oo)]
 for yy in (.3,1.):
  zz=1/np.tanh(yy); vv=BB*1.5*beta/zz;oo=1-1/zz**2
  for label,dv,do in [('exact',0,0),('v_plus',.01,0),('v_minus',-.01,0),('O_plus',0,.01),('O_minus',0,-.01),('both_plus',.01,.01)]:
   u0=[zz,vv*(1+dv),oo*(1+do)];tt=np.linspace(0,12,241)
   assert u0[1]**2/6+u0[2]<1
   sols=[solve_ivp(rhs,(0,12),u0,method='DOP853',rtol=r,atol=a,t_eval=tt) for r,a in [(1e-9,1e-11),(1e-11,1e-13)]]
   assert all(q.success and q.y.shape==(3,241) for q in sols)
   U=sols[1].y;rhoV=(1-U[2])/(1-U[2]-U[1]**2/6);tie=2/(1+beta)/rhoV
   conv=float(np.max(np.abs(sols[0].y-U)/(1+np.abs(U))))
   row=dict(beta=beta,y0=yy,case=label,convergence=conv,tie_initial=float(tie[0]-1),tie_final=float(tie[-1]-1),tie_max=float(np.max(np.abs(tie-1))),physical=bool(np.all(U[0]>=1-1e-12) and np.all(U[2]>=-1e-12) and np.all(U[1]**2/6+U[2]<1)))
   out['histories'].append(row)
checks['all_36_histories']=len(out['histories'])==36
checks['ODE_convergence']=all(r['convergence']<1e-6 for r in out['histories'])
checks['exact_tie_drift']=all(r['tie_max']<1e-7 for r in out['histories'] if r['case']=='exact')
checks['physical_domain']=all(r['physical'] for r in out['histories'])
# Independent chain-rule and direct fixed-p differentiation. Units G=1,K=4pi,Vstar=1.
for bb in ('0.333333333333333333333333333333333333333333333333333333333333333333333333333333333','0.666666666666666666666666666666666666666666666666666666666666666666666666666666667','.9'):
 for yy in ('.1','1','3'):
  for uu in ('.01','.5','.99'):
   vals=[]
   for prec in (40,80):
    with mp.workdps(prec):
     beta=mp.mpf(bb);y=mp.mpf(yy);u=mp.mpf(uu);q=(1-beta)/beta;BB=2*mp.sqrt(3*(1-beta))/(3*beta);xi=mp.mpf('.5')/(1+beta);K=4*mp.pi
     V=lambda phi:mp.sinh(phi/BB)**(-2*q)
     a=lambda phi:mp.sqrt(xi*V(phi));phi=BB*y;aa=a(phi);p=u*aa
     W=lambda phi,pp: a(phi)**2/K*(-pp/a(phi)-mp.log(1-pp/a(phi)))
     f=-u-mp.log(1-u);g=2*f-u*u/(1-u);gp=-u*u/(1-u)**2
     ap=mp.diff(a,phi);app=mp.diff(a,phi,2)
     direct=mp.diff(lambda ph:W(ph,p),phi,2)
     chain=(g-u*gp)*ap**2/K+aa*g*app/K
     wpp=1/(K*(1-u)**2);wpphi=-u*u*ap/(K*(1-u)**2)
     total=mp.diff(V,phi,2)+direct; schur=total-wpphi*wpphi/wpp
     vals.append([direct,chain,total,schur])
     if prec==80:
      out['mass_fixtures'].append(dict(beta=float(beta),y=float(y),u=float(u),chain_error=float(abs(direct-chain)/(1+abs(direct))),precision_error=float(abs(direct-vals[0][0])/(1+abs(direct))),fixed_p_mass_over_V=float(total/V(phi)),polarization_schur_over_V=float(schur/V(phi)),dropped_chain_mutant_error=float(abs(direct-(g-u*gp)*ap**2/K)/(1+abs(direct)))))
checks['mass_chain_identity']=all(r['chain_error']<1e-25 for r in out['mass_fixtures'])
checks['mass_precision']=all(r['precision_error']<1e-25 for r in out['mass_fixtures'])
checks['dropped_chain_mutant_rejected']=all(r['dropped_chain_mutant_error']>1e-25 for r in out['mass_fixtures'])
out['seconds']=time.time()-t0
out['software']={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__,'mpmath':mp.__version__}
out['inputs']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('FROZEN_CRITERIA.md')]}
p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2))
print(json.dumps({'checks':checks,'histories':len(out['histories']),'mass_fixtures':len(out['mass_fixtures']),'seconds':out['seconds']},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
