"""Independent statistics over unchanged solvers. Raw D; no sign acceptance."""
import pathlib,runpy,json,sys
import numpy as np
ROOT=pathlib.Path.cwd()
simulate=runpy.run_path(str(ROOT/'real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py'))['simulate']
killed=runpy.run_path(str(ROOT/'real_research/reviews/jwst_cap_attempt_audit_2026_09_22/f0773c84727d48feaac1155b82ebf844.py'))['killed_transport']
C=4*np.sqrt(2)/9
checks={};results={}
def stats(D,w):
    assert len(D)>100 and np.isfinite(D).all() and D.min()>=-1e-12
    a=w/w.mean();mu=float(np.mean(a*D));x=D-mu;V=float(np.mean(a*x*x))
    psi_mu=a*x;psi_V=a*(x*x-V);psi_H=psi_V-1.5*C*np.sqrt(mu)*psi_mu
    return {'mu':mu,'V':V,'H':float(V-C*mu**1.5),'mu_se':float(np.std(psi_mu,ddof=1)/np.sqrt(len(D))),'V_se':float(np.std(psi_V,ddof=1)/np.sqrt(len(D))),'H_se':float(np.std(psi_H,ddof=1)/np.sqrt(len(D)))}
for mode,N,cs,ks in [('main',32000,1300101,1300111),('positive',64000,1300201,1300211),('fresh',32000,1400101,1400111)]:
    cons=simulate(N,tau0=1,q=0,h=0,source='central',seed=cs);D=cons['delay'];T=cons['time']
    checks[mode+'_raw_complete']=bool(len(D)==len(T)==N and np.isfinite(D).all() and np.isfinite(T).all() and D.min()>=-1e-12 and T.min()>=1-1e-12)
    checks[mode+'_alpha0']=bool(abs(D.mean()-.5)<=5*D.std(ddof=1)/np.sqrt(N))
    results[mode]={'N':N,'seed':cs,'kill_seed_base':ks,'raw_min_D':float(D.min()),'raw_negative_count':int((D<0).sum()),'alpha0_mean':float(D.mean()),'cases':[]}
    for i,alpha in enumerate([.5,2.,4.]):
        w=np.exp(-alpha*T);weighted=stats(D,w);pw=float(w.mean());ess=float(w.sum()**2/np.dot(w,w))
        E,ne=killed(N,tau0=1,alpha=alpha,seed=ks+i);direct=stats(E,np.ones(ne));pk=ne/N
        z={k:float((weighted[k]-direct[k])/np.hypot(weighted[k+'_se'],direct[k+'_se'])) for k in ['mu','V']}
        z['p']=float((pw-pk)/np.sqrt(w.var(ddof=1)/N+pk*(1-pk)/N))
        tag=mode+'_'+str(alpha)
        checks[tag+'_sizes']=bool(len(E)==ne and ne>=100 and ess>=100)
        checks[tag+'_agreement']=all(abs(v)<=5 for v in z.values())
        rec={'alpha':alpha,'weighted':weighted,'killed':direct,'p_weighted':pw,'p_killed':pk,'ESS':ess,'escaped':ne,'agreement_z':z,'raw_min_killed_D':float(E.min())}
        if mode=='main':
            En,nen=killed(N,tau0=1,alpha=alpha/2,seed=ks+i);ns=stats(En,np.ones(nen));pn=nen/N
            zn={k:float((weighted[k]-ns[k])/np.hypot(weighted[k+'_se'],ns[k+'_se'])) for k in ['mu','V']};zn['p']=float((pw-pn)/np.sqrt(w.var(ddof=1)/N+pn*(1-pn)/N))
            negative_pass=checks[mode+'_alpha0'] and nen>=100 and ess>=100 and all(abs(v)<=5 for v in zn.values())
            checks[tag+'_negative_rejected']=not negative_pass;rec['negative_agreement_z']=zn
        results[mode]['cases'].append(rec)
out={'checks':checks,'results':results,'interpretation':'Finite non-detection of negative cap margin only. Independent statistics and killed/weighted implementations; no universal selection theorem or novelty. Alpha cases share conservative paths.'}
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'passed':sum(checks.values())}));assert all(checks.values())
