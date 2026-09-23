import numpy as np,json,pathlib,runpy,sys
sim=runpy.run_path('real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py')['simulate']
def stats(D,w,C):
 a=w/w.mean();mu=np.mean(a*D);u=D-mu;V=np.mean(a*u*u);pm=a*u;pv=a*(u*u-V)
 return {**dict(mu=float(mu),V=float(V),H=float(V-C*mu**1.5)),**{k+'_se':float(v.std(ddof=1)/np.sqrt(len(D))) for k,v in [('mu',pm),('V',pv),('H',pv-1.5*C*np.sqrt(mu)*pm)]}}
def transform(out,a):
 t,d=out['time'],out['delay'];z=t-d
 assert np.isfinite([t,d,z]).all() and z.min()>=-1e-12 and z.max()<=1+1e-12 and d.min()>=-1e-12
 Z=np.sqrt(1-a*a*(1-z*z));D=a*d;E=D-a*a*(1-z*z)/(1+Z)
 assert E.min()>=-1e-12
 return D,E
checks={};rows=[];a=.05
for mode,N,base in [('main',256000,1700100),('positive',512000,1700200)]:
 for i,tau in enumerate([1,4]):
  D,E=transform(sim(N,tau0=tau,q=0,h=0,source='central',seed=base+1+i),a)
  Dr,Er=transform(sim(N,tau0=tau,q=0,h=0,source='central',seed=base+11+i),a)
  U=np.random.default_rng(base+21+i).random(N);C=4*np.sqrt(2)/(9*np.sqrt(tau/a))
  basez=float((D.mean()-a*tau/2)/(D.std(ddof=1)/np.sqrt(N)))
  for beta in [4,16,64]:
   alpha=beta/a;w=np.exp(-alpha*E);s=stats(D,w,C);accepted=Dr[U<np.exp(-alpha*Er)];nr=len(accepted);r=stats(accepted,np.ones(nr),C);p=nr/N;ess=float(w.sum()**2/np.dot(w,w))
   z={k:float((s[k]-r[k])/np.hypot(s[k+'_se'],r[k+'_se'])) for k in ['mu','V']};z['p']=float((w.mean()-p)/np.sqrt(w.var(ddof=1)/N+p*(1-p)/N))
   cert=bool(nr>=100 and ess>=100 and abs(basez)<=5 and all(abs(v)<=5 for v in z.values()));checks[f'{mode}_{tau}_{beta}']=cert
   rec=dict(mode=mode,N=N,tau=tau,beta=beta,weighted=s,rejection=r,accepted=nr,ESS=ess,z=z,baseline_z=basez,log_escape_weighted=float(-alpha+np.log(w.mean())),log_escape_rejection=float(-alpha+np.log(p)),certificate=cert)
   if mode=='main':
    en=Dr[U<np.exp(-alpha*Er/2)];sn=stats(en,np.ones(len(en)),C);pn=len(en)/N;zn={k:float((s[k]-sn[k])/np.hypot(s[k+'_se'],sn[k+'_se'])) for k in ['mu','V']};zn['p']=float((w.mean()-pn)/np.sqrt(w.var(ddof=1)/N+pn*(1-pn)/N));checks[f'negative_{tau}_{beta}']=not all(abs(v)<=5 for v in zn.values());rec['negative_z']=zn
   rows.append(rec)
out={'checks':checks,'rows':rows,'scope':'Finite diagnostic; same transport solver shared across independent estimators, piecewise opacity continuity caveat; no observable flux or novelty claim.'};pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print({'passed':sum(checks.values()),'total':len(checks)});assert all(checks.values())
