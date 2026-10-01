#!/usr/bin/env python3
"""Conditional reservoir-capped P2, transferring existing Moster mapping; no new physical fit.
Budget-only edge, not CMASS's extra first-turnaround/retention gate. MUTATE deletes exterior dark mass.
"""
import sys,os,pathlib,json,math,time
sys.dont_write_bytecode=True
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
HERE=pathlib.Path(__file__).resolve().parent; REPO=HERE.parents[2]
sys.path.insert(0,str(REPO/'campaign_fresh_gravity'))
import numpy as np
import CFG4_common as C
import CFG2_common as C2
MUT=os.environ.get('MUTATE')=='1'; start=time.monotonic(); O={'mutate':MUT,'checks':{},'kids':{},'sparc':{},'a0':C.A0,'kappa':'1/2 FITTED','Z':C.Z_FRAME}
def ck(n,b,v):O['checks'][n]={'ok':bool(b),'value':v};print(n,b,v,flush=True)
# Exact inherited Moster z-dependent inversion from CFG3, avoiding its CLASS initialization.
p=REPO/'campaign_fresh_gravity/CFG3_common.py';s=p.read_text();ns={'np':np};exec(s[s.index('def mstar_of_mh('):],ns); mh=ns['mh_of_mstar']
GK={'np':np,'math':math,'os':os,'REPO':str(REPO),'G_SI':C.G_SI,'_trap':C._trap}
GK,_=C.exec_slices(str(REPO/'real_research/derivation_chain_2026/FP1_static_sector.py'),[('# ---- KiDS: L355\'s machinery','w0 = np.zeros(len(ES)); w0[0] = 1.0')],ns=GK)
REFINE=os.environ.get('REFINE')=='1';FAC=float(os.environ.get('KIDS_MB_MS','1.4'));O['kids_Mb_over_Mstar']=FAC
rr=GK['rrK'] if not REFINE else np.geomspace(1e-3,100,8000)*GK['MPCm'];MS=GK['MS'];MPC=GK['MPCm'];LM=GK['LM']; FIX=C.ESDFix(rr,GK['Rp'],GK['PCm2'],MS);w=np.zeros(len(GK['ES']));w[0]=1
O['projection_grid']={'points':len(rr),'max_Mpc':float(rr[-1]/MPC),'refined':REFINE}
for foot,a0 in C.A0.items():
 tabs={k:np.zeros((len(w),len(LM),4,GK['npb'])) for k in ['P2','cap','Newton']};edges=[]
 for im,lm in enumerate(LM):
  mb=10**lm*MS;host=float(mh(10**lm/FAC,GK['ZL']))*MS;budget=host-mb
  if budget<=0:raise RuntimeError('negative host reservoir')
  ph=mb*(C.nu_p2(C.G_SI*mb/rr**2/a0)-1); re=math.sqrt(C.G_SI*budget*(budget+2*mb)/(a0*mb))
  def capped_dark(r):
   val=np.minimum(mb*(C.nu_p2(C.G_SI*mb/r**2/a0)-1),budget)
   return np.where(r>re,0,val) if MUT else val
  cap=capped_dark(rr); far=float(capped_dark(max(rr[-1],2*re)))
  ck(f'Gauss_retained/{foot}/{lm}',abs(far/budget-1)<1e-12,{'outside_to_budget':far/budget,'grid_outer_to_budget':float(cap[-1]/budget),'edge_Mpc':re/MPC})
  edges.append({'logMb':float(lm),'logMh':math.log10(host/MS),'edge_Mpc':re/MPC})
  for key,mass in [('P2',mb+ph),('cap',mb+cap),('Newton',np.full_like(rr,mb))]:
   ds=FIX(mass,mb);tabs[key][0,im]=[np.interp(GK['Rd'][b],GK['Rp']/MPC,ds) for b in range(4)]
 rows={}
 for key,T in tabs.items():
  rows[key]={}
  for Amax in [0.,1.,2.]:
   val,pars=GK['kfit']({foot:T},foot,w,Amax)
   # Recover selected masses under the source's identical diagonal-per-bin profiling rule.
   selected=[]
   for b in range(4):
    candidates=[]
    for im,lm in enumerate(LM):
     mk=T[0,im,b]; t2=GK['T2H'][b];wv=1/GK['Sd'][b]**2
     amp=float(np.clip(np.sum(wv*t2*(GK['Ed'][b]-mk))/np.sum(wv*t2*t2),0,Amax)) if Amax else 0.
     candidates.append(float(np.sum(((GK['Ed'][b]-mk-amp*t2)/GK['Sd'][b])**2)))
    i=int(np.argmin(candidates));selected.append(edges[i])
   rows[key][str(Amax)]={'chi2':val,'profiled_A':pars,'Amax':Amax,'selected_mass_edge':selected}
 # Fixed unit two-halo benchmark: still profiles inherited Mb grid, fits no two-halo amplitude.
 for key,T in tabs.items():
  fixed=T.copy()
  for b in range(4):fixed[0,:,b,:]+=GK['T2H'][b]
  val,_=GK['kfit']({foot:fixed},foot,w,0.)
  rows[key]['fixed1']={'chi2':val,'fixed_A':[1.,1.,1.,1.],'Amax':None}
 base=rows['P2']['0.0']['chi2'];ref={'canonical':139.800,'alt':133.948}[foot]
 ck('KiDS_baseline/'+foot,abs(base-ref)<.001,{'new':base,'reference_rounded':ref})
 for key in rows:
  for d in rows[key].values():d['delta_chi2_vs_unbounded_P2']=d['chi2']-base;d['within_CFG4_9_gate']=d['chi2']-base<=9
 O['kids'][foot]={'scores':rows,'edges':edges}
 print('KIDS',foot,rows,flush=True)
# Same algebraic RAR and baryonic mass-budget approximation already used by CFG2/4.
# Independent spherical dark cap acceleration min[gphi, G Mc/r^2] leaves actual rotmod baryonic force intact.
GAL=C.load_sparc();UPS=C2.UPS;ng=len(GAL);ngood=0
base_ref=json.loads((REPO/'campaign_fresh_gravity/CFG4_galaxy_law_results.json').read_text())['numbers']['H2']
for foot,a0 in C.A0.items():
 ss={k:np.zeros(len(UPS)) for k in ['P2','cap','Newton']};ww=np.zeros(len(UPS));capped=np.zeros(len(UPS),int);fraction=[];outside=[]
 for g in GAL:
  if not g['meta']:raise RuntimeError('missing independent mass budget '+g['name'])
  mbtot,ms=C2.mass_budget(g,UPS);hosts=np.array([C2.Mh_of_Mstar(max(x,1e5)) for x in ms]);budget=hosts-mbtot
  if np.any(budget<=0):raise RuntimeError('negative SPARC reservoir '+g['name'])
  rad=g['R'][None,:]*3.0857e19;vb=C2.vbar2_grid(g,UPS);gb=vb*1e6/rad;go=(g['Vobs'][None,:]*1e3)**2/rad
  ok=(gb>0)&(go>0)&np.isfinite(gb)&np.isfinite(go)&(g['Vobs'][None,:]>0)
  weight=np.where(ok,1/(np.clip(g['eV'],1,None)/np.clip(g['Vobs'],1,None))**2,0)
  ph=(C.nu_p2(np.where(ok,gb,1)/a0)-1)*gb;capmax=C.G_SI*budget[:,None]*C.MSUN/rad**2
  cp=np.minimum(ph,capmax);cp=np.where(ph>capmax,0,cp) if MUT else cp
  for key,model in [('P2',gb+ph),('cap',gb+cp),('Newton',gb)]:
   resid=np.log10(np.where(ok,go,1))-np.log10(np.where(ok,model,1));ss[key]+=np.sum(weight*resid**2,axis=1)
  ww+=weight.sum(axis=1);capped+=np.sum(ok&(ph>capmax),axis=1)
  fraction.append(np.max(np.where(ok,ph/capmax,0),axis=1))
  # Largest required fraction at each U for reporting names (no fitted cutoff).
 rows={}
 for key in ss:
  rms=np.sqrt(ss[key]/ww);iu=int(np.argmin(rms));rows[key]={'rms':float(rms[iu]),'U':float(UPS[iu]),'index':iu,'n_capped_points':int(capped[iu]),'maximum_required_budget_fraction':float(np.max(np.array(fraction)[:,iu])),'CFG4_RAR_gate':bool(rms[iu]<=.110 and .5<=UPS[iu]<=.8)}
 ref=base_ref[foot+'|P2'];ck('SPARC_baseline/'+foot,abs(rows['P2']['rms']-ref['rms'])<1e-12 and rows['P2']['U']==ref['U'],{'new':rows['P2'],'reference':ref})
 ck('SPARC_Newton_negative/'+foot,rows['Newton']['rms']>=.25,rows['Newton'])
 O['sparc'][foot]={'scores':rows,'galaxies':ng,'maximum_budget_fraction_per_U':np.max(np.array(fraction),axis=0).tolist(),'U_grid':UPS.tolist()};print('SPARC',foot,rows,flush=True)
O['scope']=['Mosters parameters inherited unchanged: CFG3 KiDS Mstar=Mb/1.4 at z=.25; CFG2 SPARC measured stars+gas and Moster z0','cap-only reservoir Mh-Mb; no extra CMASS seed-retention/turnaround gate','existing baryon-mass and two-halo amplitude nuisance profiling retained; Amax=1 and2 are profiled upper bounds, not fixed amplitudes','SPARC algebraic RAR with spherical dark-cap acceleration; not a nonspherical field solve','cross-population transfer of empirical LCDM-calibrated host mapping; no action or self-consistent halo formation claimed']
O['runtime_s']=time.monotonic()-start;O['control_verdict']='pass' if all(x['ok'] for x in O['checks'].values()) else 'failed'
(HERE/('replacement_joint_results'+('_MUTATE' if MUT else '')+('_REFINE' if REFINE else '')+('_FAC'+str(FAC) if FAC!=1.4 else '')+'.json')).write_text(json.dumps(O,indent=2));print('done',O['runtime_s'],O['control_verdict']);sys.exit(0 if O['control_verdict']=='pass' else 1)
