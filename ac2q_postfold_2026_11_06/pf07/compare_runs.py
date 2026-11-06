import argparse,json
from pathlib import Path
import numpy as np
from dealias import Padded,transfer
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('runs',nargs='+');a=ap.parse_args();rows=[];fields=[]
for dirname in a.runs:
 data=json.loads((Path(dirname)/'result.json').read_text());n=data['n'];factor=data['padding'];s=Padded(n,factor=factor);y=np.array(data['final_state']);s.fine.P=np.array(data['final_P']);z=s.lift(y,s.fine.n)
 def residual(z,sys):
  l,b,pl,r=sys.unpack(z);bx=sys.dx(b);pb=r+2*sys.M**2*np.exp(4*b)/pl*(2*sys.dxx(b)+3*bx*bx)
  return float(np.max(abs(sys.dx(pl)-bx*pb))),float(sys.k*np.max(abs(pl)))
 from evolve_projected import System
 coarse=System(n,128);rc,scale=residual(y,coarse);rf,_=residual(z,s.fine);zp=s.fine.project(z);yp=s.project(y);ypp=s.project(yp)
 fine_correction=zp-z;high=fine_correction-s.lift(s.lift(fine_correction,n),s.fine.n)
 f=s.fine.constrain(zp);vals={k:f[k]for k in ['q','N','b','pb']};vals['r']=zp[1+2*s.fine.n:];spectra={}
 for k,x in vals.items():
  spec=np.fft.fft(x-x.mean());tail=abs(s.fine.modes)>=n/3
  spectra[k]=float(np.sum(abs(spec[tail])**2)/(np.sum(abs(spec)**2)+1e-100))
 fields.append({k:transfer(x,31)for k,x in vals.items()})
 rows.append(dict(run=dirname,time=data['time'],raw_coarse_momentum=rc,raw_lifted_momentum=rf,raw_normalized=rf/scale,projected_momentum=residual(zp,s.fine)[0],projection_change=float(max(abs(yp-y))),idempotence=float(max(abs(ypp-yp))),fine_only_correction=float(max(abs(high))),spectra=spectra))
comparisons=[]
for i in range(1,len(rows)):
 if abs(rows[i]['time']-rows[0]['time'])>1e-9:continue
 comparisons.append(dict(reference=rows[0]['run'],other=rows[i]['run'],fields={k:dict(max_abs=float(max(abs(fields[0][k]-fields[i][k]))),reference_variation=float(np.ptp(fields[0][k])))for k in fields[0]}))
out={'rows':rows,'comparisons':comparisons,'raw_constraint_pass':all(x['raw_normalized']<1e-7 for x in rows)};open(a.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
