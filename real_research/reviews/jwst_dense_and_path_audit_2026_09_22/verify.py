"""Independent harness; unchanged Qwen path kernel and two audited solvers."""
import json,pathlib,runpy,sys
import numpy as np
ROOT=pathlib.Path.cwd();HERE=pathlib.Path(__file__).resolve().parent
sim=runpy.run_path(str(ROOT/'real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py'))['simulate']
kill=runpy.run_path(str(ROOT/'real_research/reviews/jwst_cap_attempt_audit_2026_09_22/f0773c84727d48feaac1155b82ebf844.py'))['killed_transport']
photon=runpy.run_path(str(HERE/'path_candidate.py'))['simulate_photon']
def stats(D,w,C):
    a=w/w.mean();mu=np.mean(a*D);u=D-mu;V=np.mean(a*u*u)
    inf=[a*u,a*(u*u-V),a*(u*u-V)-1.5*C*np.sqrt(mu)*a*u]
    return {**dict(mu=float(mu),V=float(V),H=float(V-C*mu**1.5)),**{k+'_se':float(np.std(v,ddof=1)/np.sqrt(len(D))) for k,v in zip(['mu','V','H'],inf)}}
def zscore(a):return float(a.mean()/(a.std(ddof=1)/np.sqrt(len(a))))
checks={};out={'dense':{},'path':{}}
for mode,N,cs,ks in [('main',256000,1500101,1500111),('positive',512000,1500201,1500211)]:
    out['dense'][mode]=[]
    for i,(M,alpha) in enumerate([(4,3),(8,4)]):
        cons=sim(N,tau0=M,q=0,h=0,source='central',seed=cs+i);D,T=cons['delay'],cons['time'];w=np.exp(-alpha*T);C=4*np.sqrt(2)/(9*np.sqrt(M));s=stats(D,w,C)
        E,ne=kill(N,tau0=M,alpha=alpha,seed=ks+i);k=stats(E,np.ones(ne),C);pw=float(w.mean());pk=ne/N;ess=float(w.sum()**2/np.dot(w,w))
        z={key:float((s[key]-k[key])/np.hypot(s[key+'_se'],k[key+'_se'])) for key in ['mu','V']};z['p']=float((pw-pk)/np.sqrt(w.var(ddof=1)/N+pk*(1-pk)/N))
        valid=bool(len(D)==len(T)==N and len(E)==ne and np.isfinite(D).all() and np.isfinite(T).all() and np.isfinite(E).all() and min(D.min(),E.min())>=-1e-12 and T.min()>=1-1e-12)
        base=zscore(D-M/2);certificate=valid and ne>=100 and ess>=100 and abs(base)<=5 and all(abs(v)<=5 for v in z.values())
        tag=f'{mode}_{M}';checks[tag+'_dense_data_integrity']=valid
        rec={'M':M,'alpha':alpha,'N':N,'cons_seed':cs+i,'kill_seed':ks+i,'weighted':s,'killed':k,'ESS':ess,'escaped':ne,'agreement_z':z,'alpha0_z':base,'certificate':bool(certificate)}
        if mode=='main':
            En,nn=kill(N,tau0=M,alpha=alpha/2,seed=ks+i);n=stats(En,np.ones(nn),C);pn=nn/N;zn={key:float((s[key]-n[key])/np.hypot(s[key+'_se'],n[key+'_se'])) for key in ['mu','V']};zn['p']=float((pw-pn)/np.sqrt(w.var(ddof=1)/N+pn*(1-pn)/N));rec['negative_z']=zn;checks[tag+'_negative_rejected']=not all(abs(v)<=5 for v in zn.values())
        out['dense'][mode].append(rec)
for mode,N,seeds in [('main',8000,[1100101,1100102]),('positive',16000,[1100201,1100202])]:
    out['path'][mode]=[]
    for (a,b,d),seed in zip([(1.,0.,.5),(1.,1.,.75)],seeds):
        rng=np.random.default_rng(seed);arr=np.array([photon(a,b,rng) for _ in range(N)]);T,Z,S,Q,n,escaped=arr.T;D=T-Z
        integrity=bool(len(T)==N and np.isfinite(arr).all() and np.all(escaped==1) and T.min()>=1-1e-12 and D.min()>=-1e-12 and Z.min()>=-1e-12 and Z.max()<=1+1e-12)
        p=np.exp(-a-b/3);atomz=float(((n==0).sum()-N*p)/np.sqrt(N*p*(1-p)))
        def certificate(observed):
            z={'mean':zscore(observed-d),'R':zscore((observed-d)**2-2*S/3-11*(1-Z**2)/9),'G':zscore(Z**2-1-.3*S+.9*Q),'atom':atomz}
            return integrity and all(abs(v)<=5 for v in z.values()),z
        passed,z=certificate(D);neg,nz=certificate(T);tag=f'{mode}_{a}_{b}'
        checks[tag+'_path_certificate']=passed;checks[tag+'_real_negative_rejected']=not neg
        out['path'][mode].append({'a':a,'b':b,'N':N,'seed':seed,'complete':integrity,'z':z,'negative_z':nz,'certificate':passed,'negative_certificate':neg,'real_collisions_zero':int((n==0).sum())})
out['checks']=checks;out['limitations']=['Dense certificates that fail sample-count minimum remain inconclusive; signs are data, not acceptance.','Path result is independent harness over Qwen kernel, not independent implementation.','No universal proof, novelty or observational claim.']
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'audit_checks':len(checks),'passed':sum(checks.values()),'dense_certificates':{mode:[r['certificate'] for r in cases] for mode,cases in out['dense'].items()}}));assert all(checks.values())
