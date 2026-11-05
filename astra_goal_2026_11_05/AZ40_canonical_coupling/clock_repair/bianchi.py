#!/usr/bin/env python3
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,json,itertools
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
checks={};N,th,sh,b,T=S.symbols('N theta shear2 b T',positive=True)
F=b*T*T*(S.sqrt(1-th*th/T**2)-1)
L=N*(sh/N**2-th**2/(3*N**2)+F.subs(th,th/N))
constraint=S.diff(L,N).subs(N,1)
expected=-sh+th**2/3+b*T*T*(1/S.sqrt(1-th*th/T**2)-1)
checks['lapse_constraint_from_action']=S.simplify(constraint-expected)==0
r=S.symbols('r',nonnegative=True)
Fr=T*T*((1-S.exp(-2*r))/3+b*S.expm1(r)) if hasattr(S,'expm1') else T*T*((1-S.exp(-2*r))/3+b*(S.exp(r)-1))
checks['constraint_monotone']=S.simplify(S.diff(Fr,r)-T*T*(2*S.exp(-2*r)/3+b*S.exp(r)))==0
checks['zero_shear_known_answer']=Fr.subs(r,0)==0
rows=[];series={}
for idx,(bb,s0) in enumerate(itertools.product([.1,1.,10.],[1/3,3.])):
    tc=1/np.sqrt(3*s0);end=5*tc;times=np.linspace(0,end,501)
    def state(w):
        rhs=s0*np.exp(2*w)
        def fn(rr):return (-np.expm1(-2*rr))/3+bb*np.expm1(rr)-rhs
        upper=max(1.,np.log1p(rhs/bb)+1)
        rr=brentq(fn,0,upper,xtol=1e-13,rtol=1e-14)
        q=np.sqrt(-np.expm1(-2*rr))
        return rr,q
    def ode(t,y):return [state(float(y[0]))[1]]
    sols=[solve_ivp(ode,[0,end],[0.],method='DOP853',rtol=rt,atol=at,t_eval=times) for rt,at in [(1e-9,1e-11),(1e-11,1e-13)]]
    row=dict(b=bb,S0=s0,unregulated_crossing_time=tc,end_time=end,solvers_success=[bool(s.success) for s in sols])
    if all(s.success for s in sols):
        w=sols[1].y[0];vol=np.exp(-w);st=np.array([state(float(x)) for x in w]);rr=st[:,0];theta=-st[:,1]
        residual=abs(theta*theta/3+bb*np.expm1(rr)-s0*np.exp(2*w))/(1+s0*np.exp(2*w))
        lam=bb*theta*np.exp(rr)
        row.update(min_volume=float(min(vol)),volume_at_old_crossing=float(np.interp(tc,times,vol)),min_cap_gap=float(min(1+theta)),max_abs_auxiliary=float(max(abs(lam))),max_shear2=float(max(s0*np.exp(2*w))),volume_lower_bound=float(np.exp(-end)),bound_margin_min=float(min(vol-np.exp(-times))),constraint_error=float(max(residual)),volume_agreement=float(max(abs(np.exp(-sols[0].y[0])-vol)/(1+vol))))
        series[f'm{idx}_time']=times;series[f'm{idx}_volume']=vol;series[f'm{idx}_theta']=theta;series[f'm{idx}_auxiliary']=lam
    rows.append(row)
checks.update(count=len(rows)==6,solvers=all(all(r['solvers_success']) for r in rows),agreement=all(r.get('volume_agreement',np.inf)<1e-8 for r in rows),constraint=all(r.get('constraint_error',np.inf)<1e-10 for r in rows),finite_positive_volume=all(r.get('min_volume',0)>0 for r in rows),cap_not_reached=all(r.get('min_cap_gap',0)>0 for r in rows),volume_lower_bound=all(r.get('bound_margin_min',-1)>=-1e-12 for r in rows),unregulated_crossing_control=all(abs(1-np.sqrt(3*r['S0'])*r['unregulated_crossing_time'])<1e-14 and 1-np.sqrt(3*r['S0'])*r['end_time']<0 for r in rows))
result=dict(checks={k:bool(v) for k,v in checks.items()},models=rows,scope='Exact homogeneous vacuum Bianchi-I cap-operator test; not the rolling-scalar candidate or an inhomogeneous caustic evolution.')
out=Path(args.out);out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(out/'series.npz',**series)
print(json.dumps(result,indent=2));raise SystemExit(int(not all(checks.values())))
