"""Instantaneous and time-averaged MONOPOLE equilibrium diagnostics, not live stars."""
import json,pathlib,hashlib,importlib.util
import numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];surveyfile=ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py';prevfile=ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json';ref_file=surveyfile.parent/'survey_results.json'
spec=importlib.util.spec_from_file_location('survey',surveyfile);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);d=s.load();old=json.loads(prevfile.read_text())['galaxies'];refs=json.loads(ref_file.read_text())['continuous_best'];ref=min(v['nll'] for v in refs if v['footing']=='canonical' and v['beta']==0 and v['tracer_taper_pc'] is None)
tags=['draco_L12_long','draco_marginal','draco_escape_long','sextans_L24_long','sextans_marginal','sextans_escape','sextans_escape_long']
files=[P/'runs'/f'{t}.json' for t in tags]+[pathlib.Path(__file__),surveyfile,prevfile,ref_file,surveyfile.parent/'data/members.tsv',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']
def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();rows=[]
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());u=q['physical'];r=np.array(q['radial_grid']);R=u['Runit_pc'];M=u['Munit_Msun'];name=q['parameters']['galaxy'];T=q['history'][-1]['t'];tail=[h for h in q['history'] if h['t']>=.75*T];mean_cdf=np.mean([h['cdf'] for h in tail],axis=0)
 if name=='Draco':
  base=old[name]['moments']['canonical'][0]['sigma_baryon']**2
  def diag(cdf):
   shell=np.diff(np.r_[0,cdf]);return float(np.sqrt(base+s.G*M/(3*R)*np.sum(shell*(1+r*r)**-1.5)))
  hist=[dict(t=h['t'],T_Myr=h['t']*u['tunit_Myr'],sigma_equilibrium_kms=diag(h['cdf'])) for h in q['history']]
  late=[diag(h['cdf']) for h in tail];mean={'sigma_from_time_mean_potential_kms':diag(mean_cdf),'instantaneous_late_sigma_range':[min(late),max(late)],'observed_sigma':9.55}
 else:
  edges=np.r_[0,(r+np.r_[r[1:],q['parameters']['rmax']])/2]
  def diag(cdf):
   def g(rad):
    gn=sum(s.G*250000*rad/(rad*rad+ar*ar)**1.5 for ar in d['aa']);baryon=.5*(gn+np.sqrt(gn*gn+4*s.A0['canonical']*gn));cold=s.G*M*np.interp(rad/R,edges,np.r_[0,cdf],left=0,right=cdf[-1])/rad**2
    return baryon+cold
   var=np.array([s.projection(d['R'],ar,g) for ar in d['aa']]).T;f=s.fit(d,var,np.zeros_like(var),fixed_mass=0.);return 2*(f['nll']-ref)
  # Exactly specified sparse sample for the expensive survey diagnostic.
  candidates=[h for h in q['history'] if h['t']>=20];sample=candidates[::max(1,len(candidates)//16)]
  if sample[-1] is not candidates[-1]:sample.append(candidates[-1])
  hist=[dict(t=h['t'],T_Myr=h['t']*u['tunit_Myr'],twice_NLL_above_reference=diag(h['cdf'])) for h in sample];mean={'twice_NLL_from_time_mean_potential':diag(mean_cdf),'last_quarter_t_range':[tail[0]['t'],tail[-1]['t']]}
 rows.append({'tag':tag,'name':name,'scope':'instantaneous equilibrium requirement and time-mean monopole; no actual stellar velocities evolved','history':hist,'last_quarter_mean':mean})
after=hashes();assert before==after
out={'scope':'posthoc averaging diagnostic; does NOT convert failed original profile/stationarity gates to passes','inputs_before':before,'inputs_after':after,'results':rows}
(P/'diagnostic_history.json').write_text(json.dumps(out,indent=2)+'\n')
for row in rows:print(row['tag'],row['last_quarter_mean'],flush=True)
