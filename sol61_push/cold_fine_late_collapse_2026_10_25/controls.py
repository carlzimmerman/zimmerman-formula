"""Reconcile original same-PDE controls; do not promote early coverage to late closure."""
import argparse,json,hashlib,time,resource,sys
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'cold_formation_data_2026_10_25';DATA=P.parent/'cold_full_envelope_data_2026_10_25';sys.path.insert(0,str(DATA));from physics import project,g_cold,baryon_g

def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();start=time.monotonic();meta=json.loads((DATA/'fit_002/result.json').read_text());rows=[];runs={};comparisons=[]
 for gal in ['Fornax','LeoI']:
  data=meta['datasets'][gal];M=.5*data['supply_Msun'];R=np.sqrt(.00430091*M/(.1*9.3603e-11*3.085677581491367e10));V=np.sqrt(.00430091*M/R);expected=dict(M_Msun=M,R_pc=R,V_kms=V,t_Myr=.97779222168*R/V,eta_code=1500/(R*V),vin_code=10/V,q=data['stellar_mass_Msun']/M)
  for level in ['base','fine']:
   name=gal+'_'+level+'_v4';folder=OLD/name;d=json.loads((folder/'result.json').read_text());mf=json.loads((folder/'manifest.json').read_text());assert mf['run']['status']=='completed' and mf['run']['exit_status']==0;assert d['inputs_before']==d['inputs_after'];assert all(sha(ROOT/f)==h for f,h in d['inputs_before'].items());assert all(sha(ROOT/f['path'])==f['sha256']==f['sha256_after'] for f in mf['input_artifacts']);assert all(sha(ROOT/f['path'])==f['sha256'] for f in mf['outputs']);assert all(np.isclose(d['units'][k],v,rtol=1e-13,atol=0) for k,v in expected.items());z=np.load(folder/'field.npz');times=[]
   for i,t in enumerate(z['t']):
    if i and abs(t-z['t'][i-1])<1e-12:continue
    valid=not(d['status']=='numerical gate stop' and abs(float(t)-d['t'])<1e-10);dm=abs(z['u'][i])**2*M;r=z['r']*R;times.append(float(t))
    for footing in ['canonical','alt']:
     for beta in [-.5,0.]:
      pred=[float(np.sqrt(np.mean(project(np.array(data['R_pc']),aa,lambda x:g_cold(x,r,dm)+baryon_g(x,data['stellar_mass_Msun'],data['tracer_scales_pc'],footing),beta)))) for aa in data['tracer_scales_pc']];rows.append(dict(run=name,galaxy=gal,t=float(t),time_Myr=float(t*expected['t_Myr']),snapshot_numerically_valid=valid,footing=footing,beta=beta,selected_position_population_sigma_kms=pred,selected_observed_sigma=data['selected_constant_sigma_fit']['intrinsic_sigma_kms'],cold_Mref_Msun=float(dm[z['r']<data['observed_rhalf_pc']/R].sum())))
   runs[name]=dict(status=d['status'],t=d['t'],times=times,ne=d['ne'],alpha=d['alpha'],dt=d['dt'],maxima=d['maxima'],units=d['units'],source_hashes_verified=True,early_star_controls=d['birth_controls'],stellar_numerics_valid=d['stellar_numerics_valid'],no_later_birth_substitution=True);z.close()
  za=np.load(OLD/(gal+'_base_v4')/'field.npz');zb=np.load(OLD/(gal+'_fine_v4')/'field.npz')
  for t in sorted(set(za['t'])&set(zb['t'])):
   i=list(za['t']).index(t);j=list(zb['t']).index(t);rr=np.geomspace(max(za['r'][0],zb['r'][0]),min(za['r'][-1],zb['r'][-1]),20000);ua=za['u'][i]/np.sqrt(za['w']);ub=zb['u'][j]/np.sqrt(zb['w']);ua=np.interp(rr,za['r'],ua.real)+1j*np.interp(rr,za['r'],ua.imag);ub=np.interp(rr,zb['r'],ub.real)+1j*np.interp(rr,zb['r'],ub.imag);theta=float(np.angle(np.trapz(ua.conj()*ub,rr)));ca=np.interp(rr,za['r'],np.cumsum(abs(za['u'][i])**2));cb=np.interp(rr,zb['r'],np.cumsum(abs(zb['u'][j])**2));comparisons.append(dict(galaxy=gal,t=float(t),CDF_sup_difference=float(np.max(abs(ca-cb))),unrotated_wave_L2=float(np.sqrt(np.trapz(abs(ua-ub)**2,rr))),phase_aligned_wave_L2=float(np.sqrt(np.trapz(abs(ua-ub*np.exp(-1j*theta))**2,rr))),uniform_phase_rad=theta,common_carrier_factored=True))
  za.close();zb.close()
 result=dict(scope='CCT019 original10km/s same-continuous-PDE controls only; different finite scheme; early passive stars cannot replace later-born stars; no late four-dwarf closure',runs=runs,rows=rows,comparisons=comparisons,seconds=time.monotonic()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert result['peak_RSS_bytes']<750000000;(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(runs=len(runs),rows=len(rows),comparisons=len(comparisons),seconds=result['seconds'])))
if __name__=='__main__':main()
