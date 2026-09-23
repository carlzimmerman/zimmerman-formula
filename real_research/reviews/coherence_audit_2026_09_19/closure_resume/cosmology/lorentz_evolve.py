"""Evolve a full fundamental matrix in regular charge coordinates.

Reports finite-interval transfer, not instantaneous stability or a proof.
The third coordinate is H*P/Q to give a fixed dimensionless comparison norm.
"""
from pathlib import Path
import json, math
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp

here=Path(__file__).resolve().parent
d=json.loads((here/'lorentz_canonical.json').read_text())
variables=[s.sympify(z) for z in d['variables']]
mf=s.lambdify(variables,s.sympify(d['matrix_N']),'numpy',cse=True)
of=s.lambdify(variables,s.sympify(d['observables']),'numpy',cse=True)
rows=[]
eps=1e-9;hub=299792458/67400
for mode,a0,km,dn in [('constant',.1,.1,.1),('constant',.1,.001,.5),('constant',.01,.001,.5),('constant',.001,.1,.5),('constant',.5,.001,.5)]:
    b=1/39998 if mode=='constant' else .03
    gc=1+1.5*b;j0=-1.86/(1-eps);lam=3*gc-(eps-1)*j0/2
    def bg(n):
        a=math.exp(n);q=1-3*eps*n;j=j0/a**3
        h=math.sqrt(((eps-q)*j/2+lam)/(3*gc));hd=q*j/(4*gc)
        if mode=='constant':alpha=1/40000;ad=0
        else:
            v=1e-7*a**-4;alpha=.5*v/(.5+v);ad=-4*h*alpha*(1-2*alpha)
        args=[a,h,q,j,eps,4e-6/hub,km*hub,alpha,ad,b]
        scale=np.diag([1,1,q/h,1]);invs=np.diag([1,1,h/q,1])
        return args,scale,invs,hd/h**2+3*eps/q
    def matrices(n):
        args,sc,iv,dlog=bg(n)
        B=iv@np.asarray(mf(*args))@sc
        B[2,2]+=dlog
        O=np.asarray(of(*args))@sc
        return B,O
    n0=math.log(a0);n1=n0+dn
    ends=[]
    for tolerance in [1e-9,1e-11]:
        sol=solve_ivp(lambda n,yy:(matrices(n)[0]@yy.reshape(4,4)).ravel(),
                      (n0,n1),np.eye(4).ravel(),method='DOP853',rtol=tolerance,
                      atol=tolerance*1e-3,max_step=dn/100)
        assert sol.success,sol.message
        ends.append(sol.y[:,-1].reshape(4,4))
    transfer=ends[-1];_,O0=matrices(n0);_,O1=matrices(n1)
    relative=float(np.linalg.norm(ends[0]-ends[1])/np.linalg.norm(ends[1]))
    assert relative<1e-5,relative
    row={'case':mode,'a_start':a0,'a_end':math.exp(n1),'k_Mpc_inv':km,'delta_N':dn,
         'state':['Phi','Phi_N','H*P/Q','canonical_charge_contrast'],
         'fundamental_matrix':transfer.tolist(),'state_singular_values':np.linalg.svd(transfer,compute_uv=False).tolist(),
         'observable_names':d['observable_names'],'initial_observable_matrix':O0.tolist(),
         'final_observable_transfer':(O1@transfer).tolist(),'relative_tolerance_disagreement':relative,
         'max_final_Bardeen_over_unit_initial_state':float(np.linalg.norm((O1@transfer)[4,:])),
         'max_initial_Bardeen_over_unit_initial_state':float(np.linalg.norm(O0[4,:]))}
    rows.append(row)
    print(mode,a0,km,dn,'singular max',row['state_singular_values'][0],
          'Bardeen',row['max_initial_Bardeen_over_unit_initial_state'],row['max_final_Bardeen_over_unit_initial_state'],flush=True)
(here/'lorentz_evolution.json').write_text(json.dumps(rows,indent=2)+'\n')
