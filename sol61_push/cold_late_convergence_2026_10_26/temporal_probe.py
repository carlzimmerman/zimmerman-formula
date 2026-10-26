"""Local temporal refinement from identical accepted late states, fixed grid."""
import argparse,hashlib,json,resource,sys,time
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1];sys.path.insert(0,str(P.parent/'cold_pre_stellar_settling_2026_10_25'))
from kernel_gated import Solver

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);start=time.monotonic();rows=[];pairs=[];arrays={};meta=json.loads((P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json').read_text())['datasets'];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
 for gal in ['Draco','Sextans']:
  parent=P.parent/'cold_fine_late_collapse_2026_10_25'/(gal+'_fine_late');d=json.loads((parent/'result.json').read_text());assert d['status']=='wall stop' and d['birth_time'] is None
  for f,h in d['raw_sha256'].items():assert sha(parent/f)==h
  assert d['inputs_before']==d['inputs_after']
  for f,h in d['inputs_before'].items():assert sha(ROOT/f)==h
  z=np.load(parent/'field.npz');units=d['units'];aa=np.array(meta[gal]['tracer_scales_pc'])/units['R_pc'];pb=lambda r:sum(-units['q']/len(aa)/np.sqrt(r*r+b*b) for b in aa);s=Solver(d['ne'],eta=units['eta_code'],vin=units['vin_code'],alpha=d['alpha'],pb=pb);assert np.array_equal(s.r,z['r']) and np.array_equal(s.w,z['w']);initial=z['u'][-1].copy();z.close();ref=meta[gal]['observed_rhalf_pc']/units['R_pc'];results=[]
  for h in [1e-4,5e-5,2.5e-5]:
   u=initial.copy();phi=s.phi(u);n=round(.02/h);case_start=time.monotonic();done=0;status='completed';maxima=dict(mass=0.,energy=0.,phase=0.,boundary=0.,solver=0.)
   for i in range(n):
    if time.monotonic()-case_start>60:status='wall stop';break
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>750000000:status='memory stop';break
    un,pn,info=s.order4(u,phi,h);maxima['solver']=max(maxima['solver'],info['residual'])
    if not info['converged']:status='solver stop';break
    u,phi=un,pn;done+=1;m=abs(u)**2;values=dict(mass=abs(m.sum()/d['initial']['mass']-1),energy=abs(s.energy(u,phi)-d['initial']['energy'])/d['initial']['energy_scale'],phase=s.phase_bad(u),boundary=float(m[s.r>.85*s.R].sum()))
    for k,v in values.items():maxima[k]=max(maxima[k],v)
    if not np.all(np.isfinite(u)) or any(maxima[k]>v for k,v in dict(mass=1e-8,energy=1e-4,phase=.05,boundary=1e-4,solver=1e-10).items()):status='numerical gate stop';break
   rec=dict(galaxy=gal,initial_T=d['t'],h=h,requested_deltaT=.02,attained_deltaT=done*h,status=status,steps=done,maxima=maxima,final_reference_mass_code=float(np.sum(abs(u[s.r<ref])**2)),seconds=time.monotonic()-case_start);rows.append(rec);results.append((rec,u.copy()));arrays[gal+'_'+str(h)]=u;print(json.dumps(rec),flush=True)
  for (a0,u0),(a1,u1) in zip(results[:-1],results[1:]):
   if a0['status']!='completed' or a1['status']!='completed':continue
   theta=float(np.angle(np.vdot(u0,u1)));pairs.append(dict(galaxy=gal,deltaT=.02,h_coarse=a0['h'],h_fine=a1['h'],wave_L2=float(np.linalg.norm(u1-u0)),aligned_wave_L2=float(np.linalg.norm(u1*np.exp(-1j*theta)-u0)),CDF_sup_difference=float(np.max(abs(np.cumsum(abs(u1)**2)-np.cumsum(abs(u0)**2)))),reference_mass_difference=abs(a0['final_reference_mass_code']-a1['final_reference_mass_code'])))
 np.savez_compressed(out/'temporal_fields.npz',**arrays);result=dict(scope='local time refinement only, identical inherited state and8192spatial grid; no birth or independent spatial convergence claim',rows=rows,pairs=pairs,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,seconds=time.monotonic()-start);(out/'result.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
