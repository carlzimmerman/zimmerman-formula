from pathlib import Path
import sys,time,json,hashlib,traceback
import numpy as np
P=Path(__file__).resolve().parent;COL=P.parents[1]/'collapse';sys.path.insert(0,str(COL/'mirror/campaign_fresh_gravity'));sys.path.insert(0,str(P.parent/'kick_moments'));sys.dont_write_bytecode=True
import engine_events as E
import CFG5_common as C
T=time.monotonic();sig=E.Sigma();base=sig.Pk.copy();rg=np.geomspace(.2,3000,400);out={'runs':{},'rgrid_kpc':rg.tolist()}
sha=lambda a:hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
cases=[('control',80,.03,0.,False),('control',80,.015,0.,False)]
cases += [('canonical',N,eta,0.,True) for N in [600,1000] for eta in [.03,.015]]+[('canonical',600,.03,1e-7,True)]
cases += [('alt',N,eta,0.,True) for N in [600,1000] for eta in [.03,.015]]+[('alt',600,.03,1e-7,True)]
for foot,N,eta,shift,trig in cases:
 if time.monotonic()-T>320:print('OVERALL BUDGET STOP',flush=True);break
 if foot=='alt' and time.monotonic()-T>230:print('ALT DEFERRED TO BOUND',flush=True);break
 name=f'{foot}/N{N}/eta{eta}/shift{shift}';print('START',name,flush=True);t=time.monotonic();sig.Pk=base*(1+shift);a0=C.FOOT['canonical' if foot=='control' else foot]
 try:
  r=E.run(sig,1e12,a0,trigger=trig,cooling=False,Nc=N,nb=max(3,round(.04*N)),eta=eta,time_budget=48.)
  md,dau,mb=E.profiles(r,rg);r200=E.r200_of(rg,md+mb);h=E.GK*md/rg**2*1e6/C.KPC/a0;md200=float(np.interp(r200,rg,md));events=r.pop('events')
  ep=P/('events_'+name.replace('/','_')+'.json');ep.write_text(json.dumps(events))
  row={'complete':True,'N':N,'eta':eta,'foot':foot,'power_shift':shift,'trigger':trig,'hmax':float(max(h[rg<=r200])),'r200':r200,'conversion_fraction':r['budget']['converted']/md200,'budget':r['budget'],'mass_accounting_relative':r['mass_accounting_relative'],'nstep':r['nstep'],'events':len(events),'bisections':sum(e['bisections'] for e in events),'max_phase_velocity_residual':max([e['phase_residual'] for e in events]or[0.]),'max_pressure_relative_excess':max([e['pressure_relative_excess'] for e in events if not e.get('immediate')]or[0.]),'immediate_events':sum(bool(e.get('immediate')) for e in events),'max_bracket_relative_width':max([e['bracket_width']/e['proposal_dt'] for e in events]or[0.]),'Md':md.tolist(),'Mb':mb.tolist(),'initial_profile_sha256':[sha(x) for x in E.initial_profile(sig,1e12,N)]}
 except Exception as e:
  row={'complete':False,'N':N,'eta':eta,'foot':foot,'power_shift':shift,'error':str(e)};traceback.print_exc()
 row['seconds']=time.monotonic()-t;out['runs'][name]=row;out['runtime_seconds']=time.monotonic()-T;(P/'results.json').write_text(json.dumps(out,indent=2));print('END',name,{k:v for k,v in row.items() if k not in ['Md','Mb','initial_profile_sha256']},flush=True)
out['runtime_seconds']=time.monotonic()-T;out['source_hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'engine_events.py',P/'event_step.py',P/'benchmark.py',P.parent/'kick_moments/exact_moments.py',COL/'mirror/campaign_fresh_gravity/CFG5_common.py']};(P/'results.json').write_text(json.dumps(out,indent=2));print('FINISHED',out['runtime_seconds'],flush=True)
