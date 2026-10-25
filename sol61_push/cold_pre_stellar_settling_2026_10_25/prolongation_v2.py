"""Bounded nested-basis transfer check at a valid earlier checkpoint."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from kernel_gated import Solver
P=Path(__file__).resolve().parent

def transfer(oldr,oldw,oldu,s,ne,alpha):
 xi=np.arcsinh(s.r*np.sinh(alpha)/s.R)/alpha;el=np.minimum((xi*ne).astype(int),ne-1);zz=2*(xi*ne-el)-1;nodes=np.array([-1.,-1/np.sqrt(5),1/np.sqrt(5),1.]);amp=np.r_[0,oldu/np.sqrt(oldw),0];q=np.zeros(len(s.r),complex)
 for i in range(4):
  li=np.ones(len(s.r))
  for j in range(4):
   if i!=j:li*= (zz-nodes[j])/(nodes[i]-nodes[j])
  q+=li*amp[3*el+i]
 return q*np.sqrt(s.w)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);par=P/'Draco_base_continued';d=json.loads((par/'result.json').read_text());progress=json.loads((par/'progress.json').read_text());assert progress['progress_t']==2.5 and all(x['numerically_valid'] for x in d['history'] if x['t']<=2.5)
 for f,h in d['raw_sha256'].items():assert hashlib.sha256((par/f).read_bytes()).hexdigest()==h
 uinfo=d['units'];meta=json.loads((P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json').read_text())['datasets']['Draco'];aa=np.array(meta['tracer_scales_pc'])/uinfo['R_pc'];pb=lambda r:sum(-uinfo['q']/len(aa)/np.sqrt(r*r+b*b) for b in aa);s=Solver(2*d['ne'],eta=uinfo['eta_code'],vin=uinfo['vin_code'],alpha=d['alpha'],pb=pb);old=Solver(d['ne'],eta=uinfo['eta_code'],vin=uinfo['vin_code'],alpha=d['alpha'],pb=pb);z=np.load(par/'field.npz');i=list(z['t']).index(2.5);u=z['u'][i];v=transfer(z['r'],z['w'],u,s,d['ne'],d['alpha']);phi=s.phi(v);M=float(np.vdot(v,v).real);E=s.energy(v,phi);mass_defect=abs(M/np.vdot(u,u).real-1);energy_defect=abs(E-old.energy(u,old.phi(u)))/d['initial']['energy_scale'];gates=dict(mass=abs(M/d['initial']['mass']-1),energy=abs(E-d['initial']['energy'])/d['initial']['energy_scale'],phase=s.phase_bad(v),boundary=float(np.sum(abs(v[s.r>.85*s.R])**2)));limits=dict(mass=1e-8,energy=1e-4,phase=.05,boundary=1e-4);passed=mass_defect<=1e-8 and energy_defect<=1e-4 and all(gates[k]<=t and progress['maxima'][k]<=t for k,t in limits.items());result=dict(scope='valid-prefix nested finite-element prolongation screen only; no renormalization, no energy reset',parent=str(par),checkpoint_time=2.5,old_ne=d['ne'],new_ne=s.ne,mass_defect=mass_defect,energy_defect_over_original_scale=energy_defect,potential_sup_difference=float(np.max(abs(phi-np.interp(s.r,z['r'],z['phi'][i])))),fine_gates=gates,parent_cumulative_gates=progress['maxima'],passes_continuation_screen=bool(passed));(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
