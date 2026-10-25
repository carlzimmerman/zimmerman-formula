"""Interpret only saved finite coherent histories; never infer stellar survival from absence."""
import json,hashlib,pathlib,importlib.util,math
import numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];prevfile=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json';modelsfile=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json';surveyfile=modelsfile.parent/'survey.py';ref_file=modelsfile.parent/'survey_results.json'
spec=importlib.util.spec_from_file_location('survey',surveyfile);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);d=s.load();prev=json.loads(prevfile.read_text())['galaxies'];models={v['name']:v for v in json.loads(modelsfile.read_text())['models']};ref=min(q['nll'] for q in json.loads(ref_file.read_text())['continuous_best'] if q['footing']=='canonical' and q['beta']==0 and q['tracer_taper_pc'] is None)
run_paths=sorted((P/'runs').glob('*.json'))
files=[pathlib.Path(__file__),prevfile,modelsfile,surveyfile,ref_file,modelsfile.parent/'data/members.tsv',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']+run_paths+[p.with_name(p.stem+'_fields.npz') for p in run_paths]
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();rows=[]
for path in run_paths:
 q=json.loads(path.read_text());ancestor=q
 while ancestor['parameters'].get('resume'):
  ancestor=json.loads((P/'runs'/(ancestor['parameters']['resume']+'.json')).read_text())
 par=q['parameters'];name=par['galaxy'];h=q['history'][-1];m=models[name];phys=q['physical'];M=phys['Munit_Msun'];R=phys['Runit_pc'];V=phys['Vunit_kms'];rr=np.array(q['radial_grid']);cdf=np.array(h['cdf']);edges=np.r_[0,(rr+np.r_[rr[1:],par['rmax']])/2];cdf_edges=np.r_[0,cdf];f=np.load(path.with_name(path.stem+'_fields.npz'));v=f['final'];lm=f['lm'];r=np.array(f['r']);shell=np.sum(abs(v)**2,axis=1)
 def cold(rad):return s.G*M*np.interp(rad/R,edges,cdf_edges,left=0,right=cdf[-1])/rad**2
 apert=R*np.array([.5,1.,2.,3.,5.]);target=m['cold_mass']*apert**3/(apert*apert+m['cold_scale_pc']**2)**1.5;got=M*np.interp(apert/R,edges,cdf_edges)
 mass_mismatch=float(np.max(abs(got/target-1)));corel=sum(np.sum(abs(v[r<1,j])**2) for j,(l,mm) in enumerate(lm) if l>4);envel=sum(np.sum(abs(v[r>=1,j])**2) for j,(l,mm) in enumerate(lm) if l>4)
 mode_mass=np.sum(abs(v)**2,axis=0);ell2=np.array([l*(l+1) for l,mm in lm]);marr=np.array([mm for l,mm in lm]);fraction=np.clip((1-edges[:-1])/(edges[1:]-edges[:-1]),0,1)
 Jinner=float(phys['eta_code']*np.sum(abs(v)**2*marr[None,:]*fraction[:,None]));Jouter=h['Jz']-Jinner
 coremass=float(np.sum(shell*fraction));core_j_ratio=(Jinner/max(coremass,1e-30))/q['initial']['Jz'];core_j_rms=par['eta']*float(np.sqrt(np.sum(abs(v)**2*ell2[None,:]*fraction[:,None])/max(coremass,1e-30)))
 tail=[x for x in q['history'] if x['t']>=max(24.,.75*h['t'])];stat=None
 if len(tail)>2:stat={'core_mass_range_over_mean':float(np.ptp([x['M_inner'] for x in tail])/np.mean([x['M_inner'] for x in tail])),'rhalf_range_over_mean':float(np.ptp([x['rhalf'] for x in tail])/np.mean([x['rhalf'] for x in tail]))}
 phase=30*(rr[1:]-rr[:-1])*R/par['eta'];outer=(rr[:-1]>=.7*par['absorb'])&(rr[:-1]<=par['absorb']);maxphase=float(np.max(phase[outer]))
 row={'tag':path.stem,'name':name,'status':q['status'],'T_code':h['t'],'T_Myr':h['t']*phys['tunit_Myr'],'L':par['lmax'],'mmax':par['mmax'],'nr':par['nr'],'dt':par['dt'],'gas':par['gas'],'initial_mass_Msun':M,'final_mass_Msun':h['M']*M,'removed_mass_Msun':h['removed']['M']*M,'removed_mass_fraction':h['removed']['M'],'removed_J_fraction':h['removed']['Jz']/q['initial']['Jz'],'retained_specific_J_over_initial':(h['Jz']/h['M'])/q['initial']['Jz'],'core_specific_J_over_initial_global':core_j_ratio,'core_rms_specific_J_pc_kms':core_j_rms,'inner_J_fraction':Jinner/q['initial']['Jz'],'outer_J_fraction':Jouter/q['initial']['Jz'],'positive_sink_energy_code':h['positive_sink_E'],'negative_sink_energy_code':h['negative_sink_E'],'net_sink_energy_code':h['removed']['E'],'source_work_code':h['source_work'],'initial_energy_Msun_kms2':q['initial_energy_Msun_kms2'],'target_energy_Msun_kms2':q['target_energy_Msun_kms2'],'minimum_external_work_for_target_plus_nonnegative_outflow_Msun_kms2':max(0,-q['initial_minus_target_energy_Msun_kms2']),'actual_source_work_Msun_kms2':h['source_work']*M*V*V,'final_energy_Msun_kms2':h['E']*M*V*V,'final_high_l_mass_fraction_of_initial':h['l_gt4_mass'],'initial_high_l_mass_fraction':q['initial']['l_gt4_mass'],'final_high_l_mass_Msun_inside_stellar_half_light':corel*M,'final_high_l_mass_Msun_outside_stellar_half_light':envel*M,'final_l_lplus1_per_retained_mass':float(mode_mass@ell2/h['M']),'l_edge_mass_fraction_retained':h['l_edge_mass']/h['M'],'m_edge_mass_fraction_retained':h['m_edge_mass']/h['M'],'max_aperture_mass_relative_mismatch':mass_mismatch,'aperture_pc':apert.tolist(),'cold_enclosed_Msun':got.tolist(),'target_cold_enclosed_Msun':target.tolist(),'stationarity':stat,'max_E_residual':max(abs(x.get('E_residual',0)) for x in q['history']),'max_J_residual':max(abs(x.get('J_residual',0)) for x in q['history']),'max_M_residual':max(abs(x.get('M_residual',0)) for x in q['history']),'outer_30kms_phase_per_cell':maxphase,'outer_30kms_phase_gate_pi_over4':maxphase<np.pi/4,'peak_RSS_bytes':q['peak_RSS_bytes'],'runtime_s':q['seconds']}
 row['aperture_scope']='about original cloud origin, not necessarily a fragment/stellar centre'
 row['angular_momentum_scope']='Jz about original cloud axis; not intrinsic off-axis fragment spin'
 row['energy_ledger_normalization']=q.get('energy_normalization','producer initial energy or inherited recorded scale')
 row['producer_energy_ledger_scale_code']=q.get('energy_ledger_scale_code',abs(q['initial']['E']))
 row['equivalent_initial_collective_energy_speed_kms']=(math.sqrt(2*q['initial']['E'])*V if q['initial']['E']>0 else None)
 row['escape_reference_scope']='local instantaneous test-potential escape reference; not global infinity energy' if ancestor.get('escape_phase_scope') else None
 row['escape_phase_scope']=ancestor.get('escape_phase_scope')
 row['initial_monopole_negative_weight']=ancestor.get('initial_monopole_negative_weight')
 row['monopole_bound_spectrum_complete']=ancestor.get('monopole_bound_spectrum_complete')
 row['marginal_infall_speed_kms']=q.get('marginal_infall_speed_kms')
 row['additional_positive_work_needed_after_recorded_outflow_Msun_kms2']=max(0,q['target_energy_Msun_kms2']-(q['initial_energy_Msun_kms2']+row['actual_source_work_Msun_kms2']-h['removed']['E']*M*V*V))
 row['numerical_ledger_pass']=row['max_E_residual']<.01 and row['max_J_residual']<.01 and row['max_M_residual']<1e-8
 if par['T']>0:
  if name=='Sextans':
   def gb(rad):
    gn=sum(s.G*250000*rad/(rad*rad+ar*ar)**1.5 for ar in d['aa']);return .5*(gn+np.sqrt(gn*gn+4*s.A0['canonical']*gn))
   var=np.array([s.projection(d['R'],ar,lambda rad:gb(rad)+cold(rad)) for ar in d['aa']]).T;fit=s.fit(d,var,np.zeros_like(var),fixed_mass=0.)
   row['stellar_diagnostic']={'scope':'actual-position spherical-monopole Jeans stress diagnostic, not a nonspherical stellar DF fit','nll':fit['nll'],'twice_nll_above_endpoint':2*(fit['nll']-ref)}
  else:
   x,wt=np.polynomial.legendre.leggauss(128);theta=(x+1)*np.pi/4;wt*=np.pi/4;rad=R*np.tan(theta);cold2=R*np.sum(wt*np.sin(theta)**3*cold(rad));base=prev[name]['moments']['canonical'][0]['sigma_baryon']**2
   row['stellar_diagnostic']={'scope':'full-Plummer global monopole moment, not selected-data or live stellar DF','sigma_kms':float(np.sqrt(base+cold2)),'observed_sigma_kms':float(prev[name]['observations']['vlos_sigma'])}
 row['profile_gate_10percent']=mass_mismatch<.1;row['stellar_response_test']='not launched: require converged remnant profile and stationarity first'
 rows.append(row)
after=hashes();assert before==after
out={'scope':'finite coherent collapse and history-specific energy obligations; no four-dwarf or stellar-survival closure','inputs_before':before,'inputs_after':after,'results':rows};(P/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:
 if r['T_code']>0:print(r['tag'],'T',r['T_code'],'ledger',r['numerical_ledger_pass'],'highl',round(r['final_high_l_mass_fraction_of_initial'],4),'loss',round(r['removed_mass_fraction'],4),'Jout',round(r['removed_J_fraction'],4),'inner_million',round(r['cold_enclosed_Msun'][1]/1e6,2),'stellar',r.get('stellar_diagnostic'),flush=True)
