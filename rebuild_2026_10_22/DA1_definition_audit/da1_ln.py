#!/usr/bin/env python3
"""DA1 D6: Ln's two-halo template conversion, Planck-type h 0.6736, omega_b 0.02237, omega_c 0.1200, against the native h 0.6856427, Om 0.2976016. CRG1's scratch copy with one line replaced, separate partials. P_grav itself isn't recomputed. kappa = 1/2 FITTED; not theory closed."""
import glob, json, os, re, shutil, subprocess, sys
CRG=os.environ['DA1_CRG']; HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(CRG); e=dict(os.environ); e.update(OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
src=open('crg1_lens.py').read(); old='s.ht = 0.6736; s.Ot = (0.02237 + 0.1200) / s.ht ** 2'; assert old in src
open('crg1_lens_native.py','w').write(src.replace(old,'s.ht = 0.6856427; s.Ot = 0.2976016'))
OUT={}
for tag,sc in (('base','crg1_lens.py'),('native','crg1_lens_native.py')):
    p=f'parts_ln_{tag}'; os.makedirs(p,exist_ok=True); [shutil.copy(f,p) for f in glob.glob('partials/zoom_*.json')]; e['CRG1_PARTIALS']=p; subprocess.run([sys.executable,sc],env=e,check=True,capture_output=True); OUT[tag]=json.load(open(p+'/Ln.json'))
def walk(a,b,pre=''):
    r={}
    if isinstance(a,dict):
        for k in a:
            if k in b: r.update(walk(a[k],b[k],pre+'/'+k))
    elif isinstance(a,(int,float)) and not isinstance(a,bool) and a!=b: r[pre]=(a,b)
    elif isinstance(a,str) and a!=b: r[pre]=(a,b)
    return r
d=walk(OUT['base'],OUT['native']); txt=[f"{k}: {v[0]} -> {v[1]}" for k,v in d.items() if re.search(r'dchi2|class|passed|ENV|H2H|L2H|chi2',k)]
print('\n'.join(txt)); json.dump(OUT,open(os.path.join(HERE,'da1_ln.json'),'w'),indent=1); open(os.path.join(HERE,'da1_ln.out'),'w').write('\n'.join(txt)+'\n')
