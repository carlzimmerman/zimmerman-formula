import argparse,json
from pathlib import Path
import numpy as np
from expanded_constraints import ExpandedPadded
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('runs',nargs='+');a=ap.parse_args();rows=[]
for dirname in a.runs:
 data=json.loads((Path(dirname)/'result.json').read_text());n=data['n'];m=data['evaluation'];s=ExpandedPadded(n,evaluation=m);y=np.array(data['final_state']);s.fine.P=np.array(data['final_P'])
 if 'final_gvar' in data:s.fine.gvar=np.array(data['final_gvar'])
 z=s.fine.project(s.lift(y,m));native=s.fine.rhs(z);coarse=s.lift(native,n);dot=s.lift(coarse,m)
 l,b,p,r=s.fine.unpack(z);L,bt,pt,rt=s.fine.unpack(dot);f=s.fine.constrain(z)
 bx=s.fine.dx(b);S=2*s.fine.dxx(b)+3*bx*bx;C=2*s.fine.M**2*np.exp(4*b)/p;bxt=s.fine.dx(bt)
 source=bxt*f['pb']+bx*(rt+4*C*bt*S+C*(2*s.fine.dxx(bt)+6*bx*bxt))+pt.mean()
 diagonal=bx*C*S/p;symbol=1j*s.fine.k*s.fine.modes;symbol[0]=1
 inv=lambda v:np.fft.ifft(np.fft.fft(v)/symbol).real
 pt_recon=s.fine.solve(lambda v:s.fine.dx(v)+diagonal*v+v.mean(),source,inv)
 nativept=s.fine.unpack(native)[2];scale=max(1e-10,float(max(abs(nativept))))
 diff=pt_recon-nativept;low=s.lift(np.concatenate([[0],diff,np.zeros(m),np.zeros(m)]),n)[1:1+n]
 row=dict(run=dirname,time=data['time'],canonical_pt_scale=scale,represented_relative=float(max(abs(low))/scale),full_relative=float(max(abs(diff))/scale),raw_momentum=data['records'][-1].get('raw_momentum_normalized'))
 rows.append(row)
out={'rows':rows,'represented_pass':all(r['represented_relative']<=1e-6 for r in rows)};Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
