"""Complete-field survey diagnostics and unhidden refinement/settling coverage."""
import argparse,json,csv,hashlib,time,resource,sys
from pathlib import Path
import numpy as np
from kernel import Solver
from radial_v4 import phi_shell
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'cold_full_envelope_data_2026_10_25';sys.path.insert(0,str(OLD))
from physics import project,g_cold,baryon_g
from hst_onset import projected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);assert not(out/'result.json').exists();start=time.time();meta=json.loads((OLD/'fit_002/result.json').read_text());rows=[];runs={};comparisons=[];PM=[];pmraw=np.loadtxt(OLD/'hst_data/DRACO_BINS.dat');pm=pmraw[pmraw[:,6]>0];assert pm.shape==(5,12);expected={'DRACO_BINS.dat':'1e5fd634386465f9d3992cf7f9d4a134','README.txt':'35e33df9bafb2c91bd7ccc52bec2ed47'};assert all(hashlib.md5((OLD/'hst_data'/k).read_bytes()).hexdigest()==v for k,v in expected.items());cat=next(d for d in csv.DictReader(open(ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv')) if d['name']=='Draco');D=float(cat['distance']);ang=np.deg2rad(pm[:,7]-float(cat['position_angle']));q=1-float(cat['ellipticity']);Rp=D*1000*np.deg2rad(pm[:,6]/60);Rc=Rp*np.sqrt(q)*np.sqrt(np.cos(ang)**2+np.sin(ang)**2/q**2)
 for folder in sorted(P.iterdir()):
  if not folder.is_dir() or not(folder/'manifest.json').exists() or not(folder/'field.npz').exists():continue
  d=json.loads((folder/'result.json').read_text());z=np.load(folder/'field.npz');data=meta['datasets'][d['galaxy']];units=d['units'];r=z['r']*units['R_pc'];pos=np.array(data['R_pc']);aa=data['tracer_scales_pc'];u0=z['u'][0];s=Solver(d['ne'],eta=units['eta_code'],vin=units['vin_code'],alpha=d['alpha']);ba=np.array(aa)/units['R_pc'];s.pb=sum(-units['q']/len(ba)/np.sqrt(s.r*s.r+b*b) for b in ba);invariants=[]
  for i,t in enumerate(z['t']):
   snapshot_valid=not(d['status']=='spatial/invariant/boundary stop' and abs(float(t)-d['t'])<1e-10)
   u=z['u'][i];dm=abs(u)**2*units['M_Msun'];m=abs(u)**2;phi=z['phi'][i];K=s.kinetic(u);W=float(.5*np.sum(m*phi));Ub=float(np.sum(m*s.pb));Wb=-sum(units['q']/len(ba)*np.sum(m*s.r*s.r/(s.r*s.r+b*b)**1.5) for b in ba);core=s.inventory(u,phi,data['observed_rhalf_pc']/units['R_pc']);invariants.append(dict(t=float(t),snapshot_numerically_valid=snapshot_valid,mass=float(m.sum()),energy=K+W+Ub,K=K,W_self=W,Ub=Ub,virial=2*K+W+Wb,canonical_core_inventory=core,canonical_outer_energy=K+W+Ub-core['E']))
   for foot in ['canonical','alt']:
    for beta in [-.5,0.]:
     var=np.array([project(pos,b,lambda x:g_cold(x,r,dm)+baryon_g(x,data['stellar_mass_Msun'],aa,foot),beta) for b in aa]).T;rows.append(dict(run=folder.name,snapshot_numerically_valid=snapshot_valid,galaxy=d['galaxy'],t=float(t),time_Myr=float(t*units['t_Myr']),footing=foot,beta=beta,selected_position_population_sigma_kms=np.sqrt(var.mean(axis=0)).tolist(),selected_observed_sigma=data['selected_constant_sigma_fit']['intrinsic_sigma_kms'],cold_Mref_Msun=float(dm[s.r<data['observed_rhalf_pc']/units['R_pc']].sum()),cold_r50_pc=float(np.interp(.5*dm.sum(),np.cumsum(dm),r)),cold_total_Msun=float(dm.sum())))
   if d['galaxy']=='Draco':
    for beta in [-.5,0.]:
     for geom,rr in [('circular_R',Rp),('LVD_circularized_R',Rc)]:
      g=lambda x:g_cold(x,r,dm)+baryon_g(x,data['stellar_mass_Msun'],aa,'canonical');pred=np.array([np.sqrt(projected(rr,aa[0],g,beta,k))/(4.74047*D) for k in ['PMR','PMT']]).T;obs=pm[:,[8,10]];err=pm[:,[9,11]];PM.append(dict(run=folder.name,snapshot_numerically_valid=snapshot_valid,t=float(t),beta=beta,geometry=geom,predicted_masyr=pred.tolist(),observed_masyr=obs.tolist(),errors_masyr=err.tolist(),diagonal_squared_residual=float(np.sum(((pred-obs)/err)**2))))
  tt=z['t'];allm=abs(z['u'])**2;weights=np.zeros(len(tt))
  if len(tt)>1:
   intervals=np.diff(tt);weights[:-1]+=.5*intervals;weights[1:]+=.5*intervals;weights/=weights.sum()
  else:weights[:]=1
  meanm=weights@allm;Wmean=.5*np.sum(meanm*phi_shell(s.r,meanm));Wavg=float(sum(w*x['W_self'] for w,x in zip(weights,invariants)));Wfluct=float(sum(w*.5*np.sum((m-meanm)*phi_shell(s.r,m-meanm)) for w,m in zip(weights,allm)));fluct=dict(all_snapshots_numerically_valid=all(x['snapshot_numerically_valid'] for x in invariants),interval=[float(tt[0]),float(tt[-1])],samples=len(tt),quadrature='trapezoidal saved snapshots; not continuous-time convergence',W_of_mean_density=float(Wmean),mean_W=Wavg,fluctuation_binding=Wfluct,identity_residual=float(Wavg-Wmean-Wfluct),averaged_virial_residual=float(sum(w*x['virial'] for w,x in zip(weights,invariants))))
  runs[folder.name]=dict(sampled_fluctuations=fluct,galaxy=d['galaxy'],status=d['status'],t=d['t'],birth_time=d['birth_time'],post_birth_duration=None if d['birth_time'] is None else d['t']-d['birth_time'],stellar_numerics_valid=d['stellar_numerics_valid'],birth_failures=d['birth_failures'],birth_controls=d['birth_controls'],maxima=d['maxima'],accepted=d['accepted'],rejected=d['rejected'],accepted_solver_residual_max=d['accepted_solver_residual_max'],accepted_local_error_max=d['accepted_local_error_max'],accepted_dt_range=d['accepted_dt_range'],invariants=invariants,last_cohorts=d['history'][-1]['cohorts'],settling=d['settling'],source_backreaction_omitted_estimates=d['source_backreaction_omitted_estimates'],seconds=d['seconds'],peak_RSS_bytes=d['peak_RSS_bytes'],inputs_unchanged=d['inputs_before']==d['inputs_after']);z.close()
 pairs=[]
 for gal in ['Draco','Sextans','Fornax','LeoI']:
  for suffix in ['', '_energetic']:
   left=gal+suffix+'_base';right=gal+suffix+'_fine'
   if left in runs and right in runs:pairs.append((gal,left,right))
 for left,right in [('Draco_base','Draco_base_P9'),('Draco_base','Draco_base_continued'),('Sextans_fine','Sextans_fine_continued'),('Sextans_base','Sextans_base_continued'),('Sextans_base_continued','Sextans_fine'),('Sextans_base_continued','Sextans_fine_continued'),('Draco_base_continued','Draco_base_P9')]:
  if left in runs and right in runs:pairs.append((runs[left]['galaxy'],left,right))
 def chain(name):
  folder=P/name;dd=json.loads((folder/'result.json').read_text());zz=np.load(folder/'field.npz');q={k:zz[k] for k in ['r','w']};states={}
  if 'resume_origin' in dd:
   parent=Path(dd['resume_origin']['parent']).name;_,states=chain(parent)
  states.update({float(t):u for t,u in zip(zz['t'],zz['u'])});zz.close();return q,states
 for gal,left,right in pairs:
  a=P/(left+'/field.npz');b=P/(right+'/field.npz')
  za,sa=chain(left);zb,sb=chain(right)
  for t in sorted(set(sa)&set(sb)):
   rr=np.geomspace(max(za['r'][0],zb['r'][0]),min(za['r'][-1],zb['r'][-1]),20000);ua=sa[t]/np.sqrt(za['w']);ub=sb[t]/np.sqrt(zb['w']);ua=np.interp(rr,za['r'],ua.real)+1j*np.interp(rr,za['r'],ua.imag);ub=np.interp(rr,zb['r'],ub.real)+1j*np.interp(rr,zb['r'],ub.imag);theta=float(np.angle(np.trapz(ua.conj()*ub,rr)));ca=np.interp(rr,za['r'],np.cumsum(abs(sa[t])**2));cb=np.interp(rr,zb['r'],np.cumsum(abs(sb[t])**2));comparisons.append(dict(galaxy=gal,left=left,right=right,t=float(t),lineage_included=True,CDF_sup_difference=float(np.max(abs(ca-cb))),unrotated_wave_L2=float(np.sqrt(np.trapz(abs(ua-ub)**2,rr))),phase_aligned_wave_L2=float(np.sqrt(np.trapz(abs(ua-ub*np.exp(-1j*theta))**2,rr))),relative_uniform_phase_rad=theta,common_carrier_factored=True,amplitude_rescaled=False))

 result=dict(scope='finite cold-first settling/birth coverage and complete-field data diagnostics; no formal likelihood significance, permanent settlement or action bridge',runs=runs,rows=rows,PM=PM,refinement=comparisons,PM_author_md5=expected,seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);(out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(runs=len(runs),rows=len(rows),PM=len(PM),comparisons=len(comparisons),seconds=result['seconds'])))
if __name__=='__main__':main()
