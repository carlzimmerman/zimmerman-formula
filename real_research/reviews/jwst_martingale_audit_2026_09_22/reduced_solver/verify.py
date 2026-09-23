"""Replay Qwen's unchanged reduced-state solver and audit fresh, disjoint seeds."""
import json
import runpy
from pathlib import Path
import numpy as np

base=Path('real_research/reviews/jwst_martingale_audit_2026_09_22/reduced_solver')
simulate=runpy.run_path(str(base/'qwen_candidate.py'))['simulate_photon_path']
vector_sim=runpy.run_path('real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py')['simulate']
def mean_se(a):
    return float(np.mean(a)),float(np.std(a,ddof=1)/np.sqrt(len(a)))
def stats(D,Z,T,k):
    h=Z*Z/3-2*k*Z/5
    residual=D*D+h-(7*k*k/20+1/3)
    wrong=T*T+h-(7*k*k/20+1/3)
    av,se=mean_se(residual);bad,bse=mean_se(wrong)
    md,ds=mean_se(D);f=float(np.mean(D==0));expected=np.exp(-k)
    return {'n':len(D),'mean_T':float(T.mean()),'mean_D':md,'mean_Z':float(Z.mean()),
      'mean_Z2':float(np.mean(Z*Z)),'mean_D2':float(np.mean(D*D)),
      'residual_mean':av,'residual_se':se,'residual_z':av/se,'wrong_observable_z':bad/bse,
      'mean_delay_z':(md-k/2)/ds,'unscattered_fraction':f,
      'unscattered_z':float((f-expected)/np.sqrt(expected*(1-expected)/len(D))),
      'geometry_ok':bool(np.all((Z>=-1e-10)&(Z<=1+1e-10)&(D>=-1e-10)&(T>=1-1e-10)))}

rows=[]
checks={}
# Reproduce the originally reported main results exactly.
for i,k in enumerate([1.,2.]):
    D,Z,T=np.array([simulate(k,9225200+j) for j in range(10000)]).T
    row=stats(D,Z,T,k);row.update(k=k,seed_start=9225200,kind='original_replay')
    expected=[0.6803958457140475,1.7350967254594258][i]
    checks[f'replay_k{k}']=bool(abs(row['residual_mean']+(7*k*k/20+1/3)-expected)<1e-12)
    rows.append(row)

for i,k in enumerate([1.,2.]):
    arrays=[]
    for group in range(2):
        start=9260000+100000*i+40000*group
        D,Z,T=np.array([simulate(k,start+j) for j in range(20000)]).T
        row=stats(D,Z,T,k);row.update(k=k,seed_start=start,seed_end=start+19999,kind='fresh_disjoint')
        checks[f'identity_{i}_{group}']=abs(row['residual_z'])<6
        checks[f'mean_{i}_{group}']=abs(row['mean_delay_z'])<6
        checks[f'zero_collision_{i}_{group}']=abs(row['unscattered_z'])<6
        checks[f'geometry_{i}_{group}']=row['geometry_ok']
        checks[f'observable_control_{i}_{group}']=abs(row['wrong_observable_z'])>6
        rows.append(row);arrays.append((D,Z,T))
    # Different solver, different seeds, no shared photon paths.
    ref=vector_sim(40000,k,0.,0.,'central',9250000+i)
    D=np.concatenate([a[0] for a in arrays]);Z=np.concatenate([a[1] for a in arrays])
    Dr=ref['delay'];Zr=ref['time']-Dr
    comparison={}
    for name,a,b in [('D',D,Dr),('D2',D*D,Dr*Dr),('Z',Z,Zr),('Z2',Z*Z,Zr*Zr)]:
        ma,sa=mean_se(a);mb,sb=mean_se(b);score=(ma-mb)/np.hypot(sa,sb)
        comparison[name]={'difference':ma-mb,'combined_se':float(np.hypot(sa,sb)),'z_score':float(score)}
        checks[f'two_solver_{i}_{name}']=abs(score)<6
    rows.append({'k':k,'kind':'two_solver_comparison','reduced_n':40000,'vector_n':40000,'vector_seed':9250000+i,'moments':comparison})

out={'scope':'Unchanged Qwen reduced-state code reproduced; independent seed ranges and second-solver moment comparisons. Finite numerical evidence, not novelty.',
 'original_seed_overlap':{'main':[9225200,9235199],'positive':[9225300,9235299],'shared_seeds':9900,'fraction':.99},
 'rows':rows,'checks':{key:bool(value) for key,value in checks.items()}}
(base/'certified_v2/result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(checks.values())
