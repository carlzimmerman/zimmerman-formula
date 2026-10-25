"""Actual-position Jeans diagnostics of complete evolved fields; no endpoint fitting."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,sys,hashlib,time,resource,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
P=Path(__file__).resolve().parent;OLD=P.parent/'cold_full_envelope_data_2026_10_25';sys.path.insert(0,str(OLD))
from physics import project,g_cold,baryon_g,window_logpdf
META=OLD/'fit_002/result.json'
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',required=True);args=a.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();meta=json.loads(META.read_text());rows=[];runs={};comparisons=[];start=time.time();paths=[Path(__file__),META,OLD/'physics.py'];gates=[]
 for directory in sorted(list(P.glob('*_v2'))+list(P.glob('*_v3'))+list(P.glob('*_v4'))):
  if not(directory/'result.json').exists():continue
  m=json.loads((directory/'result.json').read_text());z=np.load(directory/'field.npz');paths += [directory/'result.json',directory/'field.npz',directory/'manifest.json'];name=m['galaxy'];data=meta['datasets'][name];units=m['units'];R=np.array(data['R_pc']);aa=data['tracer_scales_pc'];r=z['r']*units['R_pc'];total=units['M_Msun'];sampled=[]
  # Every saved half-unit field plus the final retained state; no best-time cherry-pick.
  for i,t in enumerate(z['t']):
   if i and t==z['t'][i-1]:continue
   dm=abs(z['u'][i])**2*total;rad=data['observed_rhalf_pc'];cdf=np.cumsum(dm);inref=float(cdf[np.searchsorted(r,rad)-1]) if rad>r[0] else 0
   for footing in ['canonical','alt']:
    for beta in [-.5,0.]:
     var=np.array([project(R,a,lambda q:g_cold(q,r,dm)+baryon_g(q,data['stellar_mass_Msun'],aa,footing),beta) for a in aa]).T
     rms=np.sqrt(var.mean(axis=0));row=dict(run=directory.name,galaxy=name,t=float(t),time_Myr=float(t*units['t_Myr']),cold_total_Msun=float(dm.sum()),M_in_reference_Msun=inref,cold_r50_pc=float(np.interp(.5*dm.sum(),cdf,r)),snapshot_inside_phase_gate=bool(np.sum(.5*(dm[:-1]+dm[1:])*(abs(np.angle(z['u'][i,:-1].conj()*z['u'][i,1:]))>np.pi/3))/np.sum(.5*(dm[:-1]+dm[1:]))<=.05),footing=footing,beta=beta,selected_position_population_rms_kms=rms.tolist(),selected_observed_sigma=data['selected_constant_sigma_fit']['intrinsic_sigma_kms'])
     rows.append(row)
   sampled.append(dict(t=float(t),M_in_reference_Msun=inref))
  runs[directory.name]=dict(status=m['status'],t=m['t'],stellar_numerics_valid=m['stellar_numerics_valid'],birth_failures=m['birth_failures'],maxima=m['maxima'],seconds=m['seconds'],peak_RSS_bytes=m['peak_RSS_bytes'],source_backreaction_omitted_estimates=m['source_backreaction_omitted_estimates'],last_cohorts=m['history'][-1]['cohorts'],inputs_unchanged=m['inputs_before']==m['inputs_after'],supply=total,snapshots=sampled)
  z.close()
 for gal,version in [(g,v) for g in ['Draco','Sextans','Fornax','Leo I'] for v in ['v2','v3','v4']]:
  a=P/(gal.replace(' ','')+'_base_'+version);b=P/(gal.replace(' ','')+'_fine_'+version)
  if not(a/'field.npz').exists() or not(b/'field.npz').exists():continue
  za=np.load(a/'field.npz');zb=np.load(b/'field.npz');common=sorted(set(za['t'])&set(zb['t']))
  for t in common:
   i=list(za['t']).index(t);j=list(zb['t']).index(t);ma=abs(za['u'][i])**2;mb=abs(zb['u'][j])**2;rr=np.geomspace(max(za['r'][0],zb['r'][0]),min(za['r'][-1],zb['r'][-1]),10000);ca=np.interp(rr,za['r'],np.cumsum(ma));cb=np.interp(rr,zb['r'],np.cumsum(mb));ua=za['u'][i]/np.sqrt(za['w']);ub=zb['u'][j]/np.sqrt(zb['w']);uai=np.interp(rr,za['r'],ua.real)+1j*np.interp(rr,za['r'],ua.imag);ubi=np.interp(rr,zb['r'],ub.real)+1j*np.interp(rr,zb['r'],ub.imag);wave=float(np.sqrt(np.trapz(abs(uai-ubi)**2,rr)));comparisons.append(dict(galaxy=gal,version=version,t=float(t),CDF_sup_difference=float(np.max(abs(ca-cb))),unrotated_residual_wave_L2=wave))
  za.close();zb.close()
 # Raw physical wave shares exact static carrier between meshes; unrotated norm is not aligned away.
 result=dict(scope='complete-profile equilibrium moment diagnostics at actual selected survey positions; passive orbit validity separately; no likelihood significance or accepted formation endpoint',runs=runs,rows=rows,refinement=comparisons,inputs_sha256={str(f.relative_to(P.parents[1])):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(runs=len(runs),rows=len(rows),comparisons=len(comparisons),seconds=result['seconds'],peak_RSS_bytes=result['peak_RSS_bytes'])))
if __name__=='__main__':main()
