#!/usr/bin/env python3
"""Independent units check against Colossus, before corrected cluster reruns."""
import os,sys,json,hashlib
from pathlib import Path
import numpy as np
from colossus.cosmology.power_spectrum import modelEisenstein98ZeroBaryon
ROOT=Path(__file__).resolve().parents[3]
p=ROOT/'real_research/cross_thread_review_2026_09_26/XR28_common.py'
s=p.read_text();fixed=s.replace('(0.43 * k * s / h)','(0.43 * k * s)').replace('q = k * th * th / ge','q = (k / h) * th * th / ge')
assert s!=fixed
spaces=[]
for text in (s,fixed):
 d={'__file__':str(p),'__name__':'xr28_transfer_audit'};exec(compile(text,str(p),'exec'),d);spaces.append(d)
old,new=spaces;mut=os.environ.get('MUTATE')=='1';tested=old if mut else new
k=np.geomspace(1e-5,1e3,3000)
ref=modelEisenstein98ZeroBaryon(k/new['h'],new['h'],new['Om'],new['Ob'],new['T_CMB'])
err=float(np.max(np.abs(tested['T_EH98'](k)/ref-1)))
checks={'physical_k_matches_independent_EH98':err<1e-12,
        'sigma8_normalization_preserved':bool(abs(np.sqrt(tested['S_of_M'](4*np.pi/3*tested['RHOM0']*(8/tested['h'])**3)[0])-.811)<1e-8)}
rows=[]
for mass in [1e13,1e14,1e15]:
 a,oa=old['correa_mah'](mass);b,ob=new['correa_mah'](mass)
 rows.append({'mass':mass,'old_alpha':oa['alpha'],'new_alpha':ob['alpha'],'old_f':oa['f'],'new_f':ob['f'],
              'M_new_over_old':{str(z):float(b(z)/a(z)) for z in [.25,.5,1.,2.]}})
res={'mutate':mut,'checks':checks,'max_transfer_relative_error':err,'original_error':float(np.max(np.abs(old['T_EH98'](k)/ref-1))),
     'source_sha256':hashlib.sha256(s.encode()).hexdigest(),'corrected_sha256':hashlib.sha256(fixed.encode()).hexdigest(),
     'rows':rows,'scope':'Independent physical-k identity and input mass-history effect; not a cluster-fit result.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
