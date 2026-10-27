import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from isolated import Isolated
pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();rows=[];checks=[];mstar=.08408132497418408
for n,box in [(48,6),(64,6),(64,8)]:
 f=Isolated(n,box)
 for b in [.5,1,2,4]:
  cache={}
  def get(R):
   key=float(R)
   if key not in cache:cache[key]=f.evaluate(mstar*b,[R]*3)
   return cache[key]
  def der(R):return sum(get(R)['axis_log_derivatives'])
  lo=.15;hi=1.0;dl=der(lo);dh=der(hi)
  if dl*dh>=0:
   rows.append(dict(n=n,box=box,b=b,bracket=False,der_lo=dl,der_hi=dh));continue
  R=brentq(der,lo,hi,xtol=2e-5);r=get(R);r.update(b=b,Rmin=R,cells_per_axis=R/f.dx,bracket=True,energy_per_mass=r['energy']/(mstar*b));rows.append(r)
  # Envelope theorem versus independently finite-differenced minimized field energies.
  if n==48 and b==2:
   eps=1e-3;fd=(get(R*np.exp(eps))['energy']-get(R*np.exp(-eps))['energy'])/(2*eps)
   checks.append(dict(name='shape_energy_gradient',passed=abs(fd-der(R))<1e-6,value=float(abs(fd-der(R)))))
  print('well',n,box,b,R,r['energy'],r['cells_per_axis'],flush=True)
  Path(args.output).write_text(json.dumps(dict(rows=rows,checks=checks),indent=2)+'\n')
