"""Orthogonal result comparisons and compact quantitative handoff."""
import json,sys,math,time,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(p):return json.loads((HERE/p).read_text())
def main(out):
 start=time.monotonic();rates=load('run_rates_001/result.json');branches=load('run_branching_002/result.json');stat=load('run_stationary_002/result.json');roll=load('run_roll_001/result.json');charged=json.loads((HERE.parent/'run_charged/result.json').read_text())
 errors=[];grouped=[]
 for b in branches['cases']:
  r=next(q for q in rates['cases'] if q['x']==b['x']);p1=sorted((q['mass_over_mu'],q['width_over_mu']) for q in r['neutral_scalar_partial_widths']);p2=sorted((q['mass'],q['to_light_charged_fermions']) for q in b['parents']);assert len(p1)==len(p2)
  errors.extend(abs(x[1]/y[1]-1) for x,y in zip(p1,p2))
  groups={}
  for q in b['parents']:groups.setdefault(round(q['mass'],8),[]).append(q)
  gg=[]
  for m,rows in groups.items():
   keys=('to_light_charged_fermions','to_neutral_fermions','to_neutral_scalars','to_charged_scalars')
   gg.append(dict(mass_over_mu=m,multiplicity=len(rows),mean_widths_over_mu={k:sum(q[k] for q in rows)/len(rows) for k in keys}))
  grouped.append(dict(x=b['x'],groups=gg))
 xi=.02;gsm=106.75;ncoef=24*3*1.202056903159594/(4*math.pi**2);yield0=ncoef/(2*math.pi**2*gsm/45)*xi**3
 relic=[dict(kind=q['name'],assumed_initial_charged_number_per_visible_entropy=yield0,charged_rest_energy_per_visible_entropy_GeV=yield0*q['lightest_charged_GeV'],charged_rest_energy_per_hypothetical_two_spin_photino_rest_energy=12*q['charged_mass_over_photino']) for q in charged['cases'] if q['name']!='origin_control']
 checks={'actual_light_widths_agree_with_independent_projection':max(errors)<1e-9,'upstream_checks_pass':all(all(q['checks'].values()) for q in (rates,branches,stat,roll))}
 result=dict(claim_id='TK08_CROSS_AUDIT',checks=checks,max_partial_width_repeat_error=max(errors),neutral_parent_groups=grouped,initial_charged_yield=yield0,undepleted_conditional_charged_relic=relic,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite comparison of separate vertex projections and assumed no-depletion yield. No conservation of charged particle+antiparticle number is claimed; only residual signed U1 charge is exact.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
