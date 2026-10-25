"""Recompute finite artifact checks; success is bookkeeping/numerics, not formation."""
import argparse,hashlib,json,resource,subprocess,time,sys
from pathlib import Path
import numpy as np
from radial_v2 import Radial,phi_shell
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();start=time.time();checks=[];rows=[]
 def check(name,condition,value=None):checks.append(dict(name=name,passed=bool(condition),value=value))
 for f in ['test_radial.py','test_stars.py','check_controls.py','check_controls_v4.py','test_gauge.py']:
  run=subprocess.run(['/usr/bin/python3',str(P/f)],capture_output=True,text=True);check(f,run.returncode==0,run.stdout+run.stderr)
 validator='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'
 for folder in sorted(P.iterdir()):
  if not folder.is_dir() or not(folder/'manifest.json').exists() or not(folder/'field.npz').exists():continue
  run=subprocess.run(['/opt/homebrew/bin/python3',validator,str(folder/'manifest.json'),'--root',str(ROOT)],capture_output=True,text=True);check(folder.name+'_manifest',run.returncode==0,run.stdout+run.stderr);d=json.loads((folder/'result.json').read_text());check(folder.name+'_unchanged_inputs',d['inputs_before']==d['inputs_after']);check(folder.name+'_memory',d['peak_RSS_bytes']<750000000,d['peak_RSS_bytes']);z=np.load(folder/'field.npz');s=Radial(d['ne'],eta=d['units']['eta_code'],vin=d['units']['vin_code'],alpha=d.get('alpha',12.));meta=json.loads((P.parent/'cold_full_envelope_data_2026_10_25/fit_002/result.json').read_text())['datasets'][d['galaxy']];aa=np.array(meta['tracer_scales_pc'])/d['units']['R_pc'];s.pb=sum(-d['units']['q']/len(aa)/np.sqrt(s.r*s.r+a*a) for a in aa);md=0.;ed=0.;pd=0.
  for u,phi in zip(z['u'],z['phi']):
   m=abs(u)**2;md=max(md,abs(m.sum()-d['initial']['mass']));pd=max(pd,float(np.max(abs(phi_shell(z['r'],m)-phi))));ed=max(ed,abs(s.energy(u,phi)-d['initial']['energy'])/d['initial']['energy_scale'])
  check(folder.name+'_raw_mass',md<1e-8,md);check(folder.name+'_raw_energy',ed<1e-4,ed);check(folder.name+'_raw_Phi',pd<1e-12,pd);check(folder.name+'_full_supply',abs(d['units']['M_Msun']/(.5*meta['supply_Msun'])-1)<1e-14)
  final=d['history'][-1];check(folder.name+'_final_cold_aperture',abs(final['cold_in_reference_radius']-np.sum(abs(z['u'][-1])**2*(z['r']<meta['observed_rhalf_pc']/d['units']['R_pc'])))<1e-12)
  st=np.load(folder/'stars.npz')
  for i,c in enumerate(final['cohorts']):
   x=st[str(i)+'_x'];v=st[str(i)+'_v'];check(folder.name+'_star_r50_'+str(i),abs(np.median(np.linalg.norm(x,axis=1))-c['stars']['r50'])<1e-12);check(folder.name+'_star_sigma_'+str(i),abs(np.std(v[:,2])-c['stars']['sigma_los'])<1e-12)
  rows.append(dict(run=folder.name,status=d['status'],requested_T=d['requested_T'],t=d['t'],stellar_numerics_valid=d.get('stellar_numerics_valid',False),late_birth_reached=d['t']>=4,tag_experiment_reached=d['t']>=4,raw_mass_drift=md,raw_energy_error=ed,raw_Phi_error=pd));st.close();z.close()
 ray=[]
 for gal in ['Draco','Sextans','Fornax','LeoI']:
  aa=np.load(P/(gal+'_base_v4/field.npz'));bb=np.load(P/(gal+'_fine_v4/field.npz'))
  for t in sorted(set(aa['t'])&set(bb['t'])):
   i=list(aa['t']).index(t);j=list(bb['t']).index(t);rr=np.geomspace(max(aa['r'][0],bb['r'][0]),min(aa['r'][-1],bb['r'][-1]),10000);u=aa['u'][i]/np.sqrt(aa['w']);v=bb['u'][j]/np.sqrt(bb['w']);u=np.interp(rr,aa['r'],u.real)+1j*np.interp(rr,aa['r'],u.imag);v=np.interp(rr,bb['r'],v.real)+1j*np.interp(rr,bb['r'],v.imag);theta=float(np.angle(np.trapz(u.conj()*v,rr)));ray.append(dict(galaxy=gal,t=float(t),relative_uniform_phase_rad=theta,unrotated_wave_L2=float(np.sqrt(np.trapz(abs(u-v)**2,rr))),phase_aligned_wave_L2=float(np.sqrt(np.trapz(abs(u-v*np.exp(-1j*theta))**2,rr))),amplitude_rescaled=False))
  aa.close();bb.close()
 result=dict(phase_ray_diagnostics=ray,assertion_tested='finite producer provenance, independent invariant/raw-array recomputation and unit controls; stopped/inaccurate physical hypotheses remain unaccepted',checks=checks,all_checks_passed=all(c['passed'] for c in checks),runs=rows,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(checks=len(checks),passed=result['all_checks_passed'],runs=len(rows),seconds=result['seconds'])));raise SystemExit(0 if result['all_checks_passed'] else 1)
if __name__=='__main__':main()
