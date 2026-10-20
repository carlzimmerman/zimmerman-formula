"""Declared linear density-drive response with exact free exterior ghost ratios.

This measures susceptibility to an imposed source, not a natural merger rate.
The completed run owns all outputs. Original background sources remain read-only.
"""
from pathlib import Path
import cmath
import json
import math
import resource
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix, diags, eye
from scipy.sparse.linalg import splu

HERE = Path(__file__).resolve().parent
CHECKS = []

def check(name, passed, **data):
    CHECKS.append(dict(name=name, passed=bool(passed), **data))

def poly(ell, z, closed=False):
    if ell == 0:
        return 1.0
    if closed:
        return 1 + 1/z if ell == 1 else 1 + 3/z + 3/z**2
    return 1 - 1j/z if ell == 1 else 1 - 3j/z - 3/z**2

def ghost_ratio(ell, p2, r, dr):
    """c(r+dr)/c(r), on outgoing circular or real-decaying branch."""
    if abs(p2) < 1e-14:
        return complex((r/(r+dr))**ell)
    if p2 > 0:
        p = math.sqrt(p2)
        return cmath.exp(-1j*p*dr)*poly(ell,p*(r+dr))/poly(ell,p*r)
    kap = math.sqrt(-p2)
    return complex(math.exp(-kap*dr)*poly(ell,kap*(r+dr),True)/poly(ell,kap*r,True))

def circular_transform():
    # Real canonical order is (u,s,chi,v,t), with complex components sqrt2-scaled.
    T = np.zeros((5,5),complex)
    T[0,0]=T[1,0]=T[2,1]=T[3,1]=1/math.sqrt(2)
    T[0,3]=T[2,4]=1j/math.sqrt(2)
    T[1,3]=T[3,4]=-1j/math.sqrt(2)
    T[4,2]=1
    return T

def preflight():
    rho=ghost_ratio(0,.36,10.,.1)
    check('l0 outgoing phase and flux sign',abs(rho-cmath.exp(-.06j))<1e-13 and rho.imag<0)
    for ell in [0,2]:
        check('closed real decaying ghost ell'+str(ell),0<ghost_ratio(ell,-10000.,40.,.1).real<1 and ghost_ratio(ell,-10000.,40.,.1).imag==0)
    T=circular_transform()
    check('circular transform unitary',np.linalg.norm(T@T.conj().T-np.eye(5))<1e-14)
    w=.92;O=.25;MX2=4.0016
    V=np.diag([1-w*w,MX2-4*w*w,10000.,1-w*w,MX2-4*w*w])
    G=np.zeros((5,5));G[0,3]=-2*w;G[3,0]=2*w;G[1,4]=-4*w;G[4,1]=4*w
    want=np.diag([1-(w+O)**2,1-(w-O)**2,MX2-(2*w+O)**2,MX2-(2*w-O)**2,10000-O*O])
    check('correct circular sideband frequencies',np.linalg.norm(T@(V-O*O*np.eye(5)+1j*O*G)@T.conj().T-want)<1e-11)
    # An open minus phasor is outgoing h2; its physical amplitude is conjugated.
    nu=w-2.2;p=math.sqrt(nu*nu-1);rr=ghost_ratio(0,p*p,10.,.1)
    check('negative charge branch physical outgoing energy',nu<0 and rr.imag<0 and 2*nu*(-p)>0 and 2*(-p)<0)
    # Independent scalar driven discrete work identity, before coupled fragments.
    n=20;h=.1;p=.6;O=.7
    H=diags([-np.ones(n-1),2*np.ones(n)-p*p*h*h,-np.ones(n-1)],[-1,0,1],format='csc')/(h*h)
    H=H.astype(complex);rho=ghost_ratio(0,p*p,n*h,h)
    H[-1,-1]-=rho/(h*h)
    F=np.exp(-((np.arange(1,n+1)*h-.5)/.2)**2).astype(complex)
    y=splu(H).solve(F)
    edge=-2*O/h*np.imag(np.conj(y[-1])*rho*y[-1]);work=2*O*np.imag(h*np.vdot(y,F))
    check('free scalar discrete outgoing work flux',edge>0 and abs(edge-work)/edge<1e-11,edge=float(edge),work=float(work))
    check('free scalar finite difference versus continuum sinc',abs(edge/(2*O*p*abs(y[-1])**2)-math.sin(p*h)/(p*h))<1e-12)
    return {'checks':CHECKS.copy(),'all_pass':all(c['passed'] for c in CHECKS)}

def solve_drive(op, Omega, params, amp=1.0):
    N=op['N'];r=op['r'];dr=op['dr'];ell=op['ell'];rec=op['record'];w=rec['omega'];T=circular_transform()
    nus=np.array([w+Omega,w-Omega,2*w+Omega,2*w-Omega,Omega])
    mus=np.array([1.,1.,math.sqrt(params['MX2']),math.sqrt(params['MX2']),params['M_chi']])
    p2=nus*nus-mus*mus
    rho=np.array([ghost_ratio(ell,x,r[-1],dr) for x in p2])
    B=T.conj().T@np.diag(rho)@T
    ends=np.array([j*N+N-1 for j in range(5)])
    ii=np.repeat(ends,5);jj=np.tile(ends,5)
    edgeop=coo_matrix((-B.reshape(-1)/(dr*dr),(ii,jj)),shape=(5*N,5*N)).tocsc()
    A=(op['W']-Omega*Omega*eye(5*N,format='csc')+1j*Omega*op['G']+edgeop).tocsc()
    f,b,h=op['fields'];shape=np.maximum(0,1-r*r/100.)**4
    shape[r>=10]=0.
    raw=-math.sqrt(2)*r*f*shape
    raw_norm=math.sqrt(dr*np.dot(raw,raw))
    F=np.zeros(5*N,complex);F[:N]=amp*raw/raw_norm
    lu=splu(A);y=lu.solve(F)
    relres=float(np.linalg.norm(A@y-F)/np.linalg.norm(F))
    last=y[ends];c=T@last;cghost=rho*c
    kedge=-2*Omega/dr*np.imag(np.conj(c)*cghost)
    kcont=np.array([2*Omega*math.sqrt(x)*abs(z/poly(ell,math.sqrt(x)*r[-1]))**2 if x>0 else 0. for x,z in zip(p2,c)])
    kout=float(np.sum(kedge));kc=float(np.sum(kcont));work=float(2*Omega*np.imag(dr*np.vdot(y,F)))
    workrel=abs(kout-work)/max(abs(kout)+abs(work),1e-10)
    names=['Psi+','Psi-','X+','X-','chi'];qs=[1,1,2,2,0];sigs=[1,-1,1,-1,0]
    channels=[]
    for j,name in enumerate(names):
        channels.append({'name':name,'open':bool(p2[j]>0),'lab_frequency':float(nus[j]),'p2':float(p2[j]),
                         'ghost_real_imag':[float(rho[j].real),float(rho[j].imag)],
                         'K_edge':float(kedge[j]),'K_continuum_amplitude':float(kcont[j]),
                         'E_edge':float((1+sigs[j]*qs[j]*w/Omega)*kedge[j]),
                         'Q_edge':float(sigs[j]*qs[j]/Omega*kedge[j]),
                         'Jz_edge_if_chiral_m_ell':float(ell/Omega*kedge[j])})
    tail=float(max(abs(params['a']*h[-1]+6*params['lambda']*f[-1]**2+2*params['g']*b[-1]),
                   abs(params['a']*h[-1]+2*params['lambda']*f[-1]**2-2*params['g']*b[-1]),
                   abs(math.sqrt(2)*params['a']*f[-1]),abs(2*params['g']*f[-1]),
                   abs(-.75*params['M_chi']*h[-1]+3*h[-1]*h[-1])))
    row={'Q':rec['Q_target'],'L':rec['L'],'N':N,'dr':dr,'ell':ell,'Omega':Omega,'omega':w,
         'profile_record':rec,'drive_epsilon_for_unit_norm':1/raw_norm,'drive_radial_L2_norm':float(math.sqrt(dr*np.vdot(F,F).real)),
         'drive_support_radius':10.,'K_edge_total':kout,'K_continuum_total':kc,'K_source_work':work,
         'source_work_relative_difference':float(workrel),'linear_relative_residual':relres,
         'tail_interaction_max_abs_at_last_interior':tail,'channels':channels,
         'response_canonical_radial_L2_squared':float(dr*np.vdot(y,y).real)}
    tag=f"Q{rec['Q_target']} L{rec['L']} N{N} ell{ell} Omega{Omega}"
    check(tag+' linear residual',relres<1e-8)
    check(tag+' negligible endpoint profile interactions',tail<.001)
    check(tag+' relaxed background field and charge',rec['field_residual_scaled']<1e-9 and abs(rec['charge_residual_relative'])<1e-11)
    if np.any(p2>0):
        check(tag+' open discrete work identity',workrel<1e-7)
        check(tag+' outgoing channel edge signs',min(kedge[p2>0])>-1e-12 and kout>=0)
    else:
        check(tag+' closed flux and work',abs(kout)<1e-9 and abs(work)<1e-9)
    return row,lu,F,T,rho,ends,Omega,dr

def main(outdir):
    from radial_tools import operators,P
    preflight()
    rows=[];start=time.monotonic()
    for Q in [80000,160000]:
        profile=HERE/'profile_origin/run_001'/f'Q{Q}.npz'
        for L,N in [(40.,399),(60.,599),(60.,1199)]:
            for ell in [0,2]:
                op=operators(profile,Q,L,N,ell)
                for Omega in [.05,.12,.25]:
                    row,lu,F,T,rho,ends,om,dr=solve_drive(op,Omega,P)
                    rows.append(row)
                    if Q==80000 and L==60 and N==599 and ell==0 and Omega==.12:
                        y2=lu.solve(2*F);c2=T@y2[ends]
                        k2=float(np.sum(-2*om/dr*np.imag(np.conj(c2)*rho*c2)))
                        ratio=k2/row['K_edge_total']
                        check('doubled drive produces fourfold outgoing flux',abs(ratio/4-1)<1e-9,ratio=ratio)
                    print(json.dumps({k:row[k] for k in ['Q','L','N','ell','Omega','K_edge_total','K_continuum_total','K_source_work','linear_relative_residual']}),flush=True)
    comparisons=[]
    for Q in [80000,160000]:
        for ell in [0,2]:
            for Omega in [.12,.25]:
                subset=[x for x in rows if x['Q']==Q and x['ell']==ell and x['Omega']==Omega]
                for kind,coarse,fine in [('box',subset[0],subset[1]),('grid',subset[1],subset[2])]:
                    diffs={key:abs(coarse[key]-fine[key])/max(abs(coarse[key]),abs(fine[key]),1e-12) for key in ['K_edge_total','K_continuum_total']}
                    comparisons.append({'Q':Q,'ell':ell,'Omega':Omega,'kind':kind,'relative_differences':diffs})
                    check(f'Q{Q} ell{ell} Omega{Omega} {kind} outgoing flux convergence',max(diffs.values())<.05,relative_differences=diffs)
    check('all 36 declared response cases completed',len(rows)==36)
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    check('measured RSS below1GB',rss<1_000_000_000)
    result={'scope':'Driven linear susceptibility only; external U1-invariant density modulation. No natural merger/cooling efficiency or galactic torque prediction.',
            'rows':rows,'comparisons':comparisons,'checks':CHECKS,'n_checks':len(CHECKS),
            'all_checks_pass':all(c['passed'] for c in CHECKS),'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
            'normalization':'Discrete work balance uses exact FD link flux; continuum coefficient flux reported separately. Unit canonical reduced radial drive L2 norm; physical minus wave conjugated. l2 J is imposed m2 chirality.'}
    (outdir/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':len(rows),'checks':len(CHECKS),'all_pass':result['all_checks_pass'],'failed':[c['name'] for c in CHECKS if not c['passed']],'RSS':rss}),flush=True)
    raise SystemExit(0 if result['all_checks_pass'] else 1)

if __name__=='__main__':
    if sys.argv[1]=='--preflight':
        result=preflight();print(json.dumps(result,indent=2));raise SystemExit(0 if result['all_pass'] else 1)
    main(Path(sys.argv[1]))
