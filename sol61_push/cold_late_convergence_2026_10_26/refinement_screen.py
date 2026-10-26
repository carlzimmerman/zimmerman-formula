"""Unrenormalized nested-grid diagnostic; never creates a restart parent."""
import argparse,hashlib,json,resource,sys,time
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'cold_pre_stellar_settling_2026_10_25';sys.path.insert(0,str(OLD))
from kernel_gated import Solver
from prolongation_v2 import transfer

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);start=time.monotonic();records=[];arrays={};sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();meta=json.loads((P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json').read_text())['datasets']
 # Existing hand-computable nonconstant reference polynomial, on nested meshes.
 lo=Solver(8,eta=.2,vin=.3,alpha=3);hi=Solver(16,eta=.2,vin=.3,alpha=3)
 def analytic(s):
  x=np.arcsinh(s.r*np.sinh(s.alpha)/s.R)/s.alpha
  return x*(1-x)*(1+(.2+.7j)*x)
 v=transfer(lo.r,lo.w,analytic(lo)*np.sqrt(lo.w),hi,lo.ne,lo.alpha);control=float(np.max(abs(v/np.sqrt(hi.w)-analytic(hi))));assert control<1e-12
 for gal in ['Draco','Sextans']:
  parent=P.parent/'cold_fine_late_collapse_2026_10_25'/(gal+'_fine_late');d=json.loads((parent/'result.json').read_text());assert d['status']=='wall stop' and d['birth_time'] is None;assert d['inputs_before']==d['inputs_after']
  for f,h in d['inputs_before'].items():assert sha(ROOT/f)==h
  for f,h in d['raw_sha256'].items():assert sha(parent/f)==h
  z=np.load(parent/'field.npz');units=d['units'];aa=np.array(meta[gal]['tracer_scales_pc'])/units['R_pc'];pb=lambda r:sum(-units['q']/len(aa)/np.sqrt(r*r+b*b) for b in aa);old=Solver(d['ne'],eta=units['eta_code'],vin=units['vin_code'],alpha=d['alpha'],pb=pb);s=Solver(2*d['ne'],eta=old.eta,vin=units['vin_code'],alpha=d['alpha'],pb=pb);u=z['u'][-1];v=transfer(z['r'],z['w'],u,s,old.ne,old.alpha);phi=s.phi(v);M=float(np.vdot(v,v).real);E=s.energy(v,phi);massdef=abs(M/np.vdot(u,u).real-1);energydef=abs(E-old.energy(u,old.phi(u)))/d['initial']['energy_scale'];gates=dict(mass=abs(M/d['initial']['mass']-1),energy=abs(E-d['initial']['energy'])/d['initial']['energy_scale'],phase=s.phase_bad(v),boundary=float(np.sum(abs(v[s.r>.85*s.R])**2)));limits=dict(mass=1e-8,energy=1e-4,phase=.05,boundary=1e-4);accepted=massdef<=1e-8 and energydef<=1e-4 and all(gates[k]<=lim and d['maxima'][k]<=lim for k,lim in limits.items());rec=dict(galaxy=gal,parent=str(parent.relative_to(ROOT)),T=d['t'],old_ne=old.ne,new_ne=s.ne,mass_defect=massdef,energy_defect_over_original_scale=energydef,fine_gates=gates,parent_maxima=d['maxima'],limits=limits,passes_transfer_screen=bool(accepted),renormalized=False,eligible_restart=False,scope='screen only; even a passing transfer is not independent full-IC spatial convergence');records.append(rec);arrays[gal+'_r']=s.r;arrays[gal+'_w']=s.w;arrays[gal+'_u']=v;arrays[gal+'_phi']=phi;z.close();assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<750000000;print(json.dumps(rec),flush=True)
 np.savez_compressed(out/'transfers.npz',**arrays);result=dict(records=records,polynomial_control_sup_error=control,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,seconds=time.monotonic()-start);(out/'result.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
