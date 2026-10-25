import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
Q=pathlib.Path(__file__).resolve().parent;P=Q.parent/'cold_resolved_pulse_2026_10_25';ROOT=Q.parents[1];sys.path.insert(0,str(P))
from refinement_v3 import load
from binding import measure,window
from phase_support import phase_kinetic
p=argparse.ArgumentParser();p.add_argument('--case',choices=['s05','s01','dt01'],required=True);a=p.parse_args();start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();sf={'s05':P/'runs/draco_joint_s05.json','s01':P/'refined_runs/draco48x80_s01.json','dt01':Q/'late_runs/late_dt01.json'}[a.case];d=json.loads(sf.read_text());assert d['inputs_before']==d['inputs_after'];h=d['history'][-1];assert max(abs(h['E_relative_error']),abs(h['Jz_relative_error']),h['angular_edge_fraction'],h['azimuth_edge_fraction'])<.01
pins=sorted(set([ROOT/f for f in d['inputs_after']]+[sf,sf.with_suffix('.npz'),Q/'binding_phase_run.py',Q/'binding.py',Q/'phase_support.py',Q/'PHASE_CONTRACT.md',Q/'phase_controls.py',Q/'phase_controls.json',Q/'CONTRACT.md',Q/'controls.py',Q/'controls.json']))
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes()
for f,v in d['inputs_after'].items():assert before[f]==v
nt,nf=(40,64) if a.case=='s05' else (48,80);s,u0,p0,units,seed=load(nt=nt,nf=nf);del u0,p0;assert units==d['physical'];raw=np.load(sf.with_suffix('.npz'));u=raw['u'];phi=raw['phi'];assert u.shape==(len(s.r),nt,nf)
for k,v in dict(r=s.r,w=s.w,mu=s.mu,aw=s.aw,S=s.phase).items():
 if k in raw.files:assert np.array_equal(raw[k],v)
check=s.poisson(u);assert np.max(abs(check-phi))<1e-12;del check,raw
minimum_K_eigenvalue=float(np.linalg.eigvalsh(s.H)[0]);assert minimum_K_eigenvalue>-1e-10 and s.lam.min()>-1e-10
rows=[];status='completed declared windows'
for a0,b0 in [(.75,1.),(1.,2.),(2.,4.)]:
 v=window(s,u,a0,b0);r=measure(s,v,phi);kp=phase_kinetic(s,v);kr=phase_kinetic(s,u,a0,b0);assert kp<=r['K']+1e-10;bulk=r['Pz']**2/(2*r['M']);r.update(K_phase_cut=kp,K_phase_raw_window_weighted=kr,phase_cut_raw_relative_difference=abs(kp-kr)/max(abs(kr),1e-30),phase_only_self_energy_cut=kp+r['W_self'],phase_only_self_energy_raw=kr+r['W_self'],phase_only_bulk_rest_self_energy=kp-bulk+r['W_self']);del v;r.update(a=a0,b=b0,M_Msun=r['M']*units['Munit_Msun'],M_inside_reference_Msun=r['M_inside_reference']*units['Munit_Msun']);rows.append(r);rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;print(a.case,a0,b0,r['M_Msun'],r['E_self'],r['K_over_abs_W'],rss,flush=True)
 if rss>=750_000_000:status='memory headroom stop';break
out=dict(parameters=vars(a),physical=units,seed_path=str(sf.relative_to(ROOT)),T=h.get('absolute_T',h['t']),status=status,scope='cutoff-window energy and exact finite frozen-H spectral bounds; not an evolving material core or spatially retained bound-mass measurement',minimum_K_eigenvalue=minimum_K_eigenvalue,rows=rows,inputs_before=before,inputs_after=hashes(),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),argv=sys.argv,interpreter=sys.executable,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
assert before==out['inputs_after'];dest=Q/'binding_phase_runs';dest.mkdir(exist_ok=True);f=dest/(a.case+'.json');assert not f.exists();f.write_text(json.dumps(out,indent=2)+'\n');print(status,flush=True)
