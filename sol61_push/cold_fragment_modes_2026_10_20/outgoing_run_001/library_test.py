"""General-l outgoing API checks and one pinned coupled regression."""
from pathlib import Path
import json,math,sys,resource
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from outgoing_library import hankel_polynomial,ghost_ratio,outgoing_solve
from radial_tools import operators,P
B=Path(__file__).resolve().parents[1]
checks=[]
def ck(name,test):
 checks.append({'name':name,'passed':bool(test)});assert test,name
z=2.
ck('l4 outgoing polynomial matches explicit coefficients',abs(hankel_polynomial(4,z)-(1-10j/z-45/z**2+105j/z**3+105/z**4))<1e-13)
ck('l4 decaying polynomial matches explicit coefficients',abs(hankel_polynomial(4,z,True)-(1+10/z+45/z**2+105/z**3+105/z**4))<1e-13)
ck('l4 outgoing ghost has outward flux sign',ghost_ratio(4,.09,39.9,.1).imag<0)
ck('l4 closed ghost decays without flux',0<ghost_ratio(4,-10000.,39.9,.1).real<1 and ghost_ratio(4,-10000.,39.9,.1).imag==0)
op=operators(B/'profile_origin/run_001/Q80000.npz',80000,60.,599,2)
r=op['r'];f=op['fields'][0];shape=np.maximum(0,1-r*r/100)**4;shape[r>=10]=0
raw=-math.sqrt(2)*r*f*shape;F=np.zeros(5*op['N'],complex);F[:op['N']]=raw/math.sqrt(op['dr']*np.dot(raw,raw))
now=outgoing_solve(op,.25,F,P,m=2)['summary']
prior=json.loads((B/'outgoing_run_001/diagnostic/results.json').read_text())
old=next(x for x in prior['rows'] if x['Q']==80000 and x['L']==60 and x['N']==599 and x['ell']==2 and x['Omega']==.25)
for key in ['K_edge_total','K_continuum_total','K_source_work']:
 ck('pure API regression '+key,abs(now[key]/old[key]-1)<1e-10)
ck('pure API exact discrete work control',now['source_work_relative_difference']<1e-7)
ck('pure API angular normalization',abs(now['Jz_edge_total']/(2/.25*now['K_edge_total'])-1)<1e-12)
result={'checks':checks,'all_pass':all(c['passed'] for c in checks),'regression':now,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_pass':result['all_pass'],'RSS':result['peak_rss_bytes_macos']}))
