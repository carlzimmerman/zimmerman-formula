"""Posthoc same-data, same-footing anisotropy robustness, not a gate amendment."""
import pathlib,json,hashlib,importlib.util,numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];sf=ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py';rf=sf.parent/'survey_results.json';tags=['sextans_escape','sextans_escape_long'];files=[pathlib.Path(__file__),sf,rf,sf.parent/'data/members.tsv',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv']+[P/'runs'/f'{t}.json' for t in tags]
def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();sp=importlib.util.spec_from_file_location('survey',sf);s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s);d=s.load();refs=json.loads(rf.read_text())['continuous_best'];rows=[]
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());u=q['physical'];r=np.array(q['radial_grid']);edges=np.r_[0,(r+np.r_[r[1:],q['parameters']['rmax']])/2];h=q['history'][-1];tail=[v for v in q['history'] if v['t']>=.75*h['t']]
 for stage,cdf in [('final',np.array(h['cdf'])),('late_mean',np.mean([v['cdf'] for v in tail],axis=0))]:
  for footing,a0 in s.A0.items():
   def g(rad):
    gn=sum(s.G*250000*rad/(rad*rad+ar*ar)**1.5 for ar in d['aa']);base=.5*(gn+np.sqrt(gn*gn+4*a0*gn));cold=s.G*u['Munit_Msun']*np.interp(rad/u['Runit_pc'],edges,np.r_[0,cdf],left=0,right=cdf[-1])/rad**2
    return base+cold
   for beta in [0.,-.5]:
    var=np.array([s.projection(d['R'],ar,g,beta) for ar in d['aa']]).T;f=s.fit(d,var,np.zeros_like(var),fixed_mass=0.)
    ref=next(v for v in refs if v['footing']==footing and v['beta']==beta and v['tracer_taper_pc'] is None)
    row={'tag':tag,'stage':stage,'footing':footing,'beta':beta,'nll':f['nll'],'reference_same_beta_nll':ref['nll'],'twice_NLL_above_same_beta_reference':2*(f['nll']-ref['nll']),'optimizer_success':f['optimizer_success']};rows.append(row);print(row,flush=True)
after=hashes();assert before==after
(P/'stellar_robustness.json').write_text(json.dumps({'scope':'posthoc fixed beta=0 or -0.5 and distinct a0 footings; cold profiles unchanged; no live DF or safety claim and no original gate amended','inputs_before':before,'inputs_after':after,'results':rows},indent=2)+'\n')
