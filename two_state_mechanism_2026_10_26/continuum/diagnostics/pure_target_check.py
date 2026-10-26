from pathlib import Path
import subprocess,os,sys,re,json
base=Path('/Users/carlzimmerman/new_physics/zimmerman-formula/two_state_mechanism_2026_10_26/continuum');sys.path.insert(0,str(base));from run_point import replace
src=Path('/private/tmp/ukrmol-build/recorded-Rcenter');w=Path('/private/tmp/ukrmol-build/pure-target-v2');w.mkdir(exist_ok=False);os.link(src/'fort.16',w/'fort.16')
s=(src/'scattering.congen.inp').read_text();head=replace(s.split('&wfngrp')[0],'iscat','1');last='&wfngrp'+s.split('&wfngrp')[-1];(w/'congen.inp').write_text(head+last)
scat=(src/'target.scatci.01.doublet.Ag.inp').read_text();scat=replace(scat,'megul','70');scat=replace(scat,'nstat','10');(w/'scatci.inp').write_text(scat)
for exe in ['congen','scatci']:
 with (w/(exe+'.out')).open('w') as out:subprocess.run(['/private/tmp/ukrmol-build/build/bin/'+exe],input=(w/(exe+'.inp')).read_text(),text=True,stdout=out,stderr=subprocess.STDOUT,cwd=w,env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'),check=True)
s=(w/'scatci.out').read_text();i=s.rfind('EIGEN-ENERGIES');print(s[i:i+300])
