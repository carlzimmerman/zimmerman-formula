import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,datetime,hashlib,json,pathlib,resource,subprocess,sys,time,numpy as np,scipy
Q=pathlib.Path(__file__).resolve().parent;ROOT=Q.parents[1];P=Q.parent/'cold_resolved_pulse_2026_10_25';sys.path.insert(0,str(P))
from refinement_v3 import load
from binding import window
from radial_phase import radial_phase
p=argparse.ArgumentParser();p.add_argument('--case',choices=['s05','s01','dt01'],required=True);a=p.parse_args();start=time.time();utc=datetime.datetime.now(datetime.timezone.utc).isoformat();rev=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();bf=Q/'binding_phase_runs'/(a.case+'.json');d=json.loads(bf.read_text());assert d['status']=='completed declared windows';sf=ROOT/d['seed_path'];pins=sorted(set([ROOT/f for f in d['inputs_after']]+[bf,sf,sf.with_suffix('.npz'),Q/'radial_check.py',Q/'radial_phase.py',Q/'RADIAL_CONTRACT.md',Q/'radial_controls.py',Q/'radial_controls.json']))
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}
before=hashes()
for f,v in d['inputs_after'].items():assert before[f]==v
s,u0,p0,units,seed=load(nt=40 if a.case=='s05' else 48,nf=64 if a.case=='s05' else 80);del u0,p0;u=np.load(sf.with_suffix('.npz'))['u'];rows=[]
for x in d['rows']:
 v=window(s,u,x['a'],x['b']);k=radial_phase(s,v);del v;raw=radial_phase(s,u,x['a'],x['b']);assert k<=x['K_phase_cut']+1e-10;rows.append(dict(a=x['a'],b=x['b'],K_radial_phase_cut=k,K_radial_phase_raw_weighted=raw,K_radial_phase_over_abs_W=k/abs(x['W_self']),radial_only_bulk_rest_self_energy=k-x['Pz']**2/(2*x['M'])+x['W_self'],relative_cut_raw_difference=abs(k-raw)/max(abs(raw),1e-30)))
out=dict(parameters=vars(a),T=d['T'],physical=units,scope='radial-only energetic diagnostic of fixed snapshot window; not bound material mass or dynamic capture',rows=rows,inputs_before=before,inputs_after=hashes(),started_utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision_before=rev,revision_after=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),argv=sys.argv,interpreter=sys.executable,software=dict(Python=sys.version,numpy=np.__version__,scipy=scipy.__version__),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,status='completed declared radial windows');assert before==out['inputs_after'] and out['peak_RSS_bytes']<750_000_000;dest=Q/'radial_runs';dest.mkdir(exist_ok=True);f=dest/(a.case+'.json');assert not f.exists();f.write_text(json.dumps(out,indent=2)+'\n');print(rows,flush=True)
