"""Finite-box dependence of quantum growth, grouped by exactly equal momentum."""
import json,math,itertools
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=Path(__file__).parent
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
m=params['m_eV'];u=params['u'];eps=params['epsilon'];R=params['M_eV']/m;kappa=params['kappa']
rows=[];checks=[]
for dq in [.4,.2,.1,.05]:
    radius=round(2/dq);counts=Counter()
    for idx in itertools.product(range(-radius,radius+1),repeat=3):
        n2=sum(i*i for i in idx)
        if idx>(0,0,0) and 0<n2<=radius*radius:counts[n2]+=1
    shell=np.array(sorted(counts));deg=np.array([counts[int(i)] for i in shell]);q2=dq*dq*shell;K=len(shell)
    Ns=params['rho_source_eV4']/params['M_eV']*(2*math.pi/(dq*m*u))**3
    w=deg/Ns
    d=2*(u*u*q2-u*u)/(eps*(np.sqrt(1+u*u*q2)+math.sqrt(1+u*u)))
    def rhs(t,y):
        B=y[0];C=y[1:K+1];F=y[K+1:].real;S=F.sum();Z=C.sum();pair=B+kappa*Z
        return np.r_[-1j*C.sum(),-1j*(d+4*kappa*S)*C-1j*pair*(2*F+w),-2*np.imag(np.conj(pair)*C)]
    def event(t,y):return y[K+1:].real.sum()-1e-4
    event.terminal=True;event.direction=1
    initial=np.zeros(2*K+1,complex);initial[0]=1
    sol=solve_ivp(rhs,(0,100),initial,method='DOP853',rtol=1e-12,atol=np.r_[1e-13,w*1e-13,w*1e-13],max_step=.02,events=event)
    reached=len(sol.t_events[0])==1
    y=sol.y[:,-1];B=y[0];C=y[1:K+1];F=y[K+1:].real
    check=dict(name='completed and conserved dq'+str(dq),passed=bool(sol.success and reached and abs(abs(B)**2+F.sum()-1)<1e-8));checks.append(check)
    neff=float(F.sum()**2/np.sum(F*F/deg))
    # Exact Gaussian charge variance: each pair contributes 2 s^2+2|d_pair|^2.
    fp=F/deg;wp=1/Ns;s=(fp+wp/2)/2;dp2=fp*(fp+wp)/4
    relative_std=float(math.sqrt(np.sum(deg*(2*s*s+2*dp2)))/np.sum(F))
    row=dict(dq=dq,pair_count=int(sum(deg)),shell_count=K,handoff_x=float(sol.t[-1]),effective_pairs=neff,relative_sampled_daughter_charge_std=relative_std,B=[float(B.real),float(B.imag)],source_quanta=Ns,shell_squared_indices=shell.tolist(),degeneracy=deg.tolist(),F=F.tolist(),C_real=C.real.tolist(),C_imag=C.imag.tolist())
    rows.append(row);print(json.dumps({k:row[k] for k in ['dq','pair_count','shell_count','handoff_x','effective_pairs','relative_sampled_daughter_charge_std']}),flush=True)
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),non_claims=['Early Gaussian evolution only','No spatial nonlinear box-convergence result','No expansion','No quantum-classical error theorem'])
(p/'box_handoff_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Checks:',len(checks),out['all_pass']);assert out['all_pass']
