"""Radiation-background finite quantum conversion and a future-return bound."""
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import csr_matrix

checks=[]
def check(name, passed, value=None):
    checks.append(dict(name=name, passed=bool(passed), value=value))

def basis(N,K):
    def generate(left,k,prefix):
        if k==0:
            yield tuple(prefix)
        else:
            for n in range(left+1):
                yield from generate(left-n,k-1,prefix+[n])
    return list(generate(N,K,[]))

def simulate(N, q, eta=.08, h=.03, u=.001, tol=2e-9):
    q=np.array(q); K=len(q); states=basis(N,K)
    ns=np.array(states,dtype=float); total=ns.sum(axis=1)
    lookup={n:i for i,n in enumerate(states)}; dim=len(states)
    matrices=[]; norm_bounds=[]
    for j in range(K):
        rr=[]; cc=[]; vv=[]
        for i,n in enumerate(states):
            if sum(n)<N:
                dest=list(n); dest[j]+=1; dest=lookup[tuple(dest)]
                v=(n[j]+1)*math.sqrt(N-sum(n))
                rr.extend([i,dest]); cc.extend([dest,i]); vv.extend([v,v])
        T=csr_matrix((vv,(rr,cc)),shape=(dim,dim))
        matrices.append(T)
        # Exact arithmetic formula for entries; induced infinity norm bounds 2-norm.
        norm_bounds.append(float(np.max(np.asarray(abs(T).sum(axis=1)))))
    norm_bounds=np.array(norm_bounds)
    wr=math.sqrt(1+u*u); ai=.5
    def parts(x):
        a=math.sqrt(ai*ai+2*h*x)
        w=np.sqrt(1+(u*q/a)**2)
        delta=2*(q*q/a**2-1)/(w+wr)
        g=eta*a**(-1.5)*wr/w
        dp=-2*h*q*q/(a**4*w)
        gp=g*(-1.5*h/a**2+h*u*u*q*q/(a**4*w*w))
        return a,w,delta,g,dp,gp
    def action(psi, diag, g):
        out=(ns@diag)*psi
        for coef,T in zip(g,matrices): out=out+coef*(T@psi)
        return out
    def rhs(x,z):
        psi=z[:-1]; _,_,delta,g,dp,gp=parts(x)
        Hpsi=action(psi,delta,g)
        work=float(np.vdot(psi,action(psi,dp,gp)).real)
        return np.r_[-1j*Hpsi,work+0j]
    z0=np.zeros(dim+1,dtype=complex); z0[lookup[(0,)*K]]=1
    scales=np.array([.5,1,2,4,8,16.])
    times=(scales**2-ai*ai)/(2*h)
    sol=solve_ivp(rhs,(0,times[-1]),z0,method='DOP853',t_eval=times,rtol=tol,atol=tol/50)
    check(f'N{N} K{K} eta{eta} tol{tol}: integration',sol.success)
    snapshots=[]; maxnorm=0; maxwork=0
    d=2/(wr+1)  # (M-2m)/(m u^2), positive.
    for x,z in zip(sol.t,sol.y.T):
        psi=z[:-1]; prob=abs(psi)**2
        a,w,delta,g,_,_=parts(x)
        nmean=float(total@prob); energy=float(np.vdot(psi,action(psi,delta,g)).real)
        maxnorm=max(maxnorm,abs(float(prob.sum())-1))
        maxwork=max(maxwork,abs(energy-z[-1].real))
        # Each positive coefficient in R=H+d n decreases to zero for these u,q,a.
        # Integral ||R'|| <= B using triangle inequality and ||n_j||=N.
        kin=2*q*q/a**2/(w+1)
        B=N*float(kin.sum())+float(g@norm_bounds)
        future_fraction_change_bound=2*B/(d*N)
        snapshots.append(dict(a=a,converted_fraction=nmean/N,
            per_mode_pairs=(ns.T@prob).tolist(),energy=energy,work=float(z[-1].real),
            future_fraction_change_bound=future_fraction_change_bound,
            limiting_fraction_lower_bound=max(0,nmean/N-future_fraction_change_bound)))
    check(f'N{N} K{K} eta{eta} tol{tol}: norm',maxnorm<2e-6,maxnorm)
    check(f'N{N} K{K} eta{eta} tol{tol}: pressure and interaction work',maxwork<2e-5,maxwork)
    if eta==0:
        check('zero-coupling no-production control',snapshots[-1]['converted_fraction']==0)
    return dict(N=N,q=q.tolist(),eta=eta,h=h,u=u,dimension=dim,
                evaluations=sol.nfev,snapshots=snapshots,max_norm_error=maxnorm,
                max_work_error=maxwork,operator_norm_bounds=norm_bounds.tolist())

rows=[simulate(4,[.7,1,1.4]),simulate(8,[.7,1,1.4]),
      simulate(4,[.7,1,1.4],tol=2e-10),simulate(4,[.7,1,1.4],eta=0)]
diff=max(abs(a['converted_fraction']-b['converted_fraction'])
         for a,b in zip(rows[0]['snapshots'],rows[2]['snapshots']))
check('tighter integration agrees',diff<2e-6,diff)
for r in rows[:2]:
    check(f'N{r["N"]}: nonzero future lower bound',r['snapshots'][-1]['limiting_fraction_lower_bound']>0)
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),
         non_claims=['Finite mode model, not continuum','Imposed radiation background, no Friedmann backreaction',
                     'No microscopic parameter fit or abundance selection','No halo force law'])
(Path(__file__).parent/'expansion_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:
    print(json.dumps({k:r[k] for k in ['N','eta','dimension','max_norm_error','max_work_error']}))
    print(json.dumps(r['snapshots'][-1]))
print('checks',len(checks),'pass',out['all_pass'])
assert out['all_pass']
