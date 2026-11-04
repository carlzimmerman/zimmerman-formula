"""Production with checked leading on-shell exits and separately retained partners.

The microscopic branches are on-shell results. Cosmological source history
remains the explicitly early-NR, fixed-pole benchmark, not a common solution.
"""
import os,sys,math,json,time,resource
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/production'))
from decays import Cosmology,summarize,exponential_nodes,T0,MU,DM_S,NEUTRINO_ONE,HBAR

def main(out):
 start=time.monotonic();cos=Cosmology()
 matched=json.loads((HERE/'run005/result.json').read_text());legs=json.loads((HERE/'run_legs003/result.json').read_text())
 vv=json.loads((ROOT/'reviews/collision_completion_2026_11_04/neutral_loop/run004/result.json').read_text());gc=json.loads((ROOT/'reviews/collision_completion_2026_11_04/neutral_loop/run_gaugino003/result.json').read_text())
 vc=next(c for c in vv['cases'] if c['e']==.003 and abs(c['x']-25.4000254000381)<1e-9)
 masses=dict(chi=abs(gc['baseline_threshold_real'][11][11])*MU,lambda8=abs(gc['baseline_threshold_real'][0][0])*MU,lambda2=abs(gc['baseline_threshold_real'][8][8])*MU,g3=0.,g2=0.,gY=0.)
 sources=[];cohorts=[];checks={};u,w=exponential_nodes(96)
 for m,l,v in zip(matched['states'],legs['states'],vc['states']):
  name=m['id'];M=m['mass']*MU;wc=m['width'];wp=l['other_gaugino']['inclusive_SU3_SU3_width'] if l['other_gaugino'] else 0.
  total=v['width']+wc+wp;B=wc/total;partner='lambda8' if name=='S8_0' else 'lambda2'
  summary=summarize(cos,m['mass'],masses['chi']/MU,total,B,reference=False);summary['one_chi_branch']=summary.pop('photino_branch_conditional')
  chans=[]
  if name=='S8_0':chans.extend([('gg',v['sectors']['gg'],('g3','g3')),('gY',v['sectors']['gY'],('g3','gY'))])
  else:chans.append(('WY',v['sectors']['WY'],('g2','gY')))
  chans.append(('chi_partner',wc,('chi',partner)))
  if wp:chans.append(('partner_pair',wp,(partner,partner)))
  ab=cos.birth(summary['lifetime_seconds']*u);birth_energy=0.;number=0.;channelrows=[]
  for kind,width,(j,k) in chans:
   branch=width/total;mj,mk=masses[j],masses[k]
   momentum=math.sqrt((M*M-(mj+mk)**2)*(M*M-(mj-mk)**2))/(2*M)
   ej=(M*M+mj*mj-mk*mk)/(2*M);ek=M-ej
   channelrows.append(dict(kind=kind,width_mu=width,branch=branch,daughters=[j,k],pstar_GeV=momentum,energy_GeV=[ej,ek]))
   birth_energy+=branch*(ej+ek)*sum(w);number+=2*branch*sum(w)
   for daughter in sorted(set((j,k))):
    mult=(j==daughter)+(k==daughter)
    cohorts.append(dict(parent=name,channel=kind,daughter=daughter,mass_GeV=masses[daughter],
      probability_weights_per_parent=(mult*branch*w).tolist(),birth_time_seconds=(summary['lifetime_seconds']*u).tolist(),
      birth_scale_factor=ab.tolist(),comoving_momentum_GeV=(ab*momentum).tolist(),pstar_GeV=momentum,
      interpretation='Physical number per one initial NR parent. Comoving momentum is a_today=1 times physical momentum; retain this cohort off any insufficient thermal grid.'))
  gaugefrac=v['width']/total;partnerfrac=B/2+wp/total;chifrac=B/2
  checks[name+'_branch_sum']=abs(sum(c['branch'] for c in channelrows)-1)<1e-12
  checks[name+'_birth_energy']=abs(birth_energy/M-1)<1e-12
  checks[name+'_daughter_number']=abs(number-2)<1e-12
  checks[name+'_energy_partition']=abs(gaugefrac+partnerfrac+chifrac-1)<1e-12
  sources.append(dict(id=name,parent_mass_GeV=M,summary=summary,channels=channelrows,total_width_mu=total,
   lifetime_seconds=HBAR/(MU*total),gauge_branch=gaugefrac,chi_partner_branch=B,partner_pair_branch=wp/total,
   birth_energy_fractions=dict(direct_gauge=gaugefrac,chi=chifrac,partner_gauginos=partnerfrac),
   partner_number_per_parent=B+2*wp/total))
 memory=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());warm=json.loads((ROOT/'reviews/collision_completion_2026_11_04/integration/run_warm001/result.json').read_text())
 late={s['id']:memory['neutral_terminal_group_yields'][s['id']]['number_yield'] for s in sources};h=warm['case']['history'][-1]
 fac=.02**3/(2*math.pi**2/45*106.75);early={s['id']:h['comoving_number_by_group'][warm['case']['groups'].index(s['id'])]*fac for s in sources}
 photon_s=3*T0/(2*cos.gs0);norms=[]
 for label,Y in (('late_finite_memory_stage',late),('early_warm_yield_transplant',early)):
  direct=chi=partnerrad=partnerrest=stable=0.;states=[]
  for s in sources:
   y=Y[s['id']];M=s['parent_mass_GeV'];aa=s['summary']['mean_birth_scale_factor'];bb=s['chi_partner_branch'];partner='lambda8' if s['id']=='S8_0' else 'lambda2'
   dr=y*M*s['gauge_branch']*aa;cr=y*bb*masses['chi'];pr=y*M*s['birth_energy_fractions']['partner_gauginos']*aa;ps=y*s['partner_number_per_parent']*masses[partner]
   direct+=dr;chi+=cr;partnerrad+=pr;partnerrest+=ps;stable+=y*M
   states.append(dict(id=s['id'],Y_parent=y,Y_chi=y*bb,Y_partner=y*s['partner_number_per_parent'],direct_gauge_energy_today_per_s_GeV=dr,chi_rest_per_s_GeV=cr,partner_rest_per_s_GeV=ps))
  norms.append(dict(normalization=label,states=states,direct_gauge_Delta_Neff=direct/photon_s/NEUTRINO_ONE,
   chi_rest_DM_fraction=chi/DM_S,partner_rest_DM_fraction_if_stable=partnerrest/DM_S,
   partner_Delta_Neff_if_all_partner_energy_stayed_radiation=partnerrad/photon_s/NEUTRINO_ONE,
   rest_DM_multiple_if_parents_stable=stable/DM_S,
   interpretation='Distinct finite-stage yield normalization only. Partner gauginos are retained, not assigned to chi or direct gauge radiation; their scattering/secondary decays require separate evolution.'))
 checks={k:bool(v) for k,v in checks.items()}
 result=dict(claim_id='CC11_CHECKED_DECAY_SOURCE_AND_SEPARATE_PARTNER_LEDGER',sources=sources,cohorts=cohorts,normalizations=norms,checks=checks,masses_GeV=masses,
  runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  microphysical_status='Leading on-shell triangle gauge/UV/basis/normalization checks passed; Goldstino exit forbidden by the unbroken unitary transpose charge-conjugation symmetry.',
  cosmological_scope='Early NR, fixed pole, constant vacuum rates in SM RD/entropy cosmology; this source is ready for common-state integration but is not an abundance solution.',
  non_claims=['No blanket assignment of partner-gaugino energy to radiation or chi','No proof of collisionless partner propagation or a global cold-source exclusion','No substitution of the old finite-stage yield normalization into a new common physical history'])
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,sources=[{k:v for k,v in s.items() if k not in ('summary','channels')} for s in sources],normalizations=norms)),flush=True);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
