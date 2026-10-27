"""Below-electronic-threshold eigenphase scan; resonance candidates, not DR."""
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
import numpy as np
from scipy.signal import find_peaks
from run_point import replace
from kmat import read_k
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--work',required=True);p.add_argument('--bin',required=True);p.add_argument('--output',required=True);a=p.parse_args()
src=Path(a.input);w=Path(a.work);w.mkdir(parents=True,exist_ok=False)
for name in ['fort.10','fort.21']:shutil.copy2(src/name,w/name)
inp=(src/'scattering.rsolve.inp').read_text()
for key,value in [('nescat','300'),('einc','0.002,0.002'),('ieunit','1'),('raf','80'),('nrange','60')]:inp=replace(inp,key,value)
(w/'inp').write_text(inp)
with (w/'rsolve.out').open('w') as log:
 subprocess.run([str(Path(a.bin).resolve()/'rsolve')],input=inp,text=True,cwd=w,env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=240)
rows=read_k(w/'fort.19');E=np.array([x['energy_au'] for x in rows]);phase=np.unwrap(2*np.array([x['eigenphase_sum'] for x in rows]))/2;gradient=np.gradient(phase,E)
peaks,_=find_peaks(gradient,prominence=10)
result=dict(rsolve_sha256=hashlib.sha256((Path(a.bin)/'rsolve').read_bytes()).hexdigest(),energies=E.tolist(),unwrapped_eigenphase=phase.tolist(),phase_derivative=gradient.tolist(),max_unitarity_error=max(x['unitarity_error'] for x in rows),candidate_peaks=[dict(energy=float(E[i]),slope=float(gradient[i])) for i in peaks],scope='fixed-nuclei eigenphase diagnostic; no fitted widths accepted as physical')
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');shutil.copy2(w/'fort.19',out.parent/'scan_Kmat.txt');print(result['candidate_peaks'],flush=True)
